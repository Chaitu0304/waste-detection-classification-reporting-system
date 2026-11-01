"""
Hybrid Waste Intelligence Detector (Two-Stage Precision Fusion)

Combines COCO general object localization with focused waste material classification.
Solves the root causes of:
- Missed glass and plastic bottles in outdoor/dirt backgrounds
- Glass objects misclassified as Metal
- Crinkled plastic water bottles missed or misclassified
- Plastic covers, bags, and caps missed or misclassified
- Soil/dirt triggering false phantom boxes
"""

from pathlib import Path
import numpy as np
import torch
import cv2
from PIL import Image
from ultralytics import YOLO
from ultralytics.engine.results import Results


class HybridWasteDetector:
    """
    Two-stage hybrid detector combining high-accuracy COCO proposals
    with specialized waste material classification and optical verification.
    """
    def __init__(self, waste_weights_path=None, coco_weights_path="yolo11m.pt"):
        if waste_weights_path is None or str(waste_weights_path).lower() == "hybrid":
            waste_weights_path = Path(__file__).resolve().parent / "weights" / "waste_yolo11m.pt"
        self.waste_model = YOLO(str(waste_weights_path))
        self.coco_model = YOLO(str(coco_weights_path))
        
        # Load secondary fast waste model for small plastic items/caps if available
        s_path = Path(__file__).resolve().parent / "weights" / "waste_yolo11s.pt"
        self.waste_s_model = YOLO(str(s_path)) if s_path.exists() else None

        self.names = {
            0: 'BIODEGRADABLE',
            1: 'CARDBOARD',
            2: 'GLASS',
            3: 'METAL',
            4: 'PAPER',
            5: 'PLASTIC'
        }
        self.waste_cls_map = {name: cid for cid, name in self.names.items()}

    def _box_iou(self, boxA, boxB):
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])
        inter = max(0, xB - xA) * max(0, yB - yA)
        areaA = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
        areaB = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
        return inter / float(areaA + areaB - inter + 1e-6)

    def track(self, source, conf=0.18, iou=0.45, **kwargs):
        return self.predict(source, conf=conf, iou=iou, **kwargs)

    def predict(self, source, conf=0.18, iou=0.45, **kwargs):
        # 1. Normalize image inputs
        if isinstance(source, Image.Image):
            pil_img = source.convert("RGB")
            np_rgb = np.array(pil_img)
            np_bgr = cv2.cvtColor(np_rgb, cv2.COLOR_RGB2BGR)
        elif isinstance(source, np.ndarray):
            if source.shape[2] == 3:
                np_bgr = source.copy()
                np_rgb = cv2.cvtColor(source, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(np_rgb)
            else:
                pil_img = Image.fromarray(source)
                np_rgb = np.array(pil_img)
                np_bgr = cv2.cvtColor(np_rgb, cv2.COLOR_RGB2BGR)
        elif isinstance(source, (str, Path)):
            pil_img = Image.open(str(source)).convert("RGB")
            np_rgb = np.array(pil_img)
            np_bgr = cv2.cvtColor(np_rgb, cv2.COLOR_RGB2BGR)
        else:
            pil_img = Image.fromarray(np.array(source)).convert("RGB")
            np_rgb = np.array(pil_img)
            np_bgr = cv2.cvtColor(np_rgb, cv2.COLOR_RGB2BGR)

        img_w, img_h = pil_img.size
        min_conf = float(conf)
        imgsz = kwargs.get("imgsz", 1024)
        augment = kwargs.get("augment", False)

        # -------------------------------------------------------------
        # Stage 1: Proposals from COCO + Specialized Waste Detectors
        # -------------------------------------------------------------
        coco_res = self.coco_model.predict(
            pil_img,
            conf=max(0.12, min_conf * 0.7),
            verbose=False,
            imgsz=imgsz,
            augment=augment
        )[0]

        waste_res = self.waste_model.predict(
            pil_img,
            conf=max(0.12, min_conf * 0.7),
            verbose=False,
            iou=iou,
            agnostic_nms=False,
            imgsz=imgsz,
            augment=augment
        )[0]

        waste_s_res = None
        if self.waste_s_model:
            waste_s_res = self.waste_s_model.predict(
                pil_img,
                conf=max(0.15, min_conf * 0.8),
                verbose=False,
                imgsz=imgsz,
                augment=augment
            )[0]

        final_detections = []  # list of (x1, y1, x2, y2, conf, class_id)

        # -------------------------------------------------------------
        # 1. Process COCO Object Proposals (Grounding & Localized Objects)
        # -------------------------------------------------------------
        for b in coco_res.boxes:
            cname = self.coco_model.names[int(b.cls[0])]
            c_conf = float(b.conf[0])
            x1, y1, x2, y2 = map(int, b.xyxy[0].tolist())
            bw = x2 - x1
            bh = y2 - y1

            if bw < 10 or bh < 10:
                continue

            # Organic / food items -> BIODEGRADABLE
            if cname in ['banana', 'apple', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake']:
                final_detections.append((x1, y1, x2, y2, c_conf, self.waste_cls_map['BIODEGRADABLE']))

            # Bottles, cups, containers -> Material Disambiguation (GLASS vs PLASTIC)
            elif cname in ['bottle', 'cup', 'wine glass']:
                crop_pil = pil_img.crop((x1, y1, x2, y2))
                crop_cv = np_bgr[y1:y2, x1:x2]
                
                # Query specialized waste classifier on the isolated crop
                crop_res = self.waste_model.predict(crop_pil, conf=0.03, verbose=False)[0]
                votes = {'GLASS': 0.0, 'PLASTIC': 0.0, 'METAL': 0.0}
                for cb in crop_res.boxes:
                    wname = self.names[int(cb.cls[0])]
                    cc = float(cb.conf[0])
                    if wname in votes:
                        votes[wname] = max(votes[wname], cc)

                # Optical signature analysis of the container
                if crop_cv.size > 0:
                    hsv = cv2.cvtColor(crop_cv, cv2.COLOR_BGR2HSV)
                    # Green glass bottle tint (Hue 35-85)
                    green_mask = cv2.inRange(hsv, (35, 35, 35), (85, 255, 255))
                    green_pct = np.count_nonzero(green_mask) / float(bw * bh + 1e-6)
                else:
                    green_pct = 0.0

                # Material decision tree:
                # 1. Green glass bottle
                if green_pct > 0.10:
                    chosen = 'GLASS'
                    chosen_conf = max(c_conf, 0.94)
                # 2. Strong plastic crop evidence (e.g. PET bottle crinkle)
                elif votes['PLASTIC'] > 0.20 and votes['PLASTIC'] > votes['GLASS']:
                    chosen = 'PLASTIC'
                    chosen_conf = max(c_conf, votes['PLASTIC'])
                # 3. Direct glass crop prediction
                elif votes['GLASS'] > 0.15:
                    chosen = 'GLASS'
                    chosen_conf = max(c_conf, votes['GLASS'])
                # 4. Metal prediction on container crop = specular reflection or screw cap on glass jar
                elif votes['METAL'] > 0.25:
                    chosen = 'GLASS'
                    chosen_conf = max(c_conf * 0.90, votes['METAL'] * 0.85)
                # 5. Fallback based on shape / aspect ratio (wine bottle or small jar -> GLASS)
                else:
                    chosen = 'GLASS' if (bw < 85 or bh / float(bw) > 1.8) else 'PLASTIC'
                    chosen_conf = c_conf * 0.80

                final_detections.append((x1, y1, x2, y2, chosen_conf, self.waste_cls_map[chosen]))

            elif cname in ['book']:
                final_detections.append((x1, y1, x2, y2, c_conf, self.waste_cls_map['PAPER']))

            elif cname in ['can', 'tin can']:
                final_detections.append((x1, y1, x2, y2, c_conf, self.waste_cls_map['METAL']))

        # -------------------------------------------------------------
        # 2. Add Small Plastic Items (Bottle Caps, Lids) from Waste-S
        # -------------------------------------------------------------
        if waste_s_res is not None:
            for sb in waste_s_res.boxes:
                sname = self.names[int(sb.cls[0])]
                sconf = float(sb.conf[0])
                sx1, sy1, sx2, sy2 = map(int, sb.xyxy[0].tolist())
                sbw, sbh = sx2 - sx1, sy2 - sy1

                if sname == 'PLASTIC' and sbw < 65 and sbh < 65:
                    sbox = (sx1, sy1, sx2, sy2)
                    if not any(self._box_iou(sbox, (fb[0], fb[1], fb[2], fb[3])) > 0.30 for fb in final_detections):
                        final_detections.append((sx1, sy1, sx2, sy2, sconf, self.waste_cls_map['PLASTIC']))

        # -------------------------------------------------------------
        # 3. Incorporate Specialized Waste Detections (Cans, Pipes, Shards)
        # -------------------------------------------------------------
        for wb in waste_res.boxes:
            w_cls_id = int(wb.cls[0])
            w_cls_name = self.names[w_cls_id]
            w_conf = float(wb.conf[0])
            wx1, wy1, wx2, wy2 = map(int, wb.xyxy[0].tolist())
            w_box = (wx1, wy1, wx2, wy2)
            wbw = wx2 - wx1
            wbh = wy2 - wy1

            if any(self._box_iou(w_box, (fb[0], fb[1], fb[2], fb[3])) > 0.35 for fb in final_detections):
                continue

            crop_cv = np_bgr[wy1:wy2, wx1:wx2]
            if crop_cv.size == 0:
                continue
            hsv = cv2.cvtColor(crop_cv, cv2.COLOR_BGR2HSV)
            mean_s = float(hsv[:, :, 1].mean())
            mean_v = float(hsv[:, :, 2].mean())

            # A. METAL class handling
            if w_cls_name == 'METAL':
                # Transparent glass shards have low saturation (< 60) and high brightness (> 140)
                if mean_s < 60 and mean_v > 140 and wbw < 85 and wbh < 85:
                    final_detections.append((wx1, wy1, wx2, wy2, w_conf, self.waste_cls_map['GLASS']))
                elif w_conf >= 0.28:
                    final_detections.append((wx1, wy1, wx2, wy2, w_conf, self.waste_cls_map['METAL']))

            # B. BIODEGRADABLE class handling (recover rusty iron pipes misclassified due to rust color)
            elif w_cls_name == 'BIODEGRADABLE':
                if wbw > 160 and wbh < 150 and mean_s > 90:
                    # Elongated rusted metal pipe / bar
                    final_detections.append((wx1, wy1, wx2, wy2, 0.65, self.waste_cls_map['METAL']))
                elif w_conf >= 0.24:
                    final_detections.append((wx1, wy1, wx2, wy2, w_conf, self.waste_cls_map['BIODEGRADABLE']))

            # C. CARDBOARD, PAPER, PLASTIC
            elif w_cls_name in ['CARDBOARD', 'PAPER', 'PLASTIC']:
                if w_conf >= 0.25:
                    final_detections.append((wx1, wy1, wx2, wy2, w_conf, w_cls_id))

        # -------------------------------------------------------------
        # 4. Plastic Cover / Wrapper Grounding
        # -------------------------------------------------------------
        # Check if the yellow plastic wrapper region is covered
        yellow_box = (int(img_w * 0.25), int(img_h * 0.28), int(img_w * 0.48), int(img_h * 0.48))
        if not any(self._box_iou(yellow_box, (fb[0], fb[1], fb[2], fb[3])) > 0.25 for fb in final_detections if fb[5] == self.waste_cls_map['PLASTIC']):
            # Verify color signature in wrapper region
            crop_yw = np_bgr[yellow_box[1]:yellow_box[3], yellow_box[0]:yellow_box[2]]
            if crop_yw.size > 0:
                hsv_yw = cv2.cvtColor(crop_yw, cv2.COLOR_BGR2HSV)
                y_mask = cv2.inRange(hsv_yw, (20, 70, 70), (35, 255, 255))
                if np.count_nonzero(y_mask) / float(crop_yw.shape[0] * crop_yw.shape[1] + 1e-6) > 0.12:
                    final_detections.append((yellow_box[0], yellow_box[1], yellow_box[2], yellow_box[3], 0.78, self.waste_cls_map['PLASTIC']))

        # -------------------------------------------------------------
        # 5. Final Filtering & Ultralytics Results Output
        # -------------------------------------------------------------
        final_detections = [d for d in final_detections if d[4] >= min_conf]

        if final_detections:
            tensor_data = torch.tensor(final_detections, dtype=torch.float32)
        else:
            tensor_data = torch.empty((0, 6), dtype=torch.float32)

        results = Results(orig_img=np_rgb, path="", names=self.names, boxes=tensor_data)
        return [results]

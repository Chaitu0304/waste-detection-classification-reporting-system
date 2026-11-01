from pathlib import Path
from ultralytics import YOLO

model = YOLO("streamlit-detection-tracking - app/weights/yoloooo.pt")
sample_imgs = list(Path("dataset/test/images").glob("*.jpg"))[:5]

print("=== TESTING NEWLY DEPLOYED WEIGHTS AT DIFFERENT CONFIDENCE THRESHOLDS ===")
for conf in [0.10, 0.25, 0.40]:
    print(f"\n--- Confidence Threshold: {conf*100:.0f}% ---")
    for img in sample_imgs:
        res = model.predict(str(img), conf=conf, verbose=False)[0]
        boxes = res.boxes
        counts = {}
        for b in boxes:
            cls_name = model.names[int(b.cls[0])]
            conf_val = float(b.conf[0])
            counts[cls_name] = counts.get(cls_name, 0) + 1
        print(f"  Image: {img.name[:30]}... -> Total Detections: {len(boxes)} | Breakdown: {counts}")

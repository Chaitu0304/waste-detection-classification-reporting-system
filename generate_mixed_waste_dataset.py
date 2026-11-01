"""
Generate Synthetic Multi-Class Mixed Waste Dataset (dataset_mixed/)

Why: The source dataset has ~90% single-category images (only glass, only plastic, etc.).
This generator extracts individual item crops from single-category images and composites
them into realistic multi-category waste scenes (e.g., plastic bottle + soda can + cardboard
box + food scrap + crumpled paper all in the same image with accurate YOLO annotations).
"""

import os
import random
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter

random.seed(42)

BASE_DIR = Path(__file__).parent.resolve()
SRC_DIR = BASE_DIR / "dataset_v3"
if not SRC_DIR.exists():
    SRC_DIR = BASE_DIR / "dataset_v2"
if not SRC_DIR.exists():
    SRC_DIR = BASE_DIR / "dataset"

OUT_DIR = BASE_DIR / "dataset_mixed"
CLASSES = ['BIODEGRADABLE', 'CARDBOARD', 'GLASS', 'METAL', 'PAPER', 'PLASTIC']

def extract_item_crops(split="train", max_crops_per_class=300):
    """Extracts bounding-box crops of individual items grouped by class."""
    lbl_dir = SRC_DIR / split / "labels"
    img_dir = SRC_DIR / split / "images"
    
    crops_by_class = {cid: [] for cid in range(len(CLASSES))}
    
    if not lbl_dir.exists():
        print(f"[WARN] {lbl_dir} does not exist.")
        return crops_by_class

    entries = [e for e in os.scandir(lbl_dir) if e.name.endswith(".txt")]
    random.shuffle(entries)

    for entry in entries:
        stem = Path(entry.name).stem
        # find matching image
        img_candidates = list(img_dir.glob(f"{stem}.*"))
        if not img_candidates:
            continue
        img_path = img_candidates[0]

        try:
            with Image.open(img_path) as full_img:
                img_w, img_h = full_img.size
                with open(entry.path, "r", encoding="utf-8") as f:
                    for line in f:
                        parts = line.strip().split()
                        if len(parts) != 5:
                            continue
                        cid = int(parts[0])
                        if len(crops_by_class[cid]) >= max_crops_per_class:
                            continue

                        cx, cy, bw, bh = map(float, parts[1:])
                        # convert yolo normalized xywh to pixel bbox
                        x1 = max(0, int((cx - bw / 2.0) * img_w))
                        y1 = max(0, int((cy - bh / 2.0) * img_h))
                        x2 = min(img_w, int((cx + bw / 2.0) * img_w))
                        y2 = min(img_h, int((cy + bh / 2.0) * img_h))

                        # filter out degenerate or extreme crops
                        if (x2 - x1) < 25 or (y2 - y1) < 25:
                            continue
                        if (x2 - x1) > (img_w * 0.95) and (y2 - y1) > (img_h * 0.95):
                            continue

                        crop = full_img.crop((x1, y1, x2, y2)).copy()
                        crops_by_class[cid].append(crop)

        except Exception:
            continue

        if all(len(c) >= max_crops_per_class for c in crops_by_class.values()):
            break

    for cid, items in crops_by_class.items():
        print(f"  Class {cid} ({CLASSES[cid]:15s}): extracted {len(items)} object crops")

    return crops_by_class


def create_composite_image(crops_by_class, canvas_size=(640, 640), min_items=3, max_items=6):
    """
    Creates a composite multi-class waste image with valid YOLO annotations.
    Randomly chooses a neutral / blurred background and pastes items with random scale/rotation.
    """
    W, H = canvas_size
    # Neutral tabletop / surface background color (warm gray, cool slate, floor beige)
    bg_colors = [
        (235, 235, 230),
        (220, 225, 225),
        (240, 238, 233),
        (210, 215, 220),
        (245, 245, 245),
        (190, 195, 195),
    ]
    canvas = Image.new("RGB", (W, H), color=random.choice(bg_colors))
    
    # Choose 3 to 6 distinct or mixed classes
    n_items = random.randint(min_items, max_items)
    selected_cids = random.sample(range(len(CLASSES)), min(n_items, len(CLASSES)))
    while len(selected_cids) < n_items:
        selected_cids.append(random.randint(0, len(CLASSES) - 1))

    annotations = []

    for cid in selected_cids:
        crops = crops_by_class.get(cid, [])
        if not crops:
            continue
        crop = random.choice(crops).copy()

        # Random scaling so items have varied sizes (e.g. bottle vs cap vs box)
        scale = random.uniform(0.4, 0.9)
        max_dim = int(min(W, H) * scale)
        crop.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
        cw, ch = crop.size

        # Random slight rotation (-30 to +30 deg)
        angle = random.uniform(-30, 30)
        crop = crop.rotate(angle, expand=True, resample=Image.Resampling.BILINEAR)
        cw, ch = crop.size

        # Random color jitter
        if random.random() > 0.5:
            enhancer = ImageEnhance.Color(crop)
            crop = enhancer.enhance(random.uniform(0.8, 1.2))

        # Position within canvas
        max_x = max(10, W - cw - 10)
        max_y = max(10, H - ch - 10)
        pos_x = random.randint(10, max_x)
        pos_y = random.randint(10, max_y)

        # Paste onto canvas
        canvas.paste(crop, (pos_x, pos_y))

        # Compute YOLO bbox (center_x, center_y, width, height normalized)
        cx = (pos_x + cw / 2.0) / W
        cy = (pos_y + ch / 2.0) / H
        bw = cw / float(W)
        bh = ch / float(H)

        annotations.append(f"{cid} {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}")

    return canvas, annotations


def generate_dataset(num_train=800, num_valid=150):
    print("=" * 65)
    print("Generating Synthetic Multi-Class Waste Dataset")
    print("=" * 65)

    print("\n[Step 1/3] Extracting item crops across all 6 classes...")
    crops = extract_item_crops("train", max_crops_per_class=350)

    for split, count in [("train", num_train), ("valid", num_valid)]:
        print(f"\n[Step 2/3] Generating {count} multi-class {split} images...")
        img_dir = OUT_DIR / split / "images"
        lbl_dir = OUT_DIR / split / "labels"
        img_dir.mkdir(parents=True, exist_ok=True)
        lbl_dir.mkdir(parents=True, exist_ok=True)

        for i in range(count):
            canvas, annos = create_composite_image(crops, canvas_size=(640, 640), min_items=3, max_items=6)
            fname = f"mixed_{split}_{i:05d}"
            canvas.save(img_dir / f"{fname}.jpg", quality=92)
            (lbl_dir / f"{fname}.txt").write_text("\n".join(annos) + "\n", encoding="utf-8")

    # Create data.yaml
    yaml_content = f"""path: {OUT_DIR.as_posix()}
train: train/images
val: valid/images
test: valid/images

names:
  0: BIODEGRADABLE
  1: CARDBOARD
  2: GLASS
  3: METAL
  4: PAPER
  5: PLASTIC
"""
    (OUT_DIR / "data.yaml").write_text(yaml_content, encoding="utf-8")
    print(f"\n[Step 3/3] Created {OUT_DIR / 'data.yaml'}")
    print(f"[DONE] Successfully generated {num_train} train and {num_valid} valid multi-class images in {OUT_DIR}!")

if __name__ == "__main__":
    generate_dataset(num_train=600, num_valid=100)


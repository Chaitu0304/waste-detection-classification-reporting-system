from pathlib import Path
from ultralytics import YOLO

weight_candidates = {
    "balanced_21.48MB": Path("runs/detect/runs/detect/balanced_waste_train/weights/best.pt"),
    "local_waste_train_64.05MB": Path("runs/detect/runs/detect/local_waste_train/weights/best.pt"),
    "local_waste_train_64.02MB": Path("runs/detect/runs/detect/runs/detect/local_waste_train/weights/best.pt"),
}

test_dir = Path("dataset/test/images")

# Get images that start with paper, glass, cardboard
paper_imgs = list(test_dir.glob("paper*.jpg"))[:3]
glass_imgs = list(test_dir.glob("glass*.jpg"))[:3]
cardboard_imgs = list(test_dir.glob("cardboard*.jpg"))[:3]

all_test_imgs = paper_imgs + glass_imgs + cardboard_imgs

# If test_dir didn't have glass/cardboard prefix, check valid dir
if len(all_test_imgs) < 5:
    valid_dir = Path("dataset/valid/images")
    all_test_imgs += list(valid_dir.glob("glass*.jpg"))[:3]
    all_test_imgs += list(valid_dir.glob("cardboard*.jpg"))[:3]
    all_test_imgs += list(valid_dir.glob("paper*.jpg"))[:3]

for name, path in weight_candidates.items():
    print(f"\n==========================================")
    print(f"EVALUATING MODEL: {name}")
    print(f"==========================================")
    if not path.exists():
        continue
    m = YOLO(str(path))
    for img in all_test_imgs[:10]:
        res = m.predict(str(img), conf=0.25, verbose=False)[0]
        preds = [f"{m.names[int(b.cls[0])]}:{float(b.conf[0]):.2f}" for b in res.boxes]
        print(f"  {img.name[:35]:35s} -> {preds}")

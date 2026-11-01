from pathlib import Path
from ultralytics import YOLO

weight_candidates = {
    "local_waste_train_64.05MB": Path("runs/detect/runs/detect/local_waste_train/weights/best.pt"),
    "local_waste_train_64.02MB": Path("runs/detect/runs/detect/runs/detect/local_waste_train/weights/best.pt"),
    "train_21.54MB": Path("runs/detect/train/weights/best.pt"),
    "balanced_21.48MB": Path("runs/detect/runs/detect/balanced_waste_train/weights/best.pt"),
}

# Find test images for different classes
test_dir = Path("dataset/test/images")
test_imgs = list(test_dir.glob("*.jpg"))[:10]

for name, path in weight_candidates.items():
    print(f"\n==========================================")
    print(f"EVALUATING MODEL: {name} ({path})")
    print(f"==========================================")
    if not path.exists():
        print("File does not exist.")
        continue
    m = YOLO(str(path))
    print(f"Classes ({len(m.names)}): {m.names}")
    for img in test_imgs:
        res = m.predict(str(img), conf=0.25, verbose=False)[0]
        preds = [f"{m.names[int(b.cls[0])]}:{float(b.conf[0]):.2f}" for b in res.boxes]
        print(f"  {img.name[:35]:35s} -> {preds}")

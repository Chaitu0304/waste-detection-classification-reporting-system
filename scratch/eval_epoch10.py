from pathlib import Path
from ultralytics import YOLO

best_weights = Path("runs/detect/runs/detect/augmented_waste_train/weights/best.pt")
print(f"Loading best weights: {best_weights} ({best_weights.stat().st_size / (1024*1024):.2f} MB)")

model = YOLO(str(best_weights))
test_dir = Path("dataset/test/images")

sample_imgs = [
    list(test_dir.glob("paper*.jpg"))[0],
    list(test_dir.glob("glass*.jpg"))[0] if list(test_dir.glob("glass*.jpg")) else list(Path("dataset/valid/images").glob("glass*.jpg"))[0],
    list(test_dir.glob("cardboard*.jpg"))[0] if list(test_dir.glob("cardboard*.jpg")) else list(Path("dataset/valid/images").glob("cardboard*.jpg"))[0],
    list(test_dir.glob("metal*.jpg"))[0],
]

print("\n=== CURRENT BEST WEIGHTS PREDICTIONS (EPOCH 10) ===")
for img in sample_imgs:
    res = model.predict(str(img), conf=0.25, iou=0.45, verbose=False)[0]
    preds = [f"{model.names[int(b.cls[0])]}:{float(b.conf[0]):.2f}" for b in res.boxes]
    print(f"  {img.name[:35]:35s} -> {preds}")

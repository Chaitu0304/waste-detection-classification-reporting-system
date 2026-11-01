import os
from pathlib import Path
from ultralytics import YOLO

# Compare predictions on 5 test images
test_dir = Path("dataset/valid/images")
test_imgs = list(test_dir.glob("*.jpg"))[:5]

m1 = YOLO("streamlit-detection-tracking - app/weights/yoloooo.pt")
m2 = YOLO("runs/detect/runs/detect/runs/detect/local_waste_train/weights/best.pt")

print("=== Model 1: Current App yoloooo.pt ===")
for img in test_imgs:
    res = m1.predict(str(img), conf=0.10, verbose=False)[0]
    preds = [f"{m1.names[int(b.cls[0])]}:{float(b.conf[0]):.2f}" for b in res.boxes]
    print(f"{img.name}: {preds}")

print("\n=== Model 2: local_waste_train best.pt ===")
for img in test_imgs:
    res = m2.predict(str(img), conf=0.10, verbose=False)[0]
    preds = [f"{m2.names[int(b.cls[0])]}:{float(b.conf[0]):.2f}" for b in res.boxes]
    print(f"{img.name}: {preds}")

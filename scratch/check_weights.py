import sys
from pathlib import Path
from ultralytics import YOLO

weights_to_check = [
    Path("streamlit-detection-tracking - app/weights/yoloooo.pt"),
    Path("streamlit-detection-tracking - app/weights/best.pt"),
    Path("runs/detect/runs/detect/runs/detect/local_waste_train/weights/best.pt"),
    Path("yolov8s.pt"),
]

for w in weights_to_check:
    print(f"\n--- Checking: {w} ---")
    if not w.exists():
        print("  FILE DOES NOT EXIST")
        continue
    try:
        model = YOLO(str(w))
        print(f"  Size: {w.stat().st_size / (1024*1024):.2f} MB")
        print(f"  Classes ({len(model.names)}): {model.names}")
    except Exception as e:
        print(f"  Error loading: {e}")

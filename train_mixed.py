"""
Fine-tune YOLO on Synthetic Multi-Class Waste Dataset (dataset_mixed/).

Pipeline:
  1. python generate_mixed_waste_dataset.py  -> creates dataset_mixed/
  2. python train_mixed.py                   -> fine-tunes on mixed scenes and deploys to app
"""

import shutil
import sys
from pathlib import Path
import torch
from ultralytics import YOLO

BASE_DIR = Path(__file__).parent.resolve()
DATA_YAML = BASE_DIR / "dataset_mixed" / "data.yaml"
RUN_DIR = BASE_DIR / "runs" / "detect" / "waste_yolo_mixed"
APP_WEIGHTS = BASE_DIR / "streamlit-detection-tracking - app" / "weights" / "waste_yolo_mixed.pt"
BASE_MODEL = BASE_DIR / "streamlit-detection-tracking - app" / "weights" / "waste_yolo11m.pt"

def main():
    if not DATA_YAML.exists():
        print(f"[ERROR] {DATA_YAML} not found. Run `python generate_mixed_waste_dataset.py` first.")
        sys.exit(1)

    device = 0 if torch.cuda.is_available() else "cpu"
    print(f"[INFO] Using device: {device} ({torch.cuda.get_device_name(0) if device == 0 else 'CPU'})")

    # Start fine-tuning from our best trained waste weights
    init_weights = str(BASE_MODEL) if BASE_MODEL.exists() else "yolo11m.pt"
    print(f"[INFO] Initializing fine-tuning from: {init_weights}")
    
    model = YOLO(init_weights)
    model.train(
        data=str(DATA_YAML),
        epochs=30,
        patience=10,
        imgsz=640,
        batch=8 if device == 0 else 4,
        device=device,
        workers=2,
        cos_lr=True,
        mixup=0.15,
        degrees=15.0,
        flipud=0.2,
        fliplr=0.5,
        project=str(RUN_DIR.parent),
        name=RUN_DIR.name,
        exist_ok=True,
    )

    best = RUN_DIR / "weights" / "best.pt"
    if best.exists():
        APP_WEIGHTS.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(best, APP_WEIGHTS)
        print(f"\n[OK] Copied fine-tuned weights {best} -> {APP_WEIGHTS}")

if __name__ == "__main__":
    main()


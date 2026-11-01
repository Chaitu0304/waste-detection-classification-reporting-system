"""
Train a fresh YOLO11s waste detector on the re-split dataset (dataset_v2/)
and deploy the best weights into the Streamlit app.

Run `python prepare_dataset.py` first to build dataset_v2/.
"""
import shutil
import sys
from pathlib import Path

import torch
from ultralytics import YOLO

BASE_DIR = Path(__file__).parent.resolve()
DATA_YAML = BASE_DIR / "dataset_v2" / "data.yaml"
RUN_DIR = BASE_DIR / "runs" / "detect" / "waste_yolo11s_v2"
APP_WEIGHTS = BASE_DIR / "streamlit-detection-tracking - app" / "weights" / "waste_yolo11s.pt"


def main():
    if not DATA_YAML.exists():
        print(f"[ERROR] {DATA_YAML} not found. Run `python prepare_dataset.py` first.")
        sys.exit(1)

    device = 0 if torch.cuda.is_available() else "cpu"
    last_ckpt = RUN_DIR / "weights" / "last.pt"

    if last_ckpt.exists() and "--fresh" not in sys.argv:
        # Resume an interrupted run with its original arguments (don't change hyperparameters on resume)
        print(f"[INFO] Resuming from {last_ckpt}")
        YOLO(str(last_ckpt)).train(resume=True)
    else:
        # Start from COCO-pretrained weights, not from earlier waste fine-tunes
        model = YOLO("yolo11s.pt")
        model.train(
            data=str(DATA_YAML),
            epochs=80,
            patience=25,
            imgsz=640,
            batch=16,
            device=device,
            workers=4,
            cos_lr=True,
            close_mosaic=10,
            mixup=0.1,
            degrees=10.0,     # waste items appear at arbitrary orientations
            flipud=0.2,
            max_det=500,      # biodegradable images contain up to ~360 labelled objects
            seed=0,
            project=str(RUN_DIR.parent),
            name=RUN_DIR.name,
            exist_ok=True,
        )

    best = RUN_DIR / "weights" / "best.pt"
    model = YOLO(str(best))
    print("\n[INFO] Held-out test set results:")
    model.val(data=str(DATA_YAML), split="test", batch=16, workers=0, max_det=500)

    APP_WEIGHTS.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(best, APP_WEIGHTS)
    print(f"[OK] Deployed {best} -> {APP_WEIGHTS}")


if __name__ == "__main__":
    main()

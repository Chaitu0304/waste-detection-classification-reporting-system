"""
Train a fresh YOLO11m waste detector on the cleaned dataset (dataset_v3/).

Pipeline:  python prepare_dataset.py   -> dataset_v2 (balanced per-class split)
           python clean_dataset.py     -> dataset_v3 (crowded images + part-boxes removed)
           python train_v3.py          -> weights copied into the Streamlit app

Re-running resumes an interrupted run; pass --fresh to start over.
"""
import shutil
import sys
from pathlib import Path

import torch
from ultralytics import YOLO

BASE_DIR = Path(__file__).parent.resolve()
DATA_YAML = BASE_DIR / "dataset_v3" / "data.yaml"
RUN_DIR = BASE_DIR / "runs" / "detect" / "waste_yolo11m_v3"
APP_WEIGHTS = BASE_DIR / "streamlit-detection-tracking - app" / "weights" / "waste_yolo11m.pt"


def main():
    if not DATA_YAML.exists():
        print(f"[ERROR] {DATA_YAML} not found. Run prepare_dataset.py then clean_dataset.py first.")
        sys.exit(1)

    device = 0 if torch.cuda.is_available() else "cpu"
    last_ckpt = RUN_DIR / "weights" / "last.pt"

    if last_ckpt.exists() and "--fresh" not in sys.argv:
        # Resume an interrupted run with its original arguments (don't change hyperparameters on resume)
        print(f"[INFO] Resuming from {last_ckpt}")
        YOLO(str(last_ckpt)).train(resume=True)
    else:
        # Start from COCO-pretrained weights, not from earlier waste fine-tunes
        model = YOLO("yolo11m.pt")
        model.train(
            data=str(DATA_YAML),
            epochs=70,
            patience=25,
            imgsz=640,
            batch=8,          # YOLO11m at 640 fits a 6 GB GPU at batch 8
            device=device,
            workers=4,
            cos_lr=True,
            close_mosaic=10,
            mixup=0.1,
            degrees=10.0,     # waste items appear at arbitrary orientations
            flipud=0.2,
            seed=0,
            project=str(RUN_DIR.parent),
            name=RUN_DIR.name,
            exist_ok=True,
        )

    best = RUN_DIR / "weights" / "best.pt"
    APP_WEIGHTS.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(best, APP_WEIGHTS)
    print(f"[OK] Copied {best} -> {APP_WEIGHTS}")


if __name__ == "__main__":
    main()

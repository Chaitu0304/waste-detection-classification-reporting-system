import sys
import torch
import shutil
from pathlib import Path
from ultralytics import YOLO

def main():
    print("=" * 60)
    print("Starting YOLOv8 Fine-Tuning on Rebalanced Waste Dataset (6 Classes)")
    print("=" * 60)

    # 1. GPU Check
    device = 0 if torch.cuda.is_available() else "cpu"
    if device == 0:
        print(f"[OK] GPU Available: {torch.cuda.get_device_name(0)}")
    else:
        print("[WARNING] CUDA not detected. Training on CPU.")

    # 2. Paths Configuration
    base_dir = Path(__file__).parent.resolve()
    data_yaml = base_dir / "dataset_balanced" / "data.yaml"

    if not data_yaml.exists():
        print(f"[ERROR] Balanced dataset config not found at {data_yaml}")
        sys.exit(1)

    print(f"[OK] Dataset Config: {data_yaml}")
    print("[INFO] Initializing YOLOv8s base model for fine-tuning...")
    model = YOLO("yolov8s.pt")

    TARGET_EPOCHS = 30

    print(f"\n[INFO] Starting balanced fine-tuning for {TARGET_EPOCHS} epochs...")
    results = model.train(
        data=str(data_yaml),
        epochs=TARGET_EPOCHS,
        batch=16,
        imgsz=640,
        device=device,
        project="runs/detect",
        name="balanced_waste_train",
        exist_ok=True,
        cls=2.0,       # Strongly boost classification loss weight to enforce 6-class balance
        hsv_s=0.7,     # Saturation augmentation for specular highlights
        mixup=0.15,    # Mixup augmentation for texture invariance
        workers=0      # Safe multi-processing for Windows
    )

    print("\nBalanced Fine-Tuning Completed Successfully!")
    
    best_pt = base_dir / "runs" / "detect" / "balanced_waste_train" / "weights" / "best.pt"
    if best_pt.exists():
        target_app_pt = base_dir / "streamlit-detection-tracking - app" / "weights" / "yoloooo.pt"
        target_best_pt = base_dir / "streamlit-detection-tracking - app" / "weights" / "best.pt"
        target_app_pt.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(best_pt, target_app_pt)
        shutil.copy(best_pt, target_best_pt)
        print(f" -> Deployed latest fine-tuned weights to: {target_app_pt}")

if __name__ == "__main__":
    main()

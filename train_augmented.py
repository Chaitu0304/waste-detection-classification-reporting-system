import sys
import torch
import shutil
from pathlib import Path
from ultralytics import YOLO

def main():
    print("=" * 65)
    print("🚀 Starting 80-Epoch Fine-Tuning on Augmented Balanced Waste Dataset")
    print("=" * 65)

    # 1. GPU Check
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        print(f"[OK] GPU Detected: {gpu_name}")
        device = 0
    else:
        print("[WARNING] CUDA not detected. Training on CPU.")
        device = "cpu"

    # 2. Paths Configuration
    base_dir = Path(__file__).parent.resolve()
    data_yaml = base_dir / "dataset_balanced" / "data.yaml"

    if not data_yaml.exists():
        print(f"[ERROR] Dataset config not found at {data_yaml}")
        sys.exit(1)

    print(f"[OK] Dataset Config: {data_yaml}")
    print("[INFO] Initializing YOLOv8s base model for 80-epoch fine-tuning...")
    model = YOLO("yolov8s.pt")

    TARGET_EPOCHS = 80

    print(f"\n[INFO] Starting training for {TARGET_EPOCHS} epochs with mosaic & mixup augmentations...")
    results = model.train(
        data=str(data_yaml),
        epochs=TARGET_EPOCHS,
        batch=16,
        imgsz=640,
        device=device,
        project="runs/detect",
        name="augmented_waste_train",
        exist_ok=True,
        cls=2.0,            # 2.0x classification loss penalty (prioritizes correct material classification)
        mosaic=1.0,         # Stitches 4 images together to detect small & cluttered waste items
        mixup=0.20,         # Blends textures for glass & plastic transparency invariance
        degrees=15.0,       # Random rotation +/- 15 deg
        fliplr=0.5,         # Random horizontal flip
        cos_lr=True,        # Cosine annealing learning rate schedule
        patience=15,        # Early stopping safety
        workers=0           # Safe multiprocessing for Windows
    )

    print("\n🎉 Training Completed Successfully!")
    
    best_pt = base_dir / "runs" / "detect" / "augmented_waste_train" / "weights" / "best.pt"
    if best_pt.exists():
        target_app_pt = base_dir / "streamlit-detection-tracking - app" / "weights" / "yoloooo.pt"
        target_best_pt = base_dir / "streamlit-detection-tracking - app" / "weights" / "best.pt"
        target_app_pt.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(best_pt, target_app_pt)
        shutil.copy(best_pt, target_best_pt)
        print(f" -> Deployed fine-tuned 80-epoch weights to: {target_app_pt}")

if __name__ == "__main__":
    main()

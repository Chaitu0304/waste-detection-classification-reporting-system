import os
import sys
import zipfile
from pathlib import Path
import torch
from ultralytics import YOLO

def main():
    print("=" * 60)
    print("Starting Local YOLOv8 Waste Classification Training")
    print("=" * 60)
    
    # Check for dataset.zip auto-extraction
    dataset_dir = Path(__file__).parent / "dataset"
    zip_path = Path(__file__).parent / "dataset.zip"

    if zip_path.exists() and not (dataset_dir / "data.yaml").exists():
        print(f"[INFO] Found {zip_path}. Extracting to {dataset_dir}...")
        dataset_dir.mkdir(exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as z:
            z.extractall(dataset_dir)
        print("[OK] Extraction complete!")

    # Check GPU
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        print(f"[OK] GPU Detected: {gpu_name}")
        device = 0
    else:
        print("[WARNING] No CUDA GPU detected. Training on CPU will be slower.")
        device = 'cpu'

    # Check Dataset Config
    data_yaml = dataset_dir / "data.yaml"
    if not data_yaml.exists():
        print(f"[ERROR] Dataset config not found at {data_yaml}")
        print("\n[STEPS TO FIX]:")
        print("1. Open your Roboflow dashboard: https://app.roboflow.com/chaitanyas-workspace-ppjw4/waste-classification-new/1")
        print("2. Click 'Export Dataset' -> Select 'YOLOv8' -> Download zip")
        print("3. Place the downloaded ZIP in this directory as 'dataset.zip' (or extract to 'dataset/')")
        print("4. Run 'python train_local.py' again!\n")
        sys.exit(1)
        
    print(f"[OK] Dataset found: {data_yaml}")

    # Load Model (Resume from latest checkpoint if available)
    last_ckpt_candidates = [p for p in Path("runs").rglob("last.pt") if p.is_file()]
    if last_ckpt_candidates:
        last_ckpt = max(last_ckpt_candidates, key=lambda p: p.stat().st_mtime)
        print(f"[INFO] Resuming training from latest checkpoint: {last_ckpt}")
        model = YOLO(str(last_ckpt))
    else:
        print("[INFO] Loading YOLOv8s base model...")
        model = YOLO("yolov8s.pt")

    # High-Speed Train Configuration (imgsz=640, batch=32 for ~4x speedup)
    print("[INFO] Resuming training for up to 100 epochs (imgsz=640, batch=32 for 4x speed)...")
    results = model.train(
        data=str(data_yaml),
        epochs=100,
        imgsz=640,
        batch=32,
        patience=20,
        workers=0,  # Fixes Windows multiprocessing memory paging error (WinError 1455)
        device=device,
        project="runs/detect/runs/detect",
        name="local_waste_train",
        exist_ok=True
    )

    print("\n[SUCCESS] Training completed successfully!")
    best_weights_candidates = [p for p in Path("runs").rglob("best.pt") if p.is_file()]
    target_weights = Path("streamlit-detection-tracking - app/weights/yoloooo.pt")
    
    if best_weights_candidates:
        best_weights = max(best_weights_candidates, key=lambda p: p.stat().st_mtime)
        import shutil
        target_weights.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(best_weights, target_weights)
        print(f"[OK] Updated app weights from {best_weights} to: {target_weights}")

if __name__ == "__main__":
    main()

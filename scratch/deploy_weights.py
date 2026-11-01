import shutil
from pathlib import Path
from ultralytics import YOLO

base_dir = Path(".").resolve()
trained_weights = base_dir / "runs" / "detect" / "runs" / "detect" / "runs" / "detect" / "local_waste_train" / "weights" / "best.pt"
app_weights = base_dir / "streamlit-detection-tracking - app" / "weights" / "yoloooo.pt"
app_best = base_dir / "streamlit-detection-tracking - app" / "weights" / "best.pt"

print(f"Trained weights exist: {trained_weights.exists()} ({trained_weights.stat().st_size / (1024*1024):.2f} MB)")
print(f"Current app weights size: {app_weights.stat().st_size / (1024*1024):.2f} MB")

if trained_weights.exists():
    shutil.copy(trained_weights, app_weights)
    shutil.copy(trained_weights, app_best)
    print("-> Successfully updated app weights with trained best.pt!")

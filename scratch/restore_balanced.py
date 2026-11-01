import shutil
from pathlib import Path

base_dir = Path(".").resolve()
balanced_weights = base_dir / "runs" / "detect" / "runs" / "detect" / "balanced_waste_train" / "weights" / "best.pt"
app_weights = base_dir / "streamlit-detection-tracking - app" / "weights" / "yoloooo.pt"
app_best = base_dir / "streamlit-detection-tracking - app" / "weights" / "best.pt"

print(f"Balanced weights exist: {balanced_weights.exists()} ({balanced_weights.stat().st_size / (1024*1024):.2f} MB)")

if balanced_weights.exists():
    shutil.copy(balanced_weights, app_weights)
    shutil.copy(balanced_weights, app_best)
    print("-> Successfully restored fine-tuned balanced model weights (21.48 MB) to app directory!")

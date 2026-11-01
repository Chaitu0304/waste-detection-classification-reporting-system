from pathlib import Path
import sys

# Get the absolute path of the current file
file_path = Path(__file__).resolve()

# Get the parent directory of the current file
root_path = file_path.parent

# Add the root path to the sys.path list if it is not already there
if root_path not in sys.path:
    sys.path.append(str(root_path))

# Get the relative path of the root directory with respect to the current working directory
try:
    ROOT = root_path.relative_to(Path.cwd())
except ValueError:
    ROOT = root_path

# Sources
IMAGE = 'Image'
VIDEO = 'Video'
WEBCAM = 'Webcam'
RTSP = 'RTSP'
YOUTUBE = 'YouTube'

SOURCES_LIST = [IMAGE, VIDEO, WEBCAM, YOUTUBE, RTSP]

# Images config
IMAGES_DIR = ROOT / 'images'
DEFAULT_IMAGE = IMAGES_DIR / 'def.jfif'
DEFAULT_DETECT_IMAGE = IMAGES_DIR / 'def1.jpg'


# Videos config
VIDEO_DIR = ROOT / 'videos'
VIDEO_1_PATH = VIDEO_DIR / 'video_1.mp4'
VIDEO_2_PATH = VIDEO_DIR / 'video_2.mp4'
VIDEO_3_PATH = VIDEO_DIR / 'video_3.mp4'
VIDEO_4_PATH = VIDEO_DIR / 'video_4.mp4'
VIDEO_5_PATH = VIDEO_DIR / 'video_5.mp4'
VIDEOS_DICT = {
    'video_1': VIDEO_1_PATH,
    'video_2': VIDEO_2_PATH,
    'video_3': VIDEO_3_PATH,
    'video_4': VIDEO_4_PATH,
    'video_5': VIDEO_5_PATH,
}


# ML Model config
MODEL_DIR = root_path / 'weights'

AVAILABLE_MODELS = {
    "🌟 Smart Hybrid AI (Best Accuracy - Two-Stage)": {
        "path": Path("hybrid"),
        "filename": "Smart Hybrid AI (Two-Stage)",
        "description": "Two-stage precision detector: COCO object localization + focused waste material classification. Eliminates dirt hallucinations and resolves Glass/Metal/Plastic."
    }
}
_model_specs = [
    ("waste_yolo_mixed.pt", "YOLO11m Mixed (Multi-Category Fine-Tuned)", "Trained on multi-category scenes with touching/mixed waste items"),
    ("waste_yolo11m.pt", "YOLO11m (High Precision - Cleaned v3)", "Best accuracy, trained on cleaned dataset with part-boxes removed"),
    ("waste_yolo11s.pt", "YOLO11s (Fast - v2)", "Fast inference, balanced dataset"),
    ("yoloooo.pt", "YOLOv8 Tuned (Original)", "Original fine-tuned YOLOv8 weights"),
    ("best.pt", "YOLOv8 Best Checkpoint", "Original best training checkpoint"),
]

for _filename, _name, _desc in _model_specs:
    _p = MODEL_DIR / _filename
    if _p.exists():
        AVAILABLE_MODELS[_name] = {
            "path": _p,
            "filename": _filename,
            "description": _desc
        }

# Default detection model: Smart Hybrid AI preferred for best accuracy
DETECTION_MODEL = Path("hybrid")

# Webcam
WEBCAM_PATH = 0

"""
Compare waste detection models on a held-out test split.

Usage: python evaluate_models.py <data.yaml> <weights.pt> [<weights.pt> ...]
Prints per-class mAP50 / recall and, per class, how many objects were
missed entirely vs. detected with the wrong class (conf >= 0.25).
"""
import sys
import tempfile

from ultralytics import YOLO


def evaluate(weights, data):
    model = YOLO(weights)
    out = tempfile.mkdtemp()
    r = model.val(data=data, split="test", batch=16, workers=0, conf=0.25, max_det=500,
                  plots=True, verbose=False, project=out, name="cm")
    cm = r.confusion_matrix.matrix  # rows = predicted, cols = true, last = background
    names = list(model.names.values())
    print(f"\n=== {weights}")
    print(f"{'class':15s}{'mAP50':>8s}{'recall':>8s}{'missed':>8s}{'wrong cls':>10s}  most confused with")
    for i, n in enumerate(names):
        total = cm[:, i].sum()
        missed = cm[-1, i] / total
        wrong_col = cm[:-1, i].copy()
        wrong_col[i] = 0
        confused = names[int(wrong_col.argmax())] if wrong_col.sum() else "-"
        print(f"{n:15s}{r.box.ap50[i]:8.3f}{r.box.r[i]:8.3f}{missed:8.0%}{wrong_col.sum() / total:10.0%}  {confused}")
    print(f"{'ALL':15s}{r.box.map50:8.3f}{r.box.mr:8.3f}   mAP50-95={r.box.map:.3f}")


if __name__ == "__main__":
    data, *weights = sys.argv[1:]
    for w in weights:
        evaluate(w, data)

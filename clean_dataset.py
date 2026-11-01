"""
Build dataset_v3/ from dataset_v2/ (keeps the same train/valid/test membership)
with two label-quality fixes:

1. Drop "crowded" images (> MAX_BOXES boxes). These are almost all grocery
   displays / fruit piles labelled as BIODEGRADABLE with hundreds of boxes and
   many objects left unlabelled. They made up ~45% of all boxes and taught the
   model that real objects are background.
2. Remove part-boxes: a box that lies >= 90% inside a larger box of the SAME
   class (bottle label / cap inside the bottle, a flap inside a carton).
   Labels then consistently mean "one whole item". Boxes inside a box of a
   DIFFERENT class (food in a glass jar, metal cap on a bottle) are kept.

Run `python prepare_dataset.py` first to build dataset_v2/.
"""
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
SRC = BASE_DIR / "dataset_v2"
DST = BASE_DIR / "dataset_v3"
MAX_BOXES = 30
NESTED_FRACTION = 0.9
NESTED_AREA_RATIO = 1.5


def inside_fraction(a, b):
    """Fraction of box a (xyxy) that lies inside box b."""
    iw = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    ih = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    area = (a[2] - a[0]) * (a[3] - a[1])
    return iw * ih / area if area > 0 else 0.0


def clean_labels(lines):
    boxes = []
    for line in lines:
        c, x, y, w, h = line.split()
        x, y, w, h = map(float, (x, y, w, h))
        boxes.append((int(c), (x - w / 2, y - h / 2, x + w / 2, y + h / 2), w * h, line))
    keep = []
    for i, (c, box, area, line) in enumerate(boxes):
        is_part = any(
            j != i and c2 == c and area2 > area * NESTED_AREA_RATIO and inside_fraction(box, box2) >= NESTED_FRACTION
            for j, (c2, box2, area2, _) in enumerate(boxes)
        )
        if not is_part:
            keep.append(line)
    return keep


def main():
    if DST.exists():
        shutil.rmtree(DST)
    for split in ("train", "valid", "test"):
        (DST / split / "images").mkdir(parents=True)
        (DST / split / "labels").mkdir(parents=True)
        n_img = n_crowded = n_before = n_after = 0
        for lbl in sorted((SRC / split / "labels").glob("*.txt")):
            lines = [l.strip() for l in lbl.read_text().splitlines() if l.strip()]
            if len(lines) > MAX_BOXES:
                n_crowded += 1
                continue
            kept = clean_labels(lines)
            img = next((SRC / split / "images").glob(lbl.stem + ".*"))
            shutil.copy2(img, DST / split / "images" / img.name)
            (DST / split / "labels" / lbl.name).write_text("\n".join(kept) + "\n")
            n_img += 1
            n_before += len(lines)
            n_after += len(kept)
        print(f"{split:6s} images kept={n_img} dropped(crowded)={n_crowded} "
              f"boxes {n_before} -> {n_after} (removed {n_before - n_after} part-boxes)")

    yaml = (SRC / "data.yaml").read_text().replace(SRC.as_posix(), DST.as_posix())
    (DST / "data.yaml").write_text(yaml)
    print(f"[OK] Wrote {DST / 'data.yaml'}")


if __name__ == "__main__":
    main()

"""
Rebuild the train/valid/test split of the Roboflow waste dataset.

The original Roboflow export is split very unevenly by class:
  - valid has no PAPER / PLASTIC images (only 33 + 214 stray boxes)
  - test  has no GLASS / BIODEGRADABLE / CARDBOARD images
so validation mAP (used for early stopping and picking best.pt) ignored whole classes.

This script pools all images and re-splits them 80/10/10 *per class*
(class = filename prefix, e.g. "glass123_jpg.rf.<hash>.jpg") into dataset_v2/.
The original dataset/ folder is left untouched.
"""
import random
import re
import shutil
from collections import defaultdict
from pathlib import Path

random.seed(42)

BASE_DIR = Path(__file__).parent.resolve()
SRC = BASE_DIR / "dataset"
DST = BASE_DIR / "dataset_v2"
SPLITS = {"train": 0.8, "valid": 0.1, "test": 0.1}
NAMES = ['BIODEGRADABLE', 'CARDBOARD', 'GLASS', 'METAL', 'PAPER', 'PLASTIC']


def main():
    groups = defaultdict(list)
    for split in ("train", "valid", "test"):
        for img in (SRC / split / "images").iterdir():
            lbl = SRC / split / "labels" / (img.stem + ".txt")
            if lbl.exists():
                groups[re.match(r"[a-z]+", img.name).group(0)].append((img, lbl))

    if DST.exists():
        shutil.rmtree(DST)
    for split in SPLITS:
        (DST / split / "images").mkdir(parents=True)
        (DST / split / "labels").mkdir(parents=True)

    for cls, items in sorted(groups.items()):
        items.sort()
        random.shuffle(items)
        n_train = int(len(items) * SPLITS["train"])
        n_valid = int(len(items) * SPLITS["valid"])
        parts = {
            "train": items[:n_train],
            "valid": items[n_train:n_train + n_valid],
            "test": items[n_train + n_valid:],
        }
        for split, pairs in parts.items():
            for img, lbl in pairs:
                shutil.copy2(img, DST / split / "images" / img.name)
                shutil.copy2(lbl, DST / split / "labels" / lbl.name)
        print(f"{cls:15s} total={len(items):5d} " + " ".join(f"{s}={len(p)}" for s, p in parts.items()))

    (DST / "data.yaml").write_text(
        f"path: {DST.as_posix()}\n"
        "train: train/images\n"
        "val: valid/images\n"
        "test: test/images\n\n"
        f"nc: {len(NAMES)}\n"
        f"names: {NAMES}\n"
    )
    print(f"[OK] Wrote {DST / 'data.yaml'}")


if __name__ == "__main__":
    main()

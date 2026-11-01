import os
from pathlib import Path
from collections import Counter

dataset_dir = Path("dataset")
class_names = ['BIODEGRADABLE', 'CARDBOARD', 'GLASS', 'METAL', 'PAPER', 'PLASTIC']

for split in ['train', 'valid', 'test']:
    lbl_dir = dataset_dir / split / "labels"
    if not lbl_dir.exists():
        continue
    counter = Counter()
    total_files = 0
    for f in lbl_dir.glob("*.txt"):
        total_files += 1
        lines = f.read_text().splitlines()
        for line in lines:
            if line.strip():
                cls_id = int(line.split()[0])
                counter[cls_id] += 1
    print(f"\n--- Split: {split} ({total_files} files) ---")
    for cid in range(6):
        cname = class_names[cid] if cid < len(class_names) else f"Class {cid}"
        print(f"  Class {cid} ({cname:15s}): {counter[cid]} bounding boxes")

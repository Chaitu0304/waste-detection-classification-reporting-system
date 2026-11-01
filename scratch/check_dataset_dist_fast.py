import os
from pathlib import Path
from collections import Counter

dataset_dir = Path("dataset")
class_names = ['BIODEGRADABLE', 'CARDBOARD', 'GLASS', 'METAL', 'PAPER', 'PLASTIC']

for split in ['valid', 'test', 'train']:
    lbl_dir = dataset_dir / split / "labels"
    if not lbl_dir.exists():
        continue
    counter = Counter()
    total_files = 0
    for entry in os.scandir(lbl_dir):
        if entry.name.endswith(".txt"):
            total_files += 1
            with open(entry.path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        cls_id = int(line.split()[0])
                        counter[cls_id] += 1
    print(f"--- Split: {split} ({total_files} files) ---", flush=True)
    for cid in range(6):
        cname = class_names[cid] if cid < len(class_names) else f"Class {cid}"
        print(f"  Class {cid} ({cname:15s}): {counter[cid]} bounding boxes", flush=True)

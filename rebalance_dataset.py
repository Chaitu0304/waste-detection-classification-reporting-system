"""
Dataset Class Distribution & Rebalancing Inspection Utility Script

Usage:
    python rebalance_dataset.py
"""

import os
import glob
from collections import Counter

NAMES = ['BIODEGRADABLE', 'CARDBOARD', 'GLASS', 'METAL', 'PAPER', 'PLASTIC']

def analyze_distribution(dataset_dir="dataset"):
    print("==================================================")
    print("DATASET CLASS INSTANCE DISTRIBUTION AUDIT")
    print("==================================================")
    total_all = Counter()
    for split in ['train', 'valid', 'test']:
        lbl_dir = os.path.join(dataset_dir, split, 'labels')
        txt_files = glob.glob(os.path.join(lbl_dir, '*.txt'))
        split_counts = Counter()
        for f in txt_files:
            with open(f, 'r', encoding='utf-8') as fp:
                for line in fp:
                    parts = line.strip().split()
                    if parts:
                        cls_id = int(parts[0])
                        split_counts[cls_id] += 1
                        total_all[cls_id] += 1
        total_split = sum(split_counts.values())
        print(f"\nSplit: {split.upper()} ({len(txt_files)} image files, {total_split} instances)")
        for cid, name in enumerate(NAMES):
            cnt = split_counts[cid]
            pct = (cnt / total_split * 100) if total_split > 0 else 0
            print(f"  [{cid}] {name:15s}: {cnt:6d} instances ({pct:5.1f}%)")

    total_instances = sum(total_all.values())
    print("\n--------------------------------------------------")
    print(f"TOTAL OVERALL INSTANCES Across Dataset: {total_instances}")
    for cid, name in enumerate(NAMES):
        cnt = total_all[cid]
        pct = (cnt / total_instances * 100) if total_instances > 0 else 0
        print(f"  [{cid}] {name:15s}: {cnt:6d} instances ({pct:5.1f}%)")
    print("==================================================\n")

if __name__ == "__main__":
    analyze_distribution()

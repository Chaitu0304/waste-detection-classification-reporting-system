import os
import shutil
import random
from pathlib import Path
from collections import Counter

# Set random seed for reproducible sampling
random.seed(42)

BASE_DIR = Path(__file__).parent.resolve()
SRC_DATASET = BASE_DIR / "dataset"
DST_DATASET = BASE_DIR / "dataset_balanced"

def analyze_and_balance():
    print("=" * 60)
    print("[INFO] Starting Superfast Dataset Rebalancing (Option A)")
    print("=" * 60)

    # 1. Prepare Destination Directories
    if DST_DATASET.exists():
        print(f"[INFO] Removing old destination directory {DST_DATASET}...")
        shutil.rmtree(DST_DATASET)

    dst_train_img = DST_DATASET / "train" / "images"
    dst_train_lbl = DST_DATASET / "train" / "labels"
    dst_train_img.mkdir(parents=True, exist_ok=True)
    dst_train_lbl.mkdir(parents=True, exist_ok=True)

    src_train_img_dir = SRC_DATASET / "train" / "images"
    src_train_lbl_dir = SRC_DATASET / "train" / "labels"

    # Fast O(N) map of image stems to image paths
    print("\n[STEP 1/3] Mapping image paths...")
    img_map = {}
    for img_file in src_train_img_dir.iterdir():
        if img_file.is_file():
            img_map[img_file.stem] = img_file

    # 2. Categorize Training Images
    print("\n[STEP 2/3] Categorizing training labels...")
    only_bio_files = []
    minority_files = []
    glass_files = []
    plastic_files = []

    train_labels = list(src_train_lbl_dir.glob("*.txt"))

    for lbl_file in train_labels:
        stem = lbl_file.stem
        if stem not in img_map:
            continue
        
        content = lbl_file.read_text().strip()
        if not content:
            continue

        lines = content.splitlines()
        classes_in_file = set(int(l.split()[0]) for l in lines if l.strip())
        
        has_minority = any(c in classes_in_file for c in [1, 2, 3, 4, 5])
        
        if 2 in classes_in_file:
            glass_files.append(lbl_file)
        if 5 in classes_in_file:
            plastic_files.append(lbl_file)

        if has_minority:
            minority_files.append(lbl_file)
        else:
            only_bio_files.append(lbl_file)

    print(f" -> Total Train Image Labels: {len(train_labels)}")
    print(f" -> Images containing Minority Classes (Glass/Plastic/Metal/Paper/Cardboard): {len(minority_files)}")
    print(f" -> Images containing ONLY Biodegradable: {len(only_bio_files)}")
    print(f" -> Images containing Glass: {len(glass_files)}")
    print(f" -> Images containing Plastic: {len(plastic_files)}")

    # 3. Copy and Oversample Minority Files
    print("\n[STEP 3/3] Rebalancing training dataset...")
    copied_count = 0

    # Copy 100% of minority class files
    for lbl_file in minority_files:
        stem = lbl_file.stem
        img_file = img_map[stem]
        shutil.copy2(img_file, dst_train_img / img_file.name)
        shutil.copy2(lbl_file, dst_train_lbl / lbl_file.name)
        copied_count += 1

    # Oversample GLASS images (2x copy)
    for lbl_file in glass_files:
        stem = lbl_file.stem
        img_file = img_map[stem]
        new_stem = f"aug_glass_{stem}"
        shutil.copy2(img_file, dst_train_img / f"{new_stem}{img_file.suffix}")
        shutil.copy2(lbl_file, dst_train_lbl / f"{new_stem}.txt")
        copied_count += 1

    # Oversample PLASTIC images (2x copy)
    for lbl_file in plastic_files:
        stem = lbl_file.stem
        img_file = img_map[stem]
        new_stem = f"aug_plastic_{stem}"
        shutil.copy2(img_file, dst_train_img / f"{new_stem}{img_file.suffix}")
        shutil.copy2(lbl_file, dst_train_lbl / f"{new_stem}.txt")
        copied_count += 1

    # Sub-sample `only_bio_files` to cap BIODEGRADABLE instances around ~4,400
    subsample_bio_count = 220
    selected_bio_files = random.sample(only_bio_files, min(subsample_bio_count, len(only_bio_files)))

    for lbl_file in selected_bio_files:
        stem = lbl_file.stem
        img_file = img_map[stem]
        shutil.copy2(img_file, dst_train_img / img_file.name)
        shutil.copy2(lbl_file, dst_train_lbl / lbl_file.name)
        copied_count += 1

    print(f" -> Total Rebalanced Train Images Created: {copied_count}")

    # 4. Calculate Final Balanced Instance Statistics
    print("\n[RESULT] Calculating final balanced instance distribution...")
    final_counts = Counter()
    for lbl_file in dst_train_lbl.glob("*.txt"):
        lines = [l.strip() for l in lbl_file.read_text().splitlines() if l.strip()]
        for l in lines:
            final_counts[int(l.split()[0])] += 1

    class_names = ['BIODEGRADABLE', 'CARDBOARD', 'GLASS', 'METAL', 'PAPER', 'PLASTIC']
    print("\n[RESULT] FINAL REBALANCED CLASS INSTANCE COUNTS:")
    print("-" * 55)
    for cid, cname in enumerate(class_names):
        print(f"  Class {cid} ({cname:15s}): {final_counts[cid]:6d} instances")
    print("-" * 55)

    # 5. Create dataset_balanced/data.yaml
    yaml_content = f"""path: {DST_DATASET.as_posix()}
train: train/images
val: {(SRC_DATASET / 'valid' / 'images').as_posix()}
test: {(SRC_DATASET / 'test' / 'images').as_posix()}

nc: 6
names: ['BIODEGRADABLE', 'CARDBOARD', 'GLASS', 'METAL', 'PAPER', 'PLASTIC']
"""
    yaml_path = DST_DATASET / "data.yaml"
    yaml_path.write_text(yaml_content)
    print(f"\n[OK] Created balanced dataset config at: {yaml_path}")
    print("[OK] Dataset rebalancing completed successfully!")

if __name__ == "__main__":
    analyze_and_balance()

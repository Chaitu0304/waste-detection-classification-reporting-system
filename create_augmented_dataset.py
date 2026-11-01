import os
import shutil
import random
from pathlib import Path
from collections import Counter
from PIL import Image, ImageEnhance

# Set random seed for reproducibility
random.seed(42)

BASE_DIR = Path(__file__).parent.resolve()
SRC_DATASET = BASE_DIR / "dataset"
DST_DATASET = BASE_DIR / "dataset_balanced"

CLASS_NAMES = ['BIODEGRADABLE', 'CARDBOARD', 'GLASS', 'METAL', 'PAPER', 'PLASTIC']

def augment_and_write(img_path, lbl_path, dst_img_dir, dst_lbl_dir, aug_type, prefix):
    """
    Applies precise geometry/color augmentations and transforms YOLO label coordinates.
    aug_type options: 'hflip', 'vflip', 'rot180', 'color'
    """
    img = Image.open(img_path)
    lines = lbl_path.read_text().splitlines()
    
    stem = f"{prefix}_{img_path.stem}"
    dst_img_path = dst_img_dir / f"{stem}{img_path.suffix}"
    dst_lbl_path = dst_lbl_dir / f"{stem}.txt"

    new_lines = []

    if aug_type == 'hflip':
        aug_img = img.transpose(Image.FLIP_LEFT_RIGHT)
        for line in lines:
            if not line.strip():
                continue
            parts = line.split()
            cid = parts[0]
            cx, cy, w, h = map(float, parts[1:])
            new_lines.append(f"{cid} {1.0 - cx:.6f} {cy:.6f} {w:.6f} {h:.6f}")

    elif aug_type == 'vflip':
        aug_img = img.transpose(Image.FLIP_TOP_BOTTOM)
        for line in lines:
            if not line.strip():
                continue
            parts = line.split()
            cid = parts[0]
            cx, cy, w, h = map(float, parts[1:])
            new_lines.append(f"{cid} {cx:.6f} {1.0 - cy:.6f} {w:.6f} {h:.6f}")

    elif aug_type == 'rot180':
        aug_img = img.rotate(180)
        for line in lines:
            if not line.strip():
                continue
            parts = line.split()
            cid = parts[0]
            cx, cy, w, h = map(float, parts[1:])
            new_lines.append(f"{cid} {1.0 - cx:.6f} {1.0 - cy:.6f} {w:.6f} {h:.6f}")

    elif aug_type == 'color':
        # Brightness & Color enhance
        enhancer = ImageEnhance.Brightness(img)
        aug_img = enhancer.enhance(random.uniform(0.7, 1.3))
        enhancer_c = ImageEnhance.Color(aug_img)
        aug_img = enhancer_c.enhance(random.uniform(0.7, 1.3))
        for line in lines:
            if line.strip():
                new_lines.append(line.strip())

    else:
        aug_img = img
        for line in lines:
            if line.strip():
                new_lines.append(line.strip())

    aug_img.save(dst_img_path)
    dst_lbl_path.write_text("\n".join(new_lines) + "\n")

def build_augmented_dataset():
    print("=" * 65)
    print("[INFO] Creating Rebalanced Dataset with Augmented Minority Classes")
    print("=" * 65)

    if DST_DATASET.exists():
        print(f"[INFO] Removing old {DST_DATASET}...")
        shutil.rmtree(DST_DATASET)

    dst_train_img = DST_DATASET / "train" / "images"
    dst_train_lbl = DST_DATASET / "train" / "labels"
    dst_train_img.mkdir(parents=True, exist_ok=True)
    dst_train_lbl.mkdir(parents=True, exist_ok=True)

    src_train_img_dir = SRC_DATASET / "train" / "images"
    src_train_lbl_dir = SRC_DATASET / "train" / "labels"

    # Map image stem -> path
    print("\n[STEP 1/4] Mapping dataset image paths...")
    img_map = {}
    for entry in os.scandir(src_train_img_dir):
        if entry.is_file():
            p = Path(entry.path)
            img_map[p.stem] = p

    # Categorize images
    print("\n[STEP 2/4] Categorizing training labels...")
    only_bio_files = []
    minority_files = []

    lbl_entries = [Path(e.path) for e in os.scandir(src_train_lbl_dir) if e.name.endswith('.txt')]

    for lbl_file in lbl_entries:
        stem = lbl_file.stem
        if stem not in img_map:
            continue
        content = lbl_file.read_text().strip()
        if not content:
            continue
        classes = set(int(line.split()[0]) for line in content.splitlines() if line.strip())
        
        has_minority = any(c in classes for c in [1, 2, 3, 4, 5])
        if has_minority:
            minority_files.append((lbl_file, classes))
        else:
            only_bio_files.append(lbl_file)

    print(f" -> Total Train Image Labels: {len(lbl_entries)}")
    print(f" -> Images with Minority Classes (Glass/Metal/Paper/Cardboard/Plastic): {len(minority_files)}")
    print(f" -> Images with ONLY Biodegradable: {len(only_bio_files)}")

    # 3. Subsample ONLY-BIO files to ~1,500 images for a balanced representation
    print("\n[STEP 3/4] Copying & Augmenting dataset files...")
    target_bio_count = 1500
    selected_bio = random.sample(only_bio_files, min(target_bio_count, len(only_bio_files)))

    # Copy selected BIODEGRADABLE files as-is
    for lbl_file in selected_bio:
        stem = lbl_file.stem
        img_file = img_map[stem]
        shutil.copy2(img_file, dst_train_img / img_file.name)
        shutil.copy2(lbl_file, dst_train_lbl / lbl_file.name)

    print(f" -> Copied {len(selected_bio)} balanced Biodegradable images.")

    # Copy 100% of minority files + generate 2 augmented variants for each
    augmented_count = 0
    for lbl_file, classes in minority_files:
        stem = lbl_file.stem
        img_file = img_map[stem]
        
        # 1. Copy original file as-is
        shutil.copy2(img_file, dst_train_img / img_file.name)
        shutil.copy2(lbl_file, dst_train_lbl / lbl_file.name)
        augmented_count += 1

        # 2. Augment 1: Horizontal Flip
        augment_and_write(img_file, lbl_file, dst_train_img, dst_train_lbl, 'hflip', 'aug1_hflip')
        augmented_count += 1

        # 3. Augment 2: Color / Brightness Jitter
        augment_and_write(img_file, lbl_file, dst_train_img, dst_train_lbl, 'color', 'aug2_color')
        augmented_count += 1

        # 4. For GLASS (2) & CARDBOARD (1) & PAPER (4), add 180-deg rotation variant
        if any(c in classes for c in [1, 2, 4]):
            augment_and_write(img_file, lbl_file, dst_train_img, dst_train_lbl, 'rot180', 'aug3_rot180')
            augmented_count += 1

    print(f" -> Generated {augmented_count} augmented minority class images!")

    # 4. Calculate final instance statistics
    print("\n[STEP 4/4] Calculating final balanced instance distribution...")
    final_counts = Counter()
    for lbl_file in dst_train_lbl.glob("*.txt"):
        lines = lbl_file.read_text().splitlines()
        for l in lines:
            if l.strip():
                final_counts[int(l.split()[0])] += 1

    print("\n" + "=" * 65)
    print("FINAL REBALANCED & AUGMENTED CLASS INSTANCE COUNTS:")
    print("-" * 65)
    for cid, cname in enumerate(CLASS_NAMES):
        print(f"  Class {cid} ({cname:15s}): {final_counts[cid]:6d} bounding boxes")
    print("-" * 65)

    # Write dataset_balanced/data.yaml
    yaml_content = f"""path: {DST_DATASET.as_posix()}
train: train/images
val: {(SRC_DATASET / 'valid' / 'images').as_posix()}
test: {(SRC_DATASET / 'test' / 'images').as_posix()}

nc: 6
names: ['BIODEGRADABLE', 'CARDBOARD', 'GLASS', 'METAL', 'PAPER', 'PLASTIC']
"""
    yaml_path = DST_DATASET / "data.yaml"
    yaml_path.write_text(yaml_content)
    print(f"\n[OK] Balanced dataset config created at: {yaml_path}")
    print("[OK] Dataset creation completed successfully!")

if __name__ == "__main__":
    build_augmented_dataset()

"""
Priprema dataseta: sortira Galaxy Zoo 2 slike u foldere po klasama.

Ulaz:
  - folder sa raspakovanim GZ2 slikama (imena fajlova su asset_id, npr. 16.jpg)
  - CSV sa kolonama asset_id,gz2_class
    (gz2_objid_assetid_gz2class_all_samples_one_image_trimmed.csv)

Izlaz:
    images_gz2/
        Barred/  Elliptical/  Spiral/

Mapiranje GZ2 klase u tri kategorije:
    gz2_class pocinje sa 'E'   -> Elliptical   (Er, Ei, Ec, ...)
    gz2_class pocinje sa 'SB'  -> Barred       (SBa, SBc2m, ...)
    gz2_class pocinje sa 'S'   -> Spiral       (Sb, Sc1t, Sen, ...)
    ostalo ('A' = artefakt/zvezda) -> preskace se

Pokretanje:
    python prepare_dataset.py --images-dir images --csv gz2_classes.csv

Podaci se preuzimaju sa https://data.galaxyzoo.org (vidi data/README.md).
"""

import argparse
import csv
import os
import shutil

CLASS_DIRS = ('Barred', 'Elliptical', 'Spiral')
IMAGE_EXT = ('.jpg', '.jpeg', '.png')


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--images-dir', required=True,
                   help='Folder sa raspakovanim GZ2 slikama (imena = asset_id)')
    p.add_argument('--csv', required=True,
                   help='CSV sa kolonama asset_id,gz2_class')
    p.add_argument('--out-dir', default='images_gz2',
                   help='Izlazni folder (default: images_gz2)')
    p.add_argument('--move', action='store_true',
                   help='Premesti fajlove umesto kopiranja (brze, stedi prostor)')
    p.add_argument('--limit-per-class', type=int, default=None,
                   help='Uzmi najvise N slika po klasi (za balansiran podskup)')
    return p.parse_args()


def map_gz2_class(gz2_class):
    """Vraca ime klase ili None ako slika ne ulazi u dataset."""
    c = gz2_class.strip()
    if c.startswith('E'):
        return 'Elliptical'
    if c.startswith('SB'):
        return 'Barred'
    if c.startswith('S'):
        return 'Spiral'
    return None


def index_images(images_dir):
    """asset_id -> putanja do fajla."""
    index = {}
    for name in os.listdir(images_dir):
        stem, ext = os.path.splitext(name)
        if ext.lower() in IMAGE_EXT:
            index[stem] = os.path.join(images_dir, name)
    return index


def main():
    args = parse_args()

    for cls in CLASS_DIRS:
        os.makedirs(os.path.join(args.out_dir, cls), exist_ok=True)

    print(f"Indeksiram slike iz {args.images_dir} ...")
    images = index_images(args.images_dir)
    print(f"  Nadjeno {len(images)} slika.")

    counts = {cls: 0 for cls in CLASS_DIRS}
    skipped_class = 0
    missing_image = 0

    with open(args.csv, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            cls = map_gz2_class(row['gz2_class'])
            if cls is None:
                skipped_class += 1
                continue
            if args.limit_per_class and counts[cls] >= args.limit_per_class:
                continue

            src = images.get(row['asset_id'].strip())
            if src is None:
                missing_image += 1
                continue

            dst = os.path.join(args.out_dir, cls, os.path.basename(src))
            if args.move:
                shutil.move(src, dst)
            else:
                shutil.copy2(src, dst)
            counts[cls] += 1

    print("\n--- Rezultat ---")
    total = sum(counts.values())
    for cls in CLASS_DIRS:
        print(f"  {cls:<12} {counts[cls]:>7} slika")
    print(f"  {'UKUPNO':<12} {total:>7} slika")
    print(f"\n  Preskoceno (klasa A / nepoznata): {skipped_class}")
    print(f"  Nema slike za asset_id u CSV-u  : {missing_image}")
    print(f"\nDataset je u: {args.out_dir}")


if __name__ == '__main__':
    main()

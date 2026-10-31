# Dataset

Slike i oznake dolaze iz projekta **Galaxy Zoo 2** i **nisu deo ovog rada**. Dataset
nije u repozitorijumu — 243.434 slike, oko 5 GB.

## Preuzimanje

1. **Slike** — `images_gz2.zip` (sve GZ2 slike, ime fajla = `asset_id`):
   [Galaxy Zoo 2 images na Zenodo-u](https://zenodo.org/records/3565489)

2. **Oznake** — tabela sa morfološkim klasama, sa
   [data.galaxyzoo.org](https://data.galaxyzoo.org):
   *"GZ2 — Table 1 — Normal-depth sample with new debiasing method"* (Hart et al. 2016),
   plus `gz2_filename_mapping.csv` za povezivanje `objid` ↔ `asset_id`.

   Za `prepare_dataset.py` potreban je CSV sa dve kolone:

   ```
   asset_id,gz2_class
   3,Sb
   4,Sc?l
   5,Er
   ```

3. **Sortiranje u klase** — iz korena repozitorijuma:

   ```bash
   python prepare_dataset.py --images-dir images --csv gz2_classes.csv --out-dir images_gz2
   ```

## Mapiranje klasa

GZ2 oznake (`gz2_class`) su detaljne morfološke šifre (`Er`, `Sc1t`, `SBc2m`, ...).
Svedene su na tri klase po prvom slovu šifre:

| GZ2 šifra počinje sa | Klasa | Primeri |
|---|---|---|
| `E` | Elliptical | `Er`, `Ei`, `Ec` |
| `SB` | Barred | `SBa`, `SBc2m` |
| `S` (ostalo) | Spiral | `Sb`, `Sc1t`, `Sen` |
| `A` | *preskače se* | artefakti / zvezde |

Dobijena raspodela:

| Klasa | Broj slika | Udeo |
|---|---|---|
| Elliptical | ~97.600 | 41% |
| Spiral | ~95.800 | 40% |
| Barred | ~45.600 | 19% |
| **Ukupno** | **~239.000** | |

Dataset je neizbalansiran, zato `train.py` koristi `class_weight='balanced'`.

Broj je nešto manji od CSV tabele jer za ~700 redova ne postoji odgovarajuća slika —
Galaxy Zoo tim to pominje u svom README-u i savetuje da se takvi redovi ispuste.
`prepare_dataset.py` ih automatski preskače i prijavi na kraju.

## Citiranje

Ako koristiš ovaj dataset, obavezno citiraj:

- **Willett et al. (2013)**, *Galaxy Zoo 2: detailed morphological classifications for
  304,122 galaxies from the Sloan Digital Sky Survey*, MNRAS, 435, 2835.
  [DOI: 10.1093/mnras/stt1458](https://doi.org/10.1093/mnras/stt1458)
- **Hart et al. (2016)**, MNRAS, 461, 3663.
  [DOI: 10.1093/mnras/stw1588](https://doi.org/10.1093/mnras/stw1588)
  (ako se koriste debiased tabele)
- DOI samog dataseta slika.

Originalni README Galaxy Zoo tima, sa punim uslovima i kontaktima, je u
[`GALAXY_ZOO_README.txt`](GALAXY_ZOO_README.txt).

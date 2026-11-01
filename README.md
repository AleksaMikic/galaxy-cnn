# Galaxy CNN — morfološka klasifikacija galaksija

Konvolutivna neuronska mreža koja klasifikuje slike galaksija iz **Galaxy Zoo 2** u tri
morfološke klase: **Barred** (spiralna sa prečkom), **Elliptical** (eliptična) i
**Spiral** (spiralna bez prečke).

Projektni rad iz predmeta Neuralne mreže na Elektrotehničkom fakultetu Univerziteta u Beogradu.

## Autori

- **Aleksa Mikić** ([@AleksaMikic](https://github.com/AleksaMikic))
- **David M. Marković** ([@Dawidzard](https://github.com/Dawidzard))

Projekat je zajednički izrađen prije objavljivanja repozitorijuma na GitHubu.

Brojevi indeksa: `203/2023`, `134/2023`.

---

## Rezultati

Model je treniran na **239.029 slika** (80% trening / 20% validacija).

| Metrika | Trening | Validacija |
|---|---|---|
| Tačnost | 75.14% | **75.10%** |
| Preciznost (macro) | 73.90% | 73.97% |
| Osetljivost (macro) | 73.99% | 73.91% |
| F1-skor (macro) | 73.62% | 73.62% |

Po klasama (validacija):

| Klasa | Precision | Recall | F1 | Broj slika |
|---|---|---|---|---|
| Barred | 0.68 | 0.69 | 0.69 | 9.166 |
| Elliptical | 0.77 | 0.88 | 0.82 | 19.578 |
| Spiral | 0.77 | 0.65 | 0.70 | 19.061 |

Trening i validacija su praktično identični (75.14% vs 75.10%), što znači da model
**ne overfituje** — ograničenje je kapacitet/rezolucija, ne memorisanje. Najslabija
klasa je `Barred`: prečka je fina struktura koja se na 96×96 piksela često izgubi, a
ta klasa je i najmanje zastupljena u datasetu (19% uzoraka).

Grafici i pun `classification_report` su u [`results/`](results/):

| Fajl | Sadržaj |
|---|---|
| `01_histogram_klasa.png` | Raspodela po klasama i train/val split |
| `02_primeri_klasa.png` | Po jedan primerak iz svake klase |
| `03_augmentacija.png` | Primeri augmentovanih slika |
| `04_trening_krivulje.png` | Tačnost i gubitak po epohama |
| `05_matrice_konfuzije.png` | Matrice konfuzije (normalizovane) |
| `06_primeri_klasifikacije.png` | Dobro (zeleno) i loše (crveno) klasifikovane slike |
| `metrike.txt` | Metrike i izveštaj po klasama |

Pun izveštaj: [`docs/Izvjestaj.pdf`](docs/Izvjestaj.pdf)

---

## Arhitektura

`GalaxyCNN` — 7 konvolutivnih slojeva u 4 bloka, sa augmentacijom i normalizacijom
ugrađenim u sam model:

```
Augmentacija (RandomFlip h+v, RandomRotation 0.3, RandomZoom 0.1)
Rescaling(1/255)

Conv2D(32)  + BN  →  Conv2D(32)  + BN  →  MaxPool
Conv2D(64)  + BN  →  Conv2D(64)  + BN  →  MaxPool
Conv2D(128) + BN  →  Conv2D(128) + BN  →  MaxPool
Conv2D(256) + BN  →  MaxPool

Dropout(0.4) → Flatten → Dense(256, relu) → Dropout(0.4) → Dense(3, softmax)
```

Svi `Conv2D` su 3×3, `padding='same'`, aktivacija ReLU.

| Hiperparametar | Vrednost |
|---|---|
| Dimenzija slike | 96 × 96 |
| Batch size | 128 |
| Optimizator | Adam (default lr = 0.001) |
| Loss | SparseCategoricalCrossentropy |
| Epohe | 50 (sa EarlyStopping, `patience=10` na `val_accuracy`) |
| Class weights | `balanced` (dataset je neizbalansiran) |
| Seed za split | 123 |

Pošto su augmentacija i `Rescaling` **slojevi modela**, slike se pri inferenciji
prosleđuju u opsegu `[0, 255]` — ne treba ih ručno deliti sa 255.

---

## Struktura repozitorijuma

```
.
├── train.py              # Treniranje modela od nule
├── evaluate.py           # Metrike, matrice konfuzije, primeri klasifikacije
├── predict.py            # Klasifikacija jedne slike ili celog foldera
├── prepare_dataset.py    # Sortira GZ2 slike u foldere po klasama
├── models/
│   └── galaxy_cnn_model.keras   # Istrenirani model (35 MB)
├── results/              # Grafici i metrike
├── docs/
│   └── Izvjestaj.pdf     # Izveštaj projekta
├── data/
│   ├── README.md         # Kako nabaviti dataset + citiranje
│   └── GALAXY_ZOO_README.txt    # Originalni README Galaxy Zoo tima
└── legacy/               # Originalne skripte kakve su pokretane (reference)
```

---

## Pokretanje

### 1. Instalacija

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux / macOS
pip install -r requirements.txt
```

### 2. Klasifikacija slike istreniranim modelom

Ne traži dataset — model je u repozitorijumu:

```bash
python predict.py moja_galaksija.jpg
```

```
moja_galaksija.jpg
  Predikcija: Spiral (82.4% sigurnosti)
  Raspodela:  Barred:  11.3%  Elliptical:   6.3%  Spiral:  82.4%
```

### 3. Priprema dataseta (za treniranje)

Dataset nije u repozitorijumu (243.434 slike, ~5 GB). Preuzimanje i citiranje su
opisani u [`data/README.md`](data/README.md). Kad raspakuješ `images_gz2.zip` i
preuzmeš CSV sa klasama:

```bash
python prepare_dataset.py --images-dir images --csv gz2_classes.csv --out-dir images_gz2
```

Dobija se:

```
images_gz2/
    Barred/      ~45.600 slika
    Elliptical/  ~97.600 slika
    Spiral/      ~95.800 slika
```

### 4. Treniranje

```bash
python train.py --data-dir images_gz2
```

Trening na celom datasetu je rađen na Google Colab GPU-u. Na CPU-u traje
nerealno dugo — za probu smanji dataset (`--limit-per-class` u `prepare_dataset.py`)
ili broj epoha.

### 5. Evaluacija

```bash
python evaluate.py --data-dir images_gz2 --model models/galaxy_cnn_model.keras
```

> **Važno:** `--seed` i `--img-size` moraju biti isti kao pri treniranju (123 i 96).
> `validation_split` deli dataset deterministički na osnovu seed-a, pa drugi seed daje
> drugi split — i tada "validacioni" skup sadrži slike na kojima je model treniran,
> zbog čega metrike izgledaju bolje nego što jesu.

---

## Dataset i citiranje

Slike i oznake dolaze iz **Galaxy Zoo 2** i nisu naš rad. Ako koristiš dataset,
citiraj radove navedene u [`data/README.md`](data/README.md) — Willett et al. (2013)
i Hart et al. (2016).

## Napomene

- `models/galaxy_cnn_model.keras` je 35 MB i commitovan je kao običan fajl (ispod
  GitHub limita od 100 MB), bez Git LFS-a.
- Grafici u `results/` su iz originalnog Colab treninga, ne iz ponovnog pokretanja
  ovih skripti.

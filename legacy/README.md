# legacy/

Originalne skripte, onakve kakve su pokretane tokom rada na projektu. Ostavljene su
kao referenca — za pokretanje koristiti `train.py`, `evaluate.py` i `predict.py` u
korenu repozitorijuma.

## `colab_main.py`

Finalna skripta iz Google Colab-a kojom je istreniran `models/galaxy_cnn_model.keras`
i kojom su napravljeni grafici u `results/`. Export iz notebook-a, pa sadrzi
ponovljene import-e, `drive.mount()` i `/content/...` putanje.

Sastoji se od dva prolaza:

1. priprema podataka, treniranje i cuvanje modela (`seed=123`, `batch_size=128`)
2. ponovno ucitavanje sacuvanog modela i evaluacija (`seed=42`, `batch_size=32`)

Drugi prolaz koristi **drugi seed od treninga**, pa `validation_split` tu pravi
drugaciji split pa je deo "validacionih" slika model vec video u treningu. Zato
`evaluate.py` ima `--seed 123` kao default i upozorenje da seed mora odgovarati
treningu.

## `train_local_45k.py`

Ranija, jednostavnija varijanta za lokalno treniranje na balansiranom podskupu
(45.000 slika po klasi, 150x150, 4 konvolutivna bloka bez duplih Conv slojeva,
Adam lr=1e-4, bez `Rescaling` sloja). Nije verzija kojom je dobijen finalni model.

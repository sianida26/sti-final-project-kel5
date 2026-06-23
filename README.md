# Final Project STI - Kelompok 5

Final Project mata kuliah **Sistem & Teknologi Informasi (STI)** - MMT ITS.
Dua studi kasus analitik data dengan pendekatan **CRISP-DM** dan dashboard interaktif.

## Deliverable

| Notebook | Studi Kasus | Pendekatan | Output Dashboard |
| --- | --- | --- | --- |
| [Inventory CGS-1](Final-Project-STI-Kel5-Inventory-CGS1-enriched.ipynb) | Monitoring inventory instrumen Custody Gas Station (CGS-1) | CRISP-DM | Looker Studio |
| [Sales Analysis](Final-Project-STI-Kel5-Sales-Analysis.ipynb) | Analisis kinerja penjualan ritel online (2022-2026) | CRISP-DM | Plotly (inline) |

## Struktur

```
.
├── Final-Project-STI-Kel5-Inventory-CGS1-enriched.ipynb   # Analisis A
├── Final-Project-STI-Kel5-Sales-Analysis.ipynb            # Analisis B
├── data/                                                  # dataset (bersih + enriched)
└── scripts/                                               # script bantu generate notebook & preview
```

## Manajemen Proyek

Proyek dikelola dengan **GitHub Projects** (board kanban) - tiap fase CRISP-DM dari kedua
studi kasus dipecah jadi issue dan dilacak melalui kolom Backlog -> In Progress -> Done.

## Pendekatan CRISP-DM

1. **Business Understanding** - definisi konteks & business questions
2. **Data Understanding** - load data, profil kualitas
3. **Data Preparation** - cleaning, standardisasi, kolom turunan (KPI/flag)
4. **Modeling / Analisis** - agregasi & visualisasi menjawab business questions
5. **Evaluation** - temuan, rekomendasi, keterbatasan
6. **Deployment** - dashboard monitoring (Looker Studio / Plotly)

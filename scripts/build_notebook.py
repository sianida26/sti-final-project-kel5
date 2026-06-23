#!/usr/bin/env python3
"""Build enriched CRISP-DM notebook for Kel 5 STI - Inventory CGS-1."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "Final-Project-STI-Kel5-Inventory-CGS1-enriched.ipynb")


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.strip("\n").splitlines(keepends=True)}


def code(text):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
            "source": text.strip("\n").splitlines(keepends=True)}


cells = []

cells.append(md("""
# Final Project STI - Kelompok 5
## Monitoring Inventory Instrumen CGS-1
**Pendekatan: CRISP-DM** (Business Understanding -> Data Understanding -> Data Preparation -> Modeling/Analisis -> Evaluation) | **Output: interactive dashboard Looker Studio**

> Catatan: notebook ini melanjutkan & memperkaya analisis dasar (load + value_counts + chart) menjadi alur CRISP-DM yang utuh.
"""))

# ---- 1. BUSINESS UNDERSTANDING ----
cells.append(md("""
## 1. Business Understanding

**Konteks.** CGS-1 (Custody Gas Station) memiliki sejumlah instrumen lapangan (transmitter, switch, actuator, valve) yang menopang operasi. Kesiapan dan keterlacakan instrumen ini penting untuk keandalan operasi, keselamatan, dan kepatuhan (kalibrasi).

**Permasalahan.** Data instrumen tersedia tetapi belum diolah untuk menjawab pertanyaan operasional, dan kualitas datanya belum dievaluasi.

**Tujuan analisis (business questions):**
1. Bagaimana komposisi & status instrumen (aktif vs tidak aktif)?
2. Jenis instrumen (Equipment Class) dan ketergantungan vendor (Manufacturer) apa yang dominan?
3. **Seberapa lengkap data kalibrasi & identitas aset?** Instrumen mana yang belum punya data kalibrasi (potensi gap keselamatan/kepatuhan)?

**Output.** Dashboard monitoring interaktif (Looker Studio) untuk asset/maintenance management.
"""))

# ---- 2. DATA UNDERSTANDING ----
cells.append(md("""
## 2. Data Understanding
"""))

cells.append(code("""
from google.colab import drive
drive.mount('/content/drive')
"""))

cells.append(code("""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

PATH = '/content/drive/MyDrive/Inventory data/Data Inventory CGS-1.xlsx'
df = pd.read_excel(PATH)
df.columns = [str(c).strip() for c in df.columns]   # rapikan nama kolom
print('Dimensi:', df.shape)
df.head()
"""))

cells.append(code("""
# Helper: cari nama kolom secara fleksibel (data punya typo, mis. 'Instrumen Span')
def col(*keys):
    for k in keys:
        for c in df.columns:
            if k.lower() in str(c).lower():
                return c
    return None

C_STATUS = col('status')
C_CLASS  = col('equipment class', 'equipment')
C_MFR    = col('manufacturer')
C_AREA   = col('area')
C_CAL    = col('calibrate')
C_SPAN   = col('span')
C_OPR    = col('operating')
C_SERIAL = col('serial')
C_TAG    = col('tag')
{ 'status': C_STATUS, 'class': C_CLASS, 'mfr': C_MFR, 'area': C_AREA,
  'calibrate': C_CAL, 'serial': C_SERIAL, 'tag': C_TAG }
"""))

cells.append(code("""
df.info()
"""))

cells.append(code("""
# Profil kualitas data: berapa nilai yang hilang per kolom
missing = df.isnull().sum()
quality = pd.DataFrame({
    'missing': missing,
    'missing_%': (missing / len(df) * 100).round(1),
    'unique': df.nunique()
}).sort_values('missing_%', ascending=False)
quality
"""))

cells.append(md("""
**Temuan awal kualitas data.** Beberapa kolom pemeliharaan (Calibrate Range, Instrumen Span, Operating Range) dan identitas aset (Serial Number) banyak yang kosong. Ini jadi fokus tahap *Data Preparation* dan sekaligus temuan bisnis (gap pencatatan).
"""))

# ---- 3. DATA PREPARATION ----
cells.append(md("""
## 3. Data Preparation
Membersihkan & menstandardisasi data, lalu menurunkan kolom turunan (flag) untuk analisis & dashboard. Tujuan: hilangkan "null" yang muncul di chart dan siapkan indikator monitoring.
"""))

cells.append(code("""
clean = df.copy()

# 1) Rapikan string: trim spasi, samakan token kosong jadi NaN
for c in clean.select_dtypes(include='object').columns:
    clean[c] = (clean[c].astype(str).str.strip()
                .replace({'nan': np.nan, 'None': np.nan, 'NaN': np.nan, '': np.nan}))

# 2) Normalisasi Status (Active/Inactive konsisten)
if C_STATUS:
    clean[C_STATUS] = clean[C_STATUS].str.strip().str.title()

# 3) Isi kategori kosong jadi 'Unknown' supaya chart/tabel tidak menampilkan 'null'
for c in [C_CLASS, C_MFR, C_AREA]:
    if c:
        clean[c] = clean[c].fillna('Unknown')

# 4) Kolom turunan (flag monitoring)
clean['has_calibration'] = clean[C_CAL].notna() if C_CAL else False
clean['has_serial']      = clean[C_SERIAL].notna() if C_SERIAL else False
clean['is_active']       = clean[C_STATUS].str.lower().eq('active') if C_STATUS else False

# 5) Skor kelengkapan data per instrumen (% field penting yang terisi)
key_fields = [c for c in [C_TAG, C_CLASS, C_MFR, C_STATUS, C_CAL, C_SERIAL] if c]
clean['data_completeness_%'] = (df[key_fields].notna().mean(axis=1) * 100).round(0)

print('Sebelum:', df.shape, '-> Sesudah:', clean.shape)
clean.head()
"""))

# ---- 4. MODELING / ANALISIS ----
cells.append(md("""
## 4. Modeling / Analisis
Menjawab business questions di tahap 1 lewat agregasi & visualisasi.
"""))

cells.append(code("""
# KPI ringkas (untuk scorecard dashboard)
total      = len(clean)
pct_active = clean['is_active'].mean() * 100
pct_cal    = clean['has_calibration'].mean() * 100
pct_serial = clean['has_serial'].mean() * 100
print(f'Total instrumen      : {total}')
print(f'Active               : {pct_active:.1f}%')
print(f'Punya Calibrate Range: {pct_cal:.1f}%   <- indikator kepatuhan kalibrasi')
print(f'Punya Serial Number  : {pct_serial:.1f}%   <- keterlacakan aset')
print(f'Rata-rata kelengkapan data: {clean["data_completeness_%"].mean():.0f}%')
"""))

cells.append(code("""
# Q1 - Status instrumen
clean[C_STATUS].value_counts().plot(kind='pie', autopct='%1.1f%%', figsize=(5,5),
                                    colors=['#1C6F8C', '#D98A4B'])
plt.ylabel(''); plt.title('Status Equipment'); plt.show()
"""))

cells.append(code("""
# Q2 - Komposisi jenis instrumen & vendor
fig, ax = plt.subplots(1, 2, figsize=(13, 4))
clean[C_CLASS].value_counts().plot(kind='bar', ax=ax[0], color='#1C6F8C')
ax[0].set_title('Equipment Class'); ax[0].set_ylabel('Jumlah'); ax[0].tick_params(axis='x', rotation=45)
clean[C_MFR].value_counts().plot(kind='barh', ax=ax[1], color='#3E8FA8')
ax[1].set_title('Manufacturer (ketergantungan vendor)')
plt.tight_layout(); plt.show()
"""))

cells.append(code("""
# Q3 (INSIGHT UTAMA) - Cakupan kalibrasi per Equipment Class
cov = (clean.groupby(C_CLASS)['has_calibration'].mean() * 100).sort_values()
ax = cov.plot(kind='barh', figsize=(8,5), color='#2E8B6F')
plt.xlabel('% instrumen punya Calibrate Range'); plt.xlim(0, 100)
plt.title('Cakupan Data Kalibrasi per Equipment Class')
for i, v in enumerate(cov):
    ax.text(v + 1, i, f'{v:.0f}%', va='center', fontsize=9)
plt.tight_layout(); plt.show()
"""))

cells.append(code("""
# Q3 - Ringkasan gap data pada field pemeliharaan
gap_cols = [c for c in [C_CAL, C_SPAN, C_OPR, C_SERIAL] if c]
gap = (clean[gap_cols].isnull().mean() * 100).sort_values()
ax = gap.plot(kind='barh', figsize=(8,3.5), color='#D98A4B')
plt.xlabel('% data hilang'); plt.xlim(0, 100); plt.title('Gap Data Field Pemeliharaan')
for i, v in enumerate(gap):
    ax.text(v + 1, i, f'{v:.0f}%', va='center', fontsize=9)
plt.tight_layout(); plt.show()
"""))

cells.append(code("""
# Daftar instrumen yang AKTIF tapi BELUM ada data kalibrasi (prioritas tindak lanjut)
watch = clean[(clean['is_active']) & (~clean['has_calibration'])]
cols_show = [c for c in [C_TAG, C_CLASS, C_MFR, C_STATUS] if c]
print(f'{len(watch)} instrumen aktif belum punya data kalibrasi:')
watch[cols_show]
"""))

# ---- 5. EVALUATION ----
cells.append(md("""
## 5. Evaluation

**Ringkasan temuan (lihat KPI & chart di atas):**
- **Status.** Mayoritas instrumen *Active* (~94%), hanya sebagian kecil *Inactive* -> ketersediaan aset baik.
- **Komposisi & vendor.** Didominasi Actuator & Pressure Transmitter; vendor terkonsentrasi pada Rosemount & Honeywell -> ada **ketergantungan vendor** (pertimbangan untuk strategi spare-part).
- **Gap kalibrasi (insight utama).** Hanya sebagian instrumen yang memiliki *Calibrate Range* tercatat -> **gap data kalibrasi** yang signifikan. Untuk instrumen yang *Active* namun tanpa data kalibrasi, ada risiko kepatuhan/keselamatan -> jadi daftar prioritas tindak lanjut.
- **Keterlacakan aset.** Sebagian *Serial Number* kosong -> menyulitkan pelacakan & klaim garansi.

**Rekomendasi:**
1. Lengkapi data **Calibrate Range** & **Serial Number** untuk instrumen prioritas (Active tanpa kalibrasi).
2. Jadikan **% cakupan kalibrasi** sebagai KPI monitoring berkala.
3. Standardisasi input data (hindari field kosong) di sumber.

**Keterbatasan.** Sampel kecil (18 instrumen), satu area (CGS-1), snapshot satu waktu -> analisis bersifat deskriptif, belum prediktif.
"""))

# ---- 6. EXPORT + DASHBOARD ----
cells.append(md("""
## 6. Export Data Bersih (untuk Looker Studio)
Looker sebaiknya menunjuk ke data yang **sudah dibersihkan** ini supaya "null" tidak muncul & ada kolom turunan (flag) untuk scorecard/filter.
"""))

cells.append(code("""
OUT = '/content/drive/MyDrive/Inventory data/Data Inventory CGS-1_clean.xlsx'
clean.to_excel(OUT, index=False)
print('Saved:', OUT)
# Lalu di Looker Studio: Resource > Manage added data sources > ganti/ tambah source ke file _clean ini.
"""))

cells.append(md("""
### Yang ditambahkan di Looker Studio (saran)
1. **Ganti data source** ke `..._clean.xlsx` (null -> 'Unknown', ada kolom flag).
2. **Scorecard** di atas: Total Instrumen, % Active, **% Punya Kalibrasi**, Rata-rata Kelengkapan Data.
3. **Chart baru**: "Cakupan Kalibrasi per Equipment Class".
4. **Filter** yang berguna: ganti *Select date range* (snapshot, kurang relevan) dengan filter **Status / Equipment Class / Manufacturer**.
5. **Tabel**: tambah kolom `data_completeness_%`, sorot baris Active tanpa kalibrasi.
"""))

nb = {
    "cells": cells,
    "metadata": {
        "colab": {"provenance": []},
        "kernelspec": {"name": "python3", "display_name": "Python 3"},
        "language_info": {"name": "python"}
    },
    "nbformat": 4,
    "nbformat_minor": 0
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("saved", OUT, "cells:", len(cells))

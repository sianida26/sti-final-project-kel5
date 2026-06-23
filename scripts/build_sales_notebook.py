#!/usr/bin/env python3
"""Build CRISP-DM notebook: Analisis Kinerja Penjualan Ritel Online (weekly)."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "Final-Project-STI-Kel5-Sales-Analysis.ipynb")
SALES_CSV = os.path.join(HERE, "online_retail_weekly_sales.csv")
with open(SALES_CSV, encoding="utf-8") as _f:
    CSV_TEXT = _f.read().strip()


def md(t):
    return {"cell_type": "markdown", "metadata": {}, "source": t.strip("\n").splitlines(keepends=True)}


def code(t):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
            "source": t.strip("\n").splitlines(keepends=True)}


cells = []

cells.append(md("""
# Final Project STI - Kelompok 5
## Analisis Kinerja Penjualan Ritel Online (2023-2026)
**Pendekatan: CRISP-DM** (Business -> Data Understanding -> Data Preparation -> Modeling/Analisis -> Evaluation) | **Output: dashboard interaktif (Plotly) langsung di notebook**

> Studi kasus: data penjualan B2C sebuah retailer online (data agregat mingguan, anonim - tanpa identitas pelanggan).
"""))

# 1. BUSINESS UNDERSTANDING
cells.append(md("""
## 1. Business Understanding

**Konteks.** Sebuah retailer online B2C ingin memahami kinerja penjualannya selama ~3,5 tahun untuk mendukung keputusan operasional (stok, promo, target).

**Business questions:**
1. Bagaimana **tren & pertumbuhan** penjualan (revenue, transaksi, pelanggan) dari waktu ke waktu?
2. Apa **pendorong** pertumbuhan revenue - kenaikan jumlah transaksi (volume) atau nilai per transaksi (AOV)?
3. Apakah ada **pola musiman** (bulan ramai/sepi) untuk perencanaan stok & campaign?
4. Seberapa **efektif strategi diskon** terhadap revenue?

**Output.** Dashboard monitoring **interaktif (Plotly)** langsung di dalam notebook ini (hover, zoom, filter).
"""))

# 2. DATA UNDERSTANDING
cells.append(md("""
## 2. Data Understanding
"""))

_data_cell = (
    "import pandas as pd\n"
    "import numpy as np\n"
    "import io\n"
    "import matplotlib.pyplot as plt\n"
    "import matplotlib.ticker as mticker\n"
    "\n"
    "# Data penjualan mingguan ditanam langsung agar notebook portabel\n"
    "# (tidak perlu mount Google Drive / file eksternal).\n"
    'DATA = """' + CSV_TEXT + '"""\n'
    "\n"
    "df = pd.read_csv(io.StringIO(DATA))\n"
    "df['week'] = pd.to_datetime(df['week'], errors='coerce')\n"
    "df = df.dropna(subset=['week']).sort_values('week').reset_index(drop=True)\n"
    "print('Dimensi:', df.shape)\n"
    "print('Periode:', df['week'].min().date(), '->', df['week'].max().date())\n"
    "df.head()\n"
)
cells.append(code(_data_cell))

cells.append(md("""
**Kamus data (agregat per minggu):** `week` (tanggal awal minggu), `trx` (jumlah transaksi), `qty` (unit terjual), `avg_price` (harga rata-rata), `disc_share` (porsi transaksi/nilai berdiskon, 0-1), `cust` (jumlah pelanggan), `revenue` (pendapatan).
"""))

cells.append(code("""
df.info()
df.describe().T
"""))

cells.append(code("""
# Kualitas data: nilai hilang
df.isnull().sum()
"""))

# 3. DATA PREPARATION
cells.append(md("""
## 3. Data Preparation
Menurunkan kolom waktu & metrik turunan (KPI) untuk analisis dan dashboard.
"""))

cells.append(code("""
df['year']          = df['week'].dt.year
df['month']         = df['week'].dt.month
df['month_name']    = df['week'].dt.strftime('%b')
df['quarter']       = 'Q' + df['week'].dt.quarter.astype(str)
df['yearmonth']     = df['week'].dt.strftime('%Y-%m')

df['aov']           = (df['revenue'] / df['trx']).round(0)     # Average Order Value
df['units_per_trx'] = (df['qty'] / df['trx']).round(2)         # ukuran keranjang
df['rev_per_cust']  = (df['revenue'] / df['cust']).round(0)
df['disc_pct']      = (df['disc_share'] * 100).round(1)
df['rev_4w_ma']     = df['revenue'].rolling(4, min_periods=1).mean().round(0)  # smoothing

# tandai tahun parsial (data tidak penuh 1 tahun) supaya tidak salah baca YoY
weeks_per_year = df.groupby('year')['week'].count()
df['full_year'] = df['year'].map(weeks_per_year >= 50)
df[['week','revenue','trx','aov','units_per_trx','year','full_year']].head()
"""))

# 4. MODELING / ANALISIS
cells.append(md("""
## 4. Analisis & Dashboard Interaktif

> Grafik di bawah **interaktif** (Plotly): arahkan kursor untuk detail (hover), drag untuk zoom, pakai **range slider** & **dropdown tahun** pada grafik tren.
"""))

cells.append(code("""
# KPI ringkas (untuk scorecard dashboard)
print(f"Total revenue      : {df['revenue'].sum():,.0f}")
print(f"Total transaksi    : {df['trx'].sum():,.0f}")
print(f"Total unit         : {df['qty'].sum():,.0f}")
print(f"AOV keseluruhan    : {df['revenue'].sum()/df['trx'].sum():,.0f}")
print(f"Rata2 unit/transaksi: {df['units_per_trx'].mean():.2f}")
print(f"Rata2 porsi diskon : {df['disc_share'].mean()*100:.1f}%")
"""))

cells.append(code('''
# === DASHBOARD INTERAKTIF (Plotly) - KPI cards ===
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
pio.renderers.default = 'colab'   # render interaktif di Colab

INK='#1C6F8C'; LT='#9ecae1'; ACC='#D98A4B'; GRN='#2E8B6F'; BL='#5FA8BE'
tot_rev = df['revenue'].sum(); tot_trx = df['trx'].sum(); aov_all = tot_rev/tot_trx

kpi = go.Figure()
kpi.add_trace(go.Indicator(mode='number', value=tot_rev, title={'text':'Total Revenue'},
    number={'prefix':'Rp ','valueformat':',.0f'}, domain={'row':0,'column':0}))
kpi.add_trace(go.Indicator(mode='number', value=tot_trx, title={'text':'Total Transaksi'},
    number={'valueformat':',.0f'}, domain={'row':0,'column':1}))
kpi.add_trace(go.Indicator(mode='number', value=aov_all, title={'text':'AOV (Rp)'},
    number={'valueformat':',.0f'}, domain={'row':0,'column':2}))
kpi.add_trace(go.Indicator(mode='number', value=df['disc_share'].mean()*100,
    title={'text':'Rata-rata Diskon'}, number={'suffix':' %','valueformat':'.1f'},
    domain={'row':0,'column':3}))
kpi.update_layout(grid={'rows':1,'columns':4,'pattern':'independent'}, height=170,
    margin=dict(t=50,b=10), title_text='<b>Ringkasan KPI - Penjualan Ritel Online</b>')
kpi.show()
'''))

cells.append(code("""
# Q1/Q2 - Ringkasan per tahun + pertumbuhan YoY (hanya tahun penuh utk YoY)
by_year = df.groupby('year').agg(
    weeks=('week','count'), revenue=('revenue','sum'),
    trx=('trx','sum'), cust=('cust','sum')).copy()
by_year['aov'] = (by_year['revenue']/by_year['trx']).round(0)
full = by_year[by_year['weeks']>=50].copy()
full['yoy_revenue_%'] = (full['revenue'].pct_change()*100).round(1)
full['yoy_aov_%']     = (full['aov'].pct_change()*100).round(1)
print('Catatan: tahun dengan <50 minggu (parsial) dikecualikan dari YoY.')
display(by_year)
display(full[['revenue','trx','aov','yoy_revenue_%','yoy_aov_%']])
"""))

cells.append(code('''
# Tren revenue mingguan (interaktif: hover, zoom, range slider, dropdown tahun)
trend = go.Figure()
trend.add_trace(go.Scatter(x=df['week'], y=df['revenue'], mode='lines', name='Mingguan',
    line=dict(color=LT,width=1), hovertemplate='%{x|%d %b %Y}<br>Rp %{y:,.0f}<extra></extra>'))
trend.add_trace(go.Scatter(x=df['week'], y=df['rev_4w_ma'], mode='lines',
    name='Rata-rata 4 minggu', line=dict(color=INK,width=2.5),
    hovertemplate='Rp %{y:,.0f}<extra></extra>'))
btns=[dict(label='Semua', method='relayout',
           args=[{'xaxis.range':[df['week'].min(), df['week'].max()]}])]
for yy in sorted(df['year'].unique()):
    w=df[df['year']==yy]['week']
    if len(w): btns.append(dict(label=str(yy), method='relayout',
        args=[{'xaxis.range':[w.min(), w.max()]}]))
trend.update_layout(title='<b>Tren Revenue Mingguan</b>', yaxis_title='Revenue (Rp)',
    hovermode='x unified', height=440, template='plotly_white',
    updatemenus=[dict(buttons=btns, x=1.0, y=1.18, xanchor='right', showactive=True)])
trend.update_xaxes(rangeslider_visible=True)
trend.show()
'''))

cells.append(code('''
# Pertumbuhan per tahun & pola musiman
order=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
ry=df.groupby('year')['revenue'].sum()
seas=df.groupby('month_name')['revenue'].mean().reindex(order)
fig=make_subplots(rows=1, cols=2,
    subplot_titles=('Revenue per Tahun','Rata-rata Revenue per Bulan (Seasonality)'))
fig.add_trace(go.Bar(x=ry.index.astype(str), y=ry.values, marker_color=INK,
    text=[f'{v/1e9:.1f} M' for v in ry.values], textposition='outside',
    hovertemplate='%{x}<br>Rp %{y:,.0f}<extra></extra>'),1,1)
fig.add_trace(go.Bar(x=seas.index, y=seas.values, marker_color=BL,
    hovertemplate='%{x}<br>Rp %{y:,.0f}<extra></extra>'),1,2)
fig.update_layout(height=400, showlegend=False, template='plotly_white',
    title_text='<b>Pertumbuhan & Pola Musiman</b>')
fig.show()
'''))

cells.append(code('''
# AOV per tahun & efektivitas diskon
ay=df.groupby('year')['aov'].mean()
fig=make_subplots(rows=1, cols=2, subplot_titles=('AOV per Tahun','Diskon (%) vs Revenue'))
fig.add_trace(go.Bar(x=ay.index.astype(str), y=ay.values, marker_color=GRN,
    text=[f'{v/1e3:.0f} rb' for v in ay.values], textposition='outside',
    hovertemplate='%{x}<br>AOV Rp %{y:,.0f}<extra></extra>'),1,1)
fig.add_trace(go.Scatter(x=df['disc_pct'], y=df['revenue'], mode='markers',
    marker=dict(color=ACC,opacity=0.6,size=7),
    hovertemplate='Diskon %{x:.0f}%<br>Rp %{y:,.0f}<extra></extra>'),1,2)
fig.update_xaxes(title_text='Porsi diskon (%)', row=1,col=2)
fig.update_yaxes(title_text='Revenue (Rp)', row=1,col=2)
corr=df['disc_share'].corr(df['revenue'])
fig.update_layout(height=400, showlegend=False, template='plotly_white',
    title_text=f'<b>AOV & Efektivitas Diskon</b>  (korelasi diskon-revenue {corr:.2f}, mendekati 0)')
fig.show()
'''))

# 5. EVALUATION
cells.append(md("""
## 5. Evaluation

**Temuan (lihat angka & chart di atas):**
- **Pertumbuhan kuat.** Revenue tahunan naik tajam: ~3,8 M (2023) -> ~8,0 M (2024, +112%) -> ~18,3 M (2025, +129%) - sekitar **5x dalam dua tahun**. (Catatan: 2022 hanya 1 minggu & 2026 baru ~17 minggu, jadi dikecualikan dari YoY.)
- **Pendorong = nilai, bukan sekadar volume.** AOV naik 307 rb (2023) -> 417 rb (2024) -> 776 rb (2025), sementara jumlah transaksi naik lebih moderat. Pertumbuhan revenue **lebih banyak ditarik kenaikan AOV** daripada jumlah transaksi.
- **Keranjang kecil.** Rata-rata ~1,3 unit/transaksi -> mayoritas beli 1 item -> ada peluang **cross-sell/bundling**.
- **Musiman.** Revenue cenderung **puncak di Juli** (juga tinggi Juni & Januari), lemah di Mei & Oktober -> acuan perencanaan stok & campaign.
- **Diskon belum efektif.** Rata-rata porsi diskon **~36% (tinggi)**, tetapi korelasi diskon vs revenue ~0 dan vs AOV justru negatif -> indikasi **over-discounting**: diskon besar tidak terbukti mengangkat revenue.

**Rekomendasi:**
1. Pertahankan momentum **AOV** (bundling/upsell) - keranjang masih 1,3 item.
2. **Evaluasi strategi diskon** (uji kurangi diskon di segmen tertentu, ukur dampak ke revenue).
3. Manfaatkan **puncak musiman** (Jun-Jul, Jan) untuk stok & promo.
4. Dorong **akuisisi/retensi pelanggan** (jumlah pelanggan relatif stagnan dibanding lonjakan revenue).

**Keterbatasan.** Data agregat mingguan tanpa dimensi produk/pelanggan/channel; periode 2026 masih berjalan (parsial).
"""))

# 6. EXPORT + DASHBOARD
cells.append(md("""
## 6. Export Data (opsional)
"""))

cells.append(code("""
OUT = 'online_retail_weekly_enriched.csv'
df.to_csv(OUT, index=False)
print('Saved ke /content/' + OUT)
print('Data bersih + kolom turunan, kalau mau dipakai lagi di tool lain.')
# from google.colab import files; files.download(OUT)
"""))

cells.append(md("""
### Rancangan Dashboard Looker Studio (saran)
**Sumber data:** `online_retail_weekly_enriched.csv` (sudah ada kolom turunan year/month/quarter/aov/dll).

1. **Scorecard (baris atas):** Total Revenue, Total Transaksi, AOV (rata-rata), Total Pelanggan, Rata-rata Diskon %.
2. **Time series:** Revenue per minggu/bulan (pakai `week`/`yearmonth`).
3. **Bar:** Revenue per Tahun (`year`) + Revenue per Bulan (`month_name`, seasonality).
4. **Combo/line:** AOV per bulan (tren nilai transaksi).
5. **Scatter:** `disc_pct` vs `revenue` (efektivitas diskon).
6. **Filter controls:** Tahun (`year`), Kuartal (`quarter`), rentang tanggal (`week`).
"""))

nb = {"cells": cells,
      "metadata": {"colab": {"provenance": []},
                   "kernelspec": {"name": "python3", "display_name": "Python 3"},
                   "language_info": {"name": "python"}},
      "nbformat": 4, "nbformat_minor": 0}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print("saved", OUT, "cells:", len(cells))

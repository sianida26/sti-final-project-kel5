import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
HERE = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(HERE, 'online_retail_weekly_enriched.csv'), parse_dates=['week'])

fig, ax = plt.subplots(2, 2, figsize=(13, 8))
fig.suptitle('Preview - Analisis Kinerja Penjualan Ritel Online (2023-2026)', fontsize=14, fontweight='bold')

ax[0,0].plot(df['week'], df['revenue']/1e6, color='#9ecae1', lw=1, label='Mingguan')
ax[0,0].plot(df['week'], df['rev_4w_ma']/1e6, color='#1C6F8C', lw=2, label='MA 4 minggu')
ax[0,0].set_title('Tren Revenue Mingguan (juta)'); ax[0,0].legend(fontsize=8)

by_year = (df.groupby('year')['revenue'].sum()/1e9)
b = by_year.plot(kind='bar', ax=ax[0,1], color='#1C6F8C')
ax[0,1].set_title('Revenue per Tahun (miliar)'); ax[0,1].tick_params(axis='x', rotation=0)
for i,v in enumerate(by_year):
    b.text(i, v, f'{v:.1f}', ha='center', va='bottom', fontsize=9)

order=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
seas=(df.groupby('month_name')['revenue'].mean().reindex(order)/1e6)
seas.plot(kind='bar', ax=ax[1,0], color='#5FA8BE')
ax[1,0].set_title('Seasonality - Rata2 Revenue/Bulan (juta)'); ax[1,0].tick_params(axis='x', rotation=0)

ax[1,1].scatter(df['disc_pct'], df['revenue']/1e6, alpha=0.5, color='#D98A4B')
ax[1,1].set_title(f'Diskon (%) vs Revenue  (korelasi={df["disc_share"].corr(df["revenue"]):.2f})')
ax[1,1].set_xlabel('Porsi diskon (%)'); ax[1,1].set_ylabel('Revenue (juta)')

plt.tight_layout(rect=[0,0,1,0.97])
out = os.path.join(HERE, 'dashboard_preview.png')
plt.savefig(out, dpi=130)
print('saved', out)

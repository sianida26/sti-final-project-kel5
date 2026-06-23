#!/usr/bin/env python3
"""Export the Sales Plotly dashboard to one standalone interactive HTML."""
import os
import pandas as pd, numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(HERE, 'data', 'online_retail_weekly_sales.csv')
OUT = os.path.join(HERE, 'Dashboard-Sales-STI-Kel5.html')

df = pd.read_csv(CSV)
df['week'] = pd.to_datetime(df['week'], errors='coerce')
df = df.dropna(subset=['week']).sort_values('week').reset_index(drop=True)
df['year'] = df['week'].dt.year
df['month_name'] = df['week'].dt.strftime('%b')
df['aov'] = (df['revenue']/df['trx']).round(0)
df['disc_pct'] = (df['disc_share']*100).round(1)
df['rev_4w_ma'] = df['revenue'].rolling(4, min_periods=1).mean().round(0)

INK='#1C6F8C'; LT='#9ecae1'; ACC='#D98A4B'; GRN='#2E8B6F'; BL='#5FA8BE'
tot_rev=df['revenue'].sum(); tot_trx=df['trx'].sum(); aov_all=tot_rev/tot_trx

kpi=go.Figure()
kpi.add_trace(go.Indicator(mode='number', value=tot_rev, title={'text':'Total Revenue'},
    number={'prefix':'Rp ','valueformat':',.0f'}, domain={'row':0,'column':0}))
kpi.add_trace(go.Indicator(mode='number', value=tot_trx, title={'text':'Total Transaksi'},
    number={'valueformat':',.0f'}, domain={'row':0,'column':1}))
kpi.add_trace(go.Indicator(mode='number', value=aov_all, title={'text':'AOV (Rp)'},
    number={'valueformat':',.0f'}, domain={'row':0,'column':2}))
kpi.add_trace(go.Indicator(mode='number', value=df['disc_share'].mean()*100,
    title={'text':'Rata-rata Diskon'}, number={'suffix':' %','valueformat':'.1f'}, domain={'row':0,'column':3}))
kpi.update_layout(grid={'rows':1,'columns':4,'pattern':'independent'}, height=180,
    margin=dict(t=60,b=10), title_text='<b>Ringkasan KPI - Penjualan Ritel Online</b>')

trend=go.Figure()
trend.add_trace(go.Scatter(x=df['week'], y=df['revenue'], mode='lines', name='Mingguan',
    line=dict(color=LT,width=1), hovertemplate='%{x|%d %b %Y}<br>Rp %{y:,.0f}<extra></extra>'))
trend.add_trace(go.Scatter(x=df['week'], y=df['rev_4w_ma'], mode='lines', name='Rata-rata 4 minggu',
    line=dict(color=INK,width=2.5), hovertemplate='Rp %{y:,.0f}<extra></extra>'))
btns=[dict(label='Semua', method='relayout', args=[{'xaxis.range':[df['week'].min(), df['week'].max()]}])]
for yy in sorted(df['year'].unique()):
    w=df[df['year']==yy]['week']
    if len(w): btns.append(dict(label=str(yy), method='relayout', args=[{'xaxis.range':[w.min(), w.max()]}]))
trend.update_layout(title='<b>Tren Revenue Mingguan</b>', yaxis_title='Revenue (Rp)',
    hovermode='x unified', height=440, template='plotly_white',
    updatemenus=[dict(buttons=btns, x=1.0, y=1.18, xanchor='right', showactive=True)])
trend.update_xaxes(rangeslider_visible=True)

order=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
ry=df.groupby('year')['revenue'].sum(); seas=df.groupby('month_name')['revenue'].mean().reindex(order)
g1=make_subplots(rows=1, cols=2, subplot_titles=('Revenue per Tahun','Rata-rata Revenue per Bulan (Seasonality)'))
g1.add_trace(go.Bar(x=ry.index.astype(str), y=ry.values, marker_color=INK,
    text=[f'{v/1e9:.1f} M' for v in ry.values], textposition='outside',
    hovertemplate='%{x}<br>Rp %{y:,.0f}<extra></extra>'),1,1)
g1.add_trace(go.Bar(x=seas.index, y=seas.values, marker_color=BL,
    hovertemplate='%{x}<br>Rp %{y:,.0f}<extra></extra>'),1,2)
g1.update_layout(height=400, showlegend=False, template='plotly_white', title_text='<b>Pertumbuhan & Pola Musiman</b>')

ay=df.groupby('year')['aov'].mean()
g2=make_subplots(rows=1, cols=2, subplot_titles=('AOV per Tahun','Diskon (%) vs Revenue'))
g2.add_trace(go.Bar(x=ay.index.astype(str), y=ay.values, marker_color=GRN,
    text=[f'{v/1e3:.0f} rb' for v in ay.values], textposition='outside',
    hovertemplate='%{x}<br>AOV Rp %{y:,.0f}<extra></extra>'),1,1)
g2.add_trace(go.Scatter(x=df['disc_pct'], y=df['revenue'], mode='markers',
    marker=dict(color=ACC,opacity=0.6,size=7), hovertemplate='Diskon %{x:.0f}%<br>Rp %{y:,.0f}<extra></extra>'),1,2)
g2.update_xaxes(title_text='Porsi diskon (%)', row=1,col=2); g2.update_yaxes(title_text='Revenue (Rp)', row=1,col=2)
corr=df['disc_share'].corr(df['revenue'])
g2.update_layout(height=400, showlegend=False, template='plotly_white',
    title_text=f'<b>AOV & Efektivitas Diskon</b>  (korelasi diskon-revenue {corr:.2f}, mendekati 0)')

parts=[pio.to_html(kpi, include_plotlyjs='cdn', full_html=False)]
for f in (trend,g1,g2): parts.append(pio.to_html(f, include_plotlyjs=False, full_html=False))
body='\n'.join(parts)
html=f'''<!doctype html><html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dashboard Penjualan Ritel - Final Project STI Kel 5</title>
<style>body{{font-family:-apple-system,"Segoe UI",Arial,sans-serif;max-width:1100px;margin:0 auto;padding:24px;color:#1C6F8C}}
h1{{font-size:22px;margin:0 0 4px}}p.sub{{color:#5A6A70;margin:0 0 18px}}</style></head>
<body><h1>Dashboard Penjualan Ritel Online</h1>
<p class="sub">Final Project STI - Kelompok 5 | Pendekatan CRISP-DM | Interaktif: hover, zoom, range slider, filter tahun</p>
{body}</body></html>'''
open(OUT,'w',encoding='utf-8').write(html)
print('Saved', OUT, f'({len(html)//1024} KB)')

import os, pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(HERE, 'online_retail_weekly_enriched.csv'), parse_dates=['week'])
INK='#1C6F8C'; LT='#9ecae1'; ACC='#D98A4B'; GRN='#2E8B6F'; BL='#5FA8BE'
tot_rev=df['revenue'].sum(); tot_trx=df['trx'].sum(); aov_all=tot_rev/tot_trx

kpi=go.Figure()
kpi.add_trace(go.Indicator(mode='number', value=tot_rev, title={'text':'Total Revenue'}, number={'prefix':'Rp ','valueformat':',.0f'}, domain={'row':0,'column':0}))
kpi.add_trace(go.Indicator(mode='number', value=tot_trx, title={'text':'Total Transaksi'}, number={'valueformat':',.0f'}, domain={'row':0,'column':1}))
kpi.add_trace(go.Indicator(mode='number', value=aov_all, title={'text':'AOV (Rp)'}, number={'valueformat':',.0f'}, domain={'row':0,'column':2}))
kpi.add_trace(go.Indicator(mode='number', value=df['disc_share'].mean()*100, title={'text':'Rata-rata Diskon'}, number={'suffix':' %','valueformat':'.1f'}, domain={'row':0,'column':3}))
kpi.update_layout(grid={'rows':1,'columns':4,'pattern':'independent'}, height=170, margin=dict(t=50,b=10), title_text='<b>Ringkasan KPI - Penjualan Ritel Online</b>')

trend=go.Figure()
trend.add_trace(go.Scatter(x=df['week'], y=df['revenue'], mode='lines', name='Mingguan', line=dict(color=LT,width=1)))
trend.add_trace(go.Scatter(x=df['week'], y=df['rev_4w_ma'], mode='lines', name='Rata-rata 4 minggu', line=dict(color=INK,width=2.5)))
trend.update_layout(title='<b>Tren Revenue Mingguan</b>  (interaktif: hover, zoom, range slider, dropdown tahun)', yaxis_title='Revenue (Rp)', height=400, template='plotly_white')

order=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
ry=df.groupby('year')['revenue'].sum(); seas=df.groupby('month_name')['revenue'].mean().reindex(order)
f3=make_subplots(rows=1,cols=2,subplot_titles=('Revenue per Tahun','Rata-rata Revenue per Bulan (Seasonality)'))
f3.add_trace(go.Bar(x=ry.index.astype(str), y=ry.values, marker_color=INK, text=[f'{v/1e9:.1f} M' for v in ry.values], textposition='outside'),1,1)
f3.add_trace(go.Bar(x=seas.index, y=seas.values, marker_color=BL),1,2)
f3.update_layout(height=360, showlegend=False, template='plotly_white', title_text='<b>Pertumbuhan & Pola Musiman</b>')

ay=df.groupby('year')['aov'].mean()
f4=make_subplots(rows=1,cols=2,subplot_titles=('AOV per Tahun','Diskon (%) vs Revenue'))
f4.add_trace(go.Bar(x=ay.index.astype(str), y=ay.values, marker_color=GRN, text=[f'{v/1e3:.0f} rb' for v in ay.values], textposition='outside'),1,1)
f4.add_trace(go.Scatter(x=df['disc_pct'], y=df['revenue'], mode='markers', marker=dict(color=ACC,opacity=0.6,size=7)),1,2)
corr=df['disc_share'].corr(df['revenue'])
f4.update_layout(height=360, showlegend=False, template='plotly_white', title_text=f'<b>AOV & Efektivitas Diskon</b>  (korelasi diskon-revenue {corr:.2f}, mendekati 0)')

figs=[(kpi,170),(trend,400),(f3,360),(f4,360)]
imgs=[]
for i,(fig,h) in enumerate(figs):
    p=os.path.join(HERE,f'_pv{i}.png'); fig.write_image(p, width=1100, height=h, scale=2); imgs.append(p)
ims=[Image.open(p) for p in imgs]
W=max(im.width for im in ims); H=sum(im.height for im in ims)
canvas=Image.new('RGB',(W,H),'white'); y=0
for im in ims: canvas.paste(im,(0,y)); y+=im.height
out=os.path.join(HERE,'plotly_dashboard_preview.png'); canvas.save(out)
for p in imgs: os.remove(p)
print('saved', out)

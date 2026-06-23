#!/usr/bin/env python3
"""Build a Looker-Studio-ready CSV for the Sales case (ISO date, KPI turunan, flag outlier)."""
import os
import pandas as pd, numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(HERE, 'data', 'online_retail_weekly_sales.csv')
OUT = os.path.join(HERE, 'data', 'Sales-Looker-Studio.csv')

df = pd.read_csv(CSV)
df['week'] = pd.to_datetime(df['week'], errors='coerce')
df = df.dropna(subset=['week']).sort_values('week').reset_index(drop=True)

df['year']          = df['week'].dt.year
df['month']         = df['week'].dt.month
df['month_name']    = df['week'].dt.strftime('%b')
df['quarter']       = 'Q' + df['week'].dt.quarter.astype(str)
df['yearmonth']     = df['week'].dt.strftime('%Y-%m')
df['aov']           = (df['revenue']/df['trx']).round(0)
df['units_per_trx'] = (df['qty']/df['trx']).round(2)
df['rev_per_cust']  = (df['revenue']/df['cust']).round(0)
df['disc_pct']      = (df['disc_share']*100).round(1)
df['rev_4w_ma']     = df['revenue'].rolling(4, min_periods=1).mean().round(0)

# flag baris anomali (avg_price tidak masuk akal atau keranjang janggal)
df['is_outlier'] = ((df['avg_price'] > 1_500_000) | (df['units_per_trx'] > 2.5)).map({True:'Ya', False:'Tidak'})

df['week'] = df['week'].dt.strftime('%Y-%m-%d')  # ISO, Looker auto-detect Date
cols = ['week','year','month','month_name','quarter','yearmonth',
        'trx','qty','cust','revenue','avg_price','disc_share','disc_pct',
        'aov','units_per_trx','rev_per_cust','rev_4w_ma','is_outlier']
df[cols].to_csv(OUT, index=False)
print('Saved', OUT, '| rows', len(df), '| outlier:', (df['is_outlier']=='Ya').sum())

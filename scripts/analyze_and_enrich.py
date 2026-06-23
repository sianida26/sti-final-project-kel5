#!/usr/bin/env python3
"""Prep + analyze weekly online-retail sales, export enriched CSV for Looker."""
import pandas as pd
import numpy as np
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = r"D:\workspace\_scratchpad\ardl-studi-kasus\revantine_weekly.csv"

df = pd.read_csv(SRC)
df["week"] = pd.to_datetime(df["week"], errors="coerce")
df = df.dropna(subset=["week"]).sort_values("week").reset_index(drop=True)

# ---- derived columns ----
df["year"] = df["week"].dt.year
df["month"] = df["week"].dt.month
df["month_name"] = df["week"].dt.strftime("%b")
df["quarter"] = "Q" + df["week"].dt.quarter.astype(str)
df["yearmonth"] = df["week"].dt.strftime("%Y-%m")
df["aov"] = (df["revenue"] / df["trx"]).round(0)              # average order value
df["units_per_trx"] = (df["qty"] / df["trx"]).round(2)
df["rev_per_cust"] = (df["revenue"] / df["cust"]).round(0)
df["disc_pct"] = (df["disc_share"] * 100).round(1)
df["rev_4w_ma"] = df["revenue"].rolling(4, min_periods=1).mean().round(0)

OUT = os.path.join(HERE, "online_retail_weekly_enriched.csv")
df.to_csv(OUT, index=False)
# also keep a generic-named raw copy
df_raw = pd.read_csv(SRC).dropna(how="all")
df_raw.to_csv(os.path.join(HERE, "online_retail_weekly_sales.csv"), index=False)

# ---- analysis ----
print("=== RANGE ===")
print(df["week"].min().date(), "->", df["week"].max().date(), "| weeks:", len(df))

print("\n=== TOTALS ===")
print("revenue :", f"{df['revenue'].sum():,.0f}")
print("trx     :", f"{df['trx'].sum():,.0f}")
print("qty     :", f"{df['qty'].sum():,.0f}")
print("customers(sum weekly):", f"{df['cust'].sum():,.0f}")
print("overall AOV (rev/trx):", f"{df['revenue'].sum()/df['trx'].sum():,.0f}")
print("avg weekly revenue   :", f"{df['revenue'].mean():,.0f}")

print("\n=== BY YEAR ===")
by_year = df.groupby("year").agg(
    weeks=("week", "count"), revenue=("revenue", "sum"),
    trx=("trx", "sum"), cust=("cust", "sum")).copy()
by_year["aov"] = (by_year["revenue"] / by_year["trx"]).round(0)
by_year["yoy_rev_%"] = (by_year["revenue"].pct_change() * 100).round(1)
print(by_year.to_string())

print("\n=== SEASONALITY (avg weekly revenue by month) ===")
order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
seas = df.groupby("month_name")["revenue"].mean().reindex(order)
for m, v in seas.items():
    if pd.notna(v):
        print(f"  {m}: {v:,.0f}")

print("\n=== DISCOUNT EFFECT (correlation) ===")
print("disc_share vs revenue:", round(df["disc_share"].corr(df["revenue"]), 3))
print("disc_share vs trx    :", round(df["disc_share"].corr(df["trx"]), 3))
print("disc_share vs aov    :", round(df["disc_share"].corr(df["aov"]), 3))
print("avg disc_share       :", round(df["disc_share"].mean(), 3))

print("\n=== AOV / basket ===")
print("avg AOV          :", f"{df['aov'].mean():,.0f}")
print("avg units/trx    :", round(df["units_per_trx"].mean(), 2))
print("avg rev/customer :", f"{df['rev_per_cust'].mean():,.0f}")

print("\nsaved:", OUT)

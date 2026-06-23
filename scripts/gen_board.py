#!/usr/bin/env python3
"""Render a faithful GitHub-Projects board image (issues + assignee avatars) for the deck."""
import os, html
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, '.pmtmp', 'board.html')

# initial-avatar palette
C = ('C', '#1f6feb')   # Chesa
M = ('M', '#8957e5')   # Misbahul
N = None               # unassigned

todo = [
    ("[Sales] Cleaning outlier avg_price/revenue", 30, C),
    ("Pengumpulan final project", 32, C),
]
prog = [
    ("[Inventory] Dashboard Looker Studio", 24, N),
    ("Penyusunan laporan & slide presentasi", 31, C),
]
done = [
    ("Inisiasi proyek & pemilihan studi kasus", 17, M),
    ("Setup repository & board GitHub Projects", 18, C),
    ("[Inventory] Business Understanding - definisi business questions", 19, M),
    ("[Inventory] Data Understanding - load & profil kualitas data", 20, M),
    ("[Inventory] Data Preparation - cleaning & flag turunan", 21, M),
    ("[Inventory] Analisis - KPI, status, coverage kalibrasi", 22, M),
    ("[Inventory] Evaluation - temuan & rekomendasi", 23, M),
    ("[Sales] Business Understanding - definisi business questions", 25, C),
    ("[Sales] Data Understanding - ingest data mingguan", 26, C),
    ("[Sales] Data Preparation - KPI turunan", 27, C),
    ("[Sales] Analisis - dashboard Plotly interaktif", 28, C),
    ("[Sales] Evaluation - temuan & rekomendasi", 29, C),
]

def card(t, num, asg):
    av = ''
    if asg:
        av = f'<span class="av" style="background:{asg[1]}">{asg[0]}</span>'
    return (f'<div class="card"><div class="meta"><span class="ic"></span>'
            f'<span class="repo">sti-final-project-kel5 #{num}</span>{av}</div>'
            f'<div class="title">{html.escape(t)}</div></div>')

def col(dot, name, count, sub, items):
    cards = ''.join(card(*it) for it in items)
    return (f'<div class="col"><div class="chead"><span class="dot {dot}"></span>{name}'
            f'<span class="count">{count}</span></div><div class="csub">{sub}</div>{cards}</div>')

cols = (col('todo','Todo',2,"This item hasn't been started",todo)
        + col('prog','In Progress',2,'This is actively being worked on',prog)
        + col('done','Done',12,'This has been completed',done))

HTML = f'''<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box;font-family:-apple-system,"Segoe UI",Helvetica,Arial,sans-serif}}
body{{background:#0d1117;color:#e6edf3;width:1180px;padding:22px 26px}}
.top{{display:flex;align-items:center;gap:8px;font-size:13px;color:#9198a1;margin-bottom:4px}}
.top .r{{color:#4493f8}}
h1{{font-size:20px;font-weight:600;margin:6px 0 16px;display:flex;align-items:center;gap:8px}}
.lock{{font-size:14px;color:#9198a1}}
.cols{{display:flex;gap:16px;align-items:flex-start}}
.col{{background:#0d1117;border:1px solid #30363d;border-radius:8px;width:370px;padding:10px}}
.chead{{display:flex;align-items:center;gap:8px;font-size:14px;font-weight:600;margin-bottom:2px}}
.dot{{width:11px;height:11px;border-radius:50%}}
.dot.todo{{background:#9198a1}}.dot.prog{{background:#d29922}}.dot.done{{background:#8957e5}}
.count{{background:#21262d;color:#9198a1;border-radius:20px;font-size:12px;padding:1px 8px;font-weight:600}}
.csub{{font-size:12px;color:#9198a1;margin:2px 0 12px}}
.card{{background:#151b23;border:1px solid #30363d;border-radius:6px;padding:10px 12px;margin-bottom:10px}}
.meta{{display:flex;align-items:center;gap:6px;margin-bottom:6px}}
.meta .ic{{width:12px;height:12px;border-radius:50%;border:2px solid #3fb950;display:inline-block;flex:0 0 auto}}
.meta .repo{{font-size:11px;color:#9198a1}}
.av{{width:19px;height:19px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:#fff;margin-left:auto;flex:0 0 auto}}
.title{{font-size:13.5px;line-height:1.4;color:#e6edf3}}
</style></head><body>
<div class="top"><span>sianida26</span><span>/</span><span>Projects</span><span>/</span><span class="r">STI Kel 5 - Final Project</span></div>
<h1>STI Kel 5 - Final Project <span class="lock">&#128274;</span></h1>
<div class="cols">{cols}</div>
</body></html>'''

open(OUT, 'w', encoding='utf-8').write(HTML)
print('wrote', OUT)

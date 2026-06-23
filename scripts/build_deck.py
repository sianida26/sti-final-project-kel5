#!/usr/bin/env python3
"""Final Project STI Kel 5 - presentation deck (DSG VAPT visual language, no DSG branding)."""
from pptx import Presentation
from pptx.util import Inches as IN, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image as PImage
import os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PM   = os.path.join(HERE, '.pmtmp')
PREV = os.path.join(HERE, 'previews')
OUT  = os.path.join(HERE, 'Final-Project-STI-Kel5-Presentation.pptx')
BG_L = os.path.join(PM, 'bg_light.png')
BG_D = os.path.join(PM, 'bg_dark.png')

CYAN  = RGBColor(0x1E, 0xA7, 0xDD)
CYAN2 = RGBColor(0x57, 0xC2, 0xEC)
NAVY  = RGBColor(0x12, 0x30, 0x47)
TEAL  = RGBColor(0x0E, 0x3D, 0x4F)
DARK  = RGBColor(0x1E, 0x2C, 0x33)
GREY  = RGBColor(0x8A, 0x98, 0xA0)
GREYD = RGBColor(0xAE, 0xC2, 0xCC)
LINE  = RGBColor(0xD9, 0xE2, 0xE7)
PANEL = RGBColor(0xF3, 0xF7, 0xF9)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

FBLACK = 'Segoe UI Black'
FSEMI  = 'Segoe UI Semibold'
FBODY  = 'Segoe UI'

prs = Presentation()
prs.slide_width  = IN(13.333); prs.slide_height = IN(7.5)
SW, SH = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]

def slide(dark=False):
    s = prs.slides.add_slide(BLANK)
    s.shapes.add_picture(BG_D if dark else BG_L, 0, 0, SW, SH)
    return s

def box(s, x, y, w, h, fill=None, line=None, line_w=1.0, shape=MSO_SHAPE.RECTANGLE, snip=None):
    sp = s.shapes.add_shape(shape, IN(x), IN(y), IN(w), IN(h))
    if fill is None: sp.fill.background()
    else: sp.fill.solid(); sp.fill.fore_color.rgb = fill
    if line is None: sp.line.fill.background()
    else: sp.line.color.rgb = line; sp.line.width = Pt(line_w)
    sp.shadow.inherit = False
    if snip is not None:
        try: sp.adjustments[0] = snip
        except Exception: pass
    return sp

def notch(s, x, y, w, h, fill=None, line=None, line_w=1.25, sn=0.10):
    return box(s, x, y, w, h, fill=fill, line=line, line_w=line_w, shape=MSO_SHAPE.SNIP_1_RECTANGLE, snip=sn)

def text(s, x, y, w, h, runs, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, sp_after=4, line=1.05):
    tb = s.shapes.add_textbox(IN(x), IN(y), IN(w), IN(h)); tf = tb.text_frame
    tf.word_wrap = True; tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    if isinstance(runs[0], tuple): runs = [runs]
    for i, para in enumerate(runs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align; p.space_after = Pt(sp_after); p.space_before = Pt(0); p.line_spacing = line
        for (t, sz, col, font, *rest) in para:
            r = p.add_run(); r.text = t; f = r.font
            f.size = Pt(sz); f.color.rgb = col; f.name = font
            f.bold = font in (FBLACK, FSEMI)
            if rest and rest[0]: f.italic = True
    return tb

def bullet(s, x, y, w, h, items, sz=14, col=DARK, gap=8, mk=CYAN, line=1.12):
    tb = s.shapes.add_textbox(IN(x), IN(y), IN(w), IN(h)); tf = tb.text_frame
    tf.word_wrap = True; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(gap); p.line_spacing = line
        r = p.add_run(); r.text = '▪  '; r.font.size = Pt(sz-2); r.font.color.rgb = mk; r.font.name = FBODY
        r = p.add_run(); r.text = it; r.font.size = Pt(sz); r.font.color.rgb = col; r.font.name = FBODY
    return tb

def header(s, kicker, title_navy, title_cyan, n, dark=False):
    tcol = WHITE if dark else NAVY
    box(s, 0.62, 0.52, 0.16, 0.66, fill=CYAN)
    text(s, 0.92, 0.46, 11, 0.32, [[(kicker.upper(), 11, CYAN, FSEMI)]], sp_after=0)
    runs = [(title_navy, 26, tcol, FBLACK)]
    if title_cyan: runs.append((title_cyan, 26, CYAN, FBLACK))
    text(s, 0.9, 0.70, 11.6, 0.62, [runs], sp_after=0)
    footer(s, n, dark)

def footer(s, n, dark=False, cap='final project sti · kelompok 5'):
    c = GREYD if dark else GREY
    text(s, 0.62, 6.97, 7, 0.32, [[(cap, 9.5, c, FBODY)]], sp_after=0)
    text(s, 12.0, 6.95, 0.9, 0.35, [[(f'{n:02d}', 11, CYAN, FSEMI)]], align=PP_ALIGN.RIGHT, sp_after=0)

n = 0
# ---------- 1. COVER ----------
n += 1; s = slide()
text(s, 0.95, 1.95, 11.6, 2.4,
     [[('FINAL PROJECT', 50, CYAN, FBLACK)],
      [('SISTEM & TEKNOLOGI', 33, NAVY, FBLACK)],
      [('INFORMASI', 33, NAVY, FBLACK)]], sp_after=2, line=1.0)
box(s, 0.97, 4.5, 0.85, 0.03, fill=CYAN)
text(s, 1.95, 4.32, 9.6, 0.4, [[('Analisis Data & Dashboard Pemantauan dengan Pendekatan CRISP-DM', 14, DARK, FSEMI)]], sp_after=0)
text(s, 0.97, 4.85, 11, 0.35, [[('MAGISTER MANAJEMEN TEKNOLOGI · INSTITUT TEKNOLOGI SEPULUH NOPEMBER', 11, GREY, FSEMI)]], sp_after=0)
notch(s, 0.95, 5.55, 7.3, 1.25, fill=WHITE, line=LINE, line_w=1.25, sn=0.12)
text(s, 1.25, 5.68, 6.9, 1.05,
     [[('KELOMPOK 5', 11, CYAN, FSEMI)],
      [('Moch Chesa Nur Hidayat', 14, NAVY, FSEMI), ('    ·    [Anggota 2]    ·    [Anggota 3]', 13, GREY, FBODY)],
      [('GitHub: sianida26, Misbahulmunir26, …     |     Dosen: [isi nama dosen]', 10, GREY, FBODY)]],
     sp_after=3, line=1.1)
box(s, 9.55, 5.55, 2.85, 1.25, fill=PANEL, shape=MSO_SHAPE.SNIP_1_RECTANGLE, snip=0.16)
text(s, 9.75, 5.78, 2.5, 0.8, [[('23', 30, CYAN, FBLACK)], [('Juni 2026', 13, NAVY, FSEMI)]], sp_after=0, line=1.0)

# ---------- 2. AGENDA ----------
n += 1; s = slide(); header(s, 'Outline', 'AGENDA ', 'PRESENTASI', n)
items = [
    ('01', 'Latar Belakang & Tujuan', 'Konteks dua studi kasus dan pertanyaan bisnis yang ingin dijawab'),
    ('02', 'Metodologi CRISP-DM', 'Kerangka kerja pengolahan data dari awal hingga akhir'),
    ('03', 'Manajemen Proyek', 'Pelacakan pekerjaan kelompok lewat GitHub Projects'),
    ('04', 'Studi Kasus 1: Inventory CGS-1', 'Pemantauan kesiapan dan kalibrasi instrumen'),
    ('05', 'Studi Kasus 2: Penjualan Ritel', 'Tren, pendorong revenue, musiman, dan diskon'),
    ('06', 'Kesimpulan & Rekomendasi', 'Temuan utama dan langkah tindak lanjut'),
]
y = 1.66
for num, t, d in items:
    notch(s, 0.9, y, 1.0, 0.8, fill=NAVY, sn=0.18)
    text(s, 0.9, y+0.02, 1.0, 0.78, [[(num, 22, CYAN, FBLACK)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, sp_after=0)
    text(s, 2.1, y+0.10, 10.4, 0.7, [[(t, 16.5, NAVY, FSEMI)], [(d, 12, GREY, FBODY)]], sp_after=2, line=1.0)
    y += 0.88

# ---------- 3. LATAR BELAKANG ----------
n += 1; s = slide(); header(s, 'Pendahuluan', 'LATAR BELAKANG & ', 'TUJUAN', n)
text(s, 0.9, 1.62, 11.6, 0.7,
     [[('Kelompok mengambil ', 14, DARK, FBODY), ('dua studi kasus nyata', 14, CYAN, FSEMI),
       (' dari lingkungan kerja anggota, lalu mengolah datanya secara terstruktur mengikuti CRISP-DM hingga menghasilkan dashboard pemantauan.', 14, DARK, FBODY)]],
     sp_after=0, line=1.18)
cards = [
    (0.9, 'STUDI KASUS 1', 'Inventory Instrumen CGS-1',
     ['Memantau kesiapan instrumen lapangan (transmitter, valve, actuator) di Custody Gas Station (CGS-1).',
      'Menyoroti status aset, ketergantungan vendor, dan kelengkapan data kalibrasi yang menyangkut keselamatan serta kepatuhan.',
      'Hasil akhir disajikan sebagai dashboard Looker Studio.']),
    (7.0, 'STUDI KASUS 2', 'Kinerja Penjualan Ritel Online',
     ['Data penjualan B2C agregat mingguan sepanjang 2022–2026 (sekitar 3,5 tahun).',
      'Menelusuri tren pertumbuhan, pendorong revenue, pola musiman, dan efektivitas diskon.',
      'Hasil akhir disajikan sebagai dashboard interaktif Plotly.']),
]
for x, k, t, pts in cards:
    notch(s, x, 2.5, 5.45, 4.1, fill=WHITE, line=LINE, line_w=1.25, sn=0.07)
    box(s, x+0.32, 2.86, 0.6, 0.09, fill=CYAN)
    text(s, x+0.32, 3.05, 4.8, 0.3, [[(k, 11, CYAN, FSEMI)]], sp_after=0)
    text(s, x+0.32, 3.32, 4.8, 0.7, [[(t, 18, NAVY, FBLACK)]], sp_after=0, line=1.0)
    bullet(s, x+0.32, 4.18, 4.85, 2.3, pts, sz=12.5, gap=9, mk=CYAN)

# ---------- 4. CRISP-DM ----------
n += 1; s = slide(); header(s, 'Metodologi', 'KERANGKA KERJA ', 'CRISP-DM', n)
text(s, 0.9, 1.62, 11.6, 0.4,
     [[('Kedua studi kasus dikerjakan melalui enam fase CRISP-DM secara berurutan, mulai dari pemahaman bisnis hingga penyajian dashboard.', 13, GREY, FBODY)]], sp_after=0, line=1.1)
phases = [
    ('1', 'Business\nUnderstanding', 'Tujuan & pertanyaan bisnis'),
    ('2', 'Data\nUnderstanding', 'Memuat data, menilai kualitas'),
    ('3', 'Data\nPreparation', 'Pembersihan & kolom turunan'),
    ('4', 'Modeling /\nAnalisis', 'Agregasi & visualisasi'),
    ('5', 'Evaluation', 'Temuan & rekomendasi'),
    ('6', 'Deployment', 'Dashboard pemantauan'),
]
x = 0.9; w = 1.86; gap = 0.13; y = 2.5
for i,(num,t,d) in enumerate(phases):
    notch(s, x, y, w, 2.55, fill=WHITE, line=LINE, line_w=1.25, sn=0.10)
    box(s, x+w/2-0.34, y+0.3, 0.68, 0.68, fill=NAVY, shape=MSO_SHAPE.SNIP_1_RECTANGLE, snip=0.22)
    text(s, x+w/2-0.34, y+0.31, 0.68, 0.68, [[(num, 22, CYAN, FBLACK)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, sp_after=0)
    text(s, x+0.1, y+1.12, w-0.2, 0.85, [[(ln, 13, NAVY, FSEMI)] for ln in t.split('\n')], align=PP_ALIGN.CENTER, sp_after=0, line=1.0)
    text(s, x+0.12, y+1.98, w-0.24, 0.5, [[(d, 10, GREY, FBODY)]], align=PP_ALIGN.CENTER, sp_after=0, line=1.0)
    if i < 5:
        box(s, x+w+0.01, y+1.12, gap, 0.12, fill=CYAN, shape=MSO_SHAPE.CHEVRON)
    x += w + gap
text(s, 0.9, 5.35, 11.6, 0.5,
     [[('Dengan kerangka ini, analisis selalu berangkat dari pertanyaan bisnis yang jelas dan berakhir pada dashboard yang siap dipantau, bukan sekadar kumpulan grafik.', 12.5, GREY, FBODY, True)]], sp_after=0, line=1.15)

# ---------- 5. PM intro ----------
n += 1; s = slide(); header(s, 'Manajemen Proyek', 'PELACAKAN PEKERJAAN ', 'GITHUB PROJECTS', n)
text(s, 0.9, 1.62, 11.6, 0.85,
     [[('Seluruh pekerjaan kelompok dikelola lewat ', 14, DARK, FBODY), ('board kanban GitHub Projects', 14, CYAN, FSEMI),
       ('. Setiap fase CRISP-DM dari kedua studi kasus dipecah menjadi kartu tugas, lalu dilacak perpindahannya dari ', 14, DARK, FBODY),
       ('Todo → In Progress → Done', 14, NAVY, FSEMI), ('.', 14, DARK, FBODY)]], sp_after=0, line=1.18)
why = [
    ('Transparansi', 'Status setiap pekerjaan terlihat dalam satu layar, sehingga tidak ada tugas yang terlewat.'),
    ('Akuntabilitas', 'Tugas yang terpecah jelas memudahkan pembagian kerja antaranggota.'),
    ('Keterlacakan', 'Progres terukur (12 selesai, 2 berjalan, 2 antre) dan langsung terhubung ke repositori kode.'),
]
x = 0.9
for t, d in why:
    notch(s, x, 2.7, 3.78, 1.7, fill=WHITE, line=LINE, line_w=1.25, sn=0.10)
    box(s, x+0.3, 2.98, 0.5, 0.08, fill=CYAN)
    text(s, x+0.3, 3.15, 3.2, 0.4, [[(t, 15.5, NAVY, FBLACK)]], sp_after=0)
    text(s, x+0.3, 3.58, 3.25, 0.9, [[(d, 11.5, GREY, FBODY)]], sp_after=0, line=1.12)
    x += 3.97
notch(s, 0.9, 4.75, 11.53, 1.5, fill=NAVY, sn=0.05)
text(s, 1.25, 4.95, 11, 0.35, [[('TAUTAN PROYEK', 11, CYAN, FSEMI)]], sp_after=0)
text(s, 1.25, 5.3, 11, 0.42, [[('Repository :  ', 13.5, GREYD, FBODY), ('github.com/sianida26/sti-final-project-kel5', 13.5, WHITE, FSEMI)]], sp_after=0)
text(s, 1.25, 5.72, 11, 0.42, [[('Board        :  ', 13.5, GREYD, FBODY), ('github.com/users/sianida26/projects/2', 13.5, WHITE, FSEMI)]], sp_after=0)

# ---------- 6. PM board ----------
n += 1; s = slide(); header(s, 'Manajemen Proyek', 'BOARD KANBAN: ', 'STATUS PEKERJAAN', n)
img = os.path.join(PM, 'board.png')
iw, ih = PImage.open(img).size
disp_w = 8.0; disp_h = disp_w*ih/iw
if disp_h > 5.15: disp_h = 5.15; disp_w = disp_h*iw/ih
notch(s, 0.85, 1.5, disp_w+0.12, disp_h+0.12, fill=None, line=LINE, line_w=1.25, sn=0.03)
s.shapes.add_picture(img, IN(0.91), IN(1.56), IN(disp_w), IN(disp_h))
rx = 9.3
text(s, rx, 1.66, 3.4, 0.4, [[('RINGKASAN STATUS', 11, CYAN, FSEMI)]], sp_after=0)
stats = [('12', 'Done', CYAN), ('2', 'In Progress', NAVY), ('2', 'Todo', GREY)]
yy = 2.12
for v, lb, c in stats:
    notch(s, rx, yy, 3.45, 0.92, fill=WHITE, line=LINE, line_w=1.25, sn=0.14)
    box(s, rx, yy+0.12, 0.1, 0.68, fill=c)
    text(s, rx+0.35, yy+0.04, 1.2, 0.85, [[(v, 30, c, FBLACK)]], anchor=MSO_ANCHOR.MIDDLE, sp_after=0)
    text(s, rx+1.55, yy+0.04, 1.8, 0.85, [[(lb, 14.5, NAVY, FSEMI)]], anchor=MSO_ANCHOR.MIDDLE, sp_after=0)
    yy += 1.06
text(s, rx, yy+0.12, 3.45, 1.6,
     [[('16 kartu total', 13, CYAN, FSEMI)],
      [('Tiap kartu mewakili satu fase CRISP-DM dari kedua studi kasus, ditambah setup, dokumentasi, dan pengumpulan.', 11, GREY, FBODY)]],
     sp_after=6, line=1.15)

# ---------- 7. WBS ----------
n += 1; s = slide(); header(s, 'Manajemen Proyek', 'PEMETAAN TUGAS KE FASE ', 'CRISP-DM', n)
rows = [
    ('Fase CRISP-DM', 'Inventory CGS-1', 'Penjualan Ritel', True),
    ('Business Understanding', 'Menyusun 3 pertanyaan bisnis', 'Menyusun 4 pertanyaan bisnis', False),
    ('Data Understanding', 'Memuat Excel, memeriksa data hilang', 'Memuat data mingguan & kamus data', False),
    ('Data Preparation', 'Membersihkan, menandai kalibrasi/serial', 'Menurunkan KPI: AOV, MA, disc%', False),
    ('Modeling / Analisis', 'Status, vendor, cakupan kalibrasi', 'Tren, musiman, AOV, diskon', False),
    ('Evaluation', 'Gap kalibrasi, watchlist aset', 'Pertumbuhan, over-discounting', False),
    ('Deployment', 'Dashboard Looker Studio', 'Dashboard Plotly interaktif', False),
]
x0, y0 = 0.9, 1.75; cw = [4.0, 3.85, 3.78]; rh = 0.7
yy = y0
for ri, (a,b,c,hd) in enumerate(rows):
    xx = x0
    for ci, val in enumerate((a,b,c)):
        fill = NAVY if hd else (PANEL if ri%2 else WHITE)
        box(s, xx, yy, cw[ci], rh, fill=fill, line=LINE, line_w=0.75)
        col = WHITE if hd else (NAVY if ci==0 else DARK)
        fnt = FSEMI if (hd or ci==0) else FBODY
        text(s, xx+0.18, yy, cw[ci]-0.3, rh, [[(val, 12 if not hd else 13, col, fnt)]], anchor=MSO_ANCHOR.MIDDLE, sp_after=0, line=1.0)
        xx += cw[ci]
    yy += rh
box(s, x0, y0+rh, 0.06, rh*6, fill=CYAN)

# ---------- 8. Inventory BU ----------
n += 1; s = slide(); header(s, 'Studi Kasus 1 · Inventory CGS-1', 'KONTEKS & ', 'PERTANYAAN BISNIS', n)
text(s, 0.9, 1.66, 11.6, 1.0,
     [[('CGS-1 (Custody Gas Station)', 14, CYAN, FSEMI),
       (' mengoperasikan banyak instrumen lapangan yang menjadi tumpuan keandalan, keselamatan, dan kepatuhan operasi. Datanya sudah tersedia, tetapi belum diolah dan kualitasnya belum pernah dievaluasi.', 14, DARK, FBODY)]],
     sp_after=0, line=1.18)
qs = [
    ('Q1', 'Komposisi & status', 'Bagaimana sebaran instrumen yang aktif dibanding yang tidak aktif?'),
    ('Q2', 'Jenis & vendor', 'Equipment class dan manufacturer apa yang paling dominan, dan seberapa besar ketergantungan vendornya?'),
    ('Q3', 'Kelengkapan kalibrasi', 'Instrumen mana yang belum memiliki data kalibrasi, sehingga berpotensi menimbulkan gap keselamatan dan kepatuhan?'),
]
yy = 2.85
for k, t, d in qs:
    notch(s, 0.9, yy, 1.0, 1.0, fill=NAVY, sn=0.2)
    text(s, 0.9, yy+0.02, 1.0, 1.0, [[(k, 21, CYAN, FBLACK)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, sp_after=0)
    text(s, 2.1, yy+0.14, 10.3, 0.9, [[(t, 16, NAVY, FSEMI)], [(d, 12.5, GREY, FBODY)]], sp_after=2, line=1.05)
    yy += 1.16

# ---------- 9. Inventory findings ----------
n += 1; s = slide(); header(s, 'Studi Kasus 1 · Inventory CGS-1', 'TEMUAN & ', 'REKOMENDASI', n)
text(s, 0.9, 1.6, 5.7, 0.4, [[('TEMUAN UTAMA', 11.5, CYAN, FSEMI)]], sp_after=0)
bullet(s, 0.9, 2.02, 5.75, 4.6, [
    'Mayoritas instrumen berstatus Active (~94%), menandakan ketersediaan aset yang baik.',
    'Komposisi didominasi Actuator dan Pressure Transmitter, dengan vendor terpusat pada Rosemount dan Honeywell sehingga muncul ketergantungan vendor.',
    'Temuan terpenting: cukup banyak instrumen belum memiliki Calibrate Range tercatat, menyisakan gap data kalibrasi yang signifikan.',
    'Instrumen Active yang belum berkalibrasi masuk daftar prioritas karena berisiko terhadap kepatuhan dan keselamatan.',
    'Sebagian Serial Number masih kosong, menyulitkan keterlacakan aset dan klaim garansi.',
], sz=13, gap=11, mk=CYAN)
notch(s, 7.0, 1.55, 5.43, 5.05, fill=PANEL, line=LINE, line_w=1.25, sn=0.05)
text(s, 7.35, 1.8, 4.8, 0.4, [[('REKOMENDASI', 11.5, CYAN, FSEMI)]], sp_after=0)
bullet(s, 7.35, 2.24, 4.8, 3.0, [
    'Lengkapi Calibrate Range dan Serial Number, dimulai dari instrumen prioritas yang aktif namun belum berkalibrasi.',
    'Jadikan persentase cakupan kalibrasi sebagai KPI yang dipantau berkala di dashboard.',
    'Standardkan pengisian data di sumbernya agar tidak ada field yang kosong.',
], sz=12.5, gap=10, mk=CYAN)
box(s, 7.35, 5.3, 4.73, 0.02, fill=LINE)
text(s, 7.35, 5.45, 4.7, 0.9,
     [[('Keterbatasan:  ', 11, CYAN, FSEMI), ('data masih terbatas (18 instrumen, satu area, satu titik waktu), sehingga analisis bersifat deskriptif dan belum prediktif.', 11, GREY, FBODY)]],
     sp_after=0, line=1.12)

# ---------- 10. Sales BU ----------
n += 1; s = slide(); header(s, 'Studi Kasus 2 · Penjualan Ritel', 'KONTEKS & ', 'PERTANYAAN BISNIS', n)
text(s, 0.9, 1.66, 11.6, 0.9,
     [[('Sebuah retailer online B2C', 14, CYAN, FSEMI),
       (' ingin memahami kinerja penjualannya selama kurang lebih 3,5 tahun (data agregat mingguan dan anonim) sebagai dasar keputusan stok, promo, dan target penjualan.', 14, DARK, FBODY)]],
     sp_after=0, line=1.18)
qs = [
    ('Q1', 'Tren & pertumbuhan', 'Bagaimana arah tren revenue, transaksi, dan jumlah pelanggan dari waktu ke waktu?'),
    ('Q2', 'Pendorong revenue', 'Pertumbuhan lebih ditarik oleh volume transaksi atau nilai per transaksi (AOV)?'),
    ('Q3', 'Pola musiman', 'Adakah bulan ramai dan sepi yang bisa dipakai merencanakan stok dan campaign?'),
    ('Q4', 'Efektivitas diskon', 'Seberapa besar pengaruh strategi diskon terhadap revenue?'),
]
yy = 2.8
for k, t, d in qs:
    notch(s, 0.9, yy, 0.92, 0.86, fill=NAVY, sn=0.22)
    text(s, 0.9, yy+0.02, 0.92, 0.86, [[(k, 18, CYAN, FBLACK)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, sp_after=0)
    text(s, 2.0, yy+0.08, 10.3, 0.8, [[(t, 15.5, NAVY, FSEMI)], [(d, 12, GREY, FBODY)]], sp_after=2, line=1.05)
    yy += 0.98

# ---------- 11. Sales dashboard ----------
n += 1; s = slide(); header(s, 'Studi Kasus 2 · Penjualan Ritel', 'DASHBOARD ', 'INTERAKTIF (PLOTLY)', n)
img = os.path.join(PREV, 'plotly_dashboard_preview.png')
iw, ih = PImage.open(img).size
disp_h = 5.15; disp_w = disp_h*iw/ih
notch(s, 0.85, 1.5, disp_w+0.12, disp_h+0.12, fill=None, line=LINE, line_w=1.25, sn=0.03)
s.shapes.add_picture(img, IN(0.91), IN(1.56), IN(disp_w), IN(disp_h))
rx = 0.91 + disp_w + 0.45
text(s, rx, 1.66, 12.4-rx, 0.4, [[('KOMPONEN', 11.5, CYAN, FSEMI)]], sp_after=0)
bullet(s, rx, 2.1, 12.4-rx, 4.4, [
    'Scorecard KPI: revenue, transaksi, AOV, dan rata-rata diskon.',
    'Tren revenue mingguan beserta rata-rata 4 minggu (range slider dan dropdown tahun).',
    'Revenue per tahun dan pola musiman per bulan.',
    'AOV per tahun dan scatter diskon terhadap revenue.',
], sz=12.5, gap=10, mk=CYAN)
text(s, rx, 5.45, 12.4-rx, 0.9,
     [[('Interaktif:  ', 11.5, CYAN, FSEMI), ('hover, zoom, dan filter per tahun, langsung di dalam notebook.', 11.5, GREY, FBODY)]],
     sp_after=0, line=1.12)

# ---------- 12. Sales findings ----------
n += 1; s = slide(); header(s, 'Studi Kasus 2 · Penjualan Ritel', 'TEMUAN & ', 'REKOMENDASI', n)
kpis = [('5×', 'Pertumbuhan revenue\n2023 → 2025'), ('AOV ↑', 'Pendorong utama\n(bukan volume)'),
        ('~1,3', 'Unit per transaksi\n(keranjang kecil)'), ('Jun–Jul', 'Puncak musiman\n(juga Januari)')]
x = 0.9
for v, lb in kpis:
    notch(s, x, 1.6, 2.78, 1.5, fill=WHITE, line=LINE, line_w=1.25, sn=0.12)
    box(s, x+0.25, 1.9, 0.5, 0.08, fill=CYAN)
    text(s, x+0.25, 2.05, 2.4, 0.5, [[(v, 25, NAVY, FBLACK)]], sp_after=0)
    text(s, x+0.25, 2.58, 2.5, 0.7, [[(ln, 11, GREY, FBODY)] for ln in lb.split('\n')], sp_after=0, line=1.0)
    x += 2.92
text(s, 0.9, 3.42, 5.7, 0.4, [[('TEMUAN', 11.5, CYAN, FSEMI)]], sp_after=0)
bullet(s, 0.9, 3.84, 5.75, 3.0, [
    'Revenue tahunan tumbuh sekitar 5 kali lipat dalam dua tahun (2023 → 2025).',
    'Pendorong utamanya adalah kenaikan nilai per transaksi (AOV), bukan semata jumlah transaksi.',
    'Diskon belum efektif: rata-rata mencapai ~36%, tetapi korelasinya terhadap revenue mendekati nol, mengindikasikan over-discounting.',
], sz=12.5, gap=9, mk=CYAN)
notch(s, 7.0, 3.42, 5.43, 3.18, fill=PANEL, line=LINE, line_w=1.25, sn=0.06)
text(s, 7.35, 3.62, 4.8, 0.4, [[('REKOMENDASI', 11.5, CYAN, FSEMI)]], sp_after=0)
bullet(s, 7.35, 4.06, 4.8, 2.5, [
    'Jaga momentum AOV lewat bundling dan upsell, mengingat keranjang masih sekitar 1,3 item.',
    'Evaluasi strategi diskon dengan menguji pengurangan diskon dan mengukur dampaknya terhadap revenue.',
    'Manfaatkan puncak musiman (Juni–Juli dan Januari) untuk perencanaan stok dan promo.',
    'Dorong akuisisi dan retensi pelanggan karena jumlahnya cenderung stagnan.',
], sz=12, gap=8, mk=CYAN)

# ---------- 13. Kesimpulan ----------
n += 1; s = slide(); header(s, 'Penutup', 'KESIMPULAN', '', n)
bullet(s, 0.9, 1.85, 11.5, 4.2, [
    'Pendekatan CRISP-DM berhasil mengubah dua dataset mentah menjadi dashboard pemantauan yang menjawab pertanyaan bisnis nyata.',
    'Inventory CGS-1: ketersediaan aset tergolong baik (~94% aktif), tetapi gap data kalibrasi perlu segera ditindaklanjuti demi keselamatan dan kepatuhan.',
    'Penjualan ritel: pertumbuhan kuat (~5×) ditopang kenaikan AOV, sementara strategi diskon perlu dievaluasi karena terindikasi over-discounting.',
    'Manajemen proyek lewat GitHub Projects menjaga pekerjaan kelompok tetap transparan, terbagi rapi, dan terlacak (12 selesai, 2 berjalan, 2 antre).',
    'Langkah berikutnya: membersihkan outlier pada data penjualan dan menuntaskan dashboard Looker Studio untuk inventory.',
], sz=14.5, gap=16, mk=CYAN, line=1.18)

# ---------- 14. Thanks (dark) ----------
n += 1; s = slide(dark=True)
box(s, 0.95, 2.95, 0.16, 1.0, fill=CYAN)
text(s, 1.25, 2.7, 11, 1.3, [[('TERIMA KASIH', 46, WHITE, FBLACK)]], sp_after=0)
text(s, 1.27, 4.05, 11, 0.5, [[('Final Project STI · Kelompok 5 · MMT ITS', 15, GREYD, FSEMI)]], sp_after=0)
text(s, 1.27, 4.55, 11, 0.5, [[('github.com/sianida26/sti-final-project-kel5', 13, CYAN2, FBODY)]], sp_after=0)

prs.save(OUT)
print('Saved', OUT)

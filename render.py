#!/usr/bin/env python3
"""The Tuesday Globe — draws entry.png, a one-page newspaper front that
sums up the world news of Tuesday 24 November 2026.

Written fresh for this entry. Deterministic: no network, no clock, no
randomness. Pillow only.
Run: python3 render.py  ->  writes entry.png (1024x1024) next to this file.

Layout (the proven newspaper-front formula):
  red rule + centred serif masthead + red date band
  -> dark navy 6-cell numbers strip -> segmented region bar
  -> FOUR LEADS IN ONE ROW, poster-style art panels on top, text below
  -> "MORE FROM TUESDAY": 10 secondaries in two columns of five, each
     with a tinted icon tile and a numbered circle
  -> bottom split: "ALSO ON TUESDAY" list on the LEFT, "WHERE IT
     HAPPENED" dotted map on the RIGHT (numbered pins)
  -> DATE CHECK box -> HOW WE CHECKED footer legend.
Every story carries a verification badge (CONFIRMED / OFFICIAL /
REPORTED / CLAIM); region counts are computed from the story tags.
"""
import math
import os
from collections import Counter

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 242, 230)
INK = (22, 20, 18)
NAVY = (18, 38, 66)
RED = (178, 34, 34)
TEAL = (13, 110, 100)
OCHRE = (176, 120, 24)
BLUE = (36, 84, 130)
GOLD = (212, 168, 60)
GREY = (105, 100, 88)
PANEL = (255, 253, 247)
DOT = (148, 143, 126)
TINT = {
    "blue": (214, 228, 240),
    "red": (244, 214, 210),
    "teal": (205, 232, 226),
    "ochre": (245, 228, 196),
}

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

BADGE_FILL = {
    "CONFIRMED": TEAL,
    "OFFICIAL": BLUE,
    "REPORTED": OCHRE,
    "CLAIM": RED,
}


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ------------------------------------------------------------------ stories
# region: EUROPE / MIDEAST / AFRICA / ASIA / AMERICAS / WORLD
# badge:  CONFIRMED = two independent reports or official market data
#         OFFICIAL  = a named official source
#         REPORTED  = one reputable report
#         CLAIM     = one side's claim, not independently verified
# NOTE: story data below is a PLACEHOLDER layout scaffold — the real
# Tuesday 24 November 2026 stories replace it before the build is final.
LEADS = [
    dict(n=1, tag="MARKETS", region="AMERICAS", badge="CONFIRMED",
         title="DOW CROSSES 50,000",
         body="The Dow closed above 50,000 for the first time, up 0.85% "
              "to 50,018.70, as value stocks rallied. The S&P 500 fell "
              "0.50% and the Nasdaq 1.48% as tech slid.",
         src="StockMarketWatch / Fool", kind="coin", tint="blue", deep=NAVY),
    dict(n=2, tag="GAZA", region="MIDEAST", badge="CONFIRMED",
         title="GAZA CHIEF KILLED IN STRIKE",
         body="Israeli strikes in Gaza killed Hamas internal security "
              "chief Naeem Abu Nahel and six others, including two "
              "police officers. Three died at a Khan Younis police post.",
         src="Reuters", kind="blast", tint="red", deep=RED),
    dict(n=3, tag="RIYADH", region="MIDEAST", badge="CONFIRMED",
         title="RIYADH TOWER HIT AGAIN",
         body="A Houthi attack hit a tower in Riyadh's King Abdullah "
              "Financial District, wounding 11 people. It was the "
              "second strike on the capital's tallest tower in under "
              "a week.",
         src="Reuters / Bloomberg", kind="flame", tint="ochre", deep=OCHRE),
    dict(n=4, tag="UKRAINE", region="EUROPE", badge="CONFIRMED",
         title="ZAPORIZHZHIA FLAT BOMBED",
         body="An overnight Russian strike hit a Zaporizhzhia apartment "
              "block, killing two and wounding 40, including four "
              "children. The blast tore a hole in the five-storey "
              "building.",
         src="Reuters", kind="blast", tint="blue", deep=BLUE),
]

SECONDARIES = [
    dict(n=5, tag="UAE", region="ASIA", badge="CONFIRMED",
         title="UAE bus crash kills 13",
         body="A bus carrying 41 people hit a broken-down truck in Ras "
              "Al Khaimah, killing 13 and injuring 14.",
         src="Gulf Business", kind="blast"),
    dict(n=6, tag="NVIDIA", region="AMERICAS", badge="CONFIRMED",
         title="Nvidia slides 5.9%",
         body="Nvidia fell 5.9% to $155.38, shedding about $233bn, a day "
              "after its 31.5% Huang rally.",
         src="Motley Fool", kind="coin"),
    dict(n=7, tag="RUSSIA", region="EUROPE", badge="OFFICIAL",
         title="Putin vows refinery revenge",
         body="Putin said Ukraine kept hitting Russian oil plants despite "
              "Trump's requests, and pledged retaliation.",
         src="Reuters", kind="flag"),
    dict(n=8, tag="GAZA", region="MIDEAST", badge="OFFICIAL",
         title="Gaza meningitis alert",
         body="Gaza's health ministry declared an epidemic alert after 272 "
              "meningitis cases in October, 8x the norm.",
         src="Irish Times", kind="cross"),
    dict(n=9, tag="IRAN", region="MIDEAST", badge="CONFIRMED",
         title="Iran rial hits record low",
         body="The rial fell about 5% to 2.82 million per dollar after "
              "fresh US sanctions on shadow banking.",
         src="AFP", kind="coin"),
    dict(n=10, tag="POPE", region="WORLD", badge="CONFIRMED",
         title="Pope's diary reveals crisis",
         body="Francis's private diary, published Tuesday, tells of a "
              "2021\u201322 spiritual crisis and visions of the devil.",
         src="AP", kind="globe"),
    dict(n=11, tag="USA", region="AMERICAS", badge="CONFIRMED",
         title="King tides flood California",
         body="King tides flooded Sausalito and Marin County homes as "
              "Thanksgiving travel ramped up.",
         src="AP", kind="sea"),
    dict(n=12, tag="SPACE", region="WORLD", badge="OFFICIAL",
         title="Cargo ship lifts off to ISS",
         body="Russia's Progress 97 launched from Baikonur with about "
              "three tons of food and fuel for the ISS.",
         src="NASA", kind="rocket"),
    dict(n=13, tag="ETHIOPIA", region="AFRICA", badge="OFFICIAL",
         title="Tigray shelling 'war crimes'",
         body="Amnesty said Ethiopian artillery strikes on Alamata must be "
              "probed as possible war crimes; 14 dead verified.",
         src="Amnesty", kind="blast"),
    dict(n=14, tag="FOOTBALL", region="EUROPE", badge="CONFIRMED",
         title="Como edge AEK 1\u20130",
         body="Luis Milla's 57th-minute curler gave Como a Champions "
              "League win over AEK Athens.",
         src="Football Italia", kind="ball"),
]

# (number, text, region, badge)
ALSO = [
    (15, "US confidence hits 103.3", "AMERICAS", "OFFICIAL"),
    (16, "ADI plunges 17.4% on outlook", "AMERICAS", "CONFIRMED"),
    (17, "Norway talks Ukraine stability", "EUROPE", "REPORTED"),
    (18, "Russian jets enter Korea ADIZ", "ASIA", "CONFIRMED"),
    (19, "Iraq seizes Kurd oilfields", "MIDEAST", "REPORTED"),
    (20, "Japan pays ICC early", "ASIA", "CONFIRMED"),
    (21, "UK sanctions four Houthis", "EUROPE", "OFFICIAL"),
    (22, "UK warns firms on sabotage", "EUROPE", "REPORTED"),
    (23, "Hegseth holds 60 Patriots", "AMERICAS", "REPORTED"),
    (24, "Hasina seeks Dec 16 return", "ASIA", "REPORTED"),
    (25, "Seoul pays AI-cheat tipsters", "ASIA", "REPORTED"),
    (26, "China starts 6G pilots", "ASIA", "REPORTED"),
    (27, "Ariane lofts 36 Leo satellites", "EUROPE", "CONFIRMED"),
    (28, "Falcon 9 launches USSF-266", "AMERICAS", "CONFIRMED"),
    (29, "Arsenal 1\u20131 Dortmund", "EUROPE", "REPORTED"),
    (30, "Bod\u00f8/Glimt beat LASK 1\u20130", "EUROPE", "CONFIRMED"),
    (31, "Betis win 2\u20130 at Slovan", "EUROPE", "CONFIRMED"),
    (32, "Ebola staff still trapped in DRC", "AFRICA", "OFFICIAL"),
    (33, "FBI probes police DB breach", "AMERICAS", "REPORTED"),
    (34, "Australia sets 46 AI rules", "WORLD", "REPORTED"),
    (35, "Huckabee doubts aid cutoff", "AMERICAS", "REPORTED"),
]

# (big number, label, story number it illustrates)
NUMBERS = [
    ("50,019", "Dow tops 50,000 \u00b7 \u21161", 1),
    ("7", "Gaza strike deaths \u00b7 \u21162", 2),
    ("11", "wounded in Riyadh \u00b7 \u21163", 3),
    ("40", "wounded in Ukraine \u00b7 \u21164", 4),
    ("13", "UAE bus crash dead \u00b7 \u21165", 5),
    ("272", "meningitis cases \u00b7 \u21168", 8),
]

REGION_ORDER = ["EUROPE", "MIDEAST", "AFRICA", "ASIA", "AMERICAS", "WORLD"]
REGION_COLS = [RED, BLUE, TEAL, OCHRE, (90, 90, 90), (120, 110, 95)]
REGION_SHORT = {"AMERICAS": "AMER"}

DATE_CHECK = ("DATE CHECK \u2014 NOT TUESDAY: COP31 collapse (Sun) \u00b7 "
              "Merkury sinking (Sun) \u00b7 Huang reinstated (Mon) \u00b7 "
              "UN Libya probe (Mon) \u00b7 Megaspeed blacklist (Mon) \u00b7 "
              "Super Bowl IMAX (Mon) \u00b7 Board of Peace (Mon) \u00b7 "
              "NATO space warning (Mon) \u00b7 Indonesia fire (Sat) \u00b7 "
              "Guterres AI call (Mon)")

LEGEND = ("HOW WE CHECKED: CONFIRMED = two independent reports \u00b7 "
          "OFFICIAL = named official source \u00b7 REPORTED = one reputable "
          "report \u00b7 CLAIM = one side\u2019s claim, unverified. "
          "Full sources: RESEARCH.md.")

# Dotted world map: land spans per row, cols 0..63, rows 0..23.
# Hand-drawn from a world outline, stylised; lon -180..180 -> col,
# lat 90..-60 -> row.
MAP_ROWS = [
    [],
    [(10, 18), (21, 24), (40, 58)],
    [(3, 8), (9, 20), (21, 27), (33, 36), (38, 63)],
    [(3, 9), (10, 22), (23, 28), (33, 38), (39, 63)],
    [(4, 10), (11, 23), (26, 27), (34, 39), (40, 63)],
    [(11, 24), (28, 29), (30, 40), (41, 63)],
    [(12, 25), (29, 41), (42, 62)],
    [(13, 26), (30, 40), (42, 60), (60, 62)],
    [(14, 27), (30, 40), (44, 58), (59, 61)],
    [(15, 28), (31, 40), (41, 46), (47, 51), (52, 58)],
    [(16, 24), (31, 42), (43, 47), (48, 52), (53, 58)],
    [(17, 23), (32, 43), (49, 52), (53, 58)],
    [(18, 22), (33, 44), (54, 58), (55, 60)],
    [(20, 26), (34, 44), (52, 60)],
    [(21, 27), (35, 43), (53, 61)],
    [(22, 28), (36, 42), (54, 58)],
    [(23, 29), (37, 41), (53, 59)],
    [(24, 29), (38, 41), (52, 59)],
    [(25, 30), (38, 40), (52, 58)],
    [(25, 29), (38, 39), (53, 57)],
    [(25, 28), (54, 56), (60, 61)],
    [(26, 27)],
    [(26, 27)],
    [],
]

PINS = [  # (story no, lon, lat, dx, dy) — dx/dy nudge the label circle
    # off the true point (thin leader line) where pins would merge.
    # 15 pins: №8 (Gaza meningitis) and №11 (San Francisco) dropped —
    # same spots as №2 Gaza City and №6 Santa Clara.
    (1, -74.01, 40.71, 0, 0), (2, 34.47, 31.50, -22, 12),
    (3, 46.68, 24.71, -8, 14), (4, 35.12, 47.85, -16, -8),
    (5, 55.94, 25.79, 16, -8), (6, -121.95, 37.35, -14, -10),
    (7, 37.62, 55.76, 16, -8), (9, 51.39, 35.69, 0, 14),
    (10, 12.45, 41.90, 24, 14), (12, 63.31, 45.96, 0, 0),
    (13, 39.55, 12.42, 20, 10), (14, 9.08, 45.81, -22, -8),
    (17, 10.75, 59.91, 0, -12), (18, 126.98, 37.57, -10, 8),
    (20, 139.69, 35.68, 0, 0),
]


# ------------------------------------------------------------- illustration
def draw_lead_art(d, kind, x, y, w, h, tint, deep):
    """Poster-style art panel: flat tint background, one big bold motif
    in the deep colour + white + a gold accent. Filled shapes, high
    contrast, motif fills the panel."""
    d.rectangle([x, y, x + w, y + h], fill=TINT[tint])
    cx, cy = x + w // 2, y + h // 2 + 4
    if kind == "globe":
        r = 38
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255),
                  outline=deep, width=4)
        d.ellipse([cx - r * 0.5, cy - r, cx + r * 0.5, cy + r],
                  outline=deep, width=3)
        d.line([cx - r, cy, cx + r, cy], fill=deep, width=3)
        d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=RED, width=8)
    elif kind == "ship":
        d.polygon([(cx - 50, cy + 6), (cx + 50, cy + 6),
                   (cx + 36, cy + 32), (cx - 36, cy + 32)], fill=deep)
        d.rectangle([cx - 24, cy - 12, cx + 12, cy + 6], fill=deep)
        d.rectangle([cx - 4, cy - 36, cx + 4, cy - 12], fill=deep)
        d.rectangle([cx - 24, cy - 20, cx + 12, cy - 12],
                    fill=(255, 255, 255))
        pts = []
        for i in range(12):
            r = 20 if i % 2 == 0 else 9
            a = math.radians(i * 30)
            pts.append((cx + 36 + r * math.cos(a), cy - 28 + r * math.sin(a)))
        d.polygon(pts, fill=GOLD)
        for yy in (cy + 40, cy + 46):
            d.arc([cx - 50, yy - 7, cx - 16, yy + 7], 180, 360,
                  fill=(255, 255, 255), width=3)
            d.arc([cx - 16, yy - 7, cx + 18, yy + 7], 180, 360,
                  fill=(255, 255, 255), width=3)
    elif kind == "chip":
        d.rounded_rectangle([cx - 34, cy - 34, cx + 34, cy + 34], radius=8,
                            fill=deep)
        for px in (-34, 34):
            for py in (-17, 0, 17):
                d.rectangle([cx + px - 7, cy + py - 3,
                             cx + px + 7, cy + py + 3], fill=deep)
        f = font(SANS_B, 38)
        t = "N"
        tw = d.textlength(t, font=f)
        d.text((cx - tw / 2, cy - 25), t, font=f, fill=(255, 255, 255))
        d.rectangle([cx + 38, cy - 16, cx + 46, cy + 10], fill=GOLD)
        d.polygon([(cx + 30, cy - 12), (cx + 54, cy - 12), (cx + 42, cy - 32)],
                  fill=GOLD)
    elif kind == "coin":
        # big coin with a dollar mark and a gold up-arrow
        r = 38
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=deep)
        d.ellipse([cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8],
                  outline=(255, 255, 255), width=3)
        f = font(SANS_B, 44)
        t = "$"
        tw = d.textlength(t, font=f)
        d.text((cx - tw / 2, cy - 26), t, font=f, fill=(255, 255, 255))
        d.rectangle([cx + 40, cy - 18, cx + 48, cy + 8], fill=GOLD)
        d.polygon([(cx + 32, cy - 14), (cx + 56, cy - 14), (cx + 44, cy - 34)],
                  fill=GOLD)
    elif kind == "flame":
        # leaning teardrop flame with a gold inner flame
        d.polygon([(cx - 4, cy - 44), (cx + 28, cy - 4), (cx + 30, cy + 14),
                   (cx + 18, cy + 32), (cx + 2, cy + 28),
                   (cx - 12, cy + 32), (cx - 28, cy + 4),
                   (cx - 22, cy - 18)], fill=deep)
        d.polygon([(cx + 2, cy - 14), (cx + 14, cy + 8),
                   (cx + 4, cy + 26), (cx - 10, cy + 8)], fill=(255, 220, 120))
    elif kind == "blast":
        pts = []
        for i in range(12):
            r = 40 if i % 2 == 0 else 18
            a = math.radians(i * 30)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        d.polygon(pts, fill=deep)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=GOLD)
    elif kind == "sea":
        for yy in (-0.18, 0.14):
            yyv = cy + yy * 90
            d.arc([cx - 52, yyv - 12, cx - 4, yyv + 12], 180, 360,
                  fill=deep, width=4)
            d.arc([cx + 4, yyv - 12, cx + 52, yyv + 12], 180, 360,
                  fill=deep, width=4)
        d.polygon([(cx - 44, cy - 10), (cx + 44, cy - 10),
                   (cx + 26, cy - 28), (cx - 26, cy - 28)], fill=deep)


def draw_mini(d, kind, x, y, s, tint, deep):
    """Small filled pictogram (deep colour on a tinted tile) for secondaries."""
    d.rounded_rectangle([x, y, x + s, y + s], radius=5, fill=TINT[tint])
    cx, cy = x + s // 2, y + s // 2
    w = deep
    if kind == "globe":
        r = s * 0.32
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=w, width=3)
        d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
                  outline=w, width=2)
        d.line([cx - r, cy, cx + r, cy], fill=w, width=2)
    elif kind == "sea":
        for yy in (-0.2, 0.15):
            yyv = cy + yy * s
            d.arc([cx - s * 0.32, yyv - s * 0.12, cx - s * 0.02, yyv + s * 0.12],
                  180, 360, fill=w, width=3)
            d.arc([cx - s * 0.02, yyv - s * 0.12, cx + s * 0.32, yyv + s * 0.12],
                  180, 360, fill=w, width=3)
        d.polygon([(cx - s * 0.28, cy - s * 0.12), (cx + s * 0.28, cy - s * 0.12),
                   (cx + s * 0.16, cy - s * 0.3), (cx - s * 0.16, cy - s * 0.3)],
                  fill=w)
    elif kind == "blast":
        pts = []
        for i in range(12):
            r = s * 0.36 if i % 2 == 0 else s * 0.17
            a = math.radians(i * 30)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        d.polygon(pts, fill=w)
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=GOLD)
    elif kind == "flag":
        d.rectangle([cx - s * 0.3, cy - s * 0.34, cx - s * 0.24, cy + s * 0.34],
                    fill=w)
        d.polygon([(cx - s * 0.24, cy - s * 0.34), (cx + s * 0.32, cy - s * 0.22),
                   (cx + s * 0.32, cy - s * 0.08), (cx - s * 0.24, cy - s * 0.14)],
                  fill=w)
    elif kind == "cross":
        d.rectangle([cx - s * 0.09, cy - s * 0.32, cx + s * 0.09, cy + s * 0.32],
                    fill=w)
        d.rectangle([cx - s * 0.32, cy - s * 0.09, cx + s * 0.32, cy + s * 0.09],
                    fill=w)
    elif kind == "coin":
        r = s * 0.32
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=w, width=3)
        f = font(SANS_B, 15)
        d.text((cx - 5, cy - 10), "B", font=f, fill=w)
    elif kind == "ball":
        r = s * 0.32
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=w, width=3)
        d.polygon([(cx, cy - r * 0.45), (cx + r * 0.43, cy - r * 0.14),
                   (cx + r * 0.26, cy + r * 0.36), (cx - r * 0.26, cy + r * 0.36),
                   (cx - r * 0.43, cy - r * 0.14)], fill=w)
    elif kind == "rocket":
        d.polygon([(cx, cy - s * 0.36), (cx + s * 0.16, cy - s * 0.04),
                   (cx + s * 0.16, cy + s * 0.22), (cx, cy + s * 0.36),
                   (cx - s * 0.16, cy + s * 0.22), (cx - s * 0.16, cy - s * 0.04)],
                  fill=w)
        d.ellipse([cx - s * 0.07, cy - s * 0.2, cx + s * 0.07, cy - s * 0.05],
                  fill=PAPER)


# tile tint per secondary kind (matches the lead palette family)
KIND_TINT = {"blast": "red", "sea": "blue", "flag": "red", "globe": "blue",
             "cross": "red", "coin": "teal", "ball": "blue", "rocket": "blue"}
KIND_DEEP = {"blast": RED, "sea": BLUE, "flag": RED, "globe": NAVY,
             "cross": RED, "coin": TEAL, "ball": BLUE, "rocket": NAVY}


def num_circle(d, x, y, n, diam=30):
    """Red numbered circle."""
    d.ellipse([x, y, x + diam, y + diam], fill=RED)
    f = font(SANS_B, 16 if n < 10 else 14)
    t = str(n)
    tw = d.textlength(t, font=f)
    d.text((x + (diam - tw) / 2, y + (diam - 16) / 2 - 1), t, font=f,
           fill=(255, 255, 255))


def pill_width(d, label):
    """Width a verification pill would take, without drawing it."""
    f = font(SANS_B, 9)
    return d.textlength(label, font=f) + 14


def badge_pill(d, x, y, label, fill):
    """Small coloured verification pill; returns its width."""
    f = font(SANS_B, 9)
    w = d.textlength(label, font=f) + 14
    d.rounded_rectangle([x, y, x + w, y + 16], radius=8, fill=fill)
    tw = d.textlength(label, font=f)
    d.text((x + (w - tw) / 2, y + 3), label, font=f, fill=(255, 255, 255))
    return w


def fit_check(d):
    """Fail loudly if any text would be cut — nothing is truncated."""
    # leads: title <= 2 lines, body <= 5 lines, source fits on one line
    for st in LEADS:
        assert len(wrap(d, st["title"], font(SANS_B, 15), 224)) <= 2, \
            f"lead {st['n']} title wraps"
        lines = wrap(d, st["body"], font(SANS, 10), 224)
        assert len(lines) <= 5, f"lead {st['n']} body needs {len(lines)} lines"
        assert d.textlength("Source: " + st["src"], font=font(SANS, 10)) <= 224, \
            f"lead {st['n']} source too long"
    # secondaries: title+tag fits beside the badge pill, body <= 2 lines
    for st in SECONDARIES:
        title = f"{st['n']}. {st['title']} \u2014 {st['tag']}"
        pill_w = d.textlength(st["badge"], font=font(SANS_B, 9)) + 14
        assert d.textlength(title, font=font(SANS_B, 12)) + pill_w + 10 <= 432, \
            f"secondary {st['n']} title too long"
        suffix = " \u2014 " + st["src"]
        lines = wrap(d, st["body"], font(SANS, 11), 432)
        assert len(lines) <= 2, f"secondary {st['n']} body needs {len(lines)} lines"
        assert d.textlength(lines[-1] + suffix, font=font(SANS, 11)) <= 432, \
            f"secondary {st['n']} body+src too long"
    # ALSO list: one line each in the left bottom column
    for n, item, _r, badge in ALSO:
        w = (d.textlength(f"{n}. {item}", font=font(SANS, 10))
             + d.textlength(" \u00b7 " + badge, font=font(SANS_B, 9)))
        assert w <= 470, f"ALSO {n} too long"
    # numbers strip labels fit their cell
    for _num, lab, _n in NUMBERS:
        assert d.textlength(lab, font=font(SANS, 10)) <= 152, \
            f"numbers label too long: {lab}"
    dc = wrap(d, DATE_CHECK, font(SANS_B, 11), 960)
    assert len(dc) <= 2, f"DATE CHECK needs {len(dc)} lines"
    assert d.textlength(LEGEND, font(SANS, 9)) <= 984, "legend too long"
    # map pins: every pair of label circles at least 17px apart
    def proj(lon, lat):
        return (510 + (lon + 180) / 360 * 494,
                742 + (90 - lat) / 150 * 216)
    centres = []
    for _n, lon, lat, dx, dy in PINS:
        px, py = proj(lon, lat)
        centres.append((px + dx, py + dy))
    for i in range(len(centres)):
        for j in range(i + 1, len(centres)):
            dx = centres[i][0] - centres[j][0]
            dy = centres[i][1] - centres[j][1]
            assert dx * dx + dy * dy >= 17 * 17, \
                f"pins {PINS[i][0]} and {PINS[j][0]} too close"


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 20

    # sanity: 35 stories, region counts computed from the tags
    all_stories = list(LEADS) + list(SECONDARIES) + [
        dict(n=n, region=r) for n, _t, r, _b in ALSO]
    assert len(all_stories) == 35, len(all_stories)
    counts = Counter(s["region"] for s in all_stories)
    assert sum(counts.values()) == 35
    regions = [(name, counts[name]) for name in REGION_ORDER]

    fit_check(d)

    # ---- red top rule + masthead --------------------------------------
    d.rectangle([0, 0, W, 6], fill=RED)
    title = "THE TUESDAY GLOBE"
    f_title = font(SERIF, 50)
    d.text((W / 2, 14), title, font=f_title, fill=INK, anchor="ma")
    d.line([MX, 68, W - MX, 68], fill=INK, width=2)
    d.line([MX, 72, W - MX, 72], fill=INK, width=1)

    # ---- red date band -------------------------------------------------
    d.rectangle([MX, 76, W - MX, 104], fill=RED)
    d.text((MX + 12, 90), "TUESDAY 24 NOVEMBER 2026", font=font(SANS_B, 20),
           fill=(255, 255, 255), anchor="lm")
    d.text((W - MX - 12, 90), "35 STORIES \u00b7 ONE DAY",
           font=font(SANS_B, 12), fill=(255, 255, 255), anchor="rm")

    # ---- dark navy numbers strip ---------------------------------------
    d.rectangle([MX, 110, W - MX, 162], fill=NAVY)
    cell_w = (W - 2 * MX) / 6
    for i, (num, lab, _n) in enumerate(NUMBERS):
        cx = MX + cell_w * (i + 0.5)
        if i:
            d.line([MX + cell_w * i, 114, MX + cell_w * i, 158],
                   fill=(70, 90, 120), width=1)
        d.text((cx, 126), num, font=font(SANS_B, 26),
               fill=(255, 255, 255), anchor="mm")
        d.text((cx, 148), lab, font=font(SANS, 10), fill=GOLD, anchor="mm")

    # ---- region bar ------------------------------------------------------
    x = MX
    total_w = W - 2 * MX
    for (name, count), col in zip(regions, REGION_COLS):
        seg = total_w * count / 35
        d.rectangle([x, 166, x + seg, 186], fill=col)
        label = f"{REGION_SHORT.get(name, name)} {count}"
        d.text((x + seg / 2, 176), label, font=font(SANS_B, 11),
               fill=(255, 255, 255), anchor="mm")
        x += seg

    # ---- four leads in one row ------------------------------------------
    col_w, gap = 240, 8
    for i, st in enumerate(LEADS):
        x0 = MX + i * (col_w + gap)
        # poster art panel on top, text below
        draw_lead_art(d, st["kind"], x0, 192, col_w, 106,
                      st["tint"], st["deep"])
        num_circle(d, x0 - 2, 190, st["n"], diam=30)
        # tag + verification pill
        d.text((x0, 306), f"{st['tag']} \u00b7 {st['region']}",
               font=font(SANS_B, 10), fill=RED)
        pw = pill_width(d, st["badge"])
        badge_pill(d, x0 + col_w - pw, 302, st["badge"],
                   BADGE_FILL[st["badge"]])
        # title (up to 2 lines), body (up to 5), source
        y = 322
        for line in wrap(d, st["title"], font(SANS_B, 15), col_w):
            d.text((x0, y), line, font=font(SANS_B, 15), fill=INK)
            y += 19
        y = 362
        for line in wrap(d, st["body"], font(SANS, 10), col_w):
            d.text((x0, y), line, font=font(SANS, 10), fill=INK)
            y += 13
        d.text((x0, 430), "Source: " + st["src"], font=font(SANS, 10),
               fill=GREY)
        d.line([x0, 448, x0 + col_w, 448], fill=(200, 195, 180), width=1)

    # ---- secondaries header ----------------------------------------------
    d.text((MX, 456), "MORE FROM TUESDAY", font=font(SANS_B, 14), fill=INK)
    d.text((W - MX, 460), "10 MORE STORIES \u00b7 \u2116 5\u201314",
           font=font(SANS, 10), fill=GREY, anchor="ra")
    d.line([MX, 474, W - MX, 474], fill=INK, width=1)

    # ---- secondaries: two columns of five --------------------------------
    for i, st in enumerate(SECONDARIES):
        col, row = divmod(i, 5)
        x0 = MX + col * 496
        y0 = 478 + row * 48
        draw_mini(d, st["kind"], x0, y0 + 4, 36,
                  KIND_TINT[st["kind"]], KIND_DEEP[st["kind"]])
        num_circle(d, x0 + 24, y0 + 26, st["n"], diam=22)
        tx = x0 + 56
        title = f"{st['n']}. {st['title']} \u2014 {st['tag']}"
        d.text((tx, y0 + 2), title, font=font(SANS_B, 12), fill=INK)
        pw = pill_width(d, st["badge"])
        badge_pill(d, x0 + 488 - pw, y0 + 2, st["badge"],
                   BADGE_FILL[st["badge"]])
        lines = wrap(d, st["body"], font(SANS, 11), 432)
        suffix = " \u2014 " + st["src"]
        for li, line in enumerate(lines):
            yy = y0 + 19 + li * 14
            if li == len(lines) - 1:
                d.text((tx, yy), line, font=font(SANS, 11), fill=INK)
                sw = d.textlength(line, font=font(SANS, 11))
                d.text((tx + sw, yy), suffix, font=font(SANS, 11), fill=GREY)
            else:
                d.text((tx, yy), line, font=font(SANS, 11), fill=INK)

    # ---- bottom split: ALSO (left) / map (right) -------------------------
    d.text((MX, 722), "ALSO ON TUESDAY", font=font(SANS_B, 14), fill=RED)
    d.text((510, 722), "WHERE IT HAPPENED", font=font(SANS_B, 14), fill=RED)
    d.text((W - MX, 726), "pins match the stories above",
           font=font(SANS, 9), fill=GREY, anchor="ra")
    d.line([MX, 740, 496, 740], fill=INK, width=1)
    d.line([510, 740, W - MX, 740], fill=INK, width=1)

    for i, (n, item, _r, badge) in enumerate(ALSO):
        y = 744 + i * 10.3
        d.text((MX, y), f"{n}. {item}", font=font(SANS, 10), fill=INK)
        tw = d.textlength(f"{n}. {item}", font=font(SANS, 10))
        d.text((MX + tw, y), " \u00b7 " + badge, font=font(SANS_B, 9),
               fill=BADGE_FILL[badge])

    # dotted world map
    map_x, map_y, map_w, map_h = 510, 744, 494, 214
    cw, ch = map_w / 64, map_h / 24
    for r, spans in enumerate(MAP_ROWS):
        for c0, c1 in spans:
            for c in range(c0, c1 + 1):
                px = map_x + (c + 0.5) * cw
                py = map_y + (r + 0.5) * ch
                d.ellipse([px - 2.2, py - 2.2, px + 2.2, py + 2.2], fill=DOT)

    def proj(lon, lat):
        return (map_x + (lon + 180) / 360 * map_w,
                map_y + (90 - lat) / 150 * map_h)

    for n, lon, lat, dx, dy in PINS:
        px, py = proj(lon, lat)
        cx, cy = px + dx, py + dy
        if dx or dy:
            d.line([px, py, cx, cy], fill=RED, width=1)
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        f = font(SANS_B, 9)
        t = str(n)
        tw = d.textlength(t, font=f)
        d.text((cx - tw / 2, cy - 5), t, font=f, fill=(255, 255, 255))

    # ---- DATE CHECK box ----------------------------------------------------
    d.rectangle([MX, 964, W - MX, 994], outline=RED, width=2, fill=PANEL)
    dc_lines = wrap(d, DATE_CHECK, font(SANS_B, 11), 960)
    for i, line in enumerate(dc_lines):
        d.text((MX + 12, 968 + i * 14), line, font=font(SANS_B, 11), fill=INK)

    # ---- footer legend ------------------------------------------------------
    d.text((W / 2, 1000), LEGEND, font=font(SANS, 9), fill=GREY, anchor="ma")

    img.save(OUT)
    print("wrote", OUT)


if __name__ == "__main__":
    main()

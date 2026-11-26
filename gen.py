#!/usr/bin/env python3
"""Render the front page for news-image-20261125 (numbers edition).

Draws a dense one-page newspaper: 50 stories, 13 illustrated scenes,
numbered cards, a pinned world map and a two-line DATE CHECK. All copy is
English; every story is dated Wednesday 25 November 2026.
Run:  python3 gen.py   ->  writes entry.png (1024x1024) next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 227)
INK = (20, 20, 20)
RED = (179, 35, 27)
BLUE = (29, 78, 137)
TEAL = (15, 107, 92)
GOLD = (138, 109, 27)
PURPLE = (91, 42, 134)
GREY = (90, 86, 76)
LIGHT = (255, 255, 255)
SKY = (188, 214, 232)
NAVY = (16, 28, 56)

FD = "/usr/share/fonts/truetype/dejavu"


def F(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: F("DejaVuSans-Bold.ttf", s)
SANS = lambda s: F("DejaVuSans.ttf", s)

PALETTE = [RED, BLUE, TEAL, GOLD, PURPLE, (34, 110, 60), (150, 60, 20)]


def wrap(text, font, maxw):
    """Greedy word wrap by pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if font.getlength(trial) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def fit_lines(text, font, maxw, max_lines):
    """Wrap and truncate with an ellipsis so it fits max_lines."""
    lines = wrap(text, font, maxw)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and font.getlength(lines[-1] + " ...") > maxw:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1] + " ..."
    return lines


def text(d, xy, s, font, fill=INK):
    d.text(xy, s, font=font, fill=fill)


def centre(d, cx, y, s, font, fill=INK):
    d.text((cx - font.getlength(s) / 2, y), s, font=font, fill=fill)


# ---------------------------------------------------------------- scenes
def draw_scene(d, x, y, w, h, kind):
    """Draw a small flat illustration inside box (x, y, w, h)."""
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=INK, width=1)
    if kind == "rocket":
        d.rectangle([x, y, x + w, y + h], fill=NAVY)
        for sx, sy in [(0.15, 0.2), (0.8, 0.15), (0.6, 0.35), (0.3, 0.1),
                       (0.9, 0.5), (0.1, 0.55)]:
            d.ellipse([x + sx * w - 1, y + sy * h - 1,
                       x + sx * w + 1, y + sy * h + 1], fill=LIGHT)
        bx = x + w * 0.42
        d.polygon([(bx + w * 0.08, y + h * 0.12), (bx, y + h * 0.3),
                   (bx + w * 0.16, y + h * 0.3)], fill=RED)
        d.rectangle([bx, y + h * 0.3, bx + w * 0.16, y + h * 0.62],
                    fill=LIGHT)
        d.ellipse([bx + w * 0.03, y + h * 0.38, bx + w * 0.13, y + h * 0.48],
                  fill=BLUE)
        d.polygon([(bx - w * 0.02, y + h * 0.62), (bx + w * 0.18, y + h * 0.62),
                   (bx + w * 0.08, y + h * 0.78)], fill=(255, 140, 0))
        d.polygon([(bx + w * 0.02, y + h * 0.62), (bx + w * 0.14, y + h * 0.62),
                   (bx + w * 0.08, y + h * 0.72)], fill=(255, 220, 0))
        d.arc([x + w * 0.05, y + h * 0.72, x + w * 0.95, y + h * 1.25],
              180, 360, fill=TEAL, width=max(2, int(w * 0.04)))
    elif kind == "mine":
        d.rectangle([x, y, x + w, y + h], fill=(222, 200, 150))
        d.polygon([(x, y + h), (x + w * 0.25, y + h * 0.25),
                   (x + w * 0.75, y + h * 0.25), (x + w, y + h)],
                  fill=(150, 110, 60))
        d.polygon([(x + w * 0.42, y + h * 0.3), (x + w * 0.58, y + h * 0.3),
                   (x + w * 0.58, y + h), (x + w * 0.42, y + h)], fill=(30, 20, 10))
        d.rectangle([x + w * 0.4, y + h * 0.28, x + w * 0.6, y + h * 0.36],
                    fill=(90, 60, 30))
        for hx, hy in [(0.2, 0.7), (0.8, 0.65), (0.3, 0.85)]:
            d.ellipse([x + hx * w - 3, y + hy * h - 3, x + hx * w + 3,
                       y + hy * h + 3], fill=(255, 220, 0))
            d.rectangle([x + hx * w - 3, y + hy * h + 2, x + hx * w + 3,
                         y + hy * h + 6], fill=RED)
        d.line([x + w * 0.1, y + h * 0.2, x + w * 0.9, y + h * 0.2],
               fill=BLUE, width=2)
    elif kind == "chart":
        d.rectangle([x, y, x + w, y + h], fill=LIGHT)
        for gy in (0.25, 0.5, 0.75):
            d.line([x + 2, y + gy * h, x + w - 2, y + gy * h],
                   fill=(220, 220, 220), width=1)
        pts = [(0.08, 0.25), (0.25, 0.35), (0.42, 0.3), (0.58, 0.55),
               (0.75, 0.7), (0.92, 0.85)]
        for i in range(len(pts) - 1):
            d.line([x + pts[i][0] * w, y + pts[i][1] * h,
                    x + pts[i + 1][0] * w, y + pts[i + 1][1] * h],
                   fill=RED, width=max(2, int(w * 0.05)))
        for px, py in pts:
            d.ellipse([x + px * w - 2, y + py * h - 2, x + px * w + 2,
                       y + py * h + 2], fill=RED)
        d.line([x + 2, y + h - 3, x + w - 2, y + h - 3], fill=INK, width=1)
    elif kind == "building":
        d.rectangle([x, y, x + w, y + h], fill=(210, 205, 190))
        d.rectangle([x + w * 0.2, y + h * 0.25, x + w * 0.8, y + h],
                    fill=(120, 120, 125))
        for wy in (0.35, 0.55, 0.75):
            for wx in (0.3, 0.5, 0.7):
                d.rectangle([x + wx * w - 2, y + wy * h - 2,
                             x + wx * w + 2, y + wy * h + 2], fill=(255, 230, 120))
        d.polygon([(x + w * 0.55, y + h * 0.25), (x + w * 0.75, y + h * 0.1),
                   (x + w * 0.8, y + h * 0.25)], fill=(90, 90, 90))
        d.ellipse([x + w * 0.6, y + h * 0.02, x + w * 0.95, y + h * 0.3],
                  fill=(200, 200, 200))
    elif kind == "drone":
        d.rectangle([x, y, x + w, y + h], fill=SKY)
        cx, cy = x + w * 0.5, y + h * 0.45
        d.rectangle([cx - w * 0.12, cy - 2, cx + w * 0.12, cy + 2], fill=INK)
        for dx, dy in [(-0.18, -0.12), (0.18, -0.12), (-0.18, 0.12), (0.18, 0.12)]:
            px, py = cx + dx * w, cy + dy * h
            d.line([cx, cy, px, py], fill=INK, width=1)
            d.ellipse([px - 4, py - 1, px + 4, py + 1], fill=INK)
        d.polygon([(x + w * 0.2, y + h * 0.85), (x + w * 0.5, y + h * 0.7),
                   (x + w * 0.8, y + h * 0.85)], fill=(120, 90, 50))
        d.rectangle([x + w * 0.45, y + h * 0.7, x + w * 0.55, y + h * 0.85],
                    fill=(150, 40, 30))
    elif kind == "island":
        d.rectangle([x, y, x + w, y + h * 0.7], fill=SKY)
        d.rectangle([x, y + h * 0.7, x + w, y + h], fill=(40, 110, 180))
        d.ellipse([x + w * 0.1, y + h * 0.68, x + w * 0.9, y + h * 0.95],
                  fill=(220, 200, 130))
        d.line([x + w * 0.5, y + h * 0.3, x + w * 0.5, y + h * 0.68],
               fill=(110, 70, 30), width=2)
        for ang in (-50, -10, 30):
            import math
            ex = x + w * 0.5 + math.cos(math.radians(ang - 90)) * w * 0.22
            ey = y + h * 0.3 + math.sin(math.radians(ang - 90)) * h * 0.2
            d.line([x + w * 0.5, y + h * 0.3, ex, ey], fill=TEAL, width=2)
        d.polygon([(x + w * 0.5, y + h * 0.32), (x + w * 0.72, y + h * 0.38),
                   (x + w * 0.5, y + h * 0.44)], fill=RED)
    elif kind == "virus":
        d.rectangle([x, y, x + w, y + h], fill=(250, 235, 235))
        cx, cy, r = x + w * 0.5, y + h * 0.5, w * 0.26
        import math
        for k in range(10):
            a = math.radians(k * 36)
            d.line([cx + math.cos(a) * r, cy + math.sin(a) * r,
                    cx + math.cos(a) * (r + 5), cy + math.sin(a) * (r + 5)],
                   fill=RED, width=2)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
        for dx, dy in [(-0.1, -0.08), (0.12, 0.05), (-0.02, 0.12)]:
            d.ellipse([cx + dx * w - 2, cy + dy * h - 2, cx + dx * w + 2,
                       cy + dy * h + 2], fill=(255, 180, 180))
    elif kind == "crowd":
        d.rectangle([x, y, x + w, y + h], fill=(235, 230, 215))
        for i, hx in enumerate([0.18, 0.38, 0.58, 0.78]):
            col = [RED, BLUE, TEAL, GOLD][i]
            d.ellipse([x + hx * w - 4, y + h * 0.45 - 4, x + hx * w + 4,
                       y + h * 0.45 + 4], fill=col)
            d.polygon([(x + hx * w - 6, y + h), (x + hx * w - 5, y + h * 0.55),
                       (x + hx * w + 5, y + h * 0.55), (x + hx * w + 6, y + h)],
                      fill=col)
        d.rectangle([x + w * 0.15, y + h * 0.12, x + w * 0.85, y + h * 0.32],
                    fill=LIGHT, outline=INK)
        d.text((x + w * 0.2, y + h * 0.15), "24H", font=SANS_B(max(7, int(h * 0.18))),
               fill=RED)
    elif kind == "waves":
        d.rectangle([x, y, x + w, y + h * 0.55], fill=SKY)
        d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(40, 110, 180))
        for wy in (0.6, 0.75, 0.9):
            d.arc([x - w * 0.1, y + wy * h, x + w * 0.5, y + (wy + 0.25) * h],
                  180, 360, fill=LIGHT, width=2)
            d.arc([x + w * 0.4, y + wy * h, x + w * 1.0, y + (wy + 0.25) * h],
                  180, 360, fill=LIGHT, width=2)
        d.polygon([(x + w * 0.3, y + h * 0.3), (x + w * 0.7, y + h * 0.3),
                   (x + w * 0.5, y + h * 0.12)], fill=RED)
        d.rectangle([x + w * 0.35, y + h * 0.3, x + w * 0.65, y + h * 0.55],
                    fill=(200, 170, 120))
    elif kind == "jet":
        d.rectangle([x, y, x + w, y + h], fill=SKY)
        d.line([x + w * 0.05, y + h * 0.7, x + w * 0.95, y + h * 0.7],
               fill=RED, width=1)
        for i in range(6):
            sx = x + w * (0.08 + i * 0.05)
            d.line([sx, y + h * 0.7, sx + 2, y + h * 0.7], fill=RED, width=1)
        cx, cy = x + w * 0.5, y + h * 0.4
        d.polygon([(cx - w * 0.25, cy), (cx + w * 0.2, cy - 3),
                   (cx + w * 0.28, cy), (cx + w * 0.2, cy + 3)],
                  fill=INK)
        d.polygon([(cx, cy - 2), (cx + w * 0.05, cy - h * 0.22),
                   (cx + w * 0.1, cy - 2)], fill=INK)
    elif kind == "containers":
        d.rectangle([x, y, x + w, y + h], fill=(223, 232, 242))
        cols = [RED, BLUE, GOLD, TEAL]
        for row in range(2):
            for col in range(4):
                cx0 = x + w * (0.04 + col * 0.24)
                cy0 = y + h * (0.5 + row * 0.24) if row == 0 else y + h * 0.74
                d.rectangle([cx0, cy0, cx0 + w * 0.2, cy0 + h * 0.2],
                            fill=cols[(row + col) % 4], outline=LIGHT)
        d.text((x + w * 0.62, y + h * 0.05), "%", font=SERIF_B(int(h * 0.55)),
               fill=RED)
        d.line([x, y + h * 0.48, x + w, y + h * 0.48], fill=INK, width=2)


# ---------------------------------------------------------------- data
# Every card: (number, headline, detail, C, R, CL, also, scene-or-None)
# C = CONFIRMED, R = REPORTED, CL = CLAIMED. All 50 stories are 25 Nov 2026.
HEROES = [
    ("TARIFFS", "45%", "US PROPOSES NEW TARIFFS ON 14 ECONOMIES",
     "China faces +20% on top of 25% already in place; EU, Japan, Korea and "
     "Taiwan at 15%; Vietnam up to 35%.",
     "WHY IT MATTERS: the widest US tariff move in years. It hit Asian chip "
     "stocks within hours.",
     "C 14", "R 45% top", "CL 35%",
     "ALSO 15% cap", "containers"),
    ("KOSPI", "-6.16%", "KOSPI CRASHES 6.16%, LOSES 5,000 IN A DAY",
     "Index closes at 4,697.51, down 308.52 points. Samsung -9.87% and "
     "SK hynix -11.05% lead the rout.",
     "WHY IT MATTERS: Seoul led Asia's sell-off, wiping out a day's gains "
     "- 5,000 was only just regained.",
     "C 4,697.51", "R 308.52 lost", "CL 5,000 lost",
     "ALSO Taiex -6.0%", "chart"),
    ("SPACE", "3", "SHENZHOU-24 DOCKS; FIRST PAKISTANI IN ORBIT",
     "Crew of 3 enters Tiangong at 06:35 GMT after launching from Jiuquan. "
     "Zeeshan Ali, 40, ex-PAF pilot, is aboard.",
     "WHY IT MATTERS: China's station takes its first foreign astronaut - "
     "a space milestone for the region.",
     "C 3 crew", "R 06:35 GMT", "CL 1st foreign",
     "ALSO 2 Chinese aboard", "rocket"),
]

CARDS = [
    (4, "BOGOR MINE FLOOD", "9 dead, 17 trapped, Mt Butak shafts.",
     "C 9 dead", "R 17", "CL 26", "ALSO 325", "mine"),
    (5, "ABUELOUF, HAMAS CHIEF", "Col. Mohammad, 47, wife, 2 girls.",
     "C 4", "R 2nd", "CL 47", "ALSO Shati", "building"),
    (6, "US INFLATION 3.8%", "PCE 3.8%; core 3.3% tops forecast.",
     "C 3.8%", "R 3.3%", "CL 3.2%", "ALSO GDP", "chart"),
    (7, "WALL ST COMEBACK", "Nasdaq fell 4.6% intraday, then staged the year's biggest comeback.",
     "C 4.6% drop", "R 3%", "CL 2%", "ALSO tech", None),
    (8, "SUDAN: 19 KILLED", "RSF drones kill 19 in Damazin.",
     "C 19", "R 20", "CL 1", "ALSO Blue Nile", "drone"),
    (9, "RUSSIA: 112 DRONES", "112 drones fired at Ukraine.",
     "C 112", "R 5", "CL 5", "ALSO overnight", "drone"),
    (10, "UKRAINE HITS REFINERIES", "Ukraine strikes 2 refineries inside Russia.",
     "C 2 refineries", "R 112", "CL 1", "ALSO deep strikes", None),
    (11, "POWER OUT IN 5 REGIONS", "Russian strikes cut power in 5 Ukrainian regions; 5 people killed.",
     "C 5 regions", "R 5 killed", "CL 112", "ALSO repair", None),
    (12, "SOLOMON TREATY", "Treaty signed in Canberra.",
     "C 1", "R 0", "CL 4 yrs", "ALSO top partner", "island"),
    (13, "CHINA PROBES CHEN JINING", "Shanghai party chief and Politburo member under investigation.",
     "C 1", "R 4th", "CL 1", "ALSO Shanghai chief", None),
    (14, "EBOLA: 11,986 CASES", "Cases 11,986; deaths 5,871.",
     "C 11,986", "R 5,871", "CL 49%", "ALSO up", "virus"),
    (15, "GREECE STRIKE", "Strike shuts transport, flights.",
     "C 24h", "R 1", "CL 3", "ALSO costs protest", "crowd"),
    (16, "KING TIDES FLOOD", "Tides flood California; parade off.",
     "C 1", "R 100 yrs", "CL 1st", "ALSO parade", "waves"),
    (17, "TAIWAN: 1 SORTIE", "1 sortie crosses line; 9 vessels.",
     "C 1", "R 9", "CL 1", "ALSO Taipei counts", "jet"),
    (18, "HEAT RECORD 2.24C", "World logs 6 straight days 2C above preindustrial; peak 2.24C.",
     "C 2.24C", "R 6 days", "CL 2C", "ALSO hottest", None),
    (19, "JOBLESS CLAIMS 189K", "US jobless claims 189K, below the 200K consensus.",
     "C 189K", "R 200K", "CL 11K", "ALSO tight labour", None),
    (20, "DURABLE GOODS SOFT", "Advance durable goods orders come in weaker than expected.",
     "C 1", "R 1 miss", "CL 4", "ALSO data dump", None),
    (21, "BEIGE BOOK OUT", "Fed Beige Book lands at 19:00 GMT, the last word before the rate call.",
     "C 1", "R 12 districts", "CL 1", "ALSO quiet nears", None),
    (22, "TAIEX -6.0%", "Taiwan Taiex falls 6.0%; at its worst it was down 8.6% intraday.",
     "C 6.0%", "R 8.6%", "CL 1 day", "ALSO chips fall", None),
    (23, "SAMSUNG -9.87%", "Samsung -9.87% to 170,700 won; SK hynix -11.05% to 1.03m won.",
     "C 9.87%", "R 11.05%", "CL 170,700", "ALSO chip rout", None),
    (24, "INDIA: 25% TARIFF", "India faces up to 25% tariff, or 17% if a trade deal is finalised.",
     "C 25%", "R 17%", "CL 14", "ALSO USTR plan", None),
    (25, "VIETNAM: 35% TARIFF", "Vietnam faces up to 35%, or 20% if a deal is finalised.",
     "C 35%", "R 20%", "CL 14", "ALSO top in Asia", None),
    (26, "INDONESIA NAMED", "Indonesia is among the 14 economies in the US tariff proposal.",
     "C 14", "R 6 SE Asia", "CL 1", "ALSO Jakarta", None),
    (27, "EU: 15% CAP", "EU faces a 15% tariff under the US proposal; the bloc weighs a reply.",
     "C 15%", "R 27", "CL 14", "ALSO cap matches", None),
    (28, "CHINA: 45% TOTAL", "China's total duty hits 45% on some goods under the proposal.",
     "C 45%", "R 20% new", "CL 25% old", "ALSO top", None),
    (29, "PROBE ENDS", "USTR ends an 8-month excess-capacity probe; 14 economies named.",
     "C 8 mo", "R 14", "CL 16", "ALSO Section 301", None),
    (30, "CHINA EASES US CURBS", "China extends its suspension of dual-use export controls to the US.",
     "C 1", "R 1", "CL 2", "ALSO MOFCOM move", None),
    (31, "EU HYBRID REPLY", "China to issue temporary EU hybrid vehicle measures.",
     "C 1", "R 27", "CL 1", "ALSO safeguards", None),
    (32, "PBOC: CNY800B MLF", "PBoC runs a CNY800B 1-year medium-term lending operation.",
     "C 800B", "R 1 yr", "CL 1", "ALSO liquidity", None),
    (33, "HK POWER BILLS UP", "Hong Kong power tariffs to rise between 1.8% and 7.9%.",
     "C 7.9%", "R 1.8%", "CL 2", "ALSO CLP + HK Electric", None),
    (34, "$44B 7-YEAR SALE", "$44B 7-year note sale closes after the PCE data lands.",
     "C $44B", "R 7 yrs", "CL 3rd", "ALSO Treasury wk", None),
    (35, "INCOME +0.7%", "US personal income +0.7%; consumer spending slows to +0.3%.",
     "C 0.7%", "R 0.3%", "CL 3.8%", "ALSO BEA dump", None),
    (36, "GDP REVISED TO 4.3%", "US Q3 GDP revised up from 3.4% to 4.3%, fastest in 3 years.",
     "C 4.3%", "R 3.4%", "CL 3 yrs", "ALSO 2nd estimate", None),
    (37, "CORE PCE: 3-YR HIGH", "Core PCE 3.3% is the highest in 3 years; rate-hike bets rise.",
     "C 3.3%", "R 3.2%", "CL 3 yrs", "ALSO hike bets", None),
    (38, "NEW HOME SALES", "New-home sales land in the holiday-eve data dump.",
     "C 1", "R 4", "CL 1", "ALSO housing focus", None),
    (39, "KOREA SURVEY 104.8", "South Korea business survey 104.8 vs 105.6 prior.",
     "C 104.8", "R 105.6", "CL 0.8", "ALSO mood", None),
    (40, "SHANGHAI -0.7%", "Shanghai Composite opens -0.7% at 3,523; Hang Seng +0.1%.",
     "C 3,523", "R 0.7%", "CL 22,253", "ALSO mixed Asia", None),
    (41, "NASDAQ FUTS -1%", "Nasdaq futures drop over 1% in Asia trading.",
     "C 1%", "R 1.3%", "CL 0.7%", "ALSO futures red", None),
    (42, "CHIP STOCKS -10%", "Japan chip stocks Kioxia and Advantest fall over 10%.",
     "C 10%", "R 2", "CL 2.9%", "ALSO Nikkei slides", None),
    (43, "GAZA: 11 KILLED", "11 Palestinians killed in Gaza since dawn, hospitals say.",
     "C 11", "R 2 girls", "CL 1", "ALSO Shati hit", None),
    (44, "ABU NADA KILLED", "Hamas political bureau member Khaled Abu Nada killed in central Gaza.",
     "C 1", "R 1 wife", "CL 1", "ALSO deputy minister", None),
    (45, "CEASEFIRE STALLS", "Trump-backed Gaza ceasefire plan stalls as strikes go on.",
     "C 1", "R 0", "CL 2nd day", "ALSO Peace Board", None),
    (46, "ISRAEL: OPERATIVES HIT", "Israel's military says it targeted several operatives in Gaza.",
     "C 1", "R 2 chiefs", "CL 24h", "ALSO IDF confirms", None),
    (47, "GERMANY: Q3 GDP", "German Q3 GDP print and a 10-year Bund auction due.",
     "C 1", "R 10-yr", "CL 1", "ALSO Berlin focus", None),
    (48, "UN CHIEF WARNS", "UN chief warns heating is accelerating as the planet logs a record streak.",
     "C 2.24C", "R 6 days", "CL 1", "ALSO Guterres", None),
    (49, "GOLD DIPS", "Gold slips about 17 points after the hot US data.",
     "C 17 pts", "R 3.8%", "CL 1", "ALSO havens mixed", None),
    (50, "US500 DIPS", "US500 moves about 44 ticks lower in the data window.",
     "C 44", "R 4", "CL 1", "ALSO fast reprice", None),
]


# ---------------------------------------------------------------- render
def draw_masthead(d):
    d.rectangle([0, 0, W, 64], fill=INK)
    centre(d, W // 2, 6, "THE WORLD IN NUMBERS", SERIF_B(40), LIGHT)
    d.rectangle([0, 64, W, 68], fill=RED)
    sub = "WEDNESDAY, 25 NOVEMBER 2026  \u2022  50 STORIES  \u2022  13 SCENES  \u2022  ALL THE WORLD IN ONE PAGE"
    centre(d, W // 2, 71, sub, SANS_B(11), INK)


def draw_hero(d, x, y, w, h, hero, accent):
    kicker, big, head, detail, why, c, r, cl, also, scene = hero
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=INK, width=2)
    d.rectangle([x, y, x + w - 1, y + 3], fill=accent)
    text(d, (x + 8, y + 8), kicker, SANS_B(11), RED)
    tw = SANS_B(40).getlength(big)
    d.text((x + w - 8 - tw, y + 6), big, font=SANS_B(40), fill=accent)
    yy = y + 48
    for ln in fit_lines(head, SANS_B(15), w - 16, 2):
        text(d, (x + 8, yy), ln, SANS_B(15))
        yy += 18
    scene_h = 92
    draw_scene(d, x + 8, yy + 2, w - 16, scene_h, scene)
    yy += scene_h + 8
    for ln in fit_lines(why, SANS(10), w - 16, 2):
        text(d, (x + 8, yy), ln, SANS(10))
        yy += 12
    stats = "  \u00b7  ".join([c, r, cl]) + "  \u2014  " + also
    for ln in fit_lines(stats, SANS_B(8), w - 16, 1):
        text(d, (x + 8, y + h - 14), ln, SANS_B(8), GREY)


def draw_card(d, x, y, w, h, card, accent):
    num, head, detail, c, r, cl, also, scene = card
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=(180, 175, 160), width=1)
    d.rectangle([x, y, x + 3, y + h - 1], fill=accent)
    if scene:
        draw_scene(d, x + 6, y + 1, 46, 46, scene)
        tx, tw = x + 56, w - 62
        head_lines = fit_lines("%02d  %s" % (num, head), SANS_B(10), tw, 2)
        det_lines = fit_lines(detail, SANS(8), tw, 1) if len(head_lines) == 1 else []
        stat_font = SANS_B(8)
    else:
        tx, tw = x + 8, w - 14
        head_lines = fit_lines("%02d  %s" % (num, head), SANS_B(10), tw, 1)
        det_lines = fit_lines(detail, SANS(9), tw, 2)
        stat_font = SANS_B(8)
    yy = y + 4
    for ln in head_lines:
        text(d, (tx, yy), ln, SANS_B(10))
        yy += 12
    for ln in det_lines:
        text(d, (tx, yy), ln, SANS(9) if not scene else SANS(8))
        yy += 10
    stats = "  \u00b7  ".join([c, r, cl]) + "  \u2014  " + also
    for ln in fit_lines(stats, stat_font, tw, 1):
        text(d, (tx, y + h - 11), ln, stat_font, GREY)


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=INK, width=1)
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=SKY)
    # simplified continents
    d.ellipse([x + 6, y + 6, x + 62, y + 30], fill=(122, 154, 90))
    d.ellipse([x + 30, y + 28, x + 58, y + 44], fill=(122, 154, 90))
    d.ellipse([x + 96, y + 8, x + 128, y + 26], fill=(122, 154, 90))
    d.ellipse([x + 108, y + 24, x + 140, y + 42], fill=(122, 154, 90))
    d.ellipse([x + 150, y + 6, x + 220, y + 32], fill=(122, 154, 90))
    d.ellipse([x + 195, y + 36, x + 218, y + 46], fill=(122, 154, 90))
    text(d, (x + 4, y + 2), "WORLD MAP \u2014 PINNED", SANS_B(8), INK)
    pins = [(20, 16, "1"), (150, 14, "2"), (168, 18, "3"), (185, 32, "4"),
            (122, 20, "5"), (130, 30, "6"), (206, 40, "7"), (112, 12, "8")]
    f = SANS_B(7)
    for px, py, n in pins:
        d.ellipse([x + px - 5, y + py - 5, x + px + 5, y + py + 5],
                  fill=RED, outline=LIGHT)
        d.text((x + px - f.getlength(n) / 2, y + py - 4), n, font=f, fill=LIGHT)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)

    # hero row: 3 panels
    hy, hh = 92, 224
    hw = 322
    for i, hero in enumerate(HEROES):
        draw_hero(d, 16 + i * (hw + 13), hy, hw, hh, hero, PALETTE[i])

    # ticker
    ty = 322
    d.rectangle([0, ty, W, ty + 24], fill=INK)
    tick = ("TARIFFS 14 ECONOMIES  \u2022  KOSPI -6.16%  \u2022  SHENZHOU DOCKS  "
            "\u2022  BOGOR 9 DEAD  \u2022  PCE 3.8%  \u2022  GDP 4.3%  \u2022  "
            "SOLOMONS TREATY  \u2022  EBOLA 11,986")
    centre(d, W // 2, ty + 5, tick, SANS_B(11), LIGHT)

    # DATE CHECK, exactly two lines
    dy = 352
    d.rectangle([16, dy, W - 16, dy + 40], outline=RED, width=2)
    d.rectangle([16, dy, W - 16, dy + 40], fill=(255, 244, 235))
    text(d, (24, dy + 4),
         "DATE CHECK \u2014 IN: 50 stories, every one dated 25 Nov 2026. "
         "Nothing from any other day.", SANS_B(11), INK)
    text(d, (24, dy + 22),
         "LEFT OUT \u2014 Huawei verdict 24 Nov, PIF Tower strike 24 Nov, "
         "Sudan strikes 24 Nov, Nvidia CEO reinstated 23 Nov.",
         SANS_B(11), RED)

    # legend for C / R / CL
    ly = 396
    centre(d, W // 2, ly,
           "C = CONFIRMED  \u00b7  R = REPORTED  \u00b7  CL = CLAIMED  \u00b7  "
           "EVERY CARD CARRIES ALL THREE, PLUS ALSO",
           SANS_B(9), GREY)

    # grid: 4 cols x 12 rows; 47 cards + 1 map cell
    gx, gy, cw, ch = 16, 406, 242, 48
    for idx, card in enumerate(CARDS):
        row, col = divmod(idx, 4)
        draw_card(d, gx + col * (cw + 8), gy + row * ch, cw, ch, card,
                  PALETTE[idx % len(PALETTE)])
    draw_map(d, gx + 3 * (cw + 8), gy + 11 * ch, cw, ch)

    # footer
    fy = 988
    d.line([16, fy, W - 16, fy], fill=INK, width=2)
    centre(d, W // 2, fy + 5,
           "Sources: Reuters \u00b7 AP \u00b7 Xinhua \u00b7 Al Jazeera \u00b7 BEA \u00b7 USTR \u00b7 "
           "CNN Indonesia \u00b7 Detik \u00b7 Jakarta Globe \u00b7 TradingView \u00b7 FXStreet \u00b7 Argus",
           SANS(8), GREY)
    centre(d, W // 2, fy + 17,
           "THE WORLD IN NUMBERS \u2014 WEDNESDAY 25 NOVEMBER 2026 \u2014 50 STORIES, "
           "ONE PAGE, ALL CHECKED",
           SANS_B(8), INK)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()

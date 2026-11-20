#!/usr/bin/env python3
"""Render the news-image-20261120 entry poster (1024x1024).

One image summing up Friday 20 November 2026: a banner naming the day,
one wide hero panel (Russia's mass attack on Kyiv's Dnipro bridges) and
a 2x3 grid of six panels (Cyclone Akvan's Odisha landfall, the Asian
markets crash, Italy's general strike, COP31 stalling in Antalya, the
Saudi-Houthi war dragging on, Harris meeting Macron in Paris).

Flat editorial illustration, deep teal / dark-green base with amber
accents, white bold labels. Drawn with Pillow only. No network, no
clock, no randomness: running this script twice produces byte-identical
PNG output.

Usage: python3 draw_image.py   (writes entry.png next to this file)
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W = H = 1024

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# ---- palette: deep teal / dark green base, amber accents, white text ----
INK = (8, 30, 28)         # deep teal-green, page background
TEAL = (14, 46, 42)       # panel base
TEAL2 = (22, 64, 56)      # lighter teal
TEAL3 = (34, 88, 74)      # mid teal
MOSS = (96, 120, 88)      # muted green land
AMBER = (245, 166, 35)    # amber accent
AMBER2 = (255, 184, 71)   # light amber
CREAM = (238, 245, 240)   # off-white text
WHITE = (255, 255, 255)
NIGHT = (10, 18, 34)      # night sky top
NIGHT2 = (22, 38, 52)     # night sky bottom
WATER = (8, 28, 40)       # dark water
FIRE = (255, 107, 53)
FIRE2 = (229, 87, 46)
SMOKE = (150, 160, 155)
STEEL = (96, 108, 118)
DARKBAND = (6, 20, 18)    # label band
RED = (220, 60, 50)       # market fall
GREEN = (55, 201, 120)
TAN = (196, 164, 120)
STONE = (214, 200, 170)   # palace stone
SKY = (16, 34, 44)


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, path, max_w, start, minimum=12):
    """Largest font size at which text fits max_w, never below minimum."""
    size = start
    while size > minimum:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, minimum)


def vgrad(draw, box, top, bottom):
    """Vertical gradient inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    steps = max(1, y1 - y0)
    for i in range(steps):
        t = i / steps
        c = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


def puff(draw, cx, cy, scale, color=SMOKE):
    """A flat cluster of circles read as a smoke puff."""
    blobs = [(0, 0, 24), (-20, 9, 17), (20, 11, 18), (-7, -16, 15),
             (13, -14, 14), (-28, -5, 11), (28, -4, 11)]
    for dx, dy, r in blobs:
        rr = r * scale
        draw.ellipse([cx + dx * scale - rr, cy + dy * scale - rr,
                      cx + dx * scale + rr, cy + dy * scale + rr], fill=color)


def burst(draw, cx, cy, r, color=AMBER2):
    """Starburst: radiating spokes plus a bright core (flash / explosion)."""
    for k in range(12):
        ang = k * 30
        dx = math.cos(math.radians(ang)) * r
        dy = math.sin(math.radians(ang)) * r
        draw.line([(cx, cy), (cx + dx, cy + dy)], fill=color, width=3)
    draw.ellipse([cx - r // 3, cy - r // 3, cx + r // 3, cy + r // 3],
                 fill=WHITE)
    draw.ellipse([cx - r // 6, cy - r // 6, cx + r // 6, cy + r // 6],
                 fill=color)


def figure(draw, cx, base_y, scale, suit, skin=(214, 178, 148)):
    """A faceless standing figure: head circle + shoulders, flat style."""
    hr = 11 * scale
    draw.ellipse([cx - hr, base_y - 58 * scale - hr,
                  cx + hr, base_y - 58 * scale + hr], fill=skin)
    draw.rounded_rectangle(
        [cx - 22 * scale, base_y - 44 * scale,
         cx + 22 * scale, base_y + 2 * scale],
        radius=int(10 * scale), fill=suit)


def flag_us(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(178, 34, 52))
    for i in range(7):
        if i % 2 == 1:
            draw.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7],
                           fill=WHITE)
    draw.rectangle([x, y, x + w * 0.4, y + h * 0.55], fill=(36, 54, 120))


def band(draw, x, y, w, h, label, sub):
    """Bottom band of a grid panel: bold label + small sub-label."""
    draw.rectangle([x, y, x + w, y + h], fill=DARKBAND)
    draw.rectangle([x, y, x + w, y + 4], fill=AMBER)
    pad = 12
    lf = fit(draw, label, BOLD, w - 2 * pad, 30)
    draw.text((x + pad, y + 10), label, font=lf, fill=WHITE)
    sf = fit(draw, sub, REG, w - 2 * pad, 20)
    draw.text((x + pad, y + h - 30), sub, font=sf, fill=CREAM)


# ---------------------------------------------------------------- banner
def draw_banner(draw):
    draw.rectangle([0, 0, W, 90], fill=INK)
    draw.rectangle([0, 86, W, 90], fill=AMBER)
    # small globe icon at left
    cx, cy, r = 46, 45, 27
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=AMBER2, width=3)
    draw.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=AMBER2, width=3)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=AMBER2, width=2)
    draw.line([(cx, cy - r), (cx, cy + r)], fill=AMBER2, width=2)
    draw.ellipse([cx - 13, cy - r, cx + 13, cy + r], outline=AMBER2, width=2)
    f = fit(draw, "20 NOVEMBER 2026", BOLD, 860, 62)
    draw.text((92, 16), "20 NOVEMBER 2026", font=f, fill=WHITE)


# ---------------------------------------------------------------- hero: Kyiv bridges
def draw_hero(draw):
    x0, y0, x1, y1 = 0, 90, W, 410
    vgrad(draw, (x0, y0, x1, y1), NIGHT, NIGHT2)
    # stars
    for sx, sy in [(70, 120), (150, 150), (250, 112), (420, 128), (560, 110),
                   (700, 140), (820, 112), (940, 150), (980, 200), (60, 210),
                   (880, 210), (480, 180), (330, 190), (760, 190)]:
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=CREAM)
    # missile trails arcing across the sky, kept below the label block
    draw.line([(60, 285), (220, 245), (380, 238), (520, 248)],
              fill=AMBER2, width=4, joint="curve")
    draw.ellipse([512, 240, 528, 256], fill=FIRE)
    draw.ellipse([516, 244, 524, 252], fill=AMBER2)
    draw.line([(1024, 270), (880, 232), (760, 222), (660, 232)],
              fill=AMBER2, width=4, joint="curve")
    draw.ellipse([652, 224, 668, 240], fill=FIRE)
    # air-defence flash, top right
    burst(draw, 900, 130, 34)
    # river, lower part
    draw.rectangle([x0, 300, x1, y1], fill=WATER)
    for wy in (318, 348, 382, 400):
        draw.line([(0, wy), (W, wy)], fill=(20, 52, 66), width=2)
    # three bridges across the river, at staggered heights
    bridges = [
        (296, [(180, 252), (700, 252)]),
        (336, [(340, 292), (850, 292)]),
        (368, [(120, 324), (540, 324), (900, 324)]),
    ]
    for deck_y, towers in bridges:
        draw.rectangle([0, deck_y, W, deck_y + 8], fill=STEEL)
        for tx, top in towers:
            draw.rectangle([tx, top, tx + 10, deck_y], fill=STEEL)
            draw.rectangle([tx - 5, top - 8, tx + 15, top], fill=AMBER)
            draw.line([(tx + 5, top), (tx - 90, deck_y)], fill=STEEL, width=2)
            draw.line([(tx + 5, top), (tx + 100, deck_y)], fill=STEEL, width=2)
    # smoke and fire over the middle bridge, where a span is hit
    puff(draw, 560, 300, 0.8)
    draw.polygon([(520, 336), (540, 312), (556, 336)], fill=FIRE)
    draw.polygon([(540, 336), (552, 322), (564, 336)], fill=AMBER2)
    puff(draw, 180, 262, 0.6, color=(120, 128, 134))
    # label top-left
    lf = fit(draw, "KYIV BRIDGES BLITZED", BOLD, 640, 44)
    draw.text((28, 108), "KYIV BRIDGES BLITZED", font=lf, fill=WHITE)
    draw.rectangle([28, 160, 28 + 210, 166], fill=AMBER)
    sf = fit(draw, "110 missiles \u2014 Poland scrambles jets", REG, 640, 25)
    draw.text((28, 178), "110 missiles \u2014 Poland scrambles jets",
              font=sf, fill=CREAM)


# ---------------------------------------------------------------- grid panels
def panel_akvan(draw, x, y, w, h):
    # sea
    vgrad(draw, (x, y, x + w, y + h), (16, 46, 58), (10, 30, 44))
    # land (Odisha coast) on the left
    draw.polygon([(x, y), (x + 96, y), (x + 78, y + 60), (x + 92, y + 120),
                  (x + 66, y + 180), (x + 84, y + h - 82), (x, y + h - 82)],
                 fill=MOSS)
    draw.polygon([(x, y), (x + 96, y), (x + 78, y + 60), (x + 92, y + 120),
                  (x + 66, y + 180), (x + 84, y + h - 82), (x, y + h - 82)],
                 outline=AMBER2, width=2)
    # small shelters on the coast
    for sx, sy in [(x + 28, y + 150), (x + 44, y + 176), (x + 20, y + 96)]:
        draw.polygon([(sx, sy), (sx + 11, sy - 12), (sx + 22, sy)],
                     fill=CREAM)
    # cyclone spiral over the bay, centre right
    cx, cy = x + 215, y + 105
    for k in range(3):
        r = 22 + k * 18
        start = 40 + k * 120
        draw.arc([cx - r, cy - r, cx + r, cy + r], start, start + 250,
                 fill=CREAM if k % 2 == 0 else AMBER2, width=5)
    draw.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=NIGHT)
    draw.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], outline=AMBER2, width=3)
    # rain bands sweeping out from the spiral
    for (bx0, by0, bx1, by1) in [(cx + 60, cy - 40, cx + 110, cy - 70),
                                 (cx + 70, cy + 30, cx + 118, cy + 8),
                                 (cx - 30, cy + 70, cx + 20, cy + 96)]:
        draw.line([(bx0, by0), (bx1, by1)], fill=CREAM, width=3)
    band(draw, x, y + h - 82, w, 82,
         "CYCLONE AKVAN LANDS", "Odisha hit \u2014 300,000 evacuated")


def panel_markets(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(14, 26, 38))
    # AI chip motif, top-right
    cx, cy, s = x + w - 72, y + 58, 40
    draw.rounded_rectangle([cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2],
                           radius=8, fill=TEAL2, outline=AMBER, width=3)
    draw.rounded_rectangle([cx - 12, cy - 12, cx + 12, cy + 12],
                           radius=4, fill=AMBER)
    for k in range(3):
        off = -14 + k * 14
        draw.line([(cx + off, cy - s // 2 - 9), (cx + off, cy - s // 2)],
                  fill=AMBER, width=3)
        draw.line([(cx + off, cy + s // 2), (cx + off, cy + s // 2 + 9)],
                  fill=AMBER, width=3)
    # skyline silhouette along the bottom of the art area
    for bx0, by0, bx1 in [(x + 10, y + 150, x + 58), (x + 66, y + 128, x + 104),
                          (x + 112, y + 162, x + 158), (x + 166, y + 138, x + 210),
                          (x + 218, y + 168, x + 262), (x + 270, y + 146, x + 320)]:
        draw.rectangle([bx0, by0, bx1, y + h - 82], fill=(24, 40, 54))
        for wy in range(by0 + 10, y + h - 92, 16):
            for wx in range(bx0 + 6, bx1 - 6, 12):
                if (wx * 3 + wy * 5) % 4 == 0:
                    draw.rectangle([wx, wy, wx + 4, wy + 6], fill=AMBER2)
    # steep falling chart arrow
    pts = [(x + 24, y + 34), (x + 90, y + 52), (x + 150, y + 48),
           (x + 210, y + 88), (x + 272, y + 128)]
    draw.line(pts, fill=RED, width=5, joint="curve")
    draw.polygon([(x + 272, y + 128), (x + 246, y + 118), (x + 260, y + 148)],
                 fill=RED)
    # big figure
    bf = fit(draw, "\u22124.8%", BOLD, w - 40, 56)
    draw.text((x + 20, y + 148), "\u22124.8%", font=bf, fill=AMBER2)
    band(draw, x, y + h - 82, w, 82,
         "ASIA STOCKS CRASH", "Nikkei \u22124.8% \u2014 AI fears spread")


def panel_italy(draw, x, y, w, h):
    vgrad(draw, (x, y, x + w, y + h), (20, 44, 48), (12, 28, 34))
    # city square: buildings and a tower at the back
    for bx0, by0, bx1 in [(x + 8, y + 96, x + 78), (x + 86, y + 70, x + 150),
                          (x + 252, y + 88, x + 322)]:
        draw.rectangle([bx0, by0, bx1, y + h - 82], fill=(26, 52, 54))
        for wy in range(by0 + 12, y + h - 92, 18):
            for wx in range(bx0 + 8, bx1 - 8, 14):
                if (wx + wy) % 3 == 0:
                    draw.rectangle([wx, wy, wx + 5, wy + 7], fill=AMBER2)
    # Italian flag on a pole, left (green-white-red vertical bands)
    draw.line([(x + 30, y + 40), (x + 30, y + 96)], fill=CREAM, width=3)
    draw.rectangle([x + 30, y + 44, x + 44, y + 70], fill=(0, 146, 70))
    draw.rectangle([x + 44, y + 44, x + 58, y + 70], fill=WHITE)
    draw.rectangle([x + 58, y + 44, x + 72, y + 70], fill=(206, 43, 55))
    # crowd of demonstrators with placards
    suits = [(30, 44, 60), (150, 90, 90), (70, 120, 100), (200, 60, 70),
             (110, 160, 130), (40, 180, 150)]
    for (px, ph), suit in zip(
            [(x + 60, 1.0), (x + 108, 0.94), (x + 156, 1.05),
             (x + 204, 0.96), (x + 252, 1.02), (x + 296, 0.9)], suits):
        figure(draw, px, y + h - 82, ph, suit)
    # placards on sticks above the crowd
    draw.rectangle([x + 84, y + 92, x + 148, y + 118], fill=AMBER)
    draw.line([(x + 116, y + 118), (x + 116, y + 156)], fill=AMBER2, width=3)
    draw.rectangle([x + 176, y + 84, x + 240, y + 108], fill=CREAM)
    draw.line([(x + 208, y + 108), (x + 208, y + 156)], fill=AMBER2, width=3)
    draw.rectangle([x + 248, y + 96, x + 308, y + 120], fill=(206, 43, 55))
    draw.line([(x + 278, y + 120), (x + 278, y + 158)], fill=AMBER2, width=3)
    band(draw, x, y + h - 82, w, 82,
         "ITALY STRIKES", "General strike \u2014 100+ cities march")


def panel_cop31(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(18, 38, 50))
    # globe, top-centre
    cx, cy, r = x + 120, y + 72, 46
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(38, 96, 120))
    draw.ellipse([cx - 18, cy - 26, cx + 6, cy - 4], fill=MOSS)
    draw.ellipse([cx - 4, cy + 8, cx + 24, cy + 28], fill=MOSS)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=AMBER2, width=3)
    draw.arc([cx - r, cy - r, cx + r, cy + r], 300, 60, fill=AMBER2, width=2)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=AMBER2, width=2)
    draw.ellipse([cx - 16, cy - r, cx + 16, cy + r], outline=AMBER2, width=2)
    # oil drop with a red cross-out, right of the globe
    ox, oy = x + 238, y + 44
    draw.polygon([(ox, oy), (ox - 20, oy + 30), (ox - 14, oy + 46),
                  (ox + 14, oy + 46), (ox + 20, oy + 30)], fill=(20, 20, 24))
    draw.ellipse([ox - 30, oy + 12, ox + 30, oy + 72], outline=RED, width=5)
    draw.line([(ox - 22, oy + 20), (ox + 22, oy + 64)], fill=RED, width=5)
    # negotiators around a long table
    draw.rectangle([x + 30, y + 168, x + w - 30, y + 186], fill=(122, 82, 42))
    draw.rectangle([x + 30, y + 168, x + w - 30, y + 174], fill=AMBER)
    for (px, suit) in [(x + 70, (36, 54, 120)), (x + 130, (150, 30, 30)),
                        (x + 200, (52, 52, 64)), (x + 262, (40, 90, 60))]:
        figure(draw, px, y + 172, 0.9, suit)
    band(draw, x, y + h - 82, w, 82,
         "COP31 STALLS", "Fossil fuels cut from draft")


def panel_houthi(draw, x, y, w, h):
    vgrad(draw, (x, y, x + w, y + h), (10, 14, 30), (30, 22, 52))
    # stars
    for sx, sy in [(26, 20), (70, 44), (140, 16), (210, 36), (290, 22),
                   (48, 72), (250, 66)]:
        draw.ellipse([x + sx - 2, y + sy - 2, x + sx + 2, y + sy + 2],
                     fill=CREAM)
    # missile trail arcing across the sky
    draw.line([(x + 16, y + 92), (x + 90, y + 58), (x + 170, y + 42),
               (x + 236, y + 46)], fill=AMBER2, width=4, joint="curve")
    draw.ellipse([x + 228, y + 38, x + 244, y + 54], fill=FIRE)
    draw.ellipse([x + 232, y + 42, x + 240, y + 50], fill=AMBER2)
    # interception flash, upper right
    burst(draw, x + 272, y + 96, 26)
    # desert city skyline, one tall tower centre
    for bx0, by0, bx1 in [(x + 8, y + 150, x + 58), (x + 66, y + 176, x + 112),
                          (x + 268, y + 168, x + 322)]:
        draw.rectangle([bx0, by0, bx1, y + h - 82], fill=(20, 16, 44))
        for wy in range(by0 + 10, y + h - 92, 16):
            for wx in range(bx0 + 6, bx1 - 6, 12):
                if (wx * 3 + wy * 5) % 4 == 0:
                    draw.rectangle([wx, wy, wx + 4, wy + 6], fill=AMBER2)
    tx0, tx1 = x + 138, x + 218
    draw.rectangle([tx0, y + 60, tx1, y + h - 82], fill=(52, 68, 128))
    draw.rectangle([tx0, y + 60, tx1, y + 66], fill=AMBER)
    for wy in range(y + 76, y + h - 92, 14):
        for wx in range(tx0 + 8, tx1 - 8, 14):
            if (wx + wy) % 3 == 0:
                draw.rectangle([wx, wy, wx + 5, wy + 7], fill=AMBER2)
    # smoke at the tower top, from the intercepted missile's debris
    puff(draw, x + 178, y + 66, 0.5, color=(150, 146, 168))
    band(draw, x, y + h - 82, w, 82,
         "SAUDI WAR DRAGS ON", "Missile downed \u2014 Sana'a bombed")


def panel_paris(draw, x, y, w, h):
    vgrad(draw, (x, y, x + w, y + h), (58, 48, 62), (34, 30, 44))
    # palace facade: pediment + columns
    bx0, bx1 = x + 66, x + w - 66
    by = y + 62
    draw.polygon([(bx0 - 8, by), ((bx0 + bx1) // 2, by - 30), (bx1 + 8, by)],
                 fill=STONE)
    draw.ellipse([((bx0 + bx1) // 2) - 7, by - 24, ((bx0 + bx1) // 2) + 7,
                  by - 10], fill=AMBER)
    for cx in range(bx0 + 14, bx1 - 8, 40):
        draw.rectangle([cx, by + 6, cx + 11, y + 150], fill=STONE)
    draw.rectangle([bx0 - 8, y + 150, bx1 + 8, y + 160], fill=STONE)
    # flags flanking the facade
    draw.line([(x + 34, y + 48), (x + 34, y + 108)], fill=CREAM, width=3)
    draw.rectangle([x + 34, y + 52, x + 48, y + 76], fill=(0, 85, 164))
    draw.rectangle([x + 48, y + 52, x + 62, y + 76], fill=WHITE)
    draw.rectangle([x + 62, y + 52, x + 76, y + 76], fill=(239, 65, 53))
    draw.line([(x + w - 34, y + 48), (x + w - 34, y + 108)], fill=CREAM, width=3)
    flag_us(draw, x + w - 76, y + 52, 42, 24)
    # two figures shaking hands in front of the steps
    figure(draw, x + 138, y + 172, 1.0, (36, 54, 120), skin=(214, 178, 148))
    figure(draw, x + 192, y + 172, 1.0, (52, 52, 64), skin=(198, 158, 128))
    draw.line([(x + 158, y + 140), (x + 172, y + 140)], fill=AMBER2, width=4)
    draw.ellipse([x + 161, y + 134, x + 169, y + 142], fill=AMBER2)
    band(draw, x, y + h - 82, w, 82,
         "HARRIS MEETS MACRON", "Courtesy call in Paris")


# ---------------------------------------------------------------- compose
def main():
    img = Image.new("RGB", (W, H), INK)
    draw = ImageDraw.Draw(img)

    draw_banner(draw)
    draw_hero(draw)

    grid_y = 422
    col_w, row_h, gap = 330, 292, 12
    panels = [panel_akvan, panel_markets, panel_italy,
              panel_cop31, panel_houthi, panel_paris]
    for i, fn in enumerate(panels):
        row, col = divmod(i, 3)
        px = 5 + col * (col_w + gap)
        py = grid_y + row * (row_h + gap)
        # panel frame
        draw.rounded_rectangle([px - 2, py - 2, px + col_w + 2, py + row_h + 2],
                               radius=8, outline=TEAL3, width=2)
        fn(draw, px, py, col_w, row_h)

    img.save(OUT, format="PNG")
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()

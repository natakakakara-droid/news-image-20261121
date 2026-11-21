#!/usr/bin/env python3
"""Render the news-image-20261121 entry: a newspaper front page summing up
Saturday 21 November 2026 in five verified stories.

Run:  python3 render.py            -> writes entry.png (1024x1024) here.
The grader entrypoint is main.py, which only copies entry.png to the output
directory (stdlib only, no fonts needed at grade time). This renderer runs
on the build machine only, using DejaVu fonts from /usr/share/fonts.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

CREAM = (247, 242, 231)
INK = (28, 26, 23)
RED = (166, 30, 30)
GRAY = (90, 86, 78)
BLUE = (31, 78, 121)
TEAL = (14, 124, 123)
GREEN = (46, 125, 50)
GOLD = (184, 134, 11)
LIGHT = (233, 226, 210)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def hrule(draw, x0, x1, y, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- icons
def icon_scales(d, cx, cy, s):
    """Scales of justice, centred at (cx, cy), overall size s."""
    gold = (176, 124, 24)
    # base + post
    d.line([(cx - s * 0.28, cy + s * 0.42), (cx + s * 0.28, cy + s * 0.42)],
           fill=INK, width=6)
    d.line([(cx, cy - s * 0.42), (cx, cy + s * 0.42)], fill=INK, width=6)
    d.ellipse([cx - 10, cy - s * 0.48, cx + 10, cy - s * 0.48 + 20],
              fill=gold, outline=INK, width=2)
    # beam
    d.line([(cx - s * 0.42, cy - s * 0.30), (cx + s * 0.42, cy - s * 0.30)],
           fill=gold, width=7)
    for sx in (-1, 1):
        px = cx + sx * s * 0.42
        d.line([(px, cy - s * 0.30), (px - s * 0.10, cy + s * 0.10)],
               fill=INK, width=3)
        d.line([(px, cy - s * 0.30), (px + s * 0.10, cy + s * 0.10)],
               fill=INK, width=3)
        d.line([(px - s * 0.10, cy + s * 0.10), (px + s * 0.10, cy + s * 0.10)],
               fill=INK, width=3)
        # pan: shallow bowl
        d.pieslice([px - s * 0.13, cy + s * 0.02, px + s * 0.13, cy + s * 0.24],
                   0, 180, fill=gold, outline=INK, width=2)


def icon_bridge(d, x, y, w, h):
    """River bridge with a blast above it, inside box (x, y, w, h)."""
    deck_y = y + h * 0.62
    d.line([(x, deck_y), (x + w, deck_y)], fill=INK, width=5)
    # towers
    for tx in (x + w * 0.22, x + w * 0.72):
        d.rectangle([tx - 5, y + h * 0.18, tx + 5, deck_y], fill=INK)
    # arches
    d.arc([x + w * 0.02, deck_y - h * 0.34, x + w * 0.48, deck_y + h * 0.10],
          180, 360, fill=BLUE, width=5)
    d.arc([x + w * 0.52, deck_y - h * 0.34, x + w * 0.98, deck_y + h * 0.10],
          180, 360, fill=BLUE, width=5)
    # water
    for i, wy in enumerate((deck_y + 12, deck_y + 22)):
        d.line([(x + 6, wy), (x + w - 6, wy)], fill=BLUE, width=2)
    # blast starburst above centre
    bx, by = x + w * 0.5, y + h * 0.16
    pts = []
    for i in range(16):
        ang = i * math.pi / 8
        r = 26 if i % 2 == 0 else 11
        pts.append((bx + r * math.cos(ang), by + r * math.sin(ang)))
    d.polygon(pts, fill=(232, 126, 32), outline=RED, width=2)
    d.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=RED)


def icon_cyclone(d, x, y, w, h):
    """Spiral storm, inside box (x, y, w, h)."""
    cx, cy = x + w / 2, y + h / 2
    pts = []
    for i in range(220):
        t = i / 220.0 * 4.6 * math.pi
        r = 4 + (min(w, h) * 0.42 - 4) * (i / 220.0)
        pts.append((cx + r * math.cos(t), cy + r * math.sin(t) * 0.92))
    d.line(pts, fill=TEAL, width=6, joint="curve")
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=CREAM, outline=TEAL, width=3)
    # rain slashes
    for dx, dy in ((-38, -30), (36, -34), (-42, 26), (40, 28)):
        d.line([(cx + dx, cy + dy), (cx + dx - 8, cy + dy + 16)],
               fill=BLUE, width=3)


def icon_globe(d, x, y, w, h):
    """Globe with a leaf, inside box (x, y, w, h)."""
    cx, cy = x + w / 2, y + h / 2 - 6
    r = min(w, h) * 0.40
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(214, 232, 240),
              outline=BLUE, width=4)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
              outline=BLUE, width=2)
    d.line([(cx - r, cy), (cx + r, cy)], fill=BLUE, width=2)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 0, 360,
          fill=BLUE, width=2)
    # leaf
    lx, ly = cx + r * 0.55, cy + r * 0.55
    d.pieslice([lx - 26, ly - 26, lx + 26, ly + 26], 300, 60,
               fill=GREEN, outline=INK, width=2)
    d.line([(lx - 20, ly + 14), (lx + 18, ly - 16)], fill=CREAM, width=3)


def icon_deal(d, x, y, w, h):
    """EU stars circle + Big Ben tower, inside box (x, y, w, h)."""
    # EU mini-flag
    fx, fy, fs = x + 4, y + h * 0.12, w * 0.44
    d.rounded_rectangle([fx, fy, fx + fs, fy + fs], radius=8,
                        fill=(0, 51, 153))
    ccx, ccy = fx + fs / 2, fy + fs / 2
    for i in range(12):
        ang = -math.pi / 2 + i * math.pi / 6
        sx, sy = ccx + fs * 0.32 * math.cos(ang), ccy + fs * 0.32 * math.sin(ang)
        d.ellipse([sx - 2.5, sy - 2.5, sx + 2.5, sy + 2.5], fill=(255, 204, 0))
    # Big Ben
    bx = x + w * 0.58
    bw = w * 0.34
    top = y + h * 0.10
    d.rectangle([bx, top + bw * 0.55, bx + bw, y + h * 0.92], fill=INK)
    d.polygon([(bx - 3, top + bw * 0.55), (bx + bw / 2, top),
               (bx + bw + 3, top + bw * 0.55)], fill=INK)
    d.ellipse([bx + bw * 0.18, top + bw * 0.62, bx + bw * 0.82,
               top + bw * 0.62 + bw * 0.64], fill=CREAM, outline=GOLD, width=2)
    d.line([(bx + bw / 2, top + bw * 0.70), (bx + bw / 2, top + bw * 0.92)],
           fill=INK, width=2)
    d.line([(bx + bw / 2, top + bw * 0.94), (bx + bw * 0.72, top + bw * 0.78)],
           fill=INK, width=2)


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    # newspaper border
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=3)
    d.rectangle([20, 20, W - 21, H - 21], outline=INK, width=1)

    # ---- masthead
    f_mast = font(SERIF, 56)
    d.text((W / 2, 52), "THE WORLD IN ONE DAY", font=f_mast, fill=INK,
           anchor="ma")
    hrule(d, 32, W - 32, 122, 3)
    f_date = font(SANS_B, 26)
    d.text((W / 2, 134), "SATURDAY, 21 NOVEMBER 2026", font=f_date,
           fill=RED, anchor="ma")
    hrule(d, 32, W - 32, 176, 1)

    # ---- lead story: ICJ Myanmar verdict
    lx, lw = 40, 600
    f_kick = font(SANS_B, 20)
    d.text((lx, 196), "THE HAGUE  —  WORLD COURT", font=f_kick, fill=RED)
    f_head = font(SERIF, 47)
    y = text_block(d, lx, 226,
                   wrap(d, "MYANMAR GUILTY OF GENOCIDE", f_head, lw),
                   f_head, INK, 54)
    f_deck = font(SANS, 22)
    y = text_block(d, lx, y + 10,
                   wrap(d, "UN court finds a state responsible for genocide "
                           "for the first time — over the Rohingya in "
                           "Rakhine.", f_deck, lw),
                   f_deck, INK, 29)
    f_sub = font(SANS, 19)
    text_block(d, lx, y + 8,
               wrap(d, "Mass killings, rape and the burning of hundreds of "
                       "villages in 2016–18. Myanmar calls the ruling "
                       "“unfair”.", f_sub, lw),
               f_sub, GRAY, 25)
    icon_scales(d, 830, 330, 190)
    d.text((830, 448), "JUSTICE AT THE HAGUE", font=font(SANS_B, 15),
           fill=GRAY, anchor="ma")

    hrule(d, 32, W - 32, 494, 2)

    # ---- rows of two stories
    def story(x, y, w, kicker, color, headline, deck, icon_fn):
        d.text((x, y), kicker, font=font(SANS_B, 18), fill=color)
        f_h = font(SERIF, 29)
        hy = text_block(d, x, y + 28,
                        wrap(d, headline, f_h, w - 108), f_h, INK, 35)
        icon_fn(d, x + w - 100, y + 24, 100, 96)
        f_d = font(SANS, 19)
        text_block(d, x, max(hy, y + 126) + 2,
                   wrap(d, deck, f_d, w), f_d, INK, 25)

    story(40, 514, 452, "UKRAINE  —  WAR", BLUE,
          "RUSSIA HITS THREE KYIV BRIDGES",
          "400+ drones and 110 missiles in one of the war’s biggest "
          "barrages. At least nine killed; power cut across the capital.",
          icon_bridge)
    d.line([(512, 514), (512, 722)], fill=INK, width=1)
    story(544, 514, 440, "INDIA  —  WEATHER", TEAL,
          "CYCLONE AKVAN STRIKES ODISHA",
          "Storm makes landfall near Gopalpur with 90 km/h gusts. More "
          "than 300,000 people moved to shelters.",
          icon_cyclone)

    hrule(d, 32, W - 32, 740, 1)

    story(40, 758, 452, "ANTALYA  —  CLIMATE", GREEN,
          "COP31 DRAFT DROPS FOSSIL FUELS",
          "Final text omits coal, oil and gas; talks spill into overtime "
          "as the 1.5°C limit nears breach.",
          icon_globe)
    d.line([(512, 758), (512, 956)], fill=INK, width=1)
    story(544, 758, 440, "BRUSSELS  —  EUROPE", (123, 90, 20),
          "UK AND EU SEAL BREXIT RESET",
          "Food, carbon and youth-mobility deals: 100,000 young people a "
          "year may live and work across the Channel.",
          icon_deal)

    # ---- footer
    hrule(d, 32, W - 32, 972, 1)
    d.text((W / 2, 980), "FIVE STORIES. ONE DAY. — THE WORLD IN ONE DAY",
           font=font(SANS_B, 16), fill=GRAY, anchor="ma")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()

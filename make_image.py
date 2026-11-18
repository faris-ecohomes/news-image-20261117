#!/usr/bin/env python3
"""Draw the entry image: one front-page poster summing up the world news of
Monday 17 November 2026. Pure Pillow vector shapes + DejaVu type; no
photographs, no logos. Output: entry.png (1024x1024) beside this file.

Stories (all reported on 17 Nov 2026, cross-checked across wires):
 1. Trump, Xi and Putin to meet in Shenzhen on Thursday, a first three-way
    summit on the sidelines of the APEC gathering China is hosting.
 2. Ukraine strikes the Kerch Bridge with drones and missiles, closing it;
    Russia answers with a major ballistic attack on Kyiv.
 3. Iranian drones hit the US radar site in Bahrain for a third time in
    days, as the USS Theodore Roosevelt carrier group arrives.
 4. Washington tightens AI chip rules on China: new export licences for
    advanced chips and servers in overseas data centres.
 5. Quad unveils critical-minerals and defence pacts in Manila; Modi joins
    the ASEAN-India summit.
 6. WHO validates Eritrea's elimination of trachoma as a public-health
    problem after a two-decade campaign.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)
INK = (20, 24, 34)
NAVY = (18, 32, 64)
RED = (178, 34, 44)
WHITE = (255, 255, 255)
GREY = (90, 96, 110)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = f"{FONT_DIR}/DejaVuSans-Bold.ttf"
REG = f"{FONT_DIR}/DejaVuSans.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def wrap(text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = f"{cur} {w}".strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(x, y, lines, font, fill, leading):
    for line in lines:
        d.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 150], fill=NAVY)
d.text((40, 16), "THE WORLD IN ONE DAY", font=F(BOLD, 28), fill=(150, 178, 235))
date_font = F(BOLD, 49)
while d.textlength("MONDAY, NOVEMBER 17, 2026", font=date_font) > W - 76:
    date_font = F(BOLD, date_font.size - 2)
d.text((38, 54), "MONDAY, NOVEMBER 17, 2026", font=date_font, fill=WHITE)
d.rectangle([0, 150, W, 161], fill=RED)
d.text((40, 167), "Six stories that defined the day - summit, bridge, drones, chips, minerals, health",
       font=F(REG, 24), fill=GREY)

# ---------------------------------------------------------------- icons
# Each icon draws inside a box roughly 96 wide x 104 tall at (x, y).

def icon_flags(x, y, c):
    # Three summit flags on poles of rising height.
    for i, (px, ph, fc) in enumerate([(x + 10, 62, RED), (x + 44, 84, c), (x + 78, 62, NAVY)]):
        top = y + 96 - ph
        d.line([px, y + 96, px, top], fill=INK, width=4)
        d.polygon([(px, top), (px + 26, top + 10), (px, top + 20)], fill=fc)
    d.line([x + 2, y + 98, x + 94, y + 98], fill=c, width=4)


def icon_bridge(x, y, c):
    d.rectangle([x, y + 50, x + 34, y + 58], fill=c)
    d.rectangle([x + 62, y + 50, x + 96, y + 58], fill=c)
    d.rectangle([x + 8, y + 16, x + 15, y + 58], fill=c)
    d.rectangle([x + 81, y + 16, x + 88, y + 58], fill=c)
    d.line([x + 11, y + 18, x + 34, y + 50], fill=c, width=3)
    d.line([x + 85, y + 18, x + 62, y + 50], fill=c, width=3)
    d.line([x + 11, y + 18, x + 2, y + 50], fill=c, width=3)
    d.line([x + 85, y + 18, x + 94, y + 50], fill=c, width=3)
    d.line([x + 41, y + 60, x + 53, y + 74], fill=RED, width=5)  # fallen span
    for i in range(3):
        d.arc([x + 4 + i * 32, y + 80, x + 30 + i * 32, y + 96], 0, 180, fill=c, width=3)


def icon_drone(x, y, c):
    for cx, cy in [(x + 18, y + 18), (x + 78, y + 18), (x + 18, y + 74), (x + 78, y + 74)]:
        d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], outline=c, width=4)
    d.line([x + 27, y + 27, x + 69, y + 65], fill=c, width=6)
    d.line([x + 69, y + 27, x + 27, y + 65], fill=c, width=6)
    d.rectangle([x + 36, y + 34, x + 60, y + 58], fill=c)
    for r in (14, 24):
        d.arc([x + 70, y + 70, x + 70 + r, y + 70 + r], 270, 360, fill=RED, width=4)


def icon_chip(x, y, c):
    d.rectangle([x + 20, y + 18, x + 68, y + 66], outline=c, width=6)
    d.rectangle([x + 34, y + 32, x + 54, y + 52], fill=c)
    for i in range(3):
        p = x + 30 + i * 14
        d.line([p, y + 2, p, y + 18], fill=c, width=5)
        d.line([p, y + 66, p, y + 82], fill=c, width=5)
        p2 = y + 28 + i * 14
        d.line([x + 4, p2, x + 20, p2], fill=c, width=5)
        d.line([x + 68, p2, x + 84, p2], fill=c, width=5)
    d.line([x + 66, y + 88, x + 88, y + 66], fill=RED, width=6)
    d.polygon([(x + 88, y + 66), (x + 75, y + 66), (x + 88, y + 79)], fill=RED)


def icon_gem(x, y, c):
    # A cut gemstone for the critical-minerals pacts.
    d.polygon([(x + 14, y + 30), (x + 82, y + 30), (x + 48, y + 88)], fill=c)
    d.polygon([(x + 14, y + 30), (x + 30, y + 12), (x + 66, y + 12), (x + 82, y + 30)], outline=c, width=5)
    d.line([x + 30, y + 12, x + 36, y + 30], fill=c, width=3)
    d.line([x + 66, y + 12, x + 60, y + 30], fill=c, width=3)
    d.line([x + 36, y + 30, x + 48, y + 88], fill=WHITE, width=3)
    d.line([x + 60, y + 30, x + 48, y + 88], fill=WHITE, width=3)
    d.line([x + 8, y + 98, x + 88, y + 98], fill=RED, width=4)


def icon_eye(x, y, c):
    # An eye, for the blinding disease Eritrea has eliminated.
    d.arc([x + 2, y + 18, x + 94, y + 74], 180, 360, fill=c, width=6)
    d.arc([x + 2, y + 18, x + 94, y + 74], 0, 180, fill=c, width=6)
    d.ellipse([x + 34, y + 32, x + 62, y + 60], fill=c)
    d.ellipse([x + 43, y + 41, x + 53, y + 51], fill=WHITE)
    d.line([x + 60, y + 84, x + 70, y + 94], fill=RED, width=6)
    d.line([x + 70, y + 94, x + 90, y + 72], fill=RED, width=6)


# ---------------------------------------------------------------- cards
CARDS = [
    ("SUMMIT - SHENZHEN", (24, 92, 140), icon_flags,
     "TRUMP, XI AND PUTIN TO MEET IN SHENZHEN",
     "The three leaders are set for a first three-way summit on Thursday on the sidelines of the APEC gathering China is hosting."),
    ("EUROPE - WAR", (150, 44, 44), icon_bridge,
     "UKRAINE STRIKES THE KERCH BRIDGE",
     "Ukrainian drones and missiles hit the bridge linking Russia to Crimea, closing it; Russia answers with a major ballistic attack on Kyiv."),
    ("MIDDLE EAST", (146, 96, 20), icon_drone,
     "IRANIAN DRONES HIT U.S. RADAR IN BAHRAIN AGAIN",
     "A third drone attack in days targets the U.S. radar site as the USS Theodore Roosevelt carrier group arrives in the region."),
    ("BUSINESS - AI CHIPS", (30, 110, 76), icon_chip,
     "WASHINGTON TIGHTENS AI CHIP RULES ON CHINA",
     "New export licences target advanced AI chips and servers in overseas data centres used to give Chinese firms indirect access."),
    ("ASIA - DIPLOMACY", (0, 105, 110), icon_gem,
     "QUAD UNVEILS MINERALS PACTS IN MANILA",
     "The U.S., Japan, India and Australia announce critical-minerals and defence deals; Modi joins the ASEAN\u2013India summit."),
    ("HEALTH - AFRICA", (110, 60, 150), icon_eye,
     "ERITREA ELIMINATES TRACHOMA, WHO CONFIRMS",
     "The WHO validates Eritrea's elimination of trachoma as a public-health problem after a two-decade campaign against the blinding disease."),
]

TOP = 206
CARD_H = 246
GAP = 12
MARGIN = 28
COL_W = (W - 2 * MARGIN - GAP) // 2

for i, (tag, colour, icon, head, sub) in enumerate(CARDS):
    col, row = i % 2, i // 2
    x0 = MARGIN + col * (COL_W + GAP)
    y0 = TOP + row * (CARD_H + GAP)
    x1, y1 = x0 + COL_W, y0 + CARD_H
    d.rectangle([x0, y0, x1, y1], fill=WHITE, outline=(205, 198, 182), width=2)
    d.rectangle([x0, y0, x1, y0 + 42], fill=colour)
    d.text((x0 + 16, y0 + 8), tag, font=F(BOLD, 25), fill=WHITE)

    head_w = x1 - (x0 + 16) - 14
    # Headline: largest bold size that wraps to at most two lines.
    head_lines = None
    for hs in (27, 26, 25, 24, 23, 22):
        lines = wrap(head, F(BOLD, hs), head_w)
        if len(lines) <= 2:
            head_lines, head_size = lines, hs
            break
    assert head_lines, f"card {i} headline does not fit"
    hy = draw_lines(x0 + 16, y0 + 52, head_lines, F(BOLD, head_size), INK, head_size + 4)

    # Summary sits right of the icon, below the headline.
    sx = x0 + 124
    sub_w = x1 - sx - 14
    sy = hy + 8
    sub_lines = None
    for ss in (20, 19, 18, 17):
        lines = wrap(sub, F(REG, ss), sub_w)
        if sy + len(lines) * (ss + 3) <= y1 - 8:
            sub_lines, sub_size = lines, ss
            break
    assert sub_lines, f"card {i} summary does not fit"
    icon(x0 + 14, sy + 2, colour)
    draw_lines(sx, sy, sub_lines, F(REG, sub_size), GREY, sub_size + 3)

# ---------------------------------------------------------------- footer
fy = TOP + 3 * CARD_H + 2 * GAP + 14
d.rectangle([0, fy, W, fy + 4], fill=RED)
d.text((40, fy + 12), "Reported on Monday 17 November 2026 - compiled from wire reports worldwide",
       font=F(REG, 21), fill=GREY)

out = Path(__file__).with_name("entry.png")
img.save(out, optimize=True)
print(out, img.size, out.stat().st_size)

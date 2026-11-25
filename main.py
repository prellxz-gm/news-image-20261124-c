#!/usr/bin/env python3
"""news-image-20261124 variant C — 'Timeline + Proof'.

Draws a 1024x1024 summary of Tuesday 24 November 2026 world news:
a date banner, a hero block for the Strait of Hormuz story, and a
chronological timeline of the other eleven stories. Pure PIL, no network,
fully deterministic: same bytes on every run.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

PAPER = (247, 243, 234)
NAVY = (20, 33, 61)
NAVY_SOFT = (43, 58, 88)
INK = (28, 28, 28)
GREY = (92, 90, 84)
RULE = (201, 162, 39)
RED = (176, 58, 46)
RED_BG = (253, 236, 231)
ROW_LINE = (221, 213, 194)
WHITE = (255, 255, 255)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_DATE = None
F_KICK = None
F_CHIP = None
F_HERO_H = None
F_HERO_F = None
F_NUM = None
F_HEAD = None
F_FACT = None
F_TAG = None
F_FOOT = None


def load_fonts():
    global F_DATE, F_KICK, F_CHIP, F_HERO_H, F_HERO_F
    global F_NUM, F_HEAD, F_FACT, F_TAG, F_FOOT
    F_DATE = font("DejaVuSans-Bold.ttf", 56)
    F_KICK = font("DejaVuSans-Bold.ttf", 17)
    F_CHIP = font("DejaVuSans-Bold.ttf", 15)
    F_HERO_H = font("DejaVuSans-Bold.ttf", 30)
    F_HERO_F = font("DejaVuSans.ttf", 19)
    F_NUM = font("DejaVuSans-Bold.ttf", 16)
    F_HEAD = font("DejaVuSans-Bold.ttf", 19)
    F_FACT = font("DejaVuSans.ttf", 15)
    F_TAG = font("DejaVuSans-Bold.ttf", 12)
    F_FOOT = font("DejaVuSans.ttf", 15)


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_font(draw, text, start_size, max_w, name="DejaVuSans-Bold.ttf"):
    """Shrink a bold font until the text fits max_w; returns the font."""
    size = start_size
    while size > 20:
        fnt = font(name, size)
        if text_w(draw, text, fnt) <= max_w:
            return fnt
        size -= 2
    return font(name, 20)


def chip(draw, x_right, y, label, fill, fg=WHITE):
    """Right-aligned tag chip; returns its left x."""
    pad_x, h = 8, 20
    tw = text_w(draw, label, F_TAG)
    x0 = x_right - int(tw) - 2 * pad_x
    draw.rounded_rectangle([x0, y, x_right, y + h], radius=10, fill=fill)
    draw.text((x0 + pad_x, y + 4), label, font=F_TAG, fill=fg)
    return x0


# (number, headline, fact, tag) — chronological, 24 Nov 2026 only.
STORIES = [
    ("01", "Overnight strike on Zaporizhzhia kills 2, hurts 40",
     "Apartment block hit, 4 children hurt; Germany first in Delta; Zelensky seeks NATO entry.",
     "UKRAINE"),
    ("03", "Israeli strike kills Hamas security chief in Gaza",
     "Naeem Abu Nahel and 6 others dead, including 2 police officers.",
     "GAZA"),
    ("04", "Jensen Huang reinstated as Nvidia CEO",
     "Back under two weeks after resigning in an affair scandal; Trump says he urged the board.",
     "TECH"),
    ("05", "Trump to speed up federal executions",
     "Directive targets child murder, rapists and traffickers who kill their victims.",
     "USA"),
    ("06", "$375,000 reward to catch AI cheats in CSAT exam",
     "Bounty for students caught cheating with AI in the national college entrance exam.",
     "KOREA"),
    ("07", "US blacklists Singapore cloud firm Megaspeed",
     "Commerce Department adds Megaspeed International over China links.",
     "TRADE"),
    ("08", "Fighting near hospital traps Ebola response team",
     "Heavy combat in Ituri leaves a WHO team stuck as the outbreak response stalls.",
     "DRC"),
    ("09", "Oregon and Virginia sue SpaceX over Grok images",
     "States allege Grok produced child-abuse images.",
     "COURTS"),
    ("10", "Malaysia to repatriate 6,500+ Rohingya to Myanmar",
     "Mass return plan for refugees sheltering in Malaysia.",
     "ASIA"),
    ("11", "Pentagon: Canada failing as defence partner",
     "US accuses Canada of falling short as a credible North America defence partner.",
     "DEFENCE"),
    ("12", "COP31 ends in failure as world splits",
     "Analysis: climate talks collapse with nations divided on the way forward.",
     "CLIMATE"),
]

HERO_HEAD = "Three tankers hit by mines and burning in the Strait of Hormuz"
HERO_FACT = ("Iran vows to fight a US sea blockade. Vance and Rubio met Qatar's PM "
             "at the White House; Tehran refuses talks until 7 conditions are met.")


def draw_banner(draw):
    draw.rectangle([0, 0, W, 112], fill=NAVY)
    date = "TUESDAY, 24 NOVEMBER 2026"
    fnt = fit_font(draw, date, 56, W - 80)
    tw = text_w(draw, date, fnt)
    draw.text(((W - tw) / 2, 30), date, font=fnt, fill=WHITE)
    draw.rectangle([0, 112, W, 116], fill=RULE)
    kick = "THE WORLD IN ONE DAY  —  TWELVE STORIES, EVERY REGION"
    tw = text_w(draw, kick, F_KICK)
    draw.text(((W - tw) / 2, 130), kick, font=F_KICK, fill=GREY)


def draw_hero(draw):
    x0, y0, x1, y1 = 40, 160, 984, 330
    draw.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=RED_BG,
                           outline=RED, width=2)
    draw.rectangle([x0, y0 + 10, x0 + 10, y1 - 10], fill=RED)
    # hero chip
    label = "HERO  ·  02  ·  STRAIT OF HORMUZ"
    pad_x, ch = 10, 24
    tw = text_w(draw, label, F_CHIP)
    cx0, cy = x0 + 26, y0 + 14
    draw.rounded_rectangle([cx0, cy, cx0 + int(tw) + 2 * pad_x, cy + ch],
                           radius=12, fill=RED)
    draw.text((cx0 + pad_x, cy + 4), label, font=F_CHIP, fill=WHITE)
    # headline (max 2 lines) and fact (max 2 lines)
    hx, hw = x0 + 26, x1 - x0 - 52
    lines = wrap(draw, HERO_HEAD, F_HERO_H, hw)
    hy = y0 + 48
    for ln in lines[:2]:
        draw.text((hx, hy), ln, font=F_HERO_H, fill=NAVY)
        hy += 34
    flines = wrap(draw, HERO_FACT, F_HERO_F, hw)
    fy = hy + 4
    for ln in flines[:2]:
        draw.text((hx, fy), ln, font=F_HERO_F, fill=INK)
        fy += 23


def draw_timeline(draw):
    spine_x = 64
    top, row_h = 340, 56
    draw.line([(spine_x, top + 8), (spine_x, top + 11 * row_h - 8)],
              fill=RULE, width=3)
    for i, (num, head, fact, tag) in enumerate(STORIES):
        ry = top + i * row_h
        cy = ry + 12
        # dot on the spine
        draw.ellipse([spine_x - 7, cy - 7, spine_x + 7, cy + 7],
                     fill=RED, outline=WHITE, width=2)
        # number
        draw.text((88, ry + 2), num, font=F_NUM, fill=RED)
        # tag chip, right aligned
        tag_left = chip(draw, 984, ry + 2, tag, NAVY)
        # headline, must fit before the tag
        head_w = tag_left - 12 - 124
        head = head
        while text_w(draw, head, F_HEAD) > head_w and len(head) > 10:
            head = head[:-1]
        draw.text((124, ry + 1), head, font=F_HEAD, fill=NAVY)
        # one-line fact
        fact_w = 984 - 124
        f = fact
        while text_w(draw, f, F_FACT) > fact_w and len(f) > 10:
            f = f[:-4] + "..."
        draw.text((124, ry + 27), f, font=F_FACT, fill=GREY)
        # row separator
        if i < len(STORIES) - 1:
            draw.line([(124, ry + row_h - 8), (984, ry + row_h - 8)],
                      fill=ROW_LINE, width=1)


def draw_footer(draw):
    foot = "All twelve events dated Tuesday 24 November 2026 in their origin timezone."
    tw = text_w(draw, foot, F_FOOT)
    draw.text(((W - tw) / 2, 972), foot, font=F_FOOT, fill=GREY)


def main():
    load_fonts()
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_banner(draw)
    draw_hero(draw)
    draw_timeline(draw)
    draw_footer(draw)
    os.makedirs("/output", exist_ok=True)
    img.save("/output/entry.png", format="PNG", optimize=True)
    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()

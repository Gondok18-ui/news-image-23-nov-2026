#!/usr/bin/env python3
"""
The Daily Meridian -- a one-page broadsheet summing up the world news of
Monday, 23 November 2026, drawn entirely with Pillow.

This file is the generator that drew the entry's judged image,
entry.png. It is kept in the repository for provenance and
reproduction: run it locally with Pillow installed and it regenerates
the same 1024x1024 PNG (written next to this file, or to
$MAKEFUN_OUTPUT_DIR/entry.png when that variable is set). The drawing
is fully deterministic: no randomness, no clock, no network -- two
runs write the same bytes.

It is not the program the make.fun harness executes. The harness
entrypoint is main.ts (Node 22, standard library only), which copies
the entry.png held in this repository to the harness output directory.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024

# ---------------------------------------------------------------- palette
PAPER = (247, 242, 228)
PAPER_PANEL = (255, 253, 246)
INK = (25, 23, 19)
GREY = (92, 86, 76)
NAVY = (20, 48, 77)
NAVY_LIGHT = (38, 74, 110)
CREAM = (250, 246, 233)
RED = (166, 28, 28)
GOLD = (178, 132, 30)
HAIR = (120, 112, 96)
SKY = (216, 228, 230)
OCEAN = (110, 164, 196)
LAND = (106, 154, 91)
LAND2 = (178, 158, 96)
FLAME_O = (232, 122, 32)
FLAME_R = (196, 52, 36)
BLACK = (16, 15, 13)

_HERE = os.path.dirname(os.path.abspath(__file__))

FONT_DIRS = [
    # the fonts bundled with the entry come first: the grading image may
    # have no usable system fonts at all, and bundled-first also makes
    # the local and graded renders identical
    os.path.join(_HERE, "fonts"),
    "/usr/share/fonts/truetype/liberation",
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts",
]

FONT_FILES = {
    "serif": "LiberationSerif-Regular.ttf",
    "serif_b": "LiberationSerif-Bold.ttf",
    "serif_i": "LiberationSerif-Italic.ttf",
    "sans": "LiberationSans-Regular.ttf",
    "sans_b": "LiberationSans-Bold.ttf",
}
FONT_FALLBACK = {
    "serif": "DejaVuSerif.ttf",
    "serif_b": "DejaVuSerif-Bold.ttf",
    "serif_i": "DejaVuSerif.ttf",
    "sans": "DejaVuSans.ttf",
    "sans_b": "DejaVuSans-Bold.ttf",
}


_FONT_CACHE = []


def font(style, size):
    """Load a TrueType font by style name, with graceful fallbacks.

    Never raises: if every font file is missing and even Pillow's
    built-in default font cannot load (newer Pillow can raise there
    instead of returning the bitmap font), fall back to a font that was
    already loaded, so the page still draws.
    """
    for name in (FONT_FILES[style], FONT_FALLBACK[style]):
        for d in FONT_DIRS:
            p = os.path.join(d, name)
            if os.path.exists(p):
                try:
                    f = ImageFont.truetype(p, size)
                    _FONT_CACHE.append(f)
                    return f
                except Exception:
                    pass
    try:
        return ImageFont.load_default()
    except Exception:
        pass
    if _FONT_CACHE:
        return _FONT_CACHE[0]
    # last resort: any TrueType file in any searched directory
    for d in FONT_DIRS:
        try:
            names = sorted(os.listdir(d))
        except OSError:
            continue
        for name in names:
            if name.lower().endswith(".ttf"):
                try:
                    return ImageFont.truetype(os.path.join(d, name), size)
                except Exception:
                    pass
    try:
        return ImageFont.load_default()
    except Exception:
        return _FONT_CACHE[0] if _FONT_CACHE else None


# ---------------------------------------------------------------- helpers
def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(draw, text, fnt, x, y, max_w, lh, fill=INK, max_lines=None,
          align="left", width=None):
    """Draw wrapped text; returns the y just past the last line."""
    lines = wrap(draw, text, fnt, max_w)
    if max_lines is not None:
        lines = lines[:max_lines]
    for ln in lines:
        if align == "center":
            w = draw.textlength(ln, font=fnt)
            draw.text((x + (max_w - w) / 2, y), ln, font=fnt, fill=fill)
        elif align == "right":
            w = draw.textlength(ln, font=fnt)
            draw.text((x + max_w - w, y), ln, font=fnt, fill=fill)
        else:
            draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def fit_size(draw, text, style, start, max_w):
    """Largest font size <= start at which text fits max_w on one line."""
    size = start
    while size > 10 and draw.textlength(text, font=font(style, size)) > max_w:
        size -= 2
    return size


def rule(draw, x0, x1, y, w=1, fill=INK):
    draw.rectangle([x0, y, x1, y + w - 1], fill=fill)


# ---------------------------------------------------------------- drawing
def draw_globe_panel(draw, x0, y0, x1, y1):
    """The lead illustration: a cracked, overheating planet over flames,
    a thermometer at its limit, drawn as flat newspaper-style shapes."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY, outline=INK, width=2)

    # sun, top right of the panel
    sx, sy, sr = x1 - 64, y0 + 40, 17
    for dx, dy in ((-30, 0), (30, 0), (0, -30), (0, 30),
                   (-21, -21), (21, -21), (-21, 21), (21, 21)):
        draw.line([sx, sy, sx + dx, sy + dy], fill=GOLD, width=3)
    draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(240, 178, 60),
                 outline=GOLD, width=2)

    # the globe
    cx, cy, r = x0 + 108, (y0 + y1) // 2 - 2, 66
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=OCEAN, outline=NAVY,
                 width=3)
    # stylised continents: flat blobs clipped by nothing but the circle's rim
    blobs = [
        (cx - 52, cy - 44, cx - 8, cy - 12),
        (cx + 6, cy - 52, cx + 48, cy - 20),
        (cx - 30, cy + 2, cx + 12, cy + 40),
        (cx + 26, cy + 14, cx + 56, cy + 44),
        (cx - 58, cy + 18, cx - 34, cy + 46),
    ]
    for i, b in enumerate(blobs):
        draw.ellipse(list(b), fill=LAND if i % 2 == 0 else LAND2)
    # rim redrawn so the blobs stay inside the planet
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=3)
    # cracks across the globe
    crack = [(cx - 40, cy - 58), (cx - 22, cy - 30), (cx - 34, cy - 6),
             (cx - 10, cy + 22), (cx - 20, cy + 52)]
    draw.line(crack, fill=(60, 40, 30), width=3, joint="curve")
    crack2 = [(cx + 44, cy - 40), (cx + 26, cy - 14), (cx + 38, cy + 16),
              (cx + 18, cy + 44)]
    draw.line(crack2, fill=(60, 40, 30), width=3, joint="curve")

    # thermometer, right of centre, mercury at the top of the tube
    tx = x0 + 330
    top, bot = y0 + 26, y1 - 34
    draw.rounded_rectangle([tx - 11, top, tx + 11, bot], radius=11,
                           fill=CREAM, outline=INK, width=2)
    draw.rectangle([tx - 5, top + 10, tx + 5, bot], fill=RED)
    draw.ellipse([tx - 17, bot - 8, tx + 17, bot + 26], fill=RED,
                 outline=INK, width=2)
    for i in range(5):
        ty = top + 16 + i * 22
        draw.line([tx + 16, ty, tx + 30, ty], fill=INK, width=2)
    draw.text((tx + 40, top + 2), "HEAT", font=font("sans_b", 17), fill=RED)
    draw.text((tx + 40, top + 24), "RECORD", font=font("sans_b", 17), fill=RED)

    # rising smoke wisps from the globe's top
    for gx in (cx - 30, cx + 6, cx + 40):
        draw.arc([gx - 10, y0 + 8, gx + 12, y0 + 40], start=200, end=340,
                 fill=GREY, width=3)

    # flame tongues along the panel's foot
    base = y1
    fx = x0 + 18
    while fx < x1 - 30:
        draw.polygon([(fx, base), (fx + 13, base - 26), (fx + 26, base)],
                     fill=FLAME_O)
        draw.polygon([(fx + 7, base), (fx + 13, base - 15), (fx + 19, base)],
                     fill=FLAME_R)
        fx += 34


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    X0, X1 = 44, 980
    CW = X1 - X0

    # page frame: heavy outer rule, hairline inside
    draw.rectangle([12, 12, W - 13, H - 13], outline=INK, width=3)
    draw.rectangle([20, 20, W - 21, H - 21], outline=HAIR, width=1)

    # ---------------- masthead
    rule(draw, X0, X1, 34, 3)
    rule(draw, X0, X1, 41, 1)
    name = "The Daily Meridian"
    nf = font("serif_b", fit_size(draw, name, "serif_b", 96, CW - 40))
    nw = draw.textlength(name, font=nf)
    draw.text(((W - nw) / 2, 48), name, font=nf, fill=INK)
    tag = "THE WHOLE WORLD  ·  ONE DAY  ·  ONE PAGE"
    tf = font("sans_b", 16)
    tw = draw.textlength(tag, font=tf)
    draw.text(((W - tw) / 2, 140), tag, font=tf, fill=GREY)
    rule(draw, X0, X1, 166, 1)
    rule(draw, X0, X1, 170, 3)

    # date bar
    draw.rectangle([X0, 182, X1, 218], fill=NAVY)
    df = font("sans_b", 22)
    draw.text((X0 + 16, 191), "MONDAY, 23 NOVEMBER 2026", font=df, fill=CREAM)
    ef = font("sans_b", 15)
    et = "LATE FINAL EDITION"
    draw.text((X1 - 16 - draw.textlength(et, font=ef), 195), et, font=ef,
              fill=(198, 214, 228))

    # ticker strip directly under the date bar
    draw.rectangle([X0, 224, X1, 264], fill=BLACK)
    tick = ("ALSO TODAY  ▪  SKUBAL SIGNS RECORD $450M METS DEAL  ▪  'EL CHAPO "
            "ISIDRO' CAPTURED IN SINALOA  ▪  NIGERIA FUNERAL-BOAT CAPSIZE "
            "KILLS 24  ▪  SHENZHOU-24 CREW NAMED  ▪  INDONESIA FACTORY "
            "FIRE: 34 MISSING  ▪  USA & UK WIN WOMEN'S WORLD CUPS")
    tick_lines = wrap(draw, tick, font("sans_b", 13), CW - 24)[:2]
    ty = 231
    for ln in tick_lines:
        lw = draw.textlength(ln, font=font("sans_b", 13))
        draw.text((X0 + (CW - lw) / 2, ty), ln, font=font("sans_b", 13),
                  fill=(240, 226, 190))
        ty += 18

    # ---------------- lead story
    kf = font("sans_b", 19)
    draw.text((X0, 280), "CLIMATE SUMMIT  ·  COP31", font=kf, fill=RED)
    draw.text((X1 - draw.textlength("LEAD STORY", font=kf), 280), "LEAD STORY",
              font=kf, fill=GREY)
    hf = font("serif_b", 56)
    y = block(draw, "Climate Talks Collapse in Anger Over Fossil Fuels",
              hf, X0, 306, CW, 64)
    dek = ("COP31 ends without a deal to phase out coal, oil and gas, as "
           "negotiators trade blame for a summit that promised everything "
           "and settled nothing.")
    y = block(draw, dek, font("serif_i", 19), X0, y + 8, CW, 25, fill=(52, 48, 42))
    rule(draw, X0, X1, y + 8, 1, HAIR)

    # illustration (left) and lead body (right)
    top = y + 22
    draw_globe_panel(draw, X0, top, 576, top + 156)
    cap = ("The planet was the summit's subject — and, delegates from the "
           "island states said as they walked out, its loser.")
    block(draw, cap, font("serif_i", 15), X0, top + 162, 532, 18,
          fill=GREY, max_lines=2)
    body = ("Two weeks of negotiation ended in recrimination as the summit "
            "broke up without the deal its hosts had promised: a timetable "
            "for phasing out the fossil fuels driving global warming. "
            "Draft texts naming coal, oil and gas were stripped out in "
            "the final hours, and island-state delegates walked out "
            "calling it a betrayal. Producer nations — Saudi Arabia "
            "above all — were blamed for blocking every formula put to "
            "the room.")
    block(draw, body, font("serif", 16), 600, top, 380, 22, max_lines=9)
    rule(draw, X0, X1, 742, 2)

    # ---------------- three panels
    panels = [
        ("WAR AT SEA", NAVY,
         "Ukraine's Drones Strike Russian Warships in Libya",
         "Naval drones hit two Russian warships in Benghazi port; the "
         "cargo ship Sparta II was set ablaze in the Gulf of Finland."),
        ("STRAIT OF HORMUZ", RED,
         "Three More Tankers Struck as Attacks Hit a Record Pace",
         "Three tankers were struck or mined; Houthis claimed a Saudi "
         "refinery strike as Trump warned Iran of new US strikes."),
        ("CYBERSECURITY", NAVY,
         "FBI Probes Apparent Hack of Police Crime Database",
         "Agents are probing a breach of the NCIC database police use "
         "for fugitives, missing persons and criminal histories."),
    ]
    col_w, gap = 296, 24
    py = 756
    for i, (label, colour, head, text) in enumerate(panels):
        px = X0 + i * (col_w + gap)
        draw.text((px, py), label, font=font("sans_b", 15), fill=colour)
        hy = block(draw, head, font("serif_b", 23), px, py + 24, col_w, 27,
                   max_lines=3)
        block(draw, text, font("serif", 15), px, hy + 6, col_w, 19,
              max_lines=4)
        if i:
            draw.line([px - gap // 2, py + 2, px - gap // 2, py + 160],
                      fill=HAIR, width=1)
    rule(draw, X0, X1, 934, 1, HAIR)

    # ---------------- four mini items
    minis = [
        ("MARKETS",
         "Nasdaq futures +3% as Huang reignites the AI trade."),
        ("SPACE",
         "Russia may orbit a nuclear-armed satellite; NATO vows defence."),
        ("MYANMAR",
         "UK sanctions junta chiefs after the genocide ruling."),
        ("WASHINGTON",
         "Democrats' House majority hits 259, largest since 1992."),
    ]
    mw = (CW - 3 * 24) // 4
    my = 946
    for i, (label, text) in enumerate(minis):
        mx = X0 + i * (mw + 24)
        draw.text((mx, my), label, font=font("sans_b", 13), fill=NAVY)
        block(draw, text, font("serif", 13), mx, my + 18, mw, 16,
              max_lines=3)

    return img


def main():
    img = build()
    here = os.path.dirname(os.path.abspath(__file__))
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        primary = os.path.join(env_dir, "entry.png")
    elif os.path.isdir("/output"):
        primary = "/output/entry.png"
    else:
        primary = os.path.join(here, "entry.png")
    # the harness target is written first, and it is the only write
    # whose failure may fail the run
    d = os.path.dirname(primary)
    if d:
        os.makedirs(d, exist_ok=True)
    img.save(primary, "PNG", optimize=True)
    # a copy beside the program is a local convenience only: in the
    # grader the repository directory is read-only, so this write is
    # best-effort and must never fail the run
    local = os.path.join(here, "entry.png")
    if os.path.abspath(local) != os.path.abspath(primary):
        try:
            img.save(local, "PNG", optimize=True)
        except Exception:
            pass


if __name__ == "__main__":
    main()

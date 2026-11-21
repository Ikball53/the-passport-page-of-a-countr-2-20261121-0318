"""Render an open passport spread for the invented Republic of Ostravia.

The issuing state renamed itself the Republic of Ostra on 1 January 2024,
midway through this document's validity. The data page still carries the
old name; the bearer's own border stamps at Karst Pass switch from
OSTRAVIA (2022-2023) to OSTRA (2024-2025). No caption explains it.
"""

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

RNG = random.Random(20240314)
HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"

W = H = 1024
DESK = (36, 44, 50)
PAPER_L = (229, 235, 239)
PAPER_R = (241, 238, 227)
INK = (23, 33, 62)
LABEL = (104, 112, 121)
GUIL_A = (146, 178, 204)
GUIL_B = (168, 202, 176)
STAMP_BLUE = (28, 68, 158)
STAMP_GREEN = (18, 116, 78)
STAMP_RED = (168, 38, 48)
STAMP_PURPLE = (88, 48, 138)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def font(size, kind="sans"):
    names = {
        "sans": "DejaVuSans.ttf",
        "bold": "DejaVuSans-Bold.ttf",
        "serif": "DejaVuSerif.ttf",
        "serifbold": "DejaVuSerif-Bold.ttf",
        "mono": "DejaVuSansMono.ttf",
        "monobold": "DejaVuSansMono-Bold.ttf",
    }
    return ImageFont.truetype(str(FONT_DIR / names[kind]), size)


def add_noise(img, strength=9, seed=7):
    rng = random.Random(seed)
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y][:3]
            n = rng.randint(-strength, strength)
            px[x, y] = (max(0, min(255, r + n)), max(0, min(255, g + n)),
                        max(0, min(255, b + n)))
    return img


def vgrad(size, top, bottom):
    w, h = size
    base = Image.new("RGB", (1, h))
    for y in range(h):
        t = y / max(1, h - 1)
        base.putpixel((0, y), tuple(int(top[i] + (bottom[i] - top[i]) * t)
                                     for i in range(3)))
    return base.resize((w, h))


def guilloche(img, box, color, phase=0.0, amp=7.0, step=9):
    """Fine interlaced sine lines clipped to box, low alpha."""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = box
    for yy in range(y0, y1, step):
        pts = []
        for xx in range(x0, x1, 4):
            pts.append((xx, yy + amp * math.sin((xx - x0) / 26.0 + phase
                                                 + yy / 41.0)))
        d.line(pts, fill=color + (46,), width=1)
    for xx in range(x0, x1, step * 2):
        pts = []
        for yy in range(y0, y1, 4):
            pts.append((xx + amp * 0.7 * math.cos((yy - y0) / 30.0 + phase),
                        yy))
        d.line(pts, fill=color + (30,), width=1)
    img.alpha_composite(layer)


def portrait(box):
    """Shaded studio portrait: gradient backdrop, soft facial shading."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    pic = vgrad((w, h), (196, 208, 220), (138, 155, 176)).convert("RGBA")
    d = ImageDraw.Draw(pic)
    cx = w // 2
    skin = (196, 152, 120)
    skin_dark = (158, 112, 84)
    skin_light = (222, 182, 148)
    hair = (52, 40, 32)
    jacket = (44, 50, 66)
    # shoulders / jacket
    d.ellipse([cx - w * 0.52, h * 0.66, cx + w * 0.52, h * 1.25], fill=jacket)
    d.polygon([(cx - 16, h * 0.70), (cx + 16, h * 0.70), (cx, h * 0.92)],
              fill=(228, 228, 224))  # shirt V
    # neck
    d.rectangle([cx - 13, h * 0.52, cx + 13, h * 0.72], fill=skin_dark)
    # head with offset highlight for shading
    d.ellipse([cx - 34, h * 0.10, cx + 34, h * 0.58], fill=skin)
    d.ellipse([cx - 30, h * 0.12, cx + 14, h * 0.52], fill=skin_light)
    d.ellipse([cx + 12, h * 0.18, cx + 34, h * 0.54], fill=skin_dark)
    # ears
    d.ellipse([cx - 39, h * 0.32, cx - 31, h * 0.44], fill=skin_dark)
    d.ellipse([cx + 31, h * 0.32, cx + 39, h * 0.44], fill=skin_dark)
    # hair cap
    d.pieslice([cx - 36, h * 0.06, cx + 36, h * 0.40], 180, 360, fill=hair)
    d.rectangle([cx - 36, h * 0.20, cx - 30, h * 0.34], fill=hair)
    d.rectangle([cx + 30, h * 0.20, cx + 36, h * 0.34], fill=hair)
    # brows, eyes, nose shadow, mouth
    d.line([(cx - 22, h * 0.33), (cx - 8, h * 0.315)], fill=hair, width=3)
    d.line([(cx + 8, h * 0.315), (cx + 22, h * 0.33)], fill=hair, width=3)
    d.ellipse([cx - 19, h * 0.365, cx - 10, h * 0.395], fill=(38, 30, 26))
    d.ellipse([cx + 10, h * 0.365, cx + 19, h * 0.395], fill=(38, 30, 26))
    d.line([(cx + 1, h * 0.40), (cx - 2, h * 0.47)], fill=skin_dark, width=2)
    d.line([(cx - 11, h * 0.515), (cx + 11, h * 0.515)], fill=(120, 72, 58),
           width=2)
    # jaw shading + stubble speckle
    d.arc([cx - 28, h * 0.38, cx + 28, h * 0.60], 20, 160, fill=skin_dark,
          width=2)
    for _ in range(260):
        sx = cx + RNG.randint(-24, 24)
        sy = int(h * RNG.uniform(0.46, 0.57))
        d.point((sx, sy), fill=(96, 70, 52))
    pic = pic.filter(ImageFilter.GaussianBlur(1.1))
    return add_noise(pic.convert("RGB"), strength=6, seed=11).convert("RGBA")


def stamp(img, cx, cy, w, h, lines, color, angle, oval=False, alpha=205):
    """Ink stamp: double border, centered lines, rotated, uneven alpha."""
    sw, sh = w + 30, h + 30
    layer = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    box = [15, 15, sw - 15, sh - 15]
    if oval:
        d.ellipse(box, outline=color + (alpha,), width=3)
        d.ellipse([box[0] + 5, box[1] + 5, box[2] - 5, box[3] - 5],
                  outline=color + (alpha - 40,), width=1)
    else:
        d.rounded_rectangle(box, 8, outline=color + (alpha,), width=3)
        d.rounded_rectangle([box[0] + 5, box[1] + 5, box[2] - 5, box[3] - 5],
                            6, outline=color + (alpha - 40,), width=1)
    total = sum(sz + 3 for _, sz in lines)
    ty = (sh - total) // 2
    for text, sz in lines:
        f = font(sz, "bold")
        tw = d.textlength(text, font=f)
        d.text(((sw - tw) / 2, ty), text, font=f, fill=color + (alpha,))
        ty += sz + 3
    # ink wear: erase sparse speckles
    px = layer.load()
    for _ in range(240):
        x, y = RNG.randrange(sw), RNG.randrange(sh)
        if px[x, y][3] > 0:
            px[x, y] = (0, 0, 0, 0)
    layer = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(layer, (int(cx - layer.width / 2),
                                int(cy - layer.height / 2)))


def emblem(d, cx, cy, r):
    """Simple shield-and-star coat of arms."""
    gold = (150, 118, 44)
    d.polygon([(cx - r, cy - r), (cx + r, cy - r), (cx + r, cy + r * 0.2),
               (cx, cy + r), (cx - r, cy + r * 0.2)], outline=gold, width=2)
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r * 0.55 if i % 2 == 0 else r * 0.24
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=gold)


def hologram(img, cx, cy, r):
    """Rainbow foil disc overlapping the photo corner."""
    layer = Image.new("RGBA", (r * 2, r * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    hues = [(220, 90, 90), (230, 170, 70), (150, 210, 110), (90, 180, 220),
            (140, 120, 230), (220, 110, 190)]
    for i in range(36):
        d.pieslice([0, 0, r * 2, r * 2], i * 10, i * 10 + 11,
                   fill=hues[i % len(hues)] + (88,))
    d.ellipse([0, 0, r * 2, r * 2], outline=(255, 255, 255, 150), width=2)
    d.ellipse([r - 7, r - 7, r + 7, r + 7], outline=(255, 255, 255, 170),
              width=1)
    img.alpha_composite(layer, (cx - r, cy - r))


def signature(d, x, y, w):
    pts = []
    for i in range(140):
        t = i / 139
        pts.append((x + t * w,
                    y + 5 * math.sin(t * 14.0) - 9 * math.sin(t * 4.3)
                    + 3 * math.cos(t * 26.0) - 6 * math.sin(t * 6.7)))
    d.line(pts, fill=(30, 40, 110), width=2)
    # a final flourish loop
    loop = []
    for i in range(40):
        a = i / 39 * 2 * math.pi
        loop.append((x + w * 0.82 + 10 * math.cos(a),
                     y - 4 + 6 * math.sin(a)))
    d.line(loop, fill=(30, 40, 110), width=2)


def field(d, x, y, label, value, vw=210):
    d.text((x, y), label, font=font(9, "sans"), fill=LABEL)
    d.text((x, y + 12), value, font=font(13, "bold"), fill=INK)


def build():
    img = Image.new("RGBA", (W, H), DESK + (255,))
    d = ImageDraw.Draw(img)
    # desk vignette
    vig = vgrad((W, H), (52, 62, 70), (26, 32, 38))
    img.alpha_composite(vig.convert("RGBA"))
    d = ImageDraw.Draw(img)

    # spread geometry
    x0, y0, x1, y1 = 72, 196, 952, 828
    spine = (x0 + x1) // 2
    # drop shadow
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([x0 + 10, y0 + 16, x1 + 10, y1 + 16], 10,
                         fill=(0, 0, 0, 150))
    img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(9)))
    d = ImageDraw.Draw(img)
    # pages
    d.rounded_rectangle([x0, y0, spine, y1], 8, fill=PAPER_L)
    d.rounded_rectangle([spine, y0, x1, y1], 8, fill=PAPER_R)
    d.rectangle([spine - 6, y0, spine + 6, y1], fill=PAPER_L)
    d.rectangle([spine, y0, spine + 6, y1], fill=PAPER_R)
    # spine shading
    for i in range(26):
        a = int(70 * (1 - i / 26))
        d.line([(spine - i, y0 + 4), (spine - i, y1 - 4)], fill=(90, 95, 100, a))
        d.line([(spine + i, y0 + 4), (spine + i, y1 - 4)], fill=(90, 90, 85, a))
    # page edge lines
    for off in (3, 6):
        d.rounded_rectangle([x0 - off, y0 + off, spine - 2, y1 - off], 8,
                            outline=(196, 198, 192))
        d.rounded_rectangle([spine + 2, y0 + off, x1 + off, y1 - off], 8,
                            outline=(202, 198, 184))
    guilloche(img, (x0 + 8, y0 + 8, spine - 8, y1 - 8), GUIL_A, phase=0.4)
    guilloche(img, (spine + 8, y0 + 8, x1 - 8, y1 - 8), GUIL_B, phase=2.1)
    d = ImageDraw.Draw(img)

    # ---- left page: data page ----
    emblem(d, x0 + 44, y0 + 44, 20)
    d.text((x0 + 76, y0 + 22), "REPUBLIC OF OSTRAVIA", font=font(21, "serifbold"),
           fill=INK)
    d.text((x0 + 76, y0 + 48), "OSTRAVSKA REPUBLIKA", font=font(11, "sans"),
           fill=LABEL)
    d.text((x0 + 76, y0 + 64), "PASSPORT  /  PAS", font=font(13, "bold"),
           fill=INK)
    d.line([(x0 + 24, y0 + 92), (spine - 24, y0 + 92)], fill=(150, 120, 60),
           width=2)

    photo = (x0 + 26, y0 + 112, x0 + 176, y0 + 302)
    img.alpha_composite(portrait(photo), (photo[0], photo[1]))
    d = ImageDraw.Draw(img)
    d.rectangle(photo, outline=(120, 128, 138), width=2)
    hologram(img, photo[2] - 6, photo[3] - 6, 24)
    d = ImageDraw.Draw(img)
    d.text((x0 + 26, photo[3] + 8), "OST4471206", font=font(11, "mono"),
           fill=LABEL)

    fx = x0 + 196
    rows = [
        ("TYPE / TIP", "P", "COUNTRY / DRZAVA", "OST"),
        ("PASSPORT NO.", "OST4471206", "SURNAME / PREZIME", "VEY"),
        ("GIVEN NAMES / IMENA", "MAREK DUSAN", "NATIONALITY", "OSTRAVIA"),
        ("DATE OF BIRTH", "09 NOV 1988", "SEX / POL", "M"),
        ("PLACE OF BIRTH", "KARST CITY", "OCCUPATION", "FREIGHT DRIVER"),
        ("DATE OF ISSUE", "14 MAR 2022", "DATE OF EXPIRY", "13 MAR 2032"),
    ]
    fy = y0 + 112
    for l1, v1, l2, v2 in rows:
        field(d, fx, fy, l1, v1)
        field(d, fx + 108, fy, l2, v2)
        fy += 44
    d.text((fx, fy + 2), "AUTHORITY / ORGAN", font=font(10, "sans"), fill=LABEL)
    d.text((fx, fy + 15), "MINISTRY OF INTERIOR", font=font(14, "bold"),
           fill=INK)
    signature(d, x0 + 30, y1 - 118, 130)
    d.line([(x0 + 28, y1 - 96), (x0 + 168, y1 - 96)], fill=LABEL, width=1)
    d.text((x0 + 28, y1 - 92), "SIGNATURE OF BEARER", font=font(9, "sans"),
           fill=LABEL)

    # MRZ
    mrz_y = y1 - 62
    d.rectangle([x0 + 18, mrz_y - 6, spine - 18, y1 - 12],
                fill=(240, 241, 238))
    d.text((x0 + 26, mrz_y), "P<OSTVEY<<MAREK<DUSAN<<<<<<<<<<<<<<<<<<<<<<",
           font=font(14, "mono"), fill=(30, 30, 34))
    d.text((x0 + 26, mrz_y + 22), "OST4471206<8OST8811094M3203137<<<<<<<<<<<<<<08",
           font=font(14, "mono"), fill=(30, 30, 34))

    # ---- right page: stamps ----
    d.text((spine + 36, y0 + 22), "VISAS / VIZY", font=font(15, "serifbold"),
           fill=INK)
    d.line([(spine + 34, y0 + 48), (x1 - 24, y0 + 48)], fill=(150, 120, 60),
           width=2)
    d.text((spine + 36, y0 + 56), "GRANICNI PRELAZI / BORDER CROSSINGS",
           font=font(10, "sans"), fill=LABEL)

    sx = spine + 108
    sy = y0 + 128
    stamp(img, sx, sy, 186, 78,
          [("OSTRAVIA", 16), ("EXIT  22 JUN 2022", 12), ("KARST PASS", 11)],
          STAMP_BLUE, -5)
    stamp(img, sx + 202, sy + 6, 186, 78,
          [("OSTRAVIA", 16), ("ENTRY  25 JUN 2022", 12), ("KARST PASS", 11)],
          STAMP_GREEN, 4)
    stamp(img, sx + 8, sy + 118, 186, 78,
          [("OSTRAVIA", 16), ("EXIT  17 OCT 2023", 12), ("KARST PASS", 11)],
          STAMP_BLUE, 3)
    stamp(img, sx + 210, sy + 112, 186, 78,
          [("OSTRAVIA", 16), ("ENTRY  19 OCT 2023", 12), ("KARST PASS", 11)],
          STAMP_GREEN, -6)
    # the state renamed itself on 1 Jan 2024: same border post, new name
    stamp(img, sx + 4, sy + 232, 186, 78,
          [("OSTRA", 16), ("ENTRY  08 FEB 2024", 12), ("KARST PASS", 11)],
          STAMP_GREEN, 5)
    stamp(img, sx + 206, sy + 238, 186, 78,
          [("OSTRA", 16), ("EXIT  30 MAY 2025", 12), ("KARST PASS", 11)],
          STAMP_BLUE, -4)
    stamp(img, sx + 105, sy + 348, 192, 84,
          [("OSTRA", 16), ("ENTRY  02 JUN 2025", 12), ("KARST PASS", 11)],
          STAMP_GREEN, 2, oval=True)
    d = ImageDraw.Draw(img)
    # perforated document number along the right edge
    for i, ch in enumerate("OST4471206"):
        d.text((x1 - 17, y0 + 100 + i * 22), ch, font=font(11, "mono"),
               fill=(158, 155, 146))
    d.text((spine + 26, y1 - 34), "7", font=font(12, "serif"), fill=LABEL)

    # gentle wear: soft crease + corner darkening
    wear = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(wear)
    wd.line([(x0 + 60, y1 - 30), (x0 + 210, y0 + 120)], fill=(120, 115, 95, 26),
            width=3)
    wd.ellipse([x1 - 120, y1 - 90, x1 + 40, y1 + 60], fill=(110, 100, 80, 22))
    img.alpha_composite(wear.filter(ImageFilter.GaussianBlur(6)))

    out = add_noise(img.convert("RGB"), strength=3, seed=23)
    out.save(OUT, optimize=True)
    if OUT.stat().st_size > 1_048_576:
        # per-pixel grain defeats PNG compression; cap the palette instead
        out.quantize(colors=256, method=Image.MEDIANCUT).save(OUT,
                                                               optimize=True)
    print(f"wrote {OUT} {out.size[0]}x{out.size[1]} {OUT.stat().st_size} bytes")


if __name__ == "__main__":
    build()

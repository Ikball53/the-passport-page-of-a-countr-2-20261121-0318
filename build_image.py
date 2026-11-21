#!/usr/bin/env python3
"""Draw the invented passport spread for the Republic of Thalvarra."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

W, H = 1024, 720
PAPER = (247, 243, 232)
PAPER2 = (241, 235, 220)
NAVY = (27, 42, 74)
TEAL = (18, 110, 110)
GOLD = (176, 141, 62)
INK = (35, 38, 48)
GREY = (110, 112, 118)
RED = (158, 44, 44)
BLUE_STAMP = (32, 70, 140)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

def f(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), (210, 202, 180))
d = ImageDraw.Draw(img, "RGBA")

# book shadow + pages
d.rounded_rectangle([18, 14, 1006, 706], radius=10, fill=(60, 55, 45, 255))
d.rectangle([24, 20, 500, 700], fill=PAPER)
d.rectangle([524, 20, 1000, 700], fill=PAPER2)
d.rectangle([500, 20, 524, 700], fill=(225, 218, 196))
for x in range(504, 521, 3):
    d.line([(x, 20), (x, 700)], fill=(200, 192, 168), width=1)

# page borders
d.rectangle([40, 36, 484, 684], outline=NAVY, width=2)
d.rectangle([540, 36, 984, 684], outline=NAVY, width=2)
d.rectangle([46, 42, 478, 678], outline=GOLD, width=1)
d.rectangle([546, 42, 978, 678], outline=GOLD, width=1)

# ---------- LEFT: data page ----------
d.text((262, 58), "REPUBLIC OF THALVARRA", font=f(SERIF_B, 21), fill=NAVY, anchor="mt")
d.text((262, 84), "TALVARIA  •  PASSPORT  •  PASEPORT", font=f(SANS, 11), fill=TEAL, anchor="mt")
d.line([(70, 106), (454, 106)], fill=GOLD, width=2)
# coat of arms: wave + lighthouse simplified
cx, cy = 262, 128
d.ellipse([cx-22, cy-22, cx+22, cy+22], outline=GOLD, width=2)
d.rectangle([cx-4, cy-14, cx+4, cy+10], fill=NAVY)
d.polygon([(cx-8, cy-14), (cx+8, cy-14), (cx, cy-20)], fill=GOLD)
for i, yy in enumerate([cy+12, cy+16]):
    d.arc([cx-14, yy-4, cx+14, yy+6], 0, 180, fill=TEAL, width=2)

# portrait box
px0, py0, px1, py1 = 64, 166, 196, 338
d.rectangle([px0, py0, px1, py1], outline=NAVY, width=2, fill=(232, 238, 240))
# dignified profile portrait with shapes
# head profile facing right
hx, hy = 128, 232
d.ellipse([hx-34, hy-52, hx+34, hy+40], fill=(216, 178, 148), outline=(120, 90, 70), width=2)
# hair bun
d.ellipse([hx-40, hy-58, hx+6, hy-30], fill=(62, 48, 42))
d.ellipse([hx-52, hy-44, hx-30, hy-22], fill=(62, 48, 42))
# nose hint
d.polygon([(hx+30, hy-4), (hx+40, hy+8), (hx+30, hy+10)], fill=(216, 178, 148), outline=(120, 90, 70))
# eye
d.ellipse([hx+12, hy-14, hx+20, hy-8], fill=(30, 30, 30))
# neck + shoulders / jacket
d.rectangle([hx-10, hy+34, hx+12, hy+56], fill=(216, 178, 148))
d.polygon([(px0+10, py1), (hx-44, hy+58), (hx+44, hy+58), (px1-10, py1)], fill=(38, 62, 92))
d.polygon([(hx-14, hy+58), (hx+14, hy+58), (hx, hy+92)], fill=(247, 243, 232))
d.text(((px0+px1)//2, py1+10), "PHOTO  •  FOTOGRAFIA", font=f(SANS, 8), fill=GREY, anchor="mt")

# data fields right of portrait
fields = [
    ("Type / Tip", "P"),
    ("Code / Kod", "TVL"),
    ("Passport No. / Nro", "TV 482 9173"),
    ("Surname / Apellido", "SOLENNE"),
    ("Given names / Nomi", "MIRA"),
    ("Nationality / Nacion", "THALVARRAN"),
    ("Date of birth / Nasc", "04 JUN 1991"),
    ("Sex / Seks", "F"),
    ("Place of birth", "PORT SENN"),
]
x, y = 214, 166
for label, val in fields:
    d.text((x, y), label.upper(), font=f(SANS, 8), fill=TEAL)
    d.text((x, y+11), val, font=f(SANS_B, 13), fill=INK)
    d.line([(x, y+28), (462, y+28)], fill=(205, 198, 178), width=1)
    y += 34

# lower data row
y2 = 486
d.line([(64, y2-10), (462, y2-10)], fill=GOLD, width=1)
lower = [
    ("Date of issue", "12 MAR 2022"),
    ("Date of expiry", "11 MAR 2032"),
    ("Authority", "PORT SENN PASSPORT OFFICE"),
    ("Holder's signature", "Mira Solenne"),
]
yy = y2
for label, val in lower:
    d.text((64, yy), label.upper(), font=f(SANS, 8), fill=TEAL)
    fontv = f(SERIF, 15) if "signature" in label else f(SANS_B, 12)
    d.text((64, yy+11), val, font=fontv, fill=INK)
    yy += 32

# endorsement = telling paperwork detail
ey = 618
d.rectangle([64, ey, 462, ey+30], outline=TEAL, width=1, fill=(240, 246, 244))
d.text((70, ey+4), "ENDORSEMENT: Licensed tide-reader. Valid for night", font=f(SANS, 8), fill=NAVY)
d.text((70, ey+16), "crossings of the Senn Channel. Fee 45 TLM • Rcpt 8814", font=f(SANS, 8), fill=NAVY)

# MRZ
d.rectangle([56, 654, 468, 676], fill=(255, 255, 255), outline=(190, 185, 165), width=1)
d.text((262, 656), "P<TVLSOLENNE<<MIRA<<<<<<<<<<<<<<<<<<<<<<<", font=f(MONO, 11), fill=INK, anchor="mt")
d.text((262, 668), "TV48291736TVL9106048F3203115<<<<<<<<<<<<04", font=f(MONO, 11), fill=INK, anchor="mt")

# ---------- RIGHT: stamps page ----------
d.text((762, 58), "VISAS  •  VIZE", font=f(SERIF_B, 19), fill=NAVY, anchor="mt")
d.text((762, 82), "Entry and exit stamps — in order of travel", font=f(SANS, 10), fill=GREY, anchor="mt")
d.line([(566, 102), (958, 102)], fill=GOLD, width=2)
# faint grid
for gy in range(120, 660, 90):
    d.line([(560, gy), (964, gy)], fill=(215, 208, 188), width=1)
d.line([(762, 110), (762, 668)], fill=(215, 208, 188), width=1)

def stamp(x, y, w, h, title, place, date, color, angle_note=""):
    d.rounded_rectangle([x, y, x+w, y+h], radius=6, outline=color, width=3)
    d.rounded_rectangle([x+5, y+5, x+w-5, y+h-5], radius=4, outline=color, width=1)
    d.text((x+w//2, y+8), title, font=f(SANS_B, 12), fill=color, anchor="mt")
    d.text((x+w//2, y+26), place, font=f(SANS, 9), fill=color, anchor="mt")
    d.text((x+w//2, y+42), date, font=f(MONO_B, 13), fill=color, anchor="mt")
    if angle_note:
        d.text((x+w//2, y+h-16), angle_note, font=f(SANS, 8), fill=color, anchor="mt")

stamp(576, 126, 172, 84, "DEPARTURE", "THALVARRA • PORT SENN FERRY", "18 JUL 2023", NAVY, "EXIT 07:40")
stamp(776, 126, 172, 84, "ARRIVAL", "FREE CITY OF BELLMAR", "18 JUL 2023", TEAL, "HARBOUR GATE")
stamp(576, 232, 172, 84, "DEPARTURE", "FREE CITY OF BELLMAR", "25 JUL 2023", TEAL, "HARBOUR GATE")
stamp(776, 232, 172, 84, "ARRIVAL", "THALVARRA • PORT SENN", "25 JUL 2023", NAVY, "RETURN FERRY")
stamp(576, 338, 172, 84, "ARRIVAL", "KINGDOM OF OSTRAVIA", "02 OCT 2024", RED, "KELD PASS • 7 DAYS")
stamp(776, 338, 172, 84, "DEPARTURE", "KINGDOM OF OSTRAVIA", "09 OCT 2024", RED, "KELD PASS")

# visa condition box
vy = 444
d.rectangle([576, vy, 948, vy+92], outline=NAVY, width=1, fill=(255, 252, 240))
d.text((588, vy+8), "OSTRAVIA TRANSIT VISA  •  No. OV-4471", font=f(SANS_B, 11), fill=NAVY)
d.text((588, vy+28), "Valid 01 OCT – 31 OCT 2024  •  Single entry  •  Fee 20 OST", font=f(SANS, 10), fill=INK)
d.text((588, vy+46), "Condition: holder must leave via Keld Pass before", font=f(SANS, 10), fill=INK)
d.text((588, vy+62), "nightfall; no overnight stay in the pass zone.", font=f(SANS, 10), fill=INK)

# second endorsement small
d.text((576, 556), "This passport contains 32 pages. If found, return to", font=f(SANS, 9), fill=GREY)
d.text((576, 570), "the nearest Thalvarran consulate. The bearer is a", font=f(SANS, 9), fill=GREY)
d.text((576, 584), "citizen of the Republic of Thalvarra.", font=f(SANS, 9), fill=GREY)
d.text((762, 660), "4  •  5", font=f(SANS, 10), fill=GREY, anchor="mt")

out = Path(__file__).resolve().parent / "entry.png"
img.save(out, optimize=True)
print(f"saved {out} {img.size} {out.stat().st_size} bytes")

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, random

W = H = 1024
random.seed(7)
img = Image.new("RGB", (W, H), (58, 62, 66))
d = ImageDraw.Draw(img, "RGBA")
# desk texture
for _ in range(2600):
    x, y = random.randrange(W), random.randrange(H)
    v = random.randrange(-8, 9)
    d.point((x, y), fill=(58+v, 62+v, 66+v))
# book shadow + pages
d.rounded_rectangle([62, 88, 962, 936], 10, fill=(30, 30, 32))
d.rounded_rectangle([52, 78, 972, 926], 10, fill=(238, 240, 236))
# centre fold shading
for i in range(26):
    a = int(70 * (1 - i/26))
    d.line([(512-i, 84), (512-i, 920)], fill=(120, 125, 120, a))
    d.line([(512+i, 84), (512+i, 920)], fill=(255, 255, 255, a//2))
d.line([(512, 80), (512, 924)], fill=(150, 152, 148), width=2)

F = "/usr/share/fonts/truetype/dejavu/"
def f(name, s): return ImageFont.truetype(F+name, s)
sans, sansb = "DejaVuSans.ttf", "DejaVuSans-Bold.ttf"
serifb, mono = "DejaVuSerif-Bold.ttf", "DejaVuSansMono.ttf"
navy = (18, 38, 74); ink = (28, 30, 34); grey = (105, 108, 112)

def guilloche(cx, cy, r, col):
    for k in range(7):
        rr = r - k*7
        d.ellipse([cx-rr, cy-rr*0.62, cx+rr, cy+rr*0.62], outline=col+(38,), width=1)
guilloche(282, 520, 210, (90, 150, 170))
guilloche(742, 500, 200, (120, 160, 140))
for x in range(70, 955, 14):
    d.line([(x, 96), (x+60, 910)], fill=(120, 170, 185, 14), width=1)

# ---- LEFT: data page ----
LX = 84
d.text((LX, 104), "REPUBLIC OF SORAVIA", font=f(serifb, 25), fill=navy)
d.text((LX, 134), "SORAVIAN PASSPORT  ·  PASS", font=f(sansb, 12), fill=grey)
# small crest: anchor in circle
d.ellipse([448, 100, 488, 140], outline=navy, width=2)
d.text((458, 108), "S", font=f(serifb, 22), fill=navy)
d.line([(LX, 158), (488, 158)], fill=navy, width=2)

# portrait box
px0, py0, px1, py1 = LX, 176, 228, 356
d.rectangle([px0, py0, px1, py1], fill=(203, 214, 220), outline=(70, 80, 90), width=2)
# portrait: woman, dark tied hair, navy uniform
cx = (px0+px1)//2
d.ellipse([cx-34, py0+22, cx+34, py0+108], fill=(232, 196, 168))          # face
d.pieslice([cx-38, py0+10, cx+38, py0+86], 180, 360, fill=(38, 30, 26))    # hair top
d.rectangle([cx-38, py0+44, cx-28, py0+104], fill=(38, 30, 26))
d.rectangle([cx+28, py0+44, cx+38, py0+104], fill=(38, 30, 26))
d.ellipse([cx-14, py0+58, cx-6, py0+66], fill=(30, 26, 24))               # eyes
d.ellipse([cx+6, py0+58, cx+14, py0+66], fill=(30, 26, 24))
d.line([(cx-10, py0+84), (cx+10, py0+84)], fill=(150, 90, 80), width=2)   # mouth
d.polygon([(px0+8, py1), (cx-40, py0+118), (cx+40, py0+118), (px1-8, py1)], fill=(24, 42, 78))  # uniform
d.polygon([(cx-12, py0+118), (cx+12, py0+118), (cx, py0+142)], fill=(240, 240, 238))             # shirt V
d.rectangle([cx-44, py0+128, cx-30, py0+136], fill=(212, 175, 55))        # epaulette L
d.rectangle([cx+30, py0+128, cx+44, py0+136], fill=(212, 175, 55))        # epaulette R
d.text((px0+2, py1+6), "KORVANE, E. M.", font=f(sans, 10), fill=grey)

fields = [
    ("Surname / Etternamn", "KORVANE"),
    ("Given names / Fornamn", "ELENA MIRA"),
    ("Date of birth / Fodselsdato", "14 MAR 1992"),
    ("Place of birth / Fodestad", "SORAVIA CITY"),
    ("Sex / Kjonn", "F"),
    ("Nationality / Nasjonalitet", "SORAVIAN"),
    ("Passport No / Passnr", "SOR8847392"),
    ("Date of issue / Utferda", "03 JUN 2021"),
    ("Date of expiry / Gyldig til", "02 JUN 2031"),
    ("Authority / Styresmakt", "MINISTRY OF THE INTERIOR"),
    ("Occupation / Yrke", "FERRY OFFICER"),
]
fx, fy = 244, 176
for label, val in fields:
    d.text((fx, fy), label, font=f(sans, 9), fill=grey)
    d.text((fx, fy+12), val, font=f(sansb, 13), fill=ink)
    fy += 38
# endorsement — the telling detail
d.rectangle([LX, 612, 488, 676], outline=(150, 60, 50), width=2)
d.text((LX+10, 620), "ENDORSEMENT / MERKNAD", font=f(sansb, 11), fill=(150, 60, 50))
d.text((LX+10, 636), "Valid for maritime travel only within", font=f(sans, 12), fill=ink)
d.text((LX+10, 650), "the Soravian Archipelago. Air travel", font=f(sans, 12), fill=ink)
d.text((LX+10, 664), "requires separate endorsement.", font=f(sans, 12), fill=ink)
# signature squiggle + fee stamp
d.text((LX, 692), "Holder's signature", font=f(sans, 9), fill=grey)
pts = [(LX+4+i*3, 722 + int(9*math.sin(i/2.6))) for i in range(44)]
d.line(pts, fill=(30, 40, 90), width=2)
d.rectangle([352, 690, 488, 736], outline=(40, 90, 140), width=2)
d.text((362, 698), "FEE PAID  40 SOR", font=f(sansb, 12), fill=(40, 90, 140))
d.text((362, 716), "03 JUN 2021 · SORAVIA CITY", font=f(sans, 9), fill=(40, 90, 140))
# MRZ
d.rectangle([LX, 760, 488, 830], fill=(245, 246, 244), outline=(170, 172, 168))
d.text((LX+8, 770), "P<SOR<KORVANE<<ELENA<MIRA<<<<<<<<<<<<", font=f(mono, 14), fill=ink)
d.text((LX+8, 794), "SOR8847392SOR9203144F3106024<<<<<<<<<", font=f(mono, 14), fill=ink)
d.text((LX, 844), "If found, return to the nearest Soravian harbour office.", font=f(sans, 10), fill=grey)

# ---- RIGHT: visas / stamps ----
RX = 536
d.text((RX, 104), "VISAS / VISUM", font=f(serifb, 22), fill=navy)
d.line([(RX, 138), (940, 138)], fill=navy, width=2)
d.text((RX, 148), "Entry and exit stamps · Inn- og utreise", font=f(sans, 11), fill=grey)

def stamp(x, y, w, h, lines, col, angle, oval=False):
    s = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(s)
    if oval:
        sd.ellipse([2, 2, w-3, h-3], outline=col+(210,), width=3)
        sd.ellipse([10, 10, w-11, h-11], outline=col+(150,), width=1)
    else:
        sd.rounded_rectangle([2, 2, w-3, h-3], 6, outline=col+(210,), width=3)
        sd.rounded_rectangle([9, 9, w-10, h-10], 4, outline=col+(150,), width=1)
    ty = 16
    for i, (t, sz, b) in enumerate(lines):
        fo = f(sansb if b else sans, sz)
        tw = sd.textlength(t, font=fo)
        sd.text(((w-tw)/2, ty), t, font=fo, fill=col+(215,))
        ty += sz + 5
    s = s.rotate(angle, expand=True, resample=Image.BICUBIC)
    img.paste(s, (x, y), s)

blue, green, black = (30, 70, 150), (25, 110, 70), (35, 35, 40)
stamp(556, 196, 176, 104, [("KESTREL ISLES", 13, True), ("ENTRY", 11, False), ("18 SEP 2022", 14, True), ("PORT SAREN", 10, False)], blue, -6)
stamp(752, 210, 176, 104, [("KESTREL ISLES", 13, True), ("EXIT", 11, False), ("02 OCT 2022", 14, True), ("PORT SAREN", 10, False)], blue, 4)
stamp(570, 356, 190, 104, [("TAVARIA", 14, True), ("ADMITTED · 30 DAYS", 10, False), ("11 MAY 2023", 14, True), ("KELD HAVEN FERRY", 10, False)], green, 3, oval=True)
stamp(766, 372, 176, 104, [("TAVARIA", 14, True), ("DEPARTED", 11, False), ("28 MAY 2023", 14, True), ("KELD HAVEN", 10, False)], green, -4, oval=True)
stamp(556, 518, 176, 104, [("MIRLAND", 14, True), ("ENTRY BY SEA", 10, False), ("07 JAN 2024", 14, True), ("NORDHAVN PIER 4", 10, False)], black, -3)
stamp(750, 532, 190, 104, [("MIRLAND", 14, True), ("EXIT · CREW LIST 118", 9, False), ("19 JAN 2024", 14, True), ("NORDHAVN", 10, False)], black, 5)
# harbour dues sticker
d.rectangle([556, 682, 760, 742], fill=(250, 244, 214), outline=(160, 140, 60), width=2)
d.text((566, 690), "HARBOUR DUES PAID", font=f(sansb, 12), fill=(120, 100, 30))
d.text((566, 708), "12 SOR · 07 JAN 2024 · NORDHAVN", font=f(sans, 10), fill=(120, 100, 30))
d.text((566, 724), "Soravian Archipelago Free Movement Zone", font=f(sans, 9), fill=(120, 100, 30))
d.text((RX, 770), "This passport remains the property of the", font=f(sans, 11), fill=grey)
d.text((RX, 788), "Republic of Soravia.", font=f(sans, 11), fill=grey)
d.text((RX, 876), "Page 7", font=f(sans, 10), fill=grey)
d.text((452, 876), "Page 6", font=f(sans, 10), fill=grey)

img = img.filter(ImageFilter.GaussianBlur(0.4))
img.save("/home/hatch/workspace/makefun/the-passport-page-of-a-countr-2-20261121-0318-entry-v2/entry.png", optimize=True)
print("saved", img.size)

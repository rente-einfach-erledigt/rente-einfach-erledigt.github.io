#!/usr/bin/env python3
"""Profil-Raster-Vorschau fuer Instagram (3 Spalten, Kacheln 3:4 wie im Profil).

Aufruf:  python3 grid.py grid.json raster.png
grid.json = [ {"bild": "posts/<id>/folie_1.png", "tag": "Di 18:00", "status": "geplant"}, ... ]
  Reihenfolge: NEUESTER zuerst (so wie im Profil oben links). status "gepostet" wird leicht abgedunkelt,
  "geplant"/"offen" bekommt ein Etikett mit tag.
Hilfsfunktion fuer die Bewertung:  python3 grid.py --farben grid.json  -> mittlere Farbe + Helligkeit je Kachel
"""
import json, sys
from PIL import Image, ImageDraw, ImageFont, ImageStat

TW, TH, GAP = 360, 480, 6
def font(sz):
    for p in ["/usr/share/fonts/opentype/inter/Inter-SemiBold.otf", "fonts/Inter-SemiBold.otf"]:
        try: return ImageFont.truetype(p, sz)
        except OSError: pass
    return ImageFont.load_default()

def tile(path):
    im = Image.open(path).convert("RGB"); w, h = im.size
    tw = min(w, int(h * 3 / 4)); th = int(tw * 4 / 3)
    x0 = (w - tw) // 2; y0 = (h - th) // 2
    return im.crop((x0, y0, x0 + tw, y0 + th)).resize((TW, TH), Image.LANCZOS)

def build(items, out):
    rows = (len(items) + 2) // 3
    sheet = Image.new("RGB", (3 * TW + 2 * GAP, rows * TH + (rows - 1) * GAP), (255, 255, 255))
    f = font(22)
    for i, it in enumerate(items):
        t = tile(it["bild"]); d = ImageDraw.Draw(t)
        if it.get("status") == "gepostet":
            t = Image.blend(t, Image.new("RGB", t.size, (255, 255, 255)), 0.25)
        elif it.get("tag"):
            tw = d.textlength(it["tag"], font=f) + 24
            d.rounded_rectangle([10, TH - 46, 10 + tw, TH - 10], 10, fill=(17, 35, 27)); d.text((22, TH - 41), it["tag"], font=f, fill=(242, 179, 61))
        sheet.paste(t, ((i % 3) * (TW + GAP), (i // 3) * (TH + GAP)))
    sheet.save(out, optimize=True); print(out)

def farben(items):
    for it in items:
        st = ImageStat.Stat(tile(it["bild"]).resize((60, 80))); r, g, b = (int(x) for x in st.mean)
        print(f'{it["bild"]}: mittel=#{r:02X}{g:02X}{b:02X} hell={int(0.299*r+0.587*g+0.114*b)}')

if __name__ == "__main__":
    if sys.argv[1] == "--farben": farben(json.load(open(sys.argv[2])))
    else: build(json.load(open(sys.argv[1])), sys.argv[2])

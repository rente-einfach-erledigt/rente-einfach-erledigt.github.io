#!/usr/bin/env python3
"""Rendert ein Karussell im Design von @rente.einfach.erledigt.

Aufruf:  python3 render.py posts/<post-id>/post.json
Ergebnis: posts/<post-id>/folie_1.png/.jpg ... folie_N.png/.jpg (1080x1350); hochgeladen werden die .jpg

post.json -> {"slides": [ {Folie}, ... ]}
Felder pro Folie (alle optional ausser kick):
  kick  : kleine Ueberschrift in Gold (GROSSBUCHSTABEN)
  pre   : Satz vor der grossen Zahl/dem Wort (z. B. "Kommentiere")
  big   : grosse Zahl oder Wort in Gold (z. B. "bis zu 540 €")
  cta   : true -> big wird als goldener Button gezeichnet (letzte Folie)
  head  : fette Ueberschrift
  body  : Fliesstext, "\n" fuer Absatz
  swipe : true -> "Wischen →" unten (erste Folie)
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
GREEN = (15, 59, 46); AMBER = (242, 179, 61); CREAM = (250, 246, 236); SOFT = (190, 210, 198)
HANDLE = "rente.einfach.erledigt"
MAXW = 880
FONT_DIRS = ["/usr/share/fonts/opentype/inter/", os.path.join(os.path.dirname(__file__), "fonts/")]

def F(name, size):
    for d in FONT_DIRS:
        p = os.path.join(d, name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    fallback = {"InterDisplay-ExtraBold.otf": "DejaVuSans-Bold.ttf", "Inter-SemiBold.otf": "DejaVuSans-Bold.ttf", "Inter-Medium.otf": "DejaVuSans.ttf"}
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/" + fallback[name], size)

BOLD, MED, SEMI = "InterDisplay-ExtraBold.otf", "Inter-Medium.otf", "Inter-SemiBold.otf"

def wrap(d, text, font, maxw=MAXW):
    lines = []
    for para in text.split("\n"):
        cur = ""
        for w in para.split():
            t = (cur + " " + w).strip()
            if d.textlength(t, font=font) <= maxw:
                cur = t
            else:
                lines.append(cur); cur = w
        lines.append(cur)
    return lines

def fit(d, text, name, size, maxw=MAXW):
    while size > 40 and max(d.textlength(w, font=F(name, size)) for w in text.split()) > maxw:
        size -= 4
    return F(name, size)

def check(d, x, y, sz, col, w):
    pts = [(x, y + 0.45 * sz), (x + 0.3 * sz, y + 0.75 * sz), (x + 0.9 * sz, y + 0.12 * sz)]
    d.line(pts, fill=col, width=w, joint="curve")
    for p in (pts[0], pts[2]):
        d.ellipse([p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2], fill=col)

def layout(d, s, y, draw=True):
    def txt(xy, t, f, c):
        if draw: d.text(xy, t, font=f, fill=c)
    if s.get("kick"):
        txt((100, y), s["kick"].upper(), F(SEMI, 34), AMBER); y += 80
    if s.get("pre"):
        f = fit(d, s["pre"], BOLD, 72)
        for ln in wrap(d, s["pre"], f):
            txt((100, y), ln, f, CREAM); y += int(f.size * 1.18)
        y += 10
    if s.get("big"):
        f = fit(d, s["big"], BOLD, 190 if len(s["big"]) < 9 else 150, MAXW - 80 if s.get("cta") else MAXW)
        if s.get("cta"):
            tw = d.textlength(s["big"], font=f); pad = 40
            if draw: d.rounded_rectangle([100, y, 100 + tw + 2 * pad, y + f.size + 60], radius=36, fill=AMBER)
            txt((100 + pad, y + 18), s["big"], f, GREEN); y += f.size + 110
        else:
            txt((100, y), s["big"], f, AMBER); y += int(f.size * 1.25)
    if s.get("head"):
        f = fit(d, s["head"], BOLD, 92)
        for ln in wrap(d, s["head"], f):
            txt((100, y), ln, f, CREAM); y += int(f.size * 1.18)
        y += 40
    if s.get("body"):
        f = F(MED, 50)
        for ln in wrap(d, s["body"], f):
            txt((100, y), ln, f, CREAM); y += int(50 * 1.35)
    return y

def render(spec_path):
    spec = json.load(open(spec_path, encoding="utf-8"))
    out = os.path.dirname(spec_path)
    slides = spec["slides"]
    files = []
    for i, s in enumerate(slides, 1):
        img = Image.new("RGB", (W, H), GREEN); d = ImageDraw.Draw(img)
        check(d, 100, 92, 46, AMBER, 10)
        d.text((165, 98), HANDLE, font=F(SEMI, 30), fill=CREAM)
        d.text((W - 100, 98), f"{i}/{len(slides)}", font=F(MED, 30), fill=SOFT, anchor="ra")
        h = layout(d, s, 0, draw=False)
        if h > H - 420:
            raise SystemExit(f"Folie {i} hat zu viel Text ({h}px). Bitte kuerzen.")
        layout(d, s, max(260, (H - h) // 2 - 40))
        if s.get("swipe"):
            d.text((100, H - 150), "Wischen  →", font=F(SEMI, 40), fill=AMBER)
        p = os.path.join(out, f"folie_{i}.png")
        img.save(p, optimize=True); files.append(p)
        img.save(os.path.join(out, f"folie_{i}.jpg"), quality=92, optimize=True)  # JPG fuer TikTok & Co.
    print("\n".join(files))

if __name__ == "__main__":
    render(sys.argv[1])

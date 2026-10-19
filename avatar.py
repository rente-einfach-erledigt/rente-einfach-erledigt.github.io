#!/usr/bin/env python3
"""Zeichnet illustrierte Beispielfiguren (flacher Illustrationsstil, keine Fotos, keine echten Personen).

avatar(spec, size) -> RGBA-Bild (quadratisch)
spec = {
  "haut": "hell" | "mittel" | "oliv" | "braun" | "dunkel",
  "haar": "kurz" | "lang" | "dutt" | "locken" | "glatze" | "seitenscheitel" | "zopf",
  "haarfarbe": "schwarz" | "braun" | "blond" | "rot" | "grau",
  "kleidung": "#RRGGBB" oder Name (gruen, blau, gold, rot, grau, weiss),
  "brille": true/false, "bart": "kein" | "kurz" | "voll", "ohrringe": true/false,
  "kinder": [ {"haut":..., "haar":..., "haarfarbe":..., "kleidung":...}, ... ]   # optional, bis zu 3 kleine Figuren
  "hintergrund": "#RRGGBB" (optional)
}
Testen: python3 avatar.py  -> schreibt avatar_test.png
"""
from PIL import Image, ImageDraw

SKIN = {"hell": (246, 214, 190), "mittel": (226, 180, 146), "oliv": (205, 160, 120), "braun": (160, 110, 76), "dunkel": (110, 72, 50)}
HAIR = {"schwarz": (34, 30, 28), "braun": (96, 62, 40), "blond": (222, 182, 108), "rot": (170, 78, 40), "grau": (178, 178, 172)}
CLOTH = {"gruen": (34, 110, 84), "blau": (52, 92, 150), "gold": (226, 160, 50), "rot": (186, 70, 60), "grau": (110, 120, 118), "weiss": (236, 236, 228),
         "lila": (120, 86, 150), "senf": (196, 150, 40), "petrol": (30, 110, 120)}

def _col(v, table, default):
    if isinstance(v, (list, tuple)): return tuple(v)
    if isinstance(v, str) and v.startswith("#") and len(v) == 7: return tuple(int(v[i:i + 2], 16) for i in (1, 3, 5))
    return table.get(v, default)

def shade(c, f): return tuple(max(0, min(255, int(x * f))) for x in c)

def _person(d, cx, top, s, spec, child=False):
    """Zeichnet eine Buestenfigur. cx = Mitte, top = Oberkante Kopf, s = Kopfbreite."""
    skin = _col(spec.get("haut", "mittel"), SKIN, SKIN["mittel"])
    hair = _col(spec.get("haarfarbe", "braun"), HAIR, HAIR["braun"])
    cloth = _col(spec.get("kleidung", "blau"), CLOTH, CLOTH["blau"])
    style = spec.get("haar", "kurz")
    hw, hh = s, s * 1.18                      # Kopf
    hx0, hy0 = cx - hw / 2, top; hx1, hy1 = cx + hw / 2, top + hh
    # Koerper / Schultern
    bw = s * (2.1 if not child else 1.8); by = hy1 + s * 0.12
    d.rounded_rectangle([cx - bw / 2, by + s * 0.18, cx + bw / 2, by + s * 1.9], radius=int(s * 0.55), fill=cloth)
    # Hals
    d.rounded_rectangle([cx - s * 0.17, hy1 - s * 0.2, cx + s * 0.17, by + s * 0.34], radius=int(s * 0.08), fill=shade(skin, 0.9))
    # V-Ausschnitt
    d.polygon([(cx - s * 0.26, by + s * 0.2), (cx + s * 0.26, by + s * 0.2), (cx, by + s * 0.55)], fill=shade(skin, 0.9))
    d.line([(cx - s * 0.3, by + s * 0.18), (cx, by + s * 0.58), (cx + s * 0.3, by + s * 0.18)], fill=shade(cloth, 0.82), width=max(2, int(s * 0.05)), joint="curve")
    # Haare hinten
    if style in ("lang", "zopf"):
        d.rounded_rectangle([hx0 - s * 0.1, hy0 + s * 0.05, hx1 + s * 0.1, hy1 + s * (0.55 if style == "lang" else 0.2)], radius=int(s * 0.45), fill=hair)
    if style == "locken":
        for i in range(9):
            import math
            a = math.pi * (0.95 + 1.1 * i / 8); r = s * 0.62
            px, py = cx + r * math.cos(a) * 0.95, top + s * 0.55 + r * math.sin(a) * 0.85
            d.ellipse([px - s * 0.24, py - s * 0.24, px + s * 0.24, py + s * 0.24], fill=hair)
    # Ohren
    for sx in (-1, 1):
        ex = cx + sx * hw / 2
        d.ellipse([ex - s * 0.09, top + s * 0.5, ex + s * 0.09, top + s * 0.74], fill=shade(skin, 0.95))
        if spec.get("ohrringe"): d.ellipse([ex - s * 0.04, top + s * 0.74, ex + s * 0.04, top + s * 0.82], fill=(242, 179, 61))
    # Kopf
    d.ellipse([hx0, hy0, hx1, hy1], fill=skin)
    # Bart
    beard = spec.get("bart", "kein")
    if beard in ("kurz", "voll"):
        bh = 0.3 if beard == "kurz" else 0.45
        d.chord([hx0 + s * 0.04, hy0 + hh * (0.48 - bh * 0.4), hx1 - s * 0.04, hy1 + s * 0.04], 10, 170, fill=hair if beard == "voll" else shade(hair, 1.0))
        d.ellipse([cx - s * 0.2, top + hh * 0.66, cx + s * 0.2, top + hh * 0.8], fill=skin)  # Mundbereich frei
    # Haare oben
    if style in ("kurz", "seitenscheitel", "lang", "zopf", "dutt"):
        d.chord([hx0 - s * 0.03, hy0 - s * 0.06, hx1 + s * 0.03, hy0 + hh * 0.7], 180, 360, fill=hair)
        if style == "seitenscheitel":
            d.polygon([(hx0, hy0 + hh * 0.3), (cx + s * 0.1, hy0 + s * 0.02), (hx1 + s * 0.02, hy0 + hh * 0.26), (hx1, hy0 + hh * 0.38), (cx - s * 0.05, hy0 + hh * 0.2)], fill=hair)
        else:
            d.pieslice([hx0 - s * 0.02, hy0 + s * 0.02, cx + s * 0.25, hy0 + hh * 0.6], 180, 300, fill=hair)
    if style == "dutt": d.ellipse([cx - s * 0.24, hy0 - s * 0.36, cx + s * 0.24, hy0 + s * 0.08], fill=hair)
    if style == "zopf": d.ellipse([hx1 - s * 0.05, hy0 + hh * 0.35, hx1 + s * 0.28, hy0 + hh * 0.62], fill=hair)
    if style == "locken":
        import math
        for i in range(7):
            a = math.pi * (1.05 + 0.9 * i / 6)
            px, py = cx + s * 0.45 * math.cos(a), top + s * 0.42 + s * 0.42 * math.sin(a)
            d.ellipse([px - s * 0.22, py - s * 0.22, px + s * 0.22, py + s * 0.22], fill=hair)
    if style == "glatze":
        d.arc([hx0 + s * 0.12, hy0 + s * 0.08, hx1 - s * 0.12, hy0 + s * 0.5], 215, 325, fill=shade(skin, 1.08), width=max(2, int(s * 0.04)))  # Glanzlicht
    # Gesicht
    ink = (40, 34, 32); ey = top + hh * 0.52
    for sx in (-1, 1):
        ex = cx + sx * s * 0.2
        d.ellipse([ex - s * 0.045, ey - s * 0.055, ex + s * 0.045, ey + s * 0.055], fill=ink)
        d.arc([ex - s * 0.11, ey - s * 0.19, ex + s * 0.11, ey - s * 0.05], 200, 340, fill=shade(hair, 0.8) if style != "glatze" else ink, width=max(2, int(s * 0.035)))
        d.ellipse([ex - s * 0.08 + sx * s * 0.02, ey + s * 0.11, ex + s * 0.08 + sx * s * 0.02, ey + s * 0.19], fill=shade(skin, 0.93))  # Wangen
    d.arc([cx - s * 0.05, ey + s * 0.02, cx + s * 0.05, ey + s * 0.16], 20, 160, fill=shade(skin, 0.75), width=max(2, int(s * 0.03)))  # Nase
    d.arc([cx - s * 0.15, ey + s * 0.1, cx + s * 0.15, ey + s * 0.32], 25, 155, fill=(150, 60, 55), width=max(3, int(s * 0.04)))  # Laecheln
    if spec.get("brille"):
        for sx in (-1, 1):
            ex = cx + sx * s * 0.2
            d.rounded_rectangle([ex - s * 0.14, ey - s * 0.1, ex + s * 0.14, ey + s * 0.1], radius=int(s * 0.05), outline=ink, width=max(2, int(s * 0.035)))
        d.line([(cx - s * 0.06, ey - s * 0.02), (cx + s * 0.06, ey - s * 0.02)], fill=ink, width=max(2, int(s * 0.03)))

def avatar(spec, size=520):
    SS = 3; S = size * SS
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    bg = _col(spec.get("hintergrund", "#16503F"), {}, (22, 80, 63))
    d.ellipse([0, 0, S - 1, S - 1], fill=bg + (255,))
    fig = Image.new("RGBA", (S, S), (0, 0, 0, 0)); fd = ImageDraw.Draw(fig)
    kids = spec.get("kinder", [])[:3]
    main_cx = S * (0.5 if not kids else 0.4)
    _person(fd, main_cx, S * 0.2, S * 0.34, spec)
    for i, k in enumerate(kids):
        kx = S * (0.74 + 0.0 * i) if len(kids) == 1 else S * (0.66 + 0.17 * i)
        _person(fd, kx, S * (0.46 + 0.04 * (i % 2)), S * 0.2, k, child=True)
    mask = Image.new("L", (S, S), 0); ImageDraw.Draw(mask).ellipse([0, 0, S - 1, S - 1], fill=255)
    clipped = Image.new("RGBA", (S, S), (0, 0, 0, 0)); clipped.paste(fig, (0, 0), Image.composite(fig.getchannel("A"), Image.new("L", (S, S), 0), mask))
    img.alpha_composite(clipped)
    return img.resize((size, size), Image.LANCZOS)

if __name__ == "__main__":
    specs = [
        {"haut": "hell", "haar": "lang", "haarfarbe": "braun", "kleidung": "gold", "ohrringe": True, "kinder": [{"haut": "hell", "haar": "zopf", "haarfarbe": "blond", "kleidung": "rot"}, {"haut": "hell", "haar": "kurz", "haarfarbe": "braun", "kleidung": "blau"}]},
        {"haut": "mittel", "haar": "seitenscheitel", "haarfarbe": "grau", "kleidung": "blau", "brille": True, "bart": "kurz"},
        {"haut": "braun", "haar": "locken", "haarfarbe": "schwarz", "kleidung": "petrol"},
        {"haut": "oliv", "haar": "dutt", "haarfarbe": "schwarz", "kleidung": "lila", "brille": True},
        {"haut": "dunkel", "haar": "glatze", "haarfarbe": "schwarz", "kleidung": "senf", "bart": "voll"},
        {"haut": "hell", "haar": "kurz", "haarfarbe": "blond", "kleidung": "gruen", "hintergrund": "#F2B33D"},
    ]
    row = Image.new("RGBA", (6 * 320, 320), (250, 246, 236, 255))
    for i, s in enumerate(specs): row.alpha_composite(avatar(s, 300), (i * 320 + 10, 10))
    row.convert("RGB").save("avatar_test.png"); print("avatar_test.png")

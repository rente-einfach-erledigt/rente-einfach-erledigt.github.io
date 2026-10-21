#!/usr/bin/env python3
"""Rendert ein Kurzvideo (1080x1920, 30 fps, MP4 mit eigener Musik) im Design von @rente.einfach.erledigt.

Aufruf:  python3 video.py videos/<id>/video.json
Ergebnis: videos/<id>/video_A.mp4  (Instagram: Ende mit Kommentar-Wort)
          videos/<id>/video_B.mp4  (TikTok, YouTube Shorts, Facebook, Threads: Ende "Link im Profil")
          videos/<id>/cover.jpg    (Titelbild = erstes Videobild; Szene 1 zeigt den Hook ab Bild 1)

video.json:
{
  "zielgruppe": "familien" | "riester" | "selbststaendige" | "einsteiger" | "grundlagen",
  "wort": "KIND",                       # Kommentar-Wort fuer Version A
  "scenes": [ {Szene}, ... ]            # 5-9 Szenen, gesamt 18-35 s
}
Szenen (dur = Sekunden, optional; sonst Standard):
  {"type":"hook", "kick":"DEIN VORSPRUNG", "text":"Alle warten auf 2027.\n*Du startest jetzt.*"}
        *Wort* = gold hervorgehoben, \n = neue Zeile. Max ~10 Woerter.
  {"type":"counter", "label":"Kinderzulage", "pre":"bis zu", "value":300, "unit":"€", "sub":"pro Kind und Jahr"}
  {"type":"persona", "name":"Lisa", "alter":31, "kinder":[2,5], "beitrag":150, "rente":67, "job":"Erzieherin", "figur":{...}}
        BEISPIELRECHNUNG: rechnet Grund-/Kinderzulage 2027 sowie eigene Beitraege + Zulagen bis zur Rente selbst
        (ohne Kursentwicklung). "figur" (optional, empfohlen) = illustrierte Figur, Optionen siehe avatar.py.
  {"type":"bars", "title":"Im Jahr 2027", "items":[{"label":"Du zahlst","value":1800},{"label":"Staat legt drauf","value":1140,"gold":true}]}
  {"type":"myth", "myth":"Riester muss ich kündigen.", "fact":"Weiterlaufen lassen oder wechseln. Kündigen kann Förderung kosten."}
  {"type":"list", "title":"3 Dinge, die du wissen musst", "items":["…","…","…"]}
  {"type":"story", "name":"Sandra, 44", "rolle":"Pflegekraft, 2 Kinder", "zitat":"Ich hab ewig gewartet. Jetzt weiß ich, *wie viel der Staat mir dazulegt.*",
   "figur":{"haut":"hell","haar":"lang","haarfarbe":"braun","kleidung":"gold","brille":false,"kinder":[{...}]}}
        Illustrierte Beispielfigur erzaehlt in Ich-Form (Optionen der figur: siehe avatar.py). Wird automatisch als
        „Beispielfigur · Illustration“ gekennzeichnet. Nie als echte Kundin/echter Kunde ausgeben, keine erfundenen Ergebnisse.
  {"type":"countdown"}                  # zeigt die echten Tage bis 01.01.2027
  {"type":"text", "kick":"…", "text":"…"}   # ruhige Textszene
  {"type":"cta", "kick":"SICHERE DIR DEN VORSPRUNG", "text":"Rechne in 30 Sekunden aus,\nwie viel dir zusteht."}
        letzte Szene. Version A: Button "Kommentiere <WORT>", Version B: "Link im Profil ✓".
Pflicht: Hinweiszeile "Keine Anlageberatung …" wird in der letzten Szene automatisch eingeblendet.
"""
import json, math, os, subprocess, sys, datetime, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from avatar import avatar

W, H, FPS = 1080, 1920, 30
GREEN = (15, 59, 46); GREEN2 = (22, 80, 63); AMBER = (242, 179, 61); CREAM = (250, 246, 236); SOFT = (190, 210, 198); DEEP = (9, 38, 30)
X0, MAXW = 96, 840            # linker Rand, max. Textbreite (rechts Platz fuer App-Buttons)
TOP, BOTTOM = 330, 1480       # sichere Zone (oben Header, unten App-UI)
HANDLE = "rente.einfach.erledigt"
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIRS = ["/usr/share/fonts/opentype/inter/", os.path.join(HERE, "fonts/")]
BOLD, SEMI, MED = "InterDisplay-ExtraBold.otf", "Inter-SemiBold.otf", "Inter-Medium.otf"
DISCLAIMER = "Keine Anlageberatung. Keine Beitragsgarantie, der Wert kann schwanken."

ACCENT = {"familien": (255, 196, 92), "riester": AMBER, "selbststaendige": (246, 170, 60), "einsteiger": (255, 205, 80), "grundlagen": AMBER}
SCALE = {"riester": 1.08}      # 40+: etwas groessere Schrift

_fc = {}
def F(name, size):
    k = (name, int(size))
    if k not in _fc:
        for d in FONT_DIRS:
            p = os.path.join(d, name)
            if os.path.exists(p):
                _fc[k] = ImageFont.truetype(p, int(size)); break
        else:
            _fc[k] = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(size))
    return _fc[k]

def ease(t): t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3
def ease_io(t): t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)
def eur(v): return f"{int(round(v)):,}".replace(",", ".")

_scratch = ImageDraw.Draw(Image.new("RGB", (8, 8)))
def tlen(s, f): return _scratch.textlength(s, font=f)

# ---------- Text-Bausteine (einmal gerendert, pro Frame nur verschoben/geblendet) ----------
def rich_line_img(line, font, col, accent):
    """Zeile mit *gold* markierten Woertern als RGBA-Bild."""
    parts, gold = [], False
    for chunk in line.split("*"):
        if chunk: parts.append((chunk, gold))
        gold = not gold
    w = int(sum(tlen(p, font) for p, _ in parts)) + 4
    asc, desc = font.getmetrics()
    img = Image.new("RGBA", (max(w, 1), asc + desc + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(img); x = 0
    for p, g in parts:
        d.text((x, 0), p, font=font, fill=accent if g else col); x += tlen(p, font)
    return img

def wrap_rich(text, font, maxw):
    out = []
    for para in text.split("\n"):
        cur = ""
        for wd in para.split():
            t = (cur + " " + wd).strip()
            if tlen(t.replace("*", ""), font) <= maxw: cur = t
            else:
                out.append(cur); cur = wd
        out.append(cur)
    # Sternchen ueber Zeilenumbrueche hinweg korrekt halten
    fixed, open_ = [], False
    for ln in out:
        new_open = open_ ^ (ln.count("*") % 2 == 1)
        fixed.append(("*" if open_ else "") + ln + ("*" if new_open else ""))
        open_ = new_open
    return fixed

def fit_font(text, name, size, maxw, max_lines):
    while size > 44:
        f = F(name, size)
        lines = wrap_rich(text, f, maxw)
        if len(lines) <= max_lines and all(tlen(w.replace("*", ""), f) <= maxw for w in text.replace("\n", " ").split()):
            return f, lines
        size -= 4
    f = F(name, size); return f, wrap_rich(text, f, maxw)

def paste(frame, img, x, y, alpha=1.0):
    if alpha <= 0.01: return
    if alpha < 0.999:
        img = img.copy(); a = img.getchannel("A").point(lambda v: int(v * alpha)); img.putalpha(a)
    frame.alpha_composite(img, (int(x), int(y)))

def text_img(s, font, col):
    asc, desc = font.getmetrics()
    img = Image.new("RGBA", (int(tlen(s, font)) + 4, asc + desc + 8), (0, 0, 0, 0))
    ImageDraw.Draw(img).text((0, 0), s, font=font, fill=col); return img

def check_icon(size, col, width):
    img = Image.new("RGBA", (int(size * 1.1), int(size * 1.0)), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    pts = [(0.08 * size, 0.5 * size), (0.38 * size, 0.8 * size), (0.98 * size, 0.18 * size)]
    d.line(pts, fill=col, width=width, joint="curve")
    for p in (pts[0], pts[2]): d.ellipse([p[0] - width / 2, p[1] - width / 2, p[0] + width / 2, p[1] + width / 2], fill=col)
    return img

# ---------- Hintergrund ----------
def make_bg():
    yy, xx = np.mgrid[0:H + 400, 0:W + 400].astype(np.float32)
    g = np.exp(-(((xx - (W + 400) * 0.72) / 620) ** 2 + ((yy - (H + 400) * 0.78) / 760) ** 2))
    base = np.zeros((H + 400, W + 400, 3), np.float32) + np.array(GREEN, np.float32)
    base += g[..., None] * (np.array(AMBER, np.float32) - base) * 0.16
    g2 = np.exp(-(((xx - (W + 400) * 0.15) / 700) ** 2 + ((yy - (H + 400) * 0.1) / 600) ** 2))
    base += g2[..., None] * (np.array(GREEN2, np.float32) - base) * 0.55
    rng = np.random.default_rng(7); base += rng.normal(0, 2.2, base.shape[:2])[..., None]
    return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGB").convert("RGBA")

# ---------- Szenen ----------
class Scene:
    dur = 3.0
    def __init__(self, s, ctx): self.s = s; self.ctx = ctx; self.dur = float(s.get("dur", self.dur)); self.prep()
    def prep(self): pass
    def draw(self, fr, t): pass
    def events(self): return [(0.0, "whoosh")]

def kick_img(text, ctx):
    return text_img(text.upper(), F(SEMI, 34 * ctx["sc"]), ctx["acc"])

class Hook(Scene):
    dur = 3.2
    def prep(self):
        sc = self.ctx["sc"]
        self.k = kick_img(self.s["kick"], self.ctx) if self.s.get("kick") else None
        f, lines = fit_font(self.s["text"], BOLD, 118 * sc, MAXW, 5)
        self.lines = [rich_line_img(l, f, CREAM, self.ctx["acc"]) for l in lines]
        self.lh = int(f.size * 1.08)
        total = (self.k.height + 36 if self.k else 0) + self.lh * len(self.lines)
        self.y0 = int(TOP + (BOTTOM - TOP - total) * 0.42)
    def draw(self, fr, t):
        y = self.y0
        if self.k: paste(fr, self.k, X0, y + 20 * (1 - ease(t / .35)), ease(t / .35)); y += self.k.height + 36
        for i, im in enumerate(self.lines):
            p = ease((t - 0.18 - i * 0.22) / 0.45)
            paste(fr, im, X0, y + i * self.lh + 60 * (1 - p), p)

class Text(Hook):
    dur = 3.4
    def prep(self):
        sc = self.ctx["sc"]
        self.k = kick_img(self.s["kick"], self.ctx) if self.s.get("kick") else None
        f, lines = fit_font(self.s["text"], BOLD, 84 * sc, MAXW, 7)
        self.lines = [rich_line_img(l, f, CREAM, self.ctx["acc"]) for l in lines]
        self.lh = int(f.size * 1.18)
        total = (self.k.height + 36 if self.k else 0) + self.lh * len(self.lines)
        self.y0 = int(TOP + (BOTTOM - TOP - total) * 0.45)

class Counter(Scene):
    dur = 3.4
    def prep(self):
        sc = self.ctx["sc"]; s = self.s
        self.lab = text_img(s.get("label", "").upper(), F(SEMI, 36 * sc), self.ctx["acc"]) if s.get("label") else None
        self.pre = text_img(s.get("pre", ""), F(MED, 64 * sc), SOFT) if s.get("pre") else None
        self.unit = s.get("unit", "€"); self.val = float(s["value"])
        self.fn = F(BOLD, 250 * sc)
        while tlen(f"{eur(self.val)} {self.unit}", self.fn) > MAXW and self.fn.size > 120: self.fn = F(BOLD, self.fn.size - 10)
        self.sub = [text_img(l, F(SEMI, 60 * sc), CREAM) for l in wrap_rich(s.get("sub", ""), F(SEMI, 60 * sc), MAXW)] if s.get("sub") else []
        self.y0 = 640
    def draw(self, fr, t):
        y = self.y0
        if self.lab: paste(fr, self.lab, X0, y, ease(t / .3)); y += self.lab.height + 30
        if self.pre: paste(fr, self.pre, X0, y, ease((t - .1) / .3)); y += self.pre.height + 4
        v = self.val * ease_io((t - 0.25) / 1.3)
        num = text_img(f"{eur(v)} {self.unit}", self.fn, self.ctx["acc"])
        sc = 1 + 0.06 * math.sin(min(1, max(0, (t - 1.55) / 0.35)) * math.pi)
        if sc > 1.001: num = num.resize((int(num.width * sc), int(num.height * sc)), Image.LANCZOS)
        paste(fr, num, X0, y, ease((t - .2) / .3)); y += int(self.fn.size * 1.15) + 20
        for i, im in enumerate(self.sub): paste(fr, im, X0, y + i * 74 + 30 * (1 - ease((t - 1.5) / .4)), ease((t - 1.5) / .4))
    def events(self): return [(0.0, "whoosh"), (1.55, "pop")]

def zulagen(E, kids_ages, i):
    if E < 120: return 0.0, 0.0
    g = 0.5 * min(E, 360) + 0.25 * max(0, min(E, 1800) - 360)
    k = sum(min(E, 300) for c in kids_ages if c + 1 + i < 18)
    return g, k

class Persona(Scene):
    """Beispielrechnung fuer eine (optional illustrierte) Beispielfigur. Zahlen rechnet video.py selbst."""
    dur = 7.0
    def prep(self):
        sc = self.ctx["sc"]; s = self.s
        kids = s.get("kinder", []); m = float(s["beitrag"]); E = m * 12; age = int(s["alter"]); ra = int(s.get("rente", 67))
        g1, k1 = zulagen(E, kids, 0); bonus = 200 if age < 25 else 0
        N = max(0, ra - age - 1); tz = bonus; te = 0
        for i in range(N): g, k = zulagen(E, kids, i); tz += g + k; te += E
        self.rows = [("Grundzulage", g1)]
        if kids: self.rows.append(("Kinderzulage", k1))
        if bonus: self.rows.append(("Einsteiger-Bonus (einmalig)", bonus))
        self.tz = tz; self.te = te; self.N = N; self.ra = ra
        self.av = avatar(s["figur"], 300) if s.get("figur") else None
        chips = [f"{len(kids)} {'Kind' if len(kids) == 1 else 'Kinder'}" if kids else "keine Kinder", f"{eur(m)} € im Monat"]
        if s.get("job"): chips.insert(0, s["job"])
        self.kick = kick_img("BEISPIELRECHNUNG", self.ctx)
        self.who = text_img(f"{s['name']}, {age}", F(BOLD, (78 if self.av else 92) * sc), CREAM)
        self.chips = [text_img(c, F(SEMI, 34 * sc), DEEP) for c in chips]
        self.rf = F(SEMI, 46 * sc); self.vf = F(BOLD, 52 * sc)
        self.lab = kick_img("ZULAGEN IM JAHR 2027", self.ctx)
        self.sf = F(MED, 38 * sc); self.bf = F(BOLD, 104 * sc)
    def draw(self, fr, t):
        d = ImageDraw.Draw(fr); acc = self.ctx["acc"]; y = 300
        if self.av:
            p = ease(t / .45); paste(fr, self.av, X0 - 6, y + 30 * (1 - p), p)
            tx, ty = X0 + 330, y + 60
        else:
            tx, ty = X0, y + 120
        paste(fr, self.kick, tx, ty, ease((t - .1) / .3)); ty += self.kick.height + 14
        paste(fr, self.who, tx, ty + 20 * (1 - ease((t - .15) / .4)), ease((t - .15) / .4)); ty += self.who.height + 14
        # Chips (umbrechen, wenn zu breit)
        x = tx; maxx = X0 + MAXW
        for i, c in enumerate(self.chips):
            w = c.width + 36
            if x + w > maxx: x = tx; ty += 64
            p = ease((t - .3 - i * .12) / .3)
            if p > 0:
                pill = Image.new("RGBA", (w, 56), (0, 0, 0, 0)); ImageDraw.Draw(pill).rounded_rectangle([0, 0, w - 1, 55], 28, fill=SOFT + (255,))
                pill.alpha_composite(c, (18, 7)); paste(fr, pill, x, ty, p)
            x += w + 12
        y = max(y + 330, ty + 100)
        paste(fr, self.lab, X0, y, ease((t - .7) / .3)); y += self.lab.height + 22
        for i, (lab, v) in enumerate(self.rows):
            p = ease((t - 0.9 - i * .35) / .35)
            if p <= 0: continue
            a = int(255 * p)
            d.text((X0, y + i * 84), lab, font=self.rf, fill=CREAM + (a,))
            vs = "+ " + eur(v) + " €"; d.text((X0 + MAXW - tlen(vs, self.vf), y + i * 84 - 4), vs, font=self.vf, fill=acc + (a,))
            d.line([(X0, y + i * 84 + 68), (X0 + MAXW, y + i * 84 + 68)], fill=GREEN2 + (a,), width=2)
        y += len(self.rows) * 84 + 40
        t0 = 0.9 + len(self.rows) * .35 + .2
        p = ease((t - t0) / .5)
        if p > 0:
            card = Image.new("RGBA", (MAXW, 330), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
            cd.rounded_rectangle([0, 0, MAXW - 1, 329], 28, fill=DEEP + (235,))
            k = ease_io((t - t0) / 1.2)
            cd.text((34, 26), f"Bis {self.ra}: eigene Beiträge", font=self.sf, fill=SOFT)
            v1 = eur(self.te * k) + " €"; cd.text((MAXW - 34 - tlen(v1, self.sf), 26), v1, font=self.sf, fill=CREAM)
            cd.text((34, 76), "+ Zulagen vom Staat", font=self.sf, fill=SOFT)
            v2 = eur(self.tz * k) + " €"; cd.text((MAXW - 34 - tlen(v2, self.sf), 76), v2, font=self.sf, fill=acc)
            cd.line([(34, 134), (MAXW - 34, 134)], fill=GREEN2, width=2)
            cd.text((34, 150), eur((self.te + self.tz) * k) + " €", font=self.bf, fill=acc)
            cd.text((34, 280), "ohne Kursentwicklung · Beispielrechnung", font=F(MED, 28), fill=SOFT)
            paste(fr, card, X0, y + 40 * (1 - p), p)
    def events(self):
        ev = [(0.0, "whoosh")] + [(0.9 + i * .35, "tick") for i in range(len(self.rows))]
        ev.append((0.9 + len(self.rows) * .35 + .2, "pop")); return ev

class Bars(Scene):
    dur = 4.2
    def prep(self):
        sc = self.ctx["sc"]
        self.title = text_img(self.s.get("title", ""), F(BOLD, 72 * sc), CREAM) if self.s.get("title") else None
        self.items = self.s["items"]; self.mx = max(i["value"] for i in self.items)
        self.lf = F(SEMI, 46 * sc); self.vf = F(BOLD, 64 * sc)
    def draw(self, fr, t):
        d = ImageDraw.Draw(fr); y = 560
        if self.title: paste(fr, self.title, X0, y, ease(t / .35)); y += self.title.height + 70
        for i, it in enumerate(self.items):
            p = ease_io((t - .35 - i * .45) / .9)
            col = self.ctx["acc"] if it.get("gold") else SOFT
            d.text((X0, y), it["label"], font=self.lf, fill=CREAM + (int(255 * min(1, p * 3)),))
            bw = int(MAXW * (it["value"] / self.mx) * p)
            if bw > 8: d.rounded_rectangle([X0, y + 72, X0 + bw, y + 72 + 96], 18, fill=col)
            if p > .05:
                vs = eur(it["value"] * p) + " €"; tx = X0 + max(bw, 0) + 20
                if tx + tlen(vs, self.vf) > X0 + MAXW: tx = X0 + bw - tlen(vs, self.vf) - 24; c2 = DEEP
                else: c2 = CREAM
                d.text((tx, y + 82), vs, font=self.vf, fill=c2)
            y += 250
    def events(self): return [(0.0, "whoosh")] + [(.35 + i * .45, "tick") for i in range(len(self.items))]

class Myth(Scene):
    dur = 5.0
    def prep(self):
        sc = self.ctx["sc"]
        self.k1 = kick_img("VIELE DENKEN", self.ctx); self.k2 = kick_img("IN WAHRHEIT", self.ctx)
        f, ls = fit_font(self.s["myth"], BOLD, 84 * sc, MAXW, 3); self.m = [text_img(l.replace("*", ""), f, SOFT) for l in ls]; self.mlh = int(f.size * 1.12)
        f2, ls2 = fit_font(self.s["fact"], BOLD, 76 * sc, MAXW, 5); self.f = [rich_line_img(l, f2, CREAM, self.ctx["acc"]) for l in ls2]; self.flh = int(f2.size * 1.14)
    def draw(self, fr, t):
        d = ImageDraw.Draw(fr); y = 470
        paste(fr, self.k1, X0, y, ease(t / .3)); y += self.k1.height + 24
        for i, im in enumerate(self.m):
            paste(fr, im, X0, y + i * self.mlh + 30 * (1 - ease((t - .1 - i * .15) / .4)), ease((t - .1 - i * .15) / .4))
            p = ease((t - 1.5 - i * .2) / .35)
            if p > 0: d.line([(X0, y + i * self.mlh + self.mlh * .52), (X0 + (im.width - 4) * p, y + i * self.mlh + self.mlh * .52)], fill=(230, 90, 70), width=9)
        y += len(self.m) * self.mlh + 90
        paste(fr, self.k2, X0, y, ease((t - 2.2) / .3)); y += self.k2.height + 24
        for i, im in enumerate(self.f): paste(fr, im, X0, y + i * self.flh + 40 * (1 - ease((t - 2.35 - i * .18) / .45)), ease((t - 2.35 - i * .18) / .45))
    def events(self): return [(0.0, "whoosh"), (1.5, "strike"), (2.3, "pop")]

class ListScene(Scene):
    dur = 5.0
    def prep(self):
        sc = self.ctx["sc"]
        f, ls = fit_font(self.s["title"], BOLD, 86 * sc, MAXW, 3); self.t = [rich_line_img(l, f, CREAM, self.ctx["acc"]) for l in ls]; self.tlh = int(f.size * 1.1)
        self.items = []
        for it in self.s["items"][:4]:
            fi = F(SEMI, 52 * sc); ls2 = wrap_rich(it, fi, MAXW - 100); self.items.append([text_img(l.replace("*", ""), fi, CREAM) for l in ls2])
        self.ck = check_icon(56, self.ctx["acc"], 9)
        n = len(self.items); self.step = max(0.45, (self.dur - 1.6) / max(1, n))
    def draw(self, fr, t):
        y = 450
        for i, im in enumerate(self.t): paste(fr, im, X0, y + i * self.tlh, ease((t - i * .12) / .35))
        y += len(self.t) * self.tlh + 70
        for i, lines in enumerate(self.items):
            p = ease((t - .7 - i * self.step) / .35)
            paste(fr, self.ck, X0 + 10 * (1 - p), y + 6, p)
            for j, im in enumerate(lines): paste(fr, im, X0 + 100 + 30 * (1 - p), y + j * 64, p)
            y += len(lines) * 64 + 52
    def events(self): return [(0.0, "whoosh")] + [(.7 + i * self.step, "tick") for i in range(len(self.items))]

class Countdown(Scene):
    dur = 3.6
    def prep(self):
        sc = self.ctx["sc"]
        self.days = max(0, (datetime.date(2027, 1, 1) - datetime.date.today()).days)
        self.k = kick_img("OFFIZIELLER START 01.01.2027", self.ctx)
        self.l1 = text_img("Noch", F(SEMI, 64 * sc), SOFT); self.fn = F(BOLD, 300 * sc); self.l2 = text_img("Tage Vorsprung.", F(BOLD, 96 * sc), CREAM)
        self.small = F(SEMI, 34 * sc)
    def draw(self, fr, t):
        d = ImageDraw.Draw(fr); y = 520
        paste(fr, self.k, X0, y, ease(t / .3)); y += self.k.height + 40
        paste(fr, self.l1, X0, y, ease((t - .1) / .3)); y += self.l1.height
        v = int(round(self.days * ease_io((t - .2) / 1.1)))
        paste(fr, text_img(str(v), self.fn, self.ctx["acc"]), X0 - 10, y - 20, ease((t - .2) / .3)); y += int(self.fn.size * 1.05)
        paste(fr, self.l2, X0, y, ease((t - 1.0) / .35)); y += self.l2.height + 80
        p = ease((t - 1.3) / 1.2)
        for xx in range(X0, X0 + MAXW, 24): d.line([(xx, y + 14), (xx + 12, y + 14)], fill=GREEN2, width=4)
        if p > 0:
            d.rounded_rectangle([X0, y + 8, X0 + int(MAXW * p), y + 20], 6, fill=self.ctx["acc"])
            d.ellipse([X0 - 14, y - 2, X0 + 18, y + 30], fill=self.ctx["acc"])
        d.ellipse([X0 + MAXW - 16, y, X0 + MAXW + 12, y + 28], fill=SOFT)
        d.text((X0, y + 50), "Heute: du", font=self.small, fill=CREAM)
        d.text((X0 + MAXW - tlen("2027: alle anderen", self.small), y + 50), "2027: alle anderen", font=self.small, fill=SOFT)
    def events(self): return [(0.0, "whoosh"), (1.3, "pop")]

class CTA(Scene):
    dur = 4.6
    def prep(self):
        sc = self.ctx["sc"]
        self.k = kick_img(self.s.get("kick", "SICHERE DIR DEN VORSPRUNG"), self.ctx)
        f, ls = fit_font(self.s.get("text", "Rechne aus, wie viel\n*dir* zusteht."), BOLD, 92 * sc, MAXW, 4)
        self.lines = [rich_line_img(l, f, CREAM, self.ctx["acc"]) for l in ls]; self.lh = int(f.size * 1.1)
        v = self.ctx["variant"]
        if v == "A":
            self.pre = text_img("Kommentiere", F(SEMI, 56 * sc), CREAM); self.btn = self.ctx["wort"]; self.post = "und du bekommst den Link per DM."
        else:
            self.pre = None; self.btn = "Link im Profil ✓"; self.post = "Förderrechner, kostenlos und ohne Anmeldung."
        self.bf = F(BOLD, 96 * sc if v == "A" else 70 * sc); self.pf = F(MED, 44 * sc)
        df = F(MED, 30); dl = wrap_rich(DISCLAIMER, df, MAXW)
        self.disc = Image.new("RGBA", (MAXW, 44 * len(dl)), (0, 0, 0, 0))
        for i, l in enumerate(dl): ImageDraw.Draw(self.disc).text((0, i * 44), l, font=df, fill=SOFT)
    def draw(self, fr, t):
        d = ImageDraw.Draw(fr); y = 470
        paste(fr, self.k, X0, y, ease(t / .3)); y += self.k.height + 34
        for i, im in enumerate(self.lines): paste(fr, im, X0, y + i * self.lh + 40 * (1 - ease((t - .1 - i * .15) / .4)), ease((t - .1 - i * .15) / .4))
        y += len(self.lines) * self.lh + 80
        if self.pre: paste(fr, self.pre, X0, y, ease((t - .7) / .3)); y += self.pre.height + 16
        p = ease((t - .9) / .4)
        if p > 0:
            bw = int(tlen(self.btn, self.bf)) + 110; bh = int(self.bf.size * 1.55)
            pulse = 1 + 0.035 * math.sin(max(0, t - 1.4) * 5.5) if t > 1.4 else 1
            btn = Image.new("RGBA", (bw, bh), (0, 0, 0, 0)); bd = ImageDraw.Draw(btn)
            bd.rounded_rectangle([0, 0, bw - 1, bh - 1], bh // 2, fill=self.ctx["acc"] + (255,))
            bd.text((55, (bh - self.bf.size * 1.2) / 2), self.btn, font=self.bf, fill=DEEP)
            if pulse != 1: btn = btn.resize((int(bw * pulse), int(bh * pulse)), Image.LANCZOS)
            paste(fr, btn, X0 - (btn.width - bw) / 2, y - (btn.height - bh) / 2 + 30 * (1 - p), p)
            y += bh + 40
            for i, ln in enumerate(wrap_rich(self.post, self.pf, MAXW)): d.text((X0, y + i * 58), ln, font=self.pf, fill=CREAM + (int(255 * ease((t - 1.3) / .4)),))
        paste(fr, self.disc, X0, BOTTOM + 40, ease((t - .5) / .4))
    def events(self): return [(0.0, "whoosh"), (0.9, "pop")]


class Story(Scene):
    """Illustrierte Beispielfigur erzaehlt in Ich-Form. Immer als Beispielfigur gekennzeichnet."""
    dur = 6.0
    def prep(self):
        sc = self.ctx["sc"]; s = self.s
        self.av = avatar(s.get("figur", {}), 420)
        self.name = text_img(s["name"], F(BOLD, 64 * sc), CREAM)
        self.role = text_img(s.get("rolle", ""), F(MED, 40 * sc), SOFT) if s.get("rolle") else None
        self.tag = text_img("BEISPIELFIGUR · ILLUSTRATION", F(SEMI, 26), DEEP)
        f, ls = fit_font("„" + s["zitat"].strip("„“\"") + "“", BOLD, 66 * sc, MAXW - 80, 6)
        self.lines = [rich_line_img(l, f, DEEP, (176, 104, 10)) for l in ls]; self.lh = int(f.size * 1.18)
        self.step = min(0.35, (self.dur - 2.2) / max(1, len(self.lines)))
    def draw(self, fr, t):
        d = ImageDraw.Draw(fr); y = 300
        p = ease(t / .45)
        paste(fr, self.av, X0 - 6, y + 40 * (1 - p), p)
        tx = X0 + 450; ty = y + 120
        paste(fr, self.name, tx, ty + 20 * (1 - ease((t - .2) / .4)), ease((t - .2) / .4))
        if self.role: paste(fr, self.role, tx, ty + self.name.height + 6, ease((t - .3) / .4))
        pt = ease((t - .4) / .4)
        if pt > 0:
            w = self.tag.width + 32; pill = Image.new("RGBA", (w, 46), (0, 0, 0, 0))
            ImageDraw.Draw(pill).rounded_rectangle([0, 0, w - 1, 45], 23, fill=SOFT + (255,)); pill.alpha_composite(self.tag, (16, 7))
            paste(fr, pill, tx, ty + self.name.height + 70, pt)
        by = y + 470; bh = len(self.lines) * self.lh + 70
        pb = ease((t - .6) / .4)
        if pb > 0:
            bub = Image.new("RGBA", (MAXW, bh + 40), (0, 0, 0, 0)); bd = ImageDraw.Draw(bub)
            bd.rounded_rectangle([0, 40, MAXW - 1, bh + 39], 36, fill=CREAM + (255,))
            bd.polygon([(110, 40), (190, 40), (120, 0)], fill=CREAM + (255,))
            for i, im in enumerate(self.lines):
                a = ease((t - 0.9 - i * self.step) / .3)
                if a > 0:
                    ln = im.copy(); ln.putalpha(ln.getchannel("A").point(lambda v: int(v * a))); bub.alpha_composite(ln, (40, 40 + 35 + i * self.lh))
            paste(fr, bub, X0, by + 30 * (1 - pb), pb)
    def events(self): return [(0.0, "whoosh"), (0.6, "pop")]

TYPES = {"hook": Hook, "text": Text, "counter": Counter, "persona": Persona, "bars": Bars, "myth": Myth, "list": ListScene, "countdown": Countdown, "cta": CTA, "story": Story}

# ---------- Header + Fortschritt ----------
def header(ctx):
    img = Image.new("RGBA", (W, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle([X0, 128, X0 + 56, 184], 14, fill=AMBER)
    ck = check_icon(36, GREEN, 7); img.alpha_composite(ck, (X0 + 9, 139))
    d.text((X0 + 76, 136), HANDLE, font=F(SEMI, 34), fill=CREAM)
    return img

# ---------- Audio (eigene Musik, lizenzfrei) ----------
SR = 44100
def synth_music(seconds, seed=1):
    n = int(seconds * SR); t = np.arange(n) / SR; out = np.zeros(n, np.float32)
    bpm = 96; beat = 60 / bpm; bar = beat * 4
    prog = [(57, 60, 64), (53, 57, 60), (48, 52, 55), (55, 59, 62)]  # Am F C G
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    for b in range(int(seconds / bar) + 1):
        s0 = int(b * bar * SR); s1 = min(n, int((b + 1) * bar * SR))
        if s0 >= n: break
        tt = t[s0:s1] - b * bar; env = np.minimum(1, tt / 0.6) * np.minimum(1, (bar - tt) / 0.4)
        for m in prog[b % 4]:
            f = hz(m); out[s0:s1] += (0.06 * np.sin(2 * np.pi * f * tt) + 0.02 * np.sin(2 * np.pi * 2 * f * tt + .3)) * env
        f = hz(prog[b % 4][0] - 12); out[s0:s1] += 0.07 * np.sin(2 * np.pi * f * tt) * env
        # Arpeggio
        for k in range(8):
            a0 = s0 + int(k * beat / 2 * SR); a1 = min(s1, a0 + int(0.22 * SR))
            if a0 >= s1: break
            ta = t[a0:a1] - t[a0]; m = prog[b % 4][[0, 1, 2, 1][k % 4]] + 12
            out[a0:a1] += 0.035 * np.sin(2 * np.pi * hz(m) * ta) * np.exp(-ta * 9)
    rng = np.random.default_rng(seed)
    for k in range(int(seconds / beat)):
        s0 = int(k * beat * SR)
        if s0 >= n: break
        if k % 2 == 0:  # Kick
            l = min(n - s0, int(.25 * SR)); tk = np.arange(l) / SR
            out[s0:s0 + l] += 0.22 * np.sin(2 * np.pi * (55 + 90 * np.exp(-tk * 30)) * tk) * np.exp(-tk * 12)
        h0 = s0 + int(beat / 2 * SR); l = min(n - h0, int(.05 * SR))
        if l > 0: out[h0:h0 + l] += 0.03 * rng.normal(0, 1, l) * np.exp(-np.arange(l) / SR * 80)
    fade = np.minimum(1, np.minimum(t / 0.8, (seconds - t) / 1.2)); return out * fade

def sfx(kind):
    rng = np.random.default_rng(3)
    if kind == "whoosh":
        l = int(.35 * SR); tt = np.arange(l) / SR; nz = rng.normal(0, 1, l)
        nz = np.convolve(nz, np.ones(25) / 25, "same"); return 0.12 * nz * np.sin(np.pi * tt / tt[-1])
    if kind == "pop":
        l = int(.18 * SR); tt = np.arange(l) / SR; return 0.18 * np.sin(2 * np.pi * (520 + 380 * np.exp(-tt * 40)) * tt) * np.exp(-tt * 22)
    if kind == "tick":
        l = int(.08 * SR); tt = np.arange(l) / SR; return 0.12 * np.sin(2 * np.pi * 1400 * tt) * np.exp(-tt * 60)
    if kind == "strike":
        l = int(.25 * SR); tt = np.arange(l) / SR; nz = rng.normal(0, 1, l); return 0.07 * nz * np.exp(-tt * 14)
    return np.zeros(1)

def write_wav(path, x):
    x = np.clip(x, -1, 1); st = np.stack([x, x], 1); pcm = (st * 32767).astype(np.int16)
    with wave.open(path, "wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

# ---------- Rendern ----------
def render(spec, out_dir, variant):
    zg = spec.get("zielgruppe", "grundlagen")
    ctx = {"acc": ACCENT.get(zg, AMBER), "sc": SCALE.get(zg, 1.0), "variant": variant, "wort": spec.get("wort", "DEPOT").upper()}
    scenes = [TYPES[s["type"]](s, ctx) for s in spec["scenes"]]
    if scenes[-1].__class__ is not CTA: raise SystemExit("Letzte Szene muss type 'cta' sein.")
    total = sum(s.dur for s in scenes)
    if not 12 <= total <= 60: raise SystemExit(f"Gesamtlaenge {total:.1f}s – erlaubt 12–60 s.")
    bg = make_bg(); hd = header(ctx)
    path = os.path.join(out_dir, f"video_{variant}.mp4"); wav = os.path.join(out_dir, f"_audio_{variant}.wav")
    # Audio
    music = synth_music(total + 0.5, seed=len(spec["scenes"]))
    t0 = 0.0
    for s in scenes:
        for at, kind in s.events():
            fx = sfx(kind); i0 = int((t0 + at) * SR); i1 = min(len(music), i0 + len(fx)); music[i0:i1] += fx[: i1 - i0]
        t0 += s.dur
    write_wav(wav, music * 0.9)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", wav, "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
           "-shortest", "-movflags", "+faststart", path]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    nframes = int(round(total * FPS)); t0 = 0.0; idx = 0; cover = None
    for si, s in enumerate(scenes):
        n = int(round((t0 + s.dur) * FPS)) - int(round(t0 * FPS))
        for k in range(n):
            t = k / FPS; gt = (idx / FPS)
            ox = int(200 + 120 * math.sin(gt * 0.25)); oy = int(200 + 160 * math.cos(gt * 0.2))
            fr = bg.crop((ox, oy, ox + W, oy + H)).copy()
            fr.alpha_composite(hd)
            dd = ImageDraw.Draw(fr)
            # Fortschrittsbalken (Story-Stil)
            segw = (W - 2 * X0 - (len(scenes) - 1) * 10) / len(scenes)
            for j in range(len(scenes)):
                x = X0 + j * (segw + 10); dd.rounded_rectangle([x, 80, x + segw, 88], 4, fill=GREEN2)
                fill = 1 if j < si else (min(1, t / s.dur) if j == si else 0)
                if fill > 0: dd.rounded_rectangle([x, 80, x + segw * fill, 88], 4, fill=CREAM)
            # Szenen-Uebergang: weiches Ausblenden am Ende
            # Szene 1 zeigt ab dem ersten Bild den fertigen Hook (Instagram nimmt Bild 1 als Profil-Kachel)
            tc = min(s.dur - 0.4, 2.2)
            layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); s.draw(layer, max(t, tc) if si == 0 else t)
            out_a = 1 - ease((t - (s.dur - 0.28)) / 0.28) if si < len(scenes) - 1 else 1
            paste(fr, layer, 0, -30 * (1 - out_a), out_a)
            rgb = fr.convert("RGB")
            if idx == 0: cover = rgb.copy()
            pr.stdin.write(rgb.tobytes()); idx += 1
        t0 += s.dur
    pr.stdin.close(); pr.wait(); os.remove(wav)
    if pr.returncode: raise SystemExit("ffmpeg-Fehler")
    if variant == "A" and cover is not None: cover.save(os.path.join(out_dir, "cover.jpg"), quality=90)
    return path, total

if __name__ == "__main__":
    spec_path = sys.argv[1]; spec = json.load(open(spec_path)); out = os.path.dirname(os.path.abspath(spec_path))
    only = sys.argv[2] if len(sys.argv) > 2 else None
    for v in (["A", "B"] if not only else [only]):
        p, total = render(spec, out, v); print(f"{p}  ({total:.1f} s)")

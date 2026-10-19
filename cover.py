#!/usr/bin/env python3
"""Rendert ein Reel-Titelbild (1080x1920) in einer Farbvariante; Text sitzt im mittleren 3:4-Bereich,
damit er auch in der Profil-Kachel vollstaendig sichtbar ist.

Aufruf: python3 cover.py videos/<id>/cover.json   -> videos/<id>/cover_<theme>.jpg
cover.json = {"theme":"gruen|creme|gold", "kick":"FAMILIEN", "head":"Was Lisa mit 2 Kindern bekommt", "figur":{...optional...}}
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render
from PIL import Image, ImageDraw
from avatar import avatar

def main(p):
    s = json.load(open(p)); render.set_theme(s.get("theme"))
    img = Image.new("RGB", (1080, 1920), render.GREEN); d = ImageDraw.Draw(img)
    fig = avatar(s["figur"], 300) if s.get("figur") else None
    h = render.layout(d, s, 0, draw=False) + (330 if fig else 0)
    y = max(560, 960 - h // 2)
    if fig: img.paste(fig, (100, y), fig); y += 330
    render.layout(d, s, y)
    render.check(d, 100, 452, 40, render.AMBER, 9); d.text((158, 456), render.HANDLE, font=render.F(render.SEMI, 28), fill=render.CREAM)
    out = os.path.join(os.path.dirname(p), f"cover_{s.get('theme') or 'gruen'}.jpg"); img.save(out, quality=90); render.set_theme(None); print(out)

if __name__ == "__main__": main(sys.argv[1])

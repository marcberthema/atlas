"""Builds the three UI exploration mocks from real Atlas content. Run: python3 explorations/ui/build.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import field, guidemap, bench, specimen, zine, transit
from common import page, esc

OUT = Path(__file__).parent
WORLDS = [
    ("field", field, "A · Field guide", "Entries are species accounts. Field marks (version, dates, licence) sit in a margin box, look-alikes get their own section, and the four families are colour-tabbed edge-index tabs on a cloth-green frame."),
    ("guidemap", guidemap, "B · Guide map", "A zoo-and-gardens map. Families are flat-colour lobes on pale water, topics are capsules with a round count chip, and entries are rounded white lobes."),
    ("bench", bench, "C · Cutting bench", "A film bench. Black ground, orange grain, perforated rails; every word of running copy sits in a white window, and dates and versions are numerals in black cells."),
    ("specimen", specimen, "D · Type specimen", "A type specimen sheet. Giant grotesque names, mono metadata in a spec table, one blue, hairline rules, and a search field that works like a type tester."),
    ("zine", zine, "E · Hand-drawn zine", "A friendly explainer. Wobbly marker borders, highlighter swipes, a globe mascot that warns on gotchas, and Lenses arrows drawn by a shaky hand."),
    ("transit", transit, "F · Transit map", "A metro diagram. Each family is a coloured line, each topic a station, the views are interchanges, and entries are stops along a line with a route strip at the top."),
]
for d, mod, _, _ in WORLDS:
    (OUT / d).mkdir(exist_ok=True)
    for name, fn in (("index", mod.landing), ("topic", mod.topic), ("lenses", mod.lenses)):
        (OUT / d / f"{name}.html").write_text(fn())
cards = "".join(
    f'<section><h2>{esc(t)}</h2><p>{esc(p)}</p><p class="l"><a href="{d}/index.html">Landing</a><a href="{d}/topic.html">GitOps topic page</a><a href="{d}/lenses.html">Lenses</a>{extra}</p></section>'
    for d, _, t, p in WORLDS for extra in [(f'<a href="{d}/azure.html">Azure</a><a href="{d}/loop.html">DevOps loop</a>' if d == "transit" else "")])
css = ("body{font:1.0625rem/1.6 system-ui,sans-serif;max-width:900px;margin:0 auto;padding:2rem 1.25rem;color:#111}h1{font-size:2rem}"
       "section{border:1px solid #bbb;border-radius:8px;padding:1rem 1.2rem;margin:1rem 0}h2{margin:0 0 .3rem;font-size:1.3rem}"
       ".l{display:flex;gap:1rem;flex-wrap:wrap}a{color:#0b4f9c}")
(OUT / "index.html").write_text(page("Atlas UI exploration", "", f"<h1>Atlas UI exploration</h1><p>Three visual worlds, three pages each, built from real Atlas content. Mocks only: nothing here is published. Fonts load from Google Fonts, so open them online.</p>{cards}", css))
for name, fn in (("azure", transit.azure), ("loop", transit.loop)):
    (OUT / "transit" / f"{name}.html").write_text(fn())
print("built", len(WORLDS) * 3 + 1, "files")

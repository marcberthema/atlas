"""The transit look (docs/themes.md): a second skin for every page, built from the same data into dist/transit/.

Families are coloured lines, topics are stations, the views are interchanges. The font (Red Hat Display, SIL Open Font License)
ships inside dist/transit/fonts/ so pages work from file:// and load nothing from outside.
"""
import html
import json
import re
import shutil

import atlas

DIR = atlas.SITE / "shared" / "transit"
OUT = atlas.DIST / "transit"
LATIN = "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"
LATIN_EXT = "U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C4,U+2113,U+2C60-2C7F,U+A720-A7FF"

# Colours: Development blue, IaC red, CI/CD green, Enterprise orange, Test violet; the same ones the Lenses use.
VARS = """
@font-face{font-family:'Red Hat Display';font-style:normal;font-weight:500 900;font-display:swap;src:url(__FONTS__RedHatDisplay-latin-ext.woff2) format('woff2');unicode-range:__EXT__}
@font-face{font-family:'Red Hat Display';font-style:normal;font-weight:500 900;font-display:swap;src:url(__FONTS__RedHatDisplay-latin.woff2) format('woff2');unicode-range:__LATIN__}
:root{color-scheme:light;--ink:#14181F;--ground:#FFFFFF;--soft:#F2F4F7;--mut:#4A5260;--rule:#D5DAE1;--iac:#0057B8;--iacf:#fff;--cic:#D6001C;--cicf:#fff;--dev:#00843D;--devf:#fff;--ent:#F28C00;--entf:#14181F;--tst:#7B3FC4;--tstf:#fff;--wire:#5C6675;--warn:#8A6700;--bad:#C62828;--acc:#0057B8;--g:'Red Hat Display','Helvetica Neue',Arial,sans-serif}
@media(prefers-color-scheme:dark){:root{color-scheme:dark;--ink:#EEF1F5;--ground:#0F131A;--soft:#1A202B;--mut:#A9B3C1;--rule:#2C3543;--iac:#4C9AFF;--iacf:#0F131A;--cic:#FF6B7A;--cicf:#0F131A;--dev:#3DC878;--devf:#0F131A;--ent:#F5A524;--entf:#0F131A;--tst:#B792FF;--tstf:#0F131A;--wire:#8793A5;--warn:#D4A72C;--bad:#EF5350;--acc:#4C9AFF}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--ground);color:var(--ink);font:500 1.0625rem/1.6 var(--g)}
::selection{background:var(--acc);color:var(--ground)}
:focus-visible{outline:3px solid var(--ink);outline-offset:3px}
a{color:inherit;text-decoration:none}
[hidden]{display:none!important}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important;scroll-behavior:auto!important}}
[data-fam=iac]{--fc:var(--cic);--fcf:var(--cicf)}[data-fam=cicd]{--fc:var(--dev);--fcf:var(--devf)}
[data-fam=development]{--fc:var(--iac);--fcf:var(--iacf)}[data-fam=enterprise]{--fc:var(--ent);--fcf:var(--entf)}[data-fam=test]{--fc:var(--tst);--fcf:var(--tstf)}[data-fam=saas]{--fc:var(--mut);--fcf:var(--ground)}[data-fam=views]{--fc:var(--ink);--fcf:var(--ground)}
"""

# The banner keeps the classic markup and script (shared/atlas.py); this is its skin.
BANNER_CSS = """
.atlas.two{display:block;position:sticky;top:0;z-index:5;background:var(--ground);border-bottom:1px solid var(--rule);margin:0 0 1.4rem;padding:.7rem max(1rem,calc(50vw - 560px)) .6rem}
.atlas .fams{display:flex;align-items:center;flex-wrap:wrap;gap:.5rem 1rem}
.atlas .home{background:var(--ink);color:var(--ground);font-weight:900;letter-spacing:.03em;padding:.25rem 1rem;border-radius:6px}
.atlas .fb{display:flex;flex:1;flex-wrap:wrap;gap:.4rem;overflow:visible}
.atlas button[data-fam]{font:900 .95rem var(--g);padding:.2rem 1rem;border-radius:999px;border:3px solid var(--fc);background:var(--ground);color:var(--ink);cursor:pointer}
.atlas button[data-fam]:hover{background:var(--soft)}
.atlas button[data-fam][aria-pressed=true]{background:var(--fc);color:var(--fcf)}
.atlas .rt{display:flex;align-items:center;gap:.4rem}
.atlas .tg{display:inline-flex;align-items:center;justify-content:center;min-height:2rem;font:900 .9rem var(--g);padding:.1rem .8rem;border-radius:999px;border:3px solid var(--ink);background:var(--ground);color:var(--ink);cursor:pointer;white-space:nowrap}
.atlas .tg:hover{background:var(--ink);color:var(--ground)}
.atlas .tg svg{width:18px;height:18px;stroke:currentColor;fill:none;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}
.atlas .tops{display:flex;flex-wrap:wrap;gap:.3rem 1rem;margin-top:.6rem}
.atlas.none .tops{display:none}
.atlas .tops>div{display:flex;flex-wrap:wrap;gap:.2rem 1.1rem}
.atlas .tops a{display:inline-flex;align-items:center;gap:.45rem;font-weight:700;padding:.1rem .3rem;border-radius:8px;white-space:nowrap}
.atlas .tops a::before{content:"";width:16px;height:16px;border-radius:50%;border:4px solid var(--fc);background:var(--ground)}
.atlas .tops a:hover::before,.atlas .tops a[aria-current=page]::before{background:var(--fc)}
.atlas .tops a[aria-current=page]{text-decoration:underline;text-underline-offset:4px}
.atlas .skip{position:absolute;left:-9999px}.atlas .skip:focus{left:8px;top:8px;z-index:10;background:var(--ground);padding:.3rem .8rem}
dialog.ai{max-width:min(560px,92vw);border:3px solid var(--ink);border-radius:14px;background:var(--ground);color:var(--ink);padding:1.4rem 1.6rem;font:500 1rem/1.55 var(--g)}
dialog.ai::backdrop{background:rgba(10,12,16,.6)}
dialog.ai h2{margin:0 3.5rem .6rem 0;font:900 1.7rem var(--g);letter-spacing:-.02em}dialog.ai p{margin:.6rem 0}
dialog.ai .cl{position:absolute;top:1rem;right:1rem;font:900 .9rem var(--g);padding:.1rem .9rem;border-radius:999px;border:3px solid var(--ink);background:var(--ground);color:var(--ink);cursor:pointer}
dialog.ai .dx{display:flex;gap:.7rem;align-items:flex-start;margin:1rem 0;font-weight:700;cursor:pointer}dialog.ai .dx input{width:1.3rem;height:1.3rem;margin-top:.2rem;accent-color:var(--acc)}
dialog.ai .dx small{display:block;font-weight:500;color:var(--mut)}
dialog.ai .vr{font-size:.9rem;color:var(--mut);word-break:break-all}dialog.ai a{text-decoration:underline}
.atlas-foot{max-width:1120px;margin:3rem auto 0;padding:1.4rem clamp(1rem,3vw,2rem) 3rem;border-top:1px solid var(--rule);color:var(--mut);font-size:.9rem}
.atlas-foot p{margin:.4rem 0;max-width:80ch}
@media(max-width:560px){.atlas .fb{flex-basis:100%;order:3}}
"""

LINE = {"iac": "iac", "cicd": "cicd", "development": "development", "enterprise": "enterprise", "test": "test", "views": "views"}


def vars_css(fonts):
    """The shared variables and base rules; `fonts` is the relative path to dist/transit/fonts/ from the page."""
    return VARS.replace("__FONTS__", fonts).replace("__EXT__", LATIN_EXT).replace("__LATIN__", LATIN)


def fill(page, path, current, fonts):
    """Fill the markers of a transit page: the variables, the banner, its css and the footer. `path` is the page's path under dist/transit/."""
    page = atlas.themed(page.replace("/*__TRANSIT_VARS__*/", vars_css(fonts)))
    prefix = "../" * path.count("/")
    assert all(page.count(m) == 1 for m in (atlas.BANNER_MARK, atlas.CSS_MARK, atlas.FOOTER_MARK)), "template needs one banner, one banner css and one footer marker"
    return (page.replace(atlas.BANNER_MARK, atlas.banner(current, prefix, atlas.twin(path, atlas.TRANSIT), atlas.TRANSIT))
                .replace(atlas.CSS_MARK, BANNER_CSS).replace(atlas.FOOTER_MARK, atlas.FOOTER))


def copy_fonts():
    dest = OUT / "fonts"
    dest.mkdir(parents=True, exist_ok=True)
    for f in (DIR / "fonts").iterdir():
        shutil.copy(f, dest / f.name)


def write(path, page):
    out = OUT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"built {out.relative_to(atlas.SITE)}")


def landing(found):
    """dist/transit/index.html. `found` is {topic id: [(entry id, name, summary)]}, as shared/build_site.py reads them."""
    reg = atlas.load()
    topics = atlas.published()
    page = (DIR / "landing.html").read_text(encoding="utf-8")
    page = page.replace("/*__LANDING_JS__*/", (atlas.SITE / "shared" / "landing.js").read_text(encoding="utf-8").rstrip("\n"))
    index = [[t["id"], t["label"], *e] for t in topics for e in found[t["id"]]]
    groups = sorted(atlas.by_family(), key=lambda g: g[0]["id"] != "views")

    def href(tid):
        return f"{tid}/index.html" if f"{tid}/index.html" in atlas.twins() else f"../{tid}/index.html"

    lines = "".join(
        '<section class="line" data-fam="{id}"><h2 class="lname">{fam}</h2>{fdesc}<ol class="route">{stns}</ol></section>'.format(
            id=f["id"], fam=html.escape(atlas.label(f, True)),
            fdesc='<p class="fdesc">' + html.escape(f["description"]) + "</p>" if f.get("description") else "",
            stns="".join(
                '<li class="stn"><a href="{h}"><i class="dot"></i><b>{label}</b><small>{n}</small><span class="d">{desc}</span></a></li>'.format(
                    h=href(t["id"]), label=html.escape(t["label"]), desc=html.escape(t["description"]),
                    n="view" if f["id"] == "views" else f"{len(found[t['id']])} entries")
                for t in ts))
        for f, ts in groups)
    twins = json.dumps(sorted(p.split("/")[0] for p in atlas.twins() if p != "index.html"))
    page = (page.replace("__NAME__", html.escape(reg["name"])).replace("__TAGLINE__", html.escape(reg["tagline"]))
                .replace("<!--__TOPICS__-->", lines)
                .replace("/*__INDEX__*/", json.dumps(index, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/"))
                .replace("/*__TWINS__*/[]", twins))
    write("index.html", fill(page, "index.html", None, "fonts/"))


# The topic pages keep the shared template, markup and script (shared/topic.html). The look is a layer: the classic variables are mapped
# to the transit ones, and the rules below change shape, weight and the family colour. A new kind of content is drawn once and shows in both looks.
TOPIC_MAP = """body{--bg:var(--ground);--fg:var(--ink);--card:var(--soft);--ok:var(--dev);--acc:var(--ink);--fam:var(--fc);--famf:var(--fcf)}"""
TOPIC_CSS = """
body{font:500 1.0625rem/1.6 var(--g);max-width:none;margin:0;padding:0}
.tpage{max-width:1120px;margin:0 auto;padding:0 clamp(1rem,3vw,2rem) 1rem}
h1{font:900 clamp(2.6rem,9vw,4.6rem)/.98 var(--g);letter-spacing:-.04em;color:var(--fg);margin:.4rem 0 .6rem}
h2{font:900 1.5rem var(--g);letter-spacing:-.02em;color:var(--fg);border-bottom:3px solid var(--fam);margin:2rem 0 .3rem;padding-bottom:.2rem}
.sub{font-size:1.15rem;color:var(--mut);max-width:64ch}
.note{border:3px solid var(--fam);background:var(--card);border-radius:12px;padding:.6rem 1rem;font-size:.95rem}
.bar{background:var(--bg);padding:.6rem 0;border-bottom:1px solid var(--rule)}
input[type=search]{font:700 1.1rem var(--g);border:3px solid var(--fg);border-radius:999px;padding:.55rem 1.2rem;background:var(--card);color:var(--fg)}
.tabs{gap:.4rem;margin-bottom:.6rem}
.tab{font:900 .95rem var(--g);border:3px solid var(--fg);border-radius:999px;padding:.2rem 1rem;color:var(--fg)}
.tab:hover{background:var(--card)}
.tab[aria-selected=true]{background:var(--fam);border-color:var(--fam);color:var(--famf)}
th{font:900 .8rem var(--g);letter-spacing:.06em;text-transform:uppercase;color:var(--fg);border-bottom:3px solid var(--fg)}
button.nm{color:var(--fg);font-weight:900;text-underline-offset:3px}
.badge,.chip,.uc{border-width:2px;font-weight:700}
.badge{color:var(--fg);border-color:var(--fg)}
.badge.ok{color:var(--ok);border-color:var(--ok)}.badge.warn{color:var(--warn);border-color:var(--warn)}.badge.bad{color:var(--bad);border-color:var(--bad)}
.pk{border-width:3px;border-color:var(--fg);font-weight:900}.pk[aria-pressed=true]{background:var(--fam);border-color:var(--fam);color:var(--famf)}
.jump{gap:.2rem .8rem}
.jump a{border-radius:8px;padding:.2rem .4rem;font-weight:700;color:var(--fg)}
.jump a::before{content:"";width:14px;height:14px;border-radius:50%;border:4px solid var(--fam);background:var(--bg);flex:none}
.jump a:hover,.jump a.on{background:transparent;text-decoration:underline;text-underline-offset:4px}
.jump a.on::before,.jump a:hover::before{background:var(--fam)}
.ph{color:var(--fg);font-weight:900;border-bottom:4px solid var(--fam)}
.ph .ic{color:var(--fam)}
.step{background:var(--fam);color:var(--famf)}
.sec>h4 .ic{color:var(--fam)}
.card,.ver,.nt,.co,details.sec,figure.code,.dg svg{border-width:2px;border-color:var(--fg);border-radius:12px}
.card .ic,.db h4,.db a{color:var(--fg)}
.co.gotcha{border-color:var(--warn)}.co.default{border-color:var(--fam)}.co.prod{border-color:var(--ok)}.co.tip{border-color:var(--mut)}
.co.default .ic{color:var(--fam)}
.pills a{border-width:2px;border-color:var(--fg);border-radius:999px;font-weight:700}.pills a:hover{background:var(--fg);color:var(--bg)}
.ch{background:var(--card)}.cp{border-width:2px;border-color:var(--fg);border-radius:999px;font-weight:700}
dialog{border:3px solid var(--fg);border-radius:14px}
.dh button{border-width:2px;border-color:var(--fg);border-radius:999px;font-weight:900}
.dg rect.n,.dg line{stroke:var(--fg)}.dg marker path{fill:var(--fg)}
.dg rect.hub{fill:var(--fam)}
.q{color:var(--warn)}
"""


def topic(page, topic_id, family):
    """The transit twin of a topic page, from the shared template once its data is filled in."""
    old = re.search(r":root\{--bg:.*?\n@media\(prefers-color-scheme:dark\)\{:root\{.*?\}\}\n", page, re.S)
    assert old, "shared/topic.html: the variable blocks changed"
    page = page.replace(old.group(0), "/*__TRANSIT_VARS__*/\n" + TOPIC_MAP + "\n")
    for marker, new in (("<body>", f'<body data-fam="{family}">'), (atlas.BANNER_MARK, atlas.BANNER_MARK + '<div class="tpage">'),
                        ('<script id="data" type="application/json">', '</div><script id="data" type="application/json">'),
                        ("</style></head>", TOPIC_CSS + "</style></head>")):
        assert page.count(marker) == 1, f"shared/topic.html needs exactly one {marker}"
        page = page.replace(marker, new)
    ids = {p.split("/")[0] for p in atlas.twins()}  # a link to a topic without a twin goes to its classic page
    page = re.sub(r"\]\(\.\./([a-z0-9-]+)/", lambda m: m[0] if m[1] in ids else f"](../../{m[1]}/", page)
    return fill(page, f"{topic_id}/index.html", topic_id, "../fonts/")


AZURE_MAP = """body{--bg:var(--ground);--fg:var(--ink);--card:var(--soft);--ok:var(--dev);--acc:var(--ink);--fam:var(--fc);--famf:var(--fcf);
--t0-bd:var(--cic);--t0-bg:color-mix(in srgb,var(--cic) 14%,var(--ground));--t1-bd:color-mix(in srgb,var(--cic) 55%,var(--ground));--t1-bg:color-mix(in srgb,var(--cic) 6%,var(--ground));
--t2-bd:var(--ent);--t2-bg:color-mix(in srgb,var(--ent) 14%,var(--ground));--t3-bd:var(--mut);--t3-bg:var(--soft)}"""
AZURE_CSS = """
.top{align-items:center}
.mode{border:3px solid var(--fg);border-radius:999px}
.mode button{font-weight:900;background:var(--bg);color:var(--fg);padding:.3rem 1rem}
.mode button[aria-pressed=true]{background:var(--fam);color:var(--famf)}
.chip{border-width:3px;font-weight:900}
.chip small{font-weight:700}
button.svc,button.rel{border-width:2px;border-radius:12px;font-weight:500}
button.svc:hover,button.rel:hover{border-color:var(--fg);box-shadow:none;transform:translateY(-2px)}
.svc b,.rel b{font-weight:900;letter-spacing:-.01em}
.col,.tf{border-width:2px;border-color:var(--fg);border-radius:12px}
.col h3{color:var(--fg);font-weight:900}
.crumbs a{color:var(--fg)}
select{border:3px solid var(--fg);border-radius:999px;font-weight:700}
.count{font-weight:700}
"""


def azure(page):
    """The transit twin of the Azure page, from its template once the data is filled in."""
    old = re.search(r":root\{\n  --bg:.*?\n\}\n@media\(prefers-color-scheme:dark\)\{:root\{\n.*?\n\}\}\n", page, re.S)
    assert old, "topics/azure/templates/index.html: the variable blocks changed"
    page = page.replace(old.group(0), "/*__TRANSIT_VARS__*/\n" + AZURE_MAP + "\n")
    for marker, new in (("<body>", '<body data-fam="iac">'), (atlas.BANNER_MARK, atlas.BANNER_MARK + '<div class="tpage">'),
                        (atlas.FOOTER_MARK, "</div>" + atlas.FOOTER_MARK), ("</style></head>", TOPIC_CSS + AZURE_CSS + "</style></head>")):
        assert page.count(marker) == 1, f"topics/azure/templates/index.html needs exactly one {marker}"
        page = page.replace(marker, new)
    return fill(page, "azure/index.html", "azure", "../fonts/")


LENSES_MAP = """body{--bg:var(--ground);--fg:var(--ink);--card:var(--soft);--lane:var(--soft);--accfg:var(--ground);--ok:var(--dev);--acc:var(--ink);--fam:var(--fc);--famf:var(--fcf)}"""
LENSES_CSS = """
body{font:500 1.0625rem/1.6 var(--g)}
main{max-width:1280px}
.atlas.two{padding-inline:max(1rem,calc(50vw - 624px))}
h1{font:900 clamp(2.6rem,9vw,4.6rem)/.98 var(--g);letter-spacing:-.04em;color:var(--fg)}
.sub{font-size:1.1rem;max-width:64ch}
.grp>.l{font:900 .8rem var(--g)}
.seg{border:3px solid var(--fg);border-radius:999px}
.seg button{font-weight:900;border-right-width:3px;border-right-color:var(--fg)}
.seg button[aria-selected=true],.seg button[aria-pressed=true]{background:var(--fg);color:var(--bg)}
.find input{border:3px solid var(--fg);border-radius:999px;padding:.5rem 1.2rem;font-weight:700;background:var(--card)}
.find ul{border:3px solid var(--fg);border-radius:14px}
.blurb{border:3px solid var(--fg);border-radius:12px}
.map,.panel,.org{border-width:3px;border-color:var(--fg);border-radius:14px}
.lane{rx:12px}.lanel{font:900 12px var(--g)}
.node rect{rx:10px;stroke:var(--cat,var(--fg));stroke-width:3.5;stroke-dasharray:none}
.node[data-cat=edge]{--cat:var(--ent)}.node[data-cat=run]{--cat:var(--iac)}.node[data-cat=data]{--cat:var(--dev)}.node[data-cat=ops]{--cat:var(--cic)}
.node text{font:900 14px var(--g)}.node .cap{font:700 12px var(--g)}
.node.in .ic{stroke:var(--fg)}
.node.out{opacity:.35}
.node.sel rect{fill:var(--fg);stroke:var(--fg)}
.node:hover rect{stroke:var(--fg)}
.edge{stroke:var(--wire);stroke-width:2;opacity:.35}.edge.on{stroke:var(--wire);stroke-width:2.6;opacity:1}
.elab{font:700 12.5px var(--g)}.framel{font:900 12px var(--g)}
.legend,.cross{font-weight:700}
.panel h2{font:900 1.3rem var(--g);color:var(--fg)}.panel h3{font:900 .8rem var(--g)}
.chip{border-width:2px;border-color:var(--fg);font-weight:700}.chip:hover{border-color:var(--fg)}
.prods li{border-width:2px;border-color:var(--fg);border-radius:10px}.prods li.hit{box-shadow:none;border-width:3px}
.az section h2,.side h3{color:var(--fg);font-weight:900;border-bottom:3px solid var(--fg)}
.az li button,.side>div,.rgbox,.go,.oc button{border-width:2px;border-color:var(--fg);border-radius:12px}
.az li button:hover,.go:hover{border-color:var(--fg);transform:translateY(-2px)}
.os{border-width:3px;border-color:var(--fg);border-radius:14px}.os.sel{box-shadow:none;border-color:var(--ent)}
.oh button,.oc button .ic,.go .ic,.oh button .ic{color:var(--fg);stroke:var(--fg)}
.oc button:hover,.oc button.sel{background:var(--fg);color:var(--bg)}
.filed,.modtag{border-width:2px;border-color:var(--fg)}
.badge circle{stroke:var(--fg)}.badge .ic{stroke:var(--fg)}
"""


def lenses(page):
    """The transit twin of the Lenses page, from its template once the data is filled in. The same script draws it: only the look differs."""
    old = re.search(r":root\{--bg:.*?\n@media\(prefers-color-scheme:dark\)\{:root\{.*?\}\}\n", page, re.S)
    assert old, "shared/lenses.html: the variable blocks changed"
    page = page.replace(old.group(0), "/*__TRANSIT_VARS__*/\n" + LENSES_MAP + "\n")
    for marker, new in (("<body>", '<body data-fam="views">'), ("</style></head>", LENSES_CSS + "</style></head>")):
        assert page.count(marker) == 1, f"shared/lenses.html needs exactly one {marker}"
        page = page.replace(marker, new)
    return fill(page, "lenses/index.html", "lenses", "../fonts/")


# Dev stages blue, Ops stages red, except Plan orange, Test violet, Release and Deploy green.
STAGE_COLOUR = {"plan": "ent", "test": "tst", "release": "dev", "deploy": "dev"}


def loop_content(reg):
    """The DevOps loop in the transit look: the same figure eight as the classic page, drawn as a line of stations."""
    import math
    W, H = 940, 330
    lem = lambda t, a=330: (W / 2 + a * math.cos(t) / (1 + math.sin(t) ** 2), H / 2 - a * .95 * math.sin(t) * math.cos(t) / (1 + math.sin(t) ** 2))
    stages = reg["stages"]
    half = len(stages) // 2
    key = lambda i: STAGE_COLOUR.get(stages[i]["id"], "iac" if i < half else "cic")
    path = lambda t0, t1: "M" + " L".join("%.1f,%.1f" % lem(t0 + (t1 - t0) * i / 120) for i in range(121))
    esc = html.escape
    segs, nodes = "", ""
    for i, sg in enumerate(stages):
        lobe, k = divmod(i, half)
        t0 = math.pi / 2 + math.pi * lobe + k * math.pi / half
        segs += f'<path class="bg" d="{path(t0, t0 + math.pi / half)}" style="stroke:var(--{key(i)})"/>'
        x, y = lem(t0 + math.pi / half / 2)
        ly = y - 26 if y < H / 2 else y + 36
        nodes += (f'<a href="#stage-{esc(sg["id"])}" aria-label="Stage {i + 1}: {esc(sg["label"])}"><g style="--sc:var(--{key(i)})"><circle class="st" cx="{x:.1f}" cy="{y:.1f}" r="15" style="stroke:var(--{key(i)})"/>'
                  f'<text x="{x:.1f}" y="{ly:.1f}" text-anchor="middle">{i + 1} {esc(sg["label"])}</text></g></a>')
    svg = (f'<svg class="loop" viewBox="0 0 {W} {H}" role="group" aria-label="The DevOps loop: {", ".join(esc(s["label"]) for s in stages)}, then back to {esc(stages[0]["label"])}">'
           f'{segs}<text class="lobe" x="{W * .25}" y="{H / 2 + 6}">Dev</text><text class="lobe" x="{W * .75}" y="{H / 2 + 6}">Ops</text>{nodes}</svg>')
    topics = atlas.published()
    groups = ""
    for lobe, name in ((0, "Dev"), (1, "Ops")):
        items = ""
        for i, sg in enumerate(stages):
            if i // half != lobe:
                continue
            mine = [t for t in topics if sg["id"] in t.get("stages", [])]
            pills = "".join(f'<li><a href="../{t["id"]}/index.html">{esc(t["label"])}</a></li>' for t in mine) or '<li class="none">No Atlas topic covers this stage yet.</li>'
            items += (f'<article class="stage" id="stage-{esc(sg["id"])}" style="--c:var(--{key(i)});--cf:var(--{key(i)}f)"><h3><small>{i + 1}</small>{esc(sg["label"])}</h3>'
                      f'<p>{esc(sg["about"])}</p><ul class="pills">{pills}</ul></article>')
        groups += f'<section class="grp2"><h2 class="lname">{name}</h2><div class="stops">{items}</div></section>'
    unplaced = [t for t in topics if not t.get("stages")]
    rest = ('<section class="grp2"><h2 class="lname">Not on the loop</h2><p class="unplaced">{}</p></section>'.format("".join(
        f'<a href="../{t["id"]}/index.html">{esc(t["label"])}</a>' for t in unplaced)) if unplaced else "")
    return ('<h1>DevOps loop</h1><p class="sub">The eight stages, and where each topic fits. A topic can belong to several stages.</p>'
            f'{svg}{groups}{rest}<p class="note">Which stages a topic belongs to is a judgement recorded in the topic\'s spec, not something a source states. '
            'This page is generated from <code>topics.json</code>; see <code>docs/views.md</code>.</p>')


def view(v, reg):
    """dist/transit/<view>/index.html for a generated view (today only the DevOps loop)."""
    page = (DIR / "view.html").read_text(encoding="utf-8")
    page = (page.replace("__TITLE__", html.escape(v["label"])).replace("__NAME__", html.escape(reg["name"]))
                .replace("<!--__CONTENT__-->", loop_content(reg)))
    return fill(page, f"{v['id']}/index.html", v["id"], "../fonts/")


def check():
    """Exit 1 when the two looks disagree: a page without a twin, different data, a missing font, a load from outside, a broken link
    or a Look switch that does not land on the other page. It reads the built dist/, so it runs at the end of the build."""
    bad = []
    data = lambda h: (re.search(r'<script id="data" type="application/json">(.*?)</script>', h, re.S) or [None, ""])[1]
    norm = lambda s: re.sub(r"\]\(\.\./(?:\.\./)?", "](../", s)
    pages = sorted(atlas.twins())
    for p in pages:
        classic, tr = atlas.DIST / p, OUT / p
        if not classic.exists() or not tr.exists():
            bad.append(f"{p}: needs a classic page and a transit twin")
            continue
        c, x = classic.read_text(encoding="utf-8"), tr.read_text(encoding="utf-8")
        if norm(data(c)) != norm(data(x)):
            bad.append(f"{p}: the two looks embed different data")
        for label, page, here, other in (("classic", c, classic, tr), ("transit", x, tr, classic)):
            m = re.search(r'class="tg lk" href="([^"]+)"', page)
            if not m or not (here.parent / m[1]).resolve() == other.resolve():
                bad.append(f"{label} {p}: the Look switch does not lead to the other look of the page")
        for href in set(re.findall(r'(?:href|src)="([^"#:][^"]*)"', x)) | set(re.findall(r"url\(([^)'\"]+)\)", x)):
            if href.startswith(("http", "mailto", "data:")) or "'+" in href or "+'" in href or "${" in href:
                continue
            if not (tr.parent / href.split("#")[0]).exists():
                bad.append(f"transit {p}: broken link {href}")
        if re.search(r'<(?:link|script|img|iframe)[^>]+(?:src|href)="https?:|url\(https?:|@import', x):
            bad.append(f"transit {p}: loads something from outside the site")
    if not list((OUT / "fonts").glob("*.woff2")) or not (OUT / "fonts" / "OFL.txt").exists():
        bad.append("dist/transit/fonts needs the font files and their licence")
    for line in bad:
        print("bad:", line)
    print(f"transit check: {len(pages)} pages, bad {len(bad)}")
    return 1 if bad else 0

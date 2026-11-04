"""World E: hand-drawn zine. Wobbly marker borders, highlighter swipes, a doodle mascot, arrows drawn by a shaky hand."""
from common import *

WOB = "255px 14px 225px 14px / 14px 225px 14px 255px"
WOB2 = "14px 225px 14px 255px / 255px 14px 225px 14px"

MASCOT = ('<svg class="mascot" viewBox="0 0 90 90" role="img" aria-label="Atlas mascot, a smiling globe"><g fill="none" stroke="#111" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">'
          '<path d="M45 8C66 7 82 23 82 45C82 67 66 83 45 82C23 83 8 66 8 45C8 23 24 9 45 8Z" fill="#7FE0D2"/>'
          '<path d="M14 36C28 30 36 40 52 34C62 30 70 33 78 30" stroke-width="2"/><path d="M12 56C26 62 38 52 54 60C64 64 72 60 80 62" stroke-width="2"/>'
          '<circle cx="34" cy="42" r="3.2" fill="#111"/><circle cx="56" cy="42" r="3.2" fill="#111"/><path d="M33 56C40 64 50 64 58 55"/></g></svg>')

CSS = """
:root{--ink:#111;--paper:#F5F8FB;--yel:#FFE14D;--pink:#FF9EC7;--teal:#7FE0D2;--mut:#3C4650;--h:'Caveat Brush','Comic Sans MS',cursive;--b:'Atkinson Hyperlegible','Trebuchet MS',sans-serif}
body{background:var(--paper) linear-gradient(rgba(60,90,130,.07) 1px,transparent 1px) 0 0/100% 28px;color:var(--ink);font:400 1.125rem/1.6 var(--b)}
::selection{background:var(--pink);color:var(--ink)}
:focus-visible{outline:3px dashed var(--ink);outline-offset:3px}
a{text-decoration:none;color:inherit}
.wrap{max-width:1080px;margin:0 auto;padding:1.5rem clamp(1rem,3vw,2rem) 4rem}
h1,h2,h3{font-family:var(--h);font-weight:400;margin:0;letter-spacing:.01em}
.hero{display:grid;grid-template-columns:auto 1fr;gap:1rem 2rem;align-items:center;margin-bottom:1.5rem}
.mascot{width:clamp(90px,16vw,150px);transform:rotate(-6deg)}
h1{font-size:clamp(3.4rem,12vw,6rem);line-height:.95}
.hl{background:linear-gradient(transparent 58%,var(--yel) 58% 92%,transparent 92%);padding:0 .1em}
.say{position:relative;display:inline-block;max-width:44ch;margin:.8rem 0 0;padding:.7rem 1.1rem;border:2.5px solid var(--ink);border-radius:WOB;background:#fff;font-size:1.15rem}
.find{display:block;max-width:640px;margin-top:1rem;border:3px solid var(--ink);border-radius:WOB2;background:#fff;padding:.2rem 1.2rem}
#q{width:100%;border:0;background:transparent;font:400 1.5rem var(--h);color:var(--ink);padding:.6rem 0;letter-spacing:.02em}#q:focus-visible{outline:0}
.find:focus-within{outline:3px dashed var(--ink);outline-offset:4px}
.hint{font-size:.95rem;color:var(--mut);margin:.5rem 0 0}
.panels{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1.6rem;margin-top:2rem}
.panel{background:#fff;border:3px solid var(--ink);border-radius:WOB;padding:1.2rem 1.4rem 1.4rem;transform:rotate(var(--rot,0deg))}
.panel:nth-child(even){border-radius:WOB2;--rot:.5deg}.panel:nth-child(odd){--rot:-.4deg}
.panel h2{font-size:2.4rem;line-height:1}.panel h2 span{background:var(--c);padding:0 .35em;border-radius:6px 14px 8px 12px}
.panel p{margin:.4rem 0 1rem;color:var(--mut);max-width:34ch}
.stickers{display:flex;flex-wrap:wrap;gap:.6rem}
.sticker{display:inline-flex;align-items:baseline;gap:.5rem;background:var(--c2,#fff);border:2.5px solid var(--ink);border-radius:WOB2;padding:.2rem .9rem;font:400 1.35rem var(--h);transition:transform .15s}
.sticker:hover{transform:rotate(-2deg) scale(1.05)}.sticker small{font:700 .85rem var(--b)}
.note{margin-top:2rem;background:var(--yel);border:3px solid var(--ink);border-radius:WOB;padding:1rem 1.4rem;max-width:560px;transform:rotate(.6deg)}
.note h2{font-size:1.9rem}.note p{margin:.2rem 0 .8rem}
.hits{display:grid;gap:.8rem;margin:1.6rem 0}.hit{display:block;background:#fff;border:2.5px solid var(--ink);border-radius:WOB2;padding:.6rem 1.2rem}
.hit:hover,.hit:focus-visible{background:var(--yel)}.hit b{display:block;font:400 1.7rem var(--h)}.hit span{display:block;color:var(--mut)}.hit small{font-weight:700;font-size:.85rem}
.none{background:#fff;border:2.5px solid var(--ink);border-radius:WOB;padding:.8rem 1.2rem}.none button{font:inherit;font-weight:700;background:var(--pink);border:2px solid var(--ink);border-radius:WOB2;padding:.1rem .8rem;cursor:pointer}
/* topic */
.crumb{display:flex;gap:.5rem;flex-wrap:wrap;font:400 1.25rem var(--h);margin-bottom:.8rem}.crumb a{background:#fff;border:2px solid var(--ink);border-radius:WOB2;padding:0 .8rem}
.layout{display:grid;grid-template-columns:190px minmax(0,1fr);gap:2rem;margin-top:1.5rem}
.toc{position:sticky;top:1rem;align-self:start;font:400 1.3rem/1.3 var(--h)}.toc ul{list-style:none;margin:0;padding:0;display:grid;gap:.4rem}.toc a:hover{background:var(--yel)}
.entry{background:#fff;border:3px solid var(--ink);border-radius:WOB;padding:1.4rem 1.6rem 1.6rem;margin-bottom:1.8rem}
.entry:nth-of-type(even){border-radius:WOB2}
.entry h2{font-size:clamp(2.4rem,6vw,3.4rem);line-height:1}
.chips{display:flex;flex-wrap:wrap;gap:.5rem;margin:.8rem 0}.chips span{border:2px solid var(--ink);border-radius:WOB2;padding:0 .7rem;font-weight:700;font-size:.95rem;font-variant-numeric:tabular-nums}
.k1{background:var(--yel)}.k2{background:var(--teal)}.k3{background:var(--pink)}.k4{background:#fff}
.sum{font-size:1.3rem;line-height:1.45;max-width:58ch;margin:0 0 .8rem}
.entry ul{max-width:64ch;padding-left:1.3rem}.entry li{margin:.4rem 0}
code{font:.9em ui-monospace,Menlo,monospace;background:#E9EEF3;padding:.05em .3em;border-radius:4px}
.gotcha{display:grid;grid-template-columns:auto 1fr;gap:.8rem;align-items:center;border:2.5px solid var(--ink);border-radius:WOB2;background:#FFF1F6;padding:.7rem 1.1rem;margin:1.1rem 0;max-width:64ch}
.gotcha svg{width:46px;transform:rotate(8deg)}.gotcha b{font:400 1.4rem var(--h);margin-right:.4rem}
.srcs{display:flex;flex-wrap:wrap;gap:.5rem}.srcs a{border-bottom:3px solid var(--yel);font-weight:700}.srcs a:hover{background:var(--yel)}
.cmp{background:#fff}.cmp h2{font-size:2.4rem;margin-bottom:.6rem}
table{border-collapse:collapse;width:100%;font-size:1rem}th,td{text-align:left;vertical-align:top;padding:.7rem .8rem;border-bottom:2px dashed #9AA6B2}
thead th{font:400 1.5rem var(--h);border-bottom:3px solid var(--ink)}tbody th{font:400 1.3rem var(--h);width:7rem}
/* lenses */
.lensbar{display:flex;flex-wrap:wrap;gap:.6rem;margin:1rem 0 .6rem}
.lensbtn{font:400 1.35rem var(--h);background:#fff;border:2.5px solid var(--ink);border-radius:WOB2;padding:.1rem 1.1rem;cursor:pointer;color:var(--ink)}.lensbtn[aria-pressed=true]{background:var(--yel)}
.about{max-width:60ch;min-height:3.3em;margin:0 0 1rem}
.lanes{filter:none}
.lane{display:grid;grid-template-columns:150px 1fr;gap:.5rem 1rem;align-items:center;padding:.6rem 0;border-top:2px dashed #9AA6B2}
.lane h2{margin:0;font-size:1.5rem}
.cells{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:.6rem}
.role{font:400 1.2rem/1.1 var(--h);padding:.7rem .4rem;min-height:3.4rem;border:2.5px solid var(--ink);border-radius:WOB2;color:var(--ink);cursor:pointer;transition:opacity .2s}
.c-edge{background:var(--yel)}.c-run{background:#fff}.c-data{background:var(--teal)}.c-ops{background:var(--pink)}
.role.dim{opacity:.28}.role[aria-pressed=true]{outline:3px dashed var(--ink);outline-offset:3px}
.panel2,.panel.p{margin-top:1.5rem}
aside.panel{background:#fff;border:3px solid var(--ink);border-radius:WOB;padding:1rem 1.4rem;max-width:60ch;transform:none;margin-top:1.5rem}aside.panel h2{font-size:2rem}aside.panel p{margin:.4rem 0;color:var(--ink)}
.wires{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;overflow:visible;color:var(--ink);z-index:0;filter:url(#rough)}
.w{opacity:.75;transition:opacity .2s}.w.on{opacity:1;stroke-width:2.8}.w.off{opacity:.1}.role,.lane h2{position:relative;z-index:1}
.wl{font:400 1.1rem 'Caveat Brush',cursive;fill:var(--ink);paint-order:stroke;stroke:var(--paper);stroke-width:5px;stroke-linejoin:round}
@media(max-width:800px){.hero{grid-template-columns:1fr}.panels,.layout{grid-template-columns:1fr}.toc{position:static}.lane{grid-template-columns:1fr}.cells{grid-template-columns:repeat(3,1fr)}.gap{display:none}}
""".replace("WOB2", WOB2).replace("WOB", WOB)
HEAD = gfont("family=Caveat+Brush&family=Atkinson+Hyperlegible:wght@400;700")
ROUGH = '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><filter id="rough"><feTurbulence type="fractalNoise" baseFrequency=".035" numOctaves="2" seed="4"/><feDisplacementMap in="SourceGraphic" scale="5"/></filter></svg>'
COL = {"iac": "var(--teal)", "cicd": "var(--yel)", "development": "var(--pink)", "enterprise": "#B8C7FF"}


def landing():
    pan = ""
    for f in families():
        st = "".join(f'<a class="sticker" href="topic.html" style="--c2:#fff">{esc(t["label"])}<small>{t["count"]}</small></a>' for t in f["topics"])
        pan += f'<section class="panel" style="--c:{COL[f["id"]]}"><h2><span>{esc(f["label"])}</span></h2><p>{esc(f["description"])}</p><div class="stickers">{st}</div></section>'
    views = "".join(f'<a class="sticker" href="{"lenses" if v["id"] == "lenses" else "topic"}.html">{esc(v["label"])}</a>' for v in T["views"])
    body = (f'<div class="wrap"><header class="hero">{MASCOT}<div><h1>{esc(T["name"])}</h1><p class="say">{esc(T["tagline"])}</p></div></header>'
            '<label class="find"><span class="sr">Search every entry</span><input id="q" type="search" placeholder="What are you looking for?" autocomplete="off"></label>'
            '<p class="hint">Press / to search, Esc to clear, the down arrow to jump to results.</p><p id="st" class="sr" role="status"></p>'
            f'<main><div id="res" class="hits" role="region" aria-label="Search results" hidden></div><div id="fams"><div class="panels">{pan}</div>'
            f'<section class="note" id="views"><h2>Views</h2><p>Pictures that cut across the topics; they are not topics themselves.</p><div class="stickers">{views}</div></section></div></main></div>')
    return page("Atlas · zine", HEAD, body + search_block(), CSS)


def topic():
    arts = ""
    for i, eid in enumerate(("opengitops", "argo-cd", "flux")):
        e = entry(eid)
        v = e["version"]
        li = "".join(f"<li>{md(b)}</li>" for b in e["bullets"])
        warn = MASCOT.replace("7FE0D2", "FF9EC7").replace('M33 56C40 64 50 64 58 55', 'M33 60C40 52 50 52 58 59').replace('aria-label="Atlas mascot, a smiling globe"', 'aria-hidden="true"').replace('role="img"', "")
        g = f'<p class="gotcha">{warn}<span><b>Gotcha!</b>{md(e["gotcha"])}</span></p>' if e["gotcha"] else ""
        src = "".join(f'<a href="{esc(l["url"])}">{esc(l["label"])}</a>' for l in e["links"])
        arts += (f'<article class="entry" id="{eid}"><h2><span class="hl">{esc(e["name"])}</span></h2><div class="chips"><span class="k1">analysed {esc(v["analysed"])}</span>'
                 f'<span class="k2">checked {esc(v["checked"])}</span><span class="k3">{esc(e["status"])}</span><span class="k4">{esc(e["license"])}</span></div>'
                 f'<p class="sum">{esc(e["summary"])}</p><ul>{li}</ul>{g}<p class="srcs">{src}</p></article>')
    c = comparison()
    head = "".join(f"<th>{esc(x)}</th>" for x in c["columns"])
    rows = "".join(f'<tr><th scope="row">{esc(r["label"])}</th>' + "".join(f"<td>{md(x)}</td>" for x in r["cells"]) + "</tr>" for r in c["rows"])
    body = (f'<div class="wrap"><nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Atlas</a><a href="index.html">IaC</a><span>GitOps</span></nav>'
            f'<header class="hero">{MASCOT}<div><h1>{esc(G["title"])}</h1><p class="say">{esc(G["intro"])}</p></div></header><div class="layout">'
            '<nav class="toc" aria-label="On this page"><ul><li><a href="#opengitops">Principles</a></li><li><a href="#argo-cd">Argo CD</a></li><li><a href="#flux">Flux</a></li><li><a href="#cmp">Argo CD vs Flux</a></li></ul></nav>'
            f'<main>{arts}<section class="entry cmp" id="cmp"><h2>{esc(c["title"])}</h2><table><thead><tr><th></th>{head}</tr></thead><tbody>{rows}</tbody></table></section></main></div></div>')
    return page("GitOps · Atlas zine", HEAD, body, CSS)


def lenses():
    markup, js = lenses_markup()
    body = (ROUGH + f'<div class="wrap"><nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Atlas</a><a href="index.html#views">Views</a><span>Lenses</span></nav>'
            f'<header class="hero">{MASCOT}<div><h1>Lenses</h1><p class="say">Where does a service go? One picture of an application, five lenses.</p></div></header><main>{markup}</main></div>{js}')
    return page("Lenses · Atlas zine", HEAD, body, CSS)

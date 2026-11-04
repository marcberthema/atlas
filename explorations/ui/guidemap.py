"""World B: zoo and gardens guide map. Families are flat-colour lobes on water; capsules are controls."""
from common import *

LOBE = {"iac": ("#8ED462", "62% 38% 46% 54% / 55% 44% 56% 45%"), "cicd": ("#2BA0FF", "40% 60% 58% 42% / 46% 58% 42% 54%"),
        "development": ("#EBC1FF", "54% 46% 40% 60% / 60% 40% 60% 40%"), "enterprise": ("#FF705D", "46% 54% 60% 40% / 42% 56% 44% 58%")}

CSS = """
:root{--water:#E4F2F0;--land:#8ED462;--ink:#1D2A22;--yel:#F5E211;--cor:#FF705D;--blue:#2BA0FF;--lil:#EBC1FF;--g:'Familjen Grotesk','Helvetica Neue',Arial,sans-serif}
body{background:var(--water);color:var(--ink);font:500 1.0625rem/1.55 var(--g)}
::selection{background:var(--yel);color:var(--ink)}
:focus-visible{outline:3px solid var(--ink);outline-offset:3px}
a{text-decoration:none}
.page{max-width:1120px;margin:0 auto;padding:1.5rem clamp(1rem,3vw,2rem) 4rem}
h1,h2,h3{font-weight:600;margin:0}
.wm{font-size:clamp(3.4rem,12vw,6rem);line-height:.95;letter-spacing:-.04em;text-wrap:balance}
.tag{font-size:1.25rem;max-width:36ch;margin:.7rem 0 1.4rem;text-wrap:pretty}
.gate{display:flex;align-items:center;gap:.6rem;background:var(--yel);border-radius:999px;padding:.4rem .5rem .4rem 1.5rem;max-width:680px;transition:transform .4s cubic-bezier(.34,1.56,.64,1)}
.gate:focus-within{transform:scale(1.02)}
.gate input{flex:1;min-width:0;font:600 1.25rem var(--g);background:transparent;border:0;color:var(--ink);padding:.7rem 0}
.gate input:focus-visible{outline:0}.gate:focus-within{outline:3px solid var(--ink);outline-offset:3px}
.gate input::placeholder{color:#4D4A00}
.chip{display:inline-grid;place-items:center;min-width:2.2rem;height:2.2rem;padding:0 .6rem;border-radius:999px;background:var(--ink);color:#fff;font-size:.95rem;font-variant-numeric:tabular-nums}
.hint{font-size:.95rem;margin:.7rem 0 0;color:#2F4037}
.map{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));margin:2.5rem -1rem 0}
.lobe{background:var(--c);border-radius:var(--r);padding:clamp(2.4rem,6vw,4.5rem) clamp(2rem,6vw,4.5rem);margin:-1rem;min-height:22rem;position:relative}
.lobe h2{font-size:clamp(2.4rem,5vw,3.4rem);letter-spacing:-.03em;line-height:1}
.lobe p{margin:.6rem 0 1.2rem;max-width:30ch;text-wrap:pretty}
.caps{display:flex;flex-wrap:wrap;gap:.5rem}
.cap{display:inline-flex;align-items:center;gap:.7rem;background:#fff;color:var(--ink);font-weight:600;padding:.45rem .5rem .45rem 1.1rem;border-radius:999px;transition:transform .4s cubic-bezier(.34,1.56,.64,1)}
.cap:hover{transform:translateY(-3px)}
.cap .chip{height:1.9rem;min-width:1.9rem}
.cap.plain{padding-right:1.1rem}
.views{margin-top:3rem;background:#fff;border-radius:60px;padding:2rem 2.5rem}
.views h2{font-size:1.8rem}.views p{margin:.3rem 0 1rem;max-width:50ch}
.hits{display:grid;gap:.6rem;margin-top:2rem}
.hit{display:block;background:#fff;border-radius:30px;padding:1rem 1.6rem}.hit:hover,.hit:focus-visible{background:var(--yel)}
.hit b{display:block;font-size:1.25rem}.hit span{display:block}.hit small{font-size:.9rem;color:#2F4037}
.none{background:#fff;border-radius:30px;padding:1rem 1.6rem}.none button{font:inherit;font-weight:600;background:var(--yel);border:0;border-radius:999px;padding:.3rem .9rem;cursor:pointer}
/* coast header */
.coast{background:var(--land);border-radius:0 0 56% 44% / 0 0 36px 30px;padding:1.4rem clamp(1.2rem,5vw,4rem) clamp(2.4rem,5vw,4rem)}
.coast .in{max-width:1120px;margin:0 auto}
.crumbs{display:flex;gap:.4rem;flex-wrap:wrap;margin-bottom:1.6rem}
.crumbs a,.crumbs span{background:#fff;color:var(--ink);padding:.3rem 1rem;border-radius:999px;font-size:.98rem}
.coast .lede{max-width:56ch;font-size:1.2rem;margin:1rem 0 0;text-wrap:pretty}
.nav{display:flex;flex-wrap:wrap;gap:.5rem;margin:1.6rem 0}
.nav a{background:var(--yel);padding:.45rem 1.1rem;border-radius:999px;font-weight:600}
.entry{background:#fff;border-radius:52px;padding:clamp(1.6rem,4.5vw,3.2rem);margin:0 auto 2rem;max-width:900px}
.entry h2{font-size:clamp(2rem,5vw,2.8rem);letter-spacing:-.03em;line-height:1.05}
.chips{display:flex;flex-wrap:wrap;gap:.45rem;margin:1rem 0}
.chips span{border-radius:999px;padding:.2rem .9rem;font-size:.95rem;font-variant-numeric:tabular-nums;font-weight:600}
.k-ver{background:var(--blue)}.k-chk{background:var(--yel)}.k-st{background:var(--land)}.k-lic{background:var(--lil)}
.sum{font-size:1.25rem;line-height:1.45;max-width:58ch;margin:0 0 1rem;text-wrap:pretty}
.entry ul{max-width:64ch;padding-left:1.2rem}.entry li{margin:.4rem 0}
code{font:.9em ui-monospace,Menlo,monospace;background:var(--water);padding:.05em .35em;border-radius:6px}
.gotcha{border:2px solid var(--cor);border-radius:26px;padding:.8rem 1.3rem;margin:1.2rem 0;max-width:64ch}.gotcha b{background:var(--cor);padding:.05rem .7rem;border-radius:999px;margin-right:.5rem;font-size:.9rem}
.srcs{display:flex;flex-wrap:wrap;gap:.5rem}.srcs a{border:2px solid var(--ink);border-radius:999px;padding:.2rem 1rem;font-weight:600}.srcs a:hover{background:var(--yel)}
.cmp{background:var(--lil);border-radius:56px;padding:2.5rem;max-width:900px;margin:0 auto}
.cmp h2{font-size:2.2rem;letter-spacing:-.03em}.cmp>p{margin:.3rem 0 1rem}
table{border-collapse:separate;border-spacing:0 6px;width:100%;font-size:1rem}
th,td{text-align:left;vertical-align:top;padding:.8rem 1rem;background:#fff}
td:last-child,th:last-child{border-radius:0 24px 24px 0}th:first-child{border-radius:24px 0 0 24px}
thead th{background:transparent;font-size:1.05rem}tbody th{width:7rem}
/* lenses */
.lensbar{display:flex;flex-wrap:wrap;gap:.5rem;margin:0 0 .6rem}
.lensbtn{font:600 1rem var(--g);background:#fff;border:2px solid var(--ink);border-radius:999px;padding:.4rem 1.2rem;cursor:pointer;color:var(--ink)}
.lensbtn[aria-pressed=true]{background:var(--ink);color:#fff}
.about{min-height:3.2em;max-width:60ch;margin:0 0 1rem}
.lanes{display:grid;gap:.7rem}
.lane{background:#fff;border-radius:40px;padding:.9rem 1.4rem 1rem}
.lane h2{font-size:1rem;margin:0 0 .5rem}
.cells{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:.4rem}
.role{font:600 .95rem/1.15 var(--g);border:0;border-radius:999px;padding:.7rem .5rem;min-height:3rem;color:var(--ink);cursor:pointer;transition:opacity .3s,transform .4s cubic-bezier(.34,1.56,.64,1)}
.role:hover{transform:translateY(-2px)}
.c-edge{background:var(--yel)}.c-run{background:var(--blue)}.c-data{background:var(--land)}.c-ops{background:var(--lil)}
.role.dim{opacity:.3}.role[aria-pressed=true]{outline:3px solid var(--ink);outline-offset:2px}
.panel{margin-top:1.4rem;background:var(--cor);border-radius:48px;padding:1.4rem 2.2rem;max-width:640px}.panel h2{font-size:1.8rem}.panel p{margin:.4rem 0}
.wires{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;overflow:visible;color:#1D2A22}.wl{font:600 .85rem "Familjen Grotesk",sans-serif;fill:#1D2A22;paint-order:stroke;stroke:#fff;stroke-width:4px;stroke-linejoin:round}
@media(max-width:760px){.map{grid-template-columns:1fr;margin:2rem 0 0}.lobe{min-height:0;margin:-.6rem 0;border-radius:36% 64% 52% 48% / 22% 26% 74% 78%;padding:2.6rem 1.8rem}
.coast{border-radius:0 0 40px 40px}.views,.cmp{padding:1.6rem 1.4rem}.entry,.cmp,.views{border-radius:34px}.cells{grid-template-columns:repeat(2,1fr)}.gap{display:none}.lane{border-radius:30px}}
"""
HEAD = gfont("family=Familjen+Grotesk:wght@500;600")


def coast(title, lede, crumbs):
    cr = "".join(f'<a href="{h}">{esc(t)}</a>' if h else f"<span>{esc(t)}</span>" for t, h in crumbs)
    return (f'<header class="coast"><div class="in"><nav class="crumbs" aria-label="Breadcrumb">{cr}</nav>'
            f'<h1 class="wm">{esc(title)}</h1><p class="lede">{esc(lede)}</p></div></header>')


def landing():
    lobes = ""
    for f in families():
        c, r = LOBE[f["id"]]
        caps = "".join(f'<a class="cap" href="topic.html">{esc(t["label"])}<span class="chip" aria-label="{t["count"]} entries">{t["count"]}</span></a>' for t in f["topics"])
        lobes += f'<section class="lobe" style="--c:{c};--r:{r}"><h2>{esc(f["label"])}</h2><p>{esc(f["description"])}</p><div class="caps">{caps}</div></section>'
    views = "".join(f'<a class="cap plain" href="{"lenses" if v["id"] == "lenses" else "topic"}.html" style="background:var(--yel)">{esc(v["label"])}</a>' for v in T["views"])
    body = (f'<div class="page"><header><h1 class="wm">{esc(T["name"])}</h1><p class="tag">{esc(T["tagline"])}</p>'
            '<label class="sr" for="q">Search every entry</label><div class="gate"><input id="q" type="search" placeholder="Search every entry" autocomplete="off"><span class="chip" aria-hidden="true">/</span></div>'
            '<p class="hint">Esc clears the search. The down arrow moves into the results.</p><p id="st" class="sr" role="status"></p></header>'
            '<main><div id="res" class="hits" role="region" aria-label="Search results" hidden></div>'
            f'<div id="fams"><div class="map">{lobes}</div><section class="views" id="views"><h2>Views</h2><p>Pictures that cut across the topics; they are not topics themselves.</p><div class="caps">{views}</div></section></div></main></div>')
    return page("Atlas · guide map", HEAD, body + search_block(), CSS)


def topic():
    ents = ""
    for eid in ("opengitops", "argo-cd", "flux"):
        e = entry(eid)
        v = e["version"]
        li = "".join(f"<li>{md(b)}</li>" for b in e["bullets"])
        g = f'<p class="gotcha"><b>Gotcha</b>{md(e["gotcha"])}</p>' if e["gotcha"] else ""
        src = "".join(f'<a href="{esc(l["url"])}">{esc(l["label"])}</a>' for l in e["links"])
        ents += (f'<article class="entry" id="{eid}"><h2>{esc(e["name"])}</h2><div class="chips"><span class="k-ver">analysed {esc(v["analysed"])}</span>'
                 f'<span class="k-chk">checked {esc(v["checked"])}</span><span class="k-st">{esc(e["status"])}</span><span class="k-lic">{esc(e["license"])}</span></div>'
                 f'<p class="sum">{esc(e["summary"])}</p><ul>{li}</ul>{g}<div class="srcs">{src}</div></article>')
    c = comparison()
    head = "".join(f"<th>{esc(x)}</th>" for x in c["columns"])
    rows = "".join(f'<tr><th scope="row">{esc(r["label"])}</th>' + "".join(f"<td>{md(x)}</td>" for x in r["cells"]) + "</tr>" for r in c["rows"])
    body = (coast(G["title"], G["intro"], [("Atlas", "index.html"), ("IaC", "index.html"), ("GitOps", None)]) +
            '<div class="page"><nav class="nav" aria-label="On this page"><a href="#opengitops">Principles</a><a href="#argo-cd">Argo CD</a><a href="#flux">Flux</a><a href="#cmp">Compare</a></nav>'
            f'<main>{ents}<section class="cmp" id="cmp"><h2>{esc(c["title"])}</h2><p>How the two operators differ.</p><table><thead><tr><th></th>{head}</tr></thead><tbody>{rows}</tbody></table></section></main></div>')
    return page("GitOps · Atlas guide map", HEAD, body, CSS)


def lenses():
    markup, js = lenses_markup()
    body = (coast("Lenses", "Where does a service go? One picture of an application, five lenses.", [("Atlas", "index.html"), ("Views", "index.html#views"), ("Lenses", None)]) +
            f'<div class="page"><main>{markup}</main></div>{js}')
    return page("Lenses · Atlas guide map", HEAD, body, CSS)

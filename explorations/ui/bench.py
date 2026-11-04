"""World C: film cutting bench. Black ground, flag-orange grain, a perforated rail; running copy only in white windows."""
from common import *

HOLE = "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='32' height='22'%3E%3Crect x='7' y='5' width='18' height='12' rx='3' fill='%23F5F5F0'/%3E%3C/svg%3E\")"
GRAIN = "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='240' height='240'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 .22 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E\")"

CSS = """
:root{--blk:#0B0B0B;--org:#FF6A13;--win:#F5F5F0;--ink:#111;--mut:#4A4A44;--c:'Barlow Condensed','Arial Narrow',sans-serif;--r:'Barlow',system-ui,sans-serif}
body{background:var(--blk);color:var(--win);font:400 1.0625rem/1.6 var(--r)}
::selection{background:var(--org);color:#000}
:focus-visible{outline:3px solid var(--win);outline-offset:3px}
.field :focus-visible,.win :focus-visible{outline-color:#000}
a{text-decoration:none}
.perf{height:22px;background:var(--blk) HOLE repeat-x 0 0/32px 22px}
.field{background:var(--org) GRAIN;color:#000;padding:1.4rem clamp(1rem,4vw,3rem) 2rem}
.in{max-width:1180px;margin:0 auto}
.wm{font:700 clamp(4rem,15vw,6rem)/.9 var(--c);text-transform:uppercase;letter-spacing:-.01em;margin:.4rem 0 1rem}
.win{background:var(--win);color:var(--ink);padding:1rem 1.2rem}
.tag{display:inline-block;max-width:44ch;margin:0 0 1.2rem;font-size:1.15rem;text-wrap:pretty}
.find{display:flex;align-items:center;gap:1rem;max-width:720px;background:var(--win);color:var(--ink);padding:.2rem 1.2rem}
.find label{font:700 1rem var(--c);text-transform:uppercase;letter-spacing:.08em;white-space:nowrap}
#q{flex:1;min-width:0;font:600 1.4rem var(--c);background:transparent;border:0;color:var(--ink);padding:.9rem 0;letter-spacing:.02em}
#q:focus-visible{outline:0}.find:focus-within{outline:3px solid #000;outline-offset:3px}
.keys{font:600 1rem var(--c);text-transform:uppercase;letter-spacing:.06em;margin:.8rem 0 0}
.main{max-width:1180px;margin:0 auto;padding:2rem clamp(1rem,4vw,3rem) 4rem}
.strip{margin:0 0 2.2rem;background:#161616}
.strip .head{display:grid;grid-template-columns:auto 1fr;gap:1rem 1.4rem;align-items:center;padding:.9rem 1.2rem}
.strip h2{font:700 2.4rem/1 var(--c);text-transform:uppercase;color:var(--org);margin:0}
.strip .head p{margin:0;color:#D6D6CE;max-width:60ch}
.frames{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:12px;padding:.5rem 12px}
.frame{position:relative;display:flex;flex-direction:column;gap:.5rem;background:var(--win);color:var(--ink);padding:1rem 1.2rem 0;min-height:11rem;transition:transform .25s cubic-bezier(.2,.8,.2,1)}
.frame:hover{transform:translateY(-4px)}
.frame h3{font:700 2rem/1 var(--c);text-transform:uppercase;margin:0}
.frame p{margin:0;font-size:1rem;color:var(--mut);flex:1}
.cell{display:flex;justify-content:space-between;align-items:baseline;background:var(--blk);color:var(--org);margin:0 -1.2rem;padding:.35rem 1.2rem;font:600 1.05rem var(--c);text-transform:uppercase;letter-spacing:.06em;font-variant-numeric:tabular-nums}
.cell b{font-weight:700;font-size:1.5rem;color:var(--win)}
.flag{position:absolute;top:-6px;right:16px;width:24px;height:44px;background:var(--org);clip-path:polygon(0 0,100% 0,100% 100%,50% 78%,0 100%)}
.bin{margin-top:1rem}
.bin h2{font:700 1.6rem var(--c);text-transform:uppercase;color:var(--org);margin:0 0 .2rem}.bin>p{margin:0 0 1rem;color:#D6D6CE}
.pins{display:flex;flex-wrap:wrap;gap:2rem}
.pin{position:relative;width:min(100%,320px);transform-origin:50% -18px;animation:sway 6s ease-in-out infinite}
.pin::before{content:"";position:absolute;left:50%;top:-22px;width:12px;height:12px;margin-left:-6px;border-radius:50%;background:var(--win)}
.pin:nth-child(2){animation-delay:-3s}
@keyframes sway{50%{transform:rotate(1.6deg)}}
.hits{display:grid;gap:8px;margin-bottom:2rem}
.hit{display:block;background:var(--win);color:var(--ink);padding:.8rem 1.2rem}.hit:hover,.hit:focus-visible{background:var(--org)}
.hit b{display:block;font:700 1.5rem var(--c);text-transform:uppercase}.hit small{font:600 .95rem var(--c);text-transform:uppercase;letter-spacing:.08em;color:var(--mut)}
.none{background:var(--win);color:var(--ink);padding:1rem 1.2rem;margin:0}.none button{font:700 1rem var(--c);text-transform:uppercase;background:var(--blk);color:var(--org);border:0;padding:.3rem .8rem;cursor:pointer}
/* topic */
.crumb{display:flex;gap:6px;flex-wrap:wrap;font:700 1rem var(--c);text-transform:uppercase;letter-spacing:.08em}
.crumb a,.crumb span{background:#000;color:var(--org);padding:.15rem .7rem}.crumb a:hover{background:var(--win);color:#000}
.reel{max-width:1180px;margin:0 auto;padding:1.5rem clamp(1rem,4vw,3rem) 4rem;display:grid;grid-template-columns:220px minmax(0,1fr);gap:1.5rem}
.rule{position:sticky;top:1rem;align-self:start}
.rule h2{font:700 1.1rem var(--c);text-transform:uppercase;letter-spacing:.1em;color:var(--org);margin:0 0 .4rem}
.rule ul{list-style:none;margin:0 0 1.4rem;padding:0;display:grid;gap:6px}
.rule a{display:block;background:#1d1d1d;color:var(--win);font:600 1.15rem var(--c);text-transform:uppercase;letter-spacing:.04em;padding:.4rem .8rem}.rule a:hover{background:var(--org);color:#000}
.film{border-left:0;display:grid;gap:18px}
.take{background:#161616;padding:12px}
.take header{display:flex;flex-wrap:wrap;align-items:baseline;gap:.4rem 1rem;padding:.3rem .4rem .7rem}
.take h2{font:700 2.6rem/1 var(--c);text-transform:uppercase;color:var(--org);margin:0}
.take .grp{font:600 1rem var(--c);text-transform:uppercase;letter-spacing:.08em;color:#BDBDB4}
.marks{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:6px;margin:0 0 6px}
.marks div{background:var(--blk);padding:.4rem .8rem;border:1px solid #333}
.marks dt{font:600 .9rem var(--c);text-transform:uppercase;letter-spacing:.1em;color:#BDBDB4}
.marks dd{margin:0;font:700 1.5rem var(--c);color:var(--org);font-variant-numeric:tabular-nums}
.take .win{padding:1.2rem 1.4rem}
.sum{font-size:1.2rem;font-weight:600;line-height:1.45;margin:0 0 .8rem;max-width:60ch;text-wrap:pretty}
.take ul{margin:0 0 1rem;padding-left:1.2rem;max-width:64ch}.take li{margin:.35rem 0}
code{font:.9em ui-monospace,Menlo,monospace;background:#E4E4DA;padding:.05em .3em}
.gotcha{background:#000;color:var(--win);padding:.8rem 1rem;margin:1rem 0;max-width:64ch}.gotcha b{font:700 1rem var(--c);text-transform:uppercase;letter-spacing:.1em;background:var(--org);color:#000;padding:.05rem .6rem;margin-right:.6rem}
.gotcha code{background:#222;color:var(--win)}
.srcs{display:flex;flex-wrap:wrap;gap:6px}.srcs a{background:#000;color:var(--org);font:700 1.05rem var(--c);text-transform:uppercase;letter-spacing:.05em;padding:.25rem .8rem}.srcs a:hover{background:var(--org);color:#000}
table{border-collapse:collapse;width:100%;font-size:1rem;color:var(--ink)}
th,td{text-align:left;vertical-align:top;padding:.7rem .8rem;border-bottom:1px solid #C9C9BE}
thead th{background:#000;color:var(--org);font:700 1.1rem var(--c);text-transform:uppercase;letter-spacing:.08em;border:0}
tbody th{font:700 1.05rem var(--c);text-transform:uppercase;letter-spacing:.05em;width:7rem}
.take h3{font:700 1.8rem var(--c);text-transform:uppercase;color:var(--org);margin:0 0 .6rem}
/* lenses */
.lensbar{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 .6rem}
.lensbtn{font:700 1.15rem var(--c);text-transform:uppercase;letter-spacing:.06em;padding:.4rem 1.1rem;border:0;background:#1d1d1d;color:var(--win);cursor:pointer}
.lensbtn[aria-pressed=true]{background:var(--org);color:#000}
.about{background:var(--win);color:var(--ink);padding:.8rem 1.2rem;max-width:62ch;min-height:3.4em;margin:0 0 1rem}
.lanes{display:grid;gap:14px}
.lane{background:#161616;padding:6px 0}
.lane h2{margin:0;padding:.4rem 1rem;font:700 1.2rem var(--c);text-transform:uppercase;letter-spacing:.1em;color:var(--org)}
.cells{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:8px;padding:0 8px 8px}
.role{font:700 1.15rem/1.1 var(--c);text-transform:uppercase;letter-spacing:.03em;border:0;padding:.8rem .6rem;min-height:3.6rem;color:#000;cursor:pointer;transition:opacity .25s}
.role:hover{transform:translateY(-2px)}
.c-edge{background:var(--org)}.c-run{background:var(--win)}.c-data{background:#CFCFC6}.c-ops{background:#9C9C93}
.role.dim{opacity:.35;clip-path:polygon(0 0,calc(100% - 14px) 0,100% 14px,100% 100%,0 100%)}
.role[aria-pressed=true]{outline:3px solid var(--win);outline-offset:2px}
.panel{margin-top:1.4rem;background:var(--win);color:var(--ink);padding:1.2rem 1.4rem;max-width:62ch}.panel h2{font:700 2rem var(--c);text-transform:uppercase;margin:0 0 .3rem}.panel p{margin:.4rem 0}
@media(max-width:760px){.reel{grid-template-columns:1fr}.rule{position:static}.strip .head{grid-template-columns:1fr}.cells{grid-template-columns:repeat(2,1fr)}.gap{display:none}.find{flex-wrap:wrap;padding:.6rem 1rem}}
"""
CSS = CSS.replace("HOLE", HOLE).replace("GRAIN", GRAIN)
HEAD = gfont("family=Barlow+Condensed:wght@600;700&family=Barlow:wght@400;600")


def field(inner):
    return f'<div class="perf"></div><header class="field"><div class="in">{inner}</div></header><div class="perf"></div>'


def landing():
    strips = ""
    for f in families():
        fr = ""
        for t in f["topics"]:
            flag = '<span class="flag" role="img" aria-label="Where you stopped last time"></span>' if t["id"] == "gitops" else ""
            fr += (f'<a class="frame" href="topic.html">{flag}<h3>{esc(t["label"])}</h3><p>{esc(t["description"])}</p>'
                   f'<span class="cell">Entries <b>{t["count"]}</b></span></a>')
        strips += (f'<section class="strip" aria-labelledby="h-{f["id"]}"><div class="perf"></div><div class="head"><h2 id="h-{f["id"]}">{esc(f["label"])}</h2><p>{esc(f["description"])}</p></div>'
                   f'<div class="frames">{fr}</div><div class="perf"></div></section>')
    pins = "".join(f'<a class="frame pin" href="{"lenses" if v["id"] == "lenses" else "topic"}.html"><h3>{esc(v["label"])}</h3><p>{esc(v["description"])}</p><span class="cell">View</span></a>' for v in T["views"])
    body = (field(f'<h1 class="wm">{esc(T["name"])}</h1><p class="win tag">{esc(T["tagline"])}</p>'
                  '<div class="find"><label for="q">Search</label><input id="q" type="search" placeholder="Every entry, by name or word" autocomplete="off"></div>'
                  '<p class="keys">/ to search · Esc to clear · ↓ into the results</p><p id="st" class="sr" role="status"></p>') +
            '<main class="main"><div id="res" class="hits" role="region" aria-label="Search results" hidden></div>'
            f'<div id="fams">{strips}<section class="bin" id="views"><h2>Set aside: views</h2><p>Pictures that cut across the topics; they are not topics themselves.</p><div class="pins">{pins}</div></section></div></main>')
    return page("Atlas · cutting bench", HEAD, body + search_block(), CSS)


def topic():
    grp = {"opengitops": "Principles", "argo-cd": "GitOps operators", "flux": "GitOps operators"}
    takes = ""
    for eid in ("opengitops", "argo-cd", "flux"):
        e = entry(eid)
        v = e["version"]
        li = "".join(f"<li>{md(b)}</li>" for b in e["bullets"])
        g = f'<p class="gotcha"><b>Gotcha</b>{md(e["gotcha"])}</p>' if e["gotcha"] else ""
        src = "".join(f'<a href="{esc(l["url"])}">{esc(l["label"])}</a>' for l in e["links"])
        takes += (f'<article class="take" id="{eid}"><header><h2>{esc(e["name"])}</h2><span class="grp">{grp[eid]}</span></header>'
                  f'<dl class="marks"><div><dt>Analysed</dt><dd>{esc(v["analysed"])}</dd></div><div><dt>Released</dt><dd>{esc(v.get("released", ""))}</dd></div>'
                  f'<div><dt>Checked</dt><dd>{esc(v["checked"])}</dd></div><div><dt>Status</dt><dd>{esc(e["status"])}</dd></div><div><dt>Licence</dt><dd>{esc(e["license"])}</dd></div></dl>'
                  f'<div class="win"><p class="sum">{esc(e["summary"])}</p><ul>{li}</ul>{g}<div class="srcs">{src}</div></div></article>')
    c = comparison()
    head = "".join(f"<th>{esc(x)}</th>" for x in c["columns"])
    rows = "".join(f'<tr><th scope="row">{esc(r["label"])}</th>' + "".join(f"<td>{md(x)}</td>" for x in r["cells"]) + "</tr>" for r in c["rows"])
    nav = ('<nav class="rule" aria-label="On this page"><h2>On the rail</h2><ul><li><a href="#opengitops">Principles</a></li><li><a href="#argo-cd">Argo CD</a></li><li><a href="#flux">Flux</a></li></ul>'
           '<h2>Set aside</h2><ul><li><a href="#cmp">Argo CD vs Flux</a></li></ul></nav>')
    body = (field(f'<nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Atlas</a><a href="index.html">IaC</a><span>GitOps</span></nav><h1 class="wm">{esc(G["title"])}</h1><p class="win tag">{esc(G["intro"])}</p>') +
            f'<div class="reel">{nav}<main class="film">{takes}<section class="take" id="cmp"><h3>{esc(c["title"])}</h3><div class="win"><table><thead><tr><th></th>{head}</tr></thead><tbody>{rows}</tbody></table></div></section></main></div>')
    return page("GitOps · Atlas cutting bench", HEAD, body, CSS)


def lenses():
    markup, js = lenses_markup()
    body = (field('<nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Atlas</a><a href="index.html#views">Views</a><span>Lenses</span></nav><h1 class="wm">Lenses</h1><p class="win tag">Where does a service go? One picture of an application, five lenses.</p>') +
            f'<main class="main">{markup}</main>{js}')
    return page("Lenses · Atlas cutting bench", HEAD, body, CSS)

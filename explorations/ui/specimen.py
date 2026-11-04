"""World D: type specimen sheet. Giant grotesque names, mono metadata, one blue, hairline rules, a type-tester search."""
from common import *

CSS = """
:root{--ink:#0A0A0A;--blue:#1B2BD4;--paper:#FBFBFD;--mut:#4F5066;--g:'Bricolage Grotesque','Helvetica Neue',Arial,sans-serif;--s:'Source Serif 4',Georgia,serif;--m:'JetBrains Mono',ui-monospace,Menlo,monospace}
body{background:var(--paper);color:var(--ink);font:400 1.0625rem/1.65 var(--s)}
::selection{background:var(--blue);color:#fff}
:focus-visible{outline:3px solid var(--blue);outline-offset:3px}
a{text-decoration:none}
.top{display:flex;justify-content:space-between;align-items:baseline;gap:1rem;padding:1rem clamp(1rem,4vw,3rem);border-bottom:3px solid var(--ink);font:500 .85rem var(--m)}
.top b{font:700 1.3rem var(--g);letter-spacing:-.02em}.top a:hover{color:var(--blue)}
.wrap{max-width:1240px;margin:0 auto;padding:0 clamp(1rem,4vw,3rem)}
.hero{padding:clamp(2rem,6vw,4.5rem) 0 2rem}
h1{font:600 clamp(3.6rem,13vw,6rem)/.9 var(--g);letter-spacing:-.045em;margin:0 0 1rem;text-wrap:balance}
.tag{font:400 1.35rem/1.4 var(--s);max-width:40ch;margin:0 0 2rem;color:var(--mut);text-wrap:pretty}
.tester{display:flex;align-items:baseline;gap:1rem;border-bottom:3px solid var(--ink)}
#q{flex:1;min-width:0;font:500 clamp(1.6rem,5vw,3.4rem)/1.2 var(--g);letter-spacing:-.03em;border:0;background:transparent;color:var(--ink);padding:.5rem 0}
#q::placeholder{color:#6A6B84}#q:focus-visible{outline:0}.tester:focus-within{border-color:var(--blue)}
.tester span{font:500 .85rem var(--m);color:var(--mut);white-space:nowrap}
.fam{display:grid;grid-template-columns:200px minmax(0,1fr);gap:1.5rem 2rem;padding:1.6rem 0 2.2rem;border-top:1px solid var(--ink)}
.fam h2{font:700 1rem var(--m);margin:0;text-transform:uppercase;letter-spacing:.04em}
.fam .d{font:400 .95rem/1.5 var(--s);color:var(--mut);margin:.5rem 0 0;max-width:24ch}
.spec{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:0 1.5rem;align-items:baseline;padding:.4rem 0 .6rem;border-bottom:1px solid #D4D5E0}
.spec h3{font:600 clamp(2.2rem,6vw,4rem)/1.05 var(--g);letter-spacing:-.04em;margin:0;transition:color .15s}
.spec:hover h3{color:var(--blue)}
.spec .n{font:500 .95rem var(--m);font-variant-numeric:tabular-nums;color:var(--mut)}
.spec p{grid-column:1/-1;margin:.1rem 0 0;color:var(--mut);max-width:62ch}
.hits{display:grid;margin:1.5rem 0}.hit{display:grid;grid-template-columns:1fr auto;gap:0 1rem;padding:.8rem 0;border-bottom:1px solid #D4D5E0}
.hit:hover b,.hit:focus-visible b{color:var(--blue)}.hit b{font:600 1.8rem/1.1 var(--g);letter-spacing:-.03em}.hit small{font:500 .85rem var(--m);color:var(--mut)}.hit span{grid-column:1/-1;color:var(--mut)}
.none{padding:1rem 0}.none button{font:inherit;color:var(--blue);background:none;border:0;border-bottom:1px solid;padding:0;cursor:pointer}
.crossing{display:flex;flex-wrap:wrap;gap:.6rem 2rem}.crossing a{font:600 1.6rem var(--g);letter-spacing:-.03em}.crossing a:hover{color:var(--blue)}
.foot{border-top:3px solid var(--ink);padding:1rem 0 3rem;font:500 .85rem var(--m);color:var(--mut)}
/* topic */
.crumb{font:500 .85rem var(--m);display:flex;gap:.6rem;flex-wrap:wrap;padding-top:1.2rem}.crumb a:hover{color:var(--blue)}
.lede{font:400 1.4rem/1.45 var(--s);max-width:48ch;color:var(--mut);margin:0 0 2.5rem;text-wrap:pretty}
.cols{display:grid;grid-template-columns:200px minmax(0,1fr);gap:2rem}
.toc{position:sticky;top:1rem;align-self:start;font:500 .9rem/1.3 var(--m)}.toc ul{list-style:none;margin:0;padding:0;display:grid;gap:.6rem}.toc a:hover{color:var(--blue)}
.entry{padding:1.4rem 0 3rem;border-top:3px solid var(--ink)}
.entry h2{font:600 clamp(2.4rem,6vw,4rem)/1 var(--g);letter-spacing:-.04em;margin:0 0 .8rem;text-wrap:balance}
.body{display:grid;grid-template-columns:230px minmax(0,1fr);gap:1rem 2.5rem}
dl.sp{margin:0;font:500 .85rem/1.3 var(--m);align-self:start}
.sp div{display:flex;justify-content:space-between;gap:1rem;padding:.45rem 0;border-bottom:1px solid #D4D5E0}.sp dt{color:var(--mut)}.sp dd{margin:0;font-variant-numeric:tabular-nums;text-align:right}
.sum{font:400 1.35rem/1.45 var(--s);max-width:56ch;margin:0 0 1rem;text-wrap:pretty}
.read{max-width:64ch}.read ul{padding-left:1.2rem}.read li{margin:.4rem 0}
code{font:.88em var(--m);background:#ECECF6;padding:.05em .3em}
.gotcha{border:2px solid var(--blue);padding:.8rem 1rem;margin:1.2rem 0}.gotcha b{font:700 .85rem var(--m);text-transform:uppercase;color:var(--blue);margin-right:.6rem}
.srcs{display:flex;flex-wrap:wrap;gap:.4rem 1.4rem;font:500 .9rem var(--m)}.srcs a{border-bottom:1px solid}.srcs a:hover{color:var(--blue)}
.cmp h2{font:600 2.6rem var(--g);letter-spacing:-.04em;margin:0 0 1rem}
table{border-collapse:collapse;width:100%}th,td{text-align:left;vertical-align:top;padding:.8rem .8rem .8rem 0;border-bottom:1px solid #D4D5E0}
thead th{font:700 .85rem var(--m);text-transform:uppercase;border-bottom:2px solid var(--ink)}tbody th{font:600 1.1rem var(--g);width:7rem}
/* lenses */
.lensbar{display:flex;flex-wrap:wrap;gap:0;margin:0 0 .8rem;border:2px solid var(--ink);width:max-content;max-width:100%}
.lensbtn{font:600 .9rem var(--m);padding:.55rem 1.1rem;border:0;border-right:2px solid var(--ink);background:transparent;color:var(--ink);cursor:pointer}.lensbtn:last-child{border-right:0}
.lensbtn[aria-pressed=true]{background:var(--blue);color:#fff}
.about{max-width:60ch;min-height:3.3em;color:var(--mut);margin:0 0 1rem}
.lane{display:grid;grid-template-columns:150px 1fr;gap:.5rem 1rem;align-items:center;padding:.7rem 0;border-top:1px solid var(--ink)}
.lane h2{margin:0;font:700 .85rem var(--m);text-transform:uppercase}
.cells{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:.5rem}
.role{font:600 1rem/1.15 var(--g);letter-spacing:-.01em;padding:.8rem .5rem;min-height:3.4rem;border:1.5px solid var(--ink);background:var(--paper);color:var(--ink);cursor:pointer;transition:opacity .2s}
.c-run{background:var(--ink);color:#fff}.c-data{background:#E1E4FA}.c-ops{background:var(--blue);color:#fff;border-color:var(--blue)}
.role.dim{opacity:.25}.role[aria-pressed=true]{outline:3px solid var(--blue);outline-offset:2px}
.panel{margin-top:1.5rem;border:2px solid var(--ink);padding:1rem 1.3rem;max-width:62ch}.panel h2{font:600 2rem var(--g);letter-spacing:-.03em;margin:0 0 .3rem}.panel p{margin:.4rem 0}
.wires{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;overflow:visible;color:var(--blue);z-index:0}
.w{opacity:.65;transition:opacity .2s}.w.on{opacity:1;stroke-width:2.4}.w.off{opacity:.1}.role,.lane h2{position:relative;z-index:1}
.wl{font:500 .8rem 'JetBrains Mono',monospace;fill:var(--ink);paint-order:stroke;stroke:var(--paper);stroke-width:5px;stroke-linejoin:round}
@media(max-width:800px){.fam,.cols,.body{grid-template-columns:1fr}.toc{position:static}.lane{grid-template-columns:1fr}.cells{grid-template-columns:repeat(3,1fr)}.gap{display:none}}
"""
HEAD = gfont("family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,600;12..96,700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=JetBrains+Mono:wght@500;700")


def top(nav=True):
    return '<header class="top"><b><a href="index.html">Atlas</a></b><span>Reference, with sources and versions</span></header>'


def landing():
    fams = ""
    for f in families():
        rows = "".join(f'<a class="spec" href="topic.html"><h3>{esc(t["label"])}</h3><span class="n">{t["count"]} entries</span><p>{esc(t["description"])}</p></a>' for t in f["topics"])
        fams += f'<section class="fam"><div><h2>{esc(f["label"])}</h2><p class="d">{esc(f["description"])}</p></div><div>{rows}</div></section>'
    views = "".join(f'<a href="{"lenses" if v["id"] == "lenses" else "topic"}.html">{esc(v["label"])}</a>' for v in T["views"])
    body = (top() + f'<main class="wrap"><div class="hero"><h1>{esc(T["name"])}</h1><p class="tag">{esc(T["tagline"])}</p>'
            '<div class="tester"><label class="sr" for="q">Search every entry</label><input id="q" type="search" placeholder="Type to search every entry" autocomplete="off"><span>/ search · esc clear</span></div><p id="st" class="sr" role="status"></p></div>'
            f'<div id="res" class="hits" role="region" aria-label="Search results" hidden></div><div id="fams">{fams}'
            f'<section class="fam" id="views"><div><h2>Views</h2><p class="d">Pictures that cut across the topics; they are not topics themselves.</p></div><div class="crossing">{views}</div></section></div></main>')
    return page("Atlas · specimen", HEAD, body + search_block(), CSS)


def topic():
    arts = ""
    for eid in ("opengitops", "argo-cd", "flux"):
        e = entry(eid)
        v = e["version"]
        li = "".join(f"<li>{md(b)}</li>" for b in e["bullets"])
        g = f'<p class="gotcha"><b>Gotcha</b>{md(e["gotcha"])}</p>' if e["gotcha"] else ""
        src = "".join(f'<a href="{esc(l["url"])}">{esc(l["label"])}</a>' for l in e["links"])
        sp = "".join(f"<div><dt>{k}</dt><dd>{esc(val)}</dd></div>" for k, val in (("Analysed", v["analysed"]), ("Released", v.get("released", "")), ("Checked", v["checked"]), ("Status", e["status"]), ("Depth", e["level"]), ("Licence", e["license"])))
        arts += (f'<article class="entry" id="{eid}"><h2>{esc(e["name"])}</h2><div class="body"><dl class="sp">{sp}</dl>'
                 f'<div class="read"><p class="sum">{esc(e["summary"])}</p><ul>{li}</ul>{g}<p class="srcs">{src}</p></div></div></article>')
    c = comparison()
    head = "".join(f"<th>{esc(x)}</th>" for x in c["columns"])
    rows = "".join(f'<tr><th scope="row">{esc(r["label"])}</th>' + "".join(f"<td>{md(x)}</td>" for x in r["cells"]) + "</tr>" for r in c["rows"])
    body = (top() + f'<main class="wrap"><nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Atlas</a><span>/</span><a href="index.html">IaC</a><span>/</span><span>GitOps</span></nav>'
            f'<div class="hero"><h1>{esc(G["title"])}</h1><p class="lede">{esc(G["intro"])}</p></div><div class="cols">'
            '<nav class="toc" aria-label="On this page"><ul><li><a href="#opengitops">OpenGitOps principles</a></li><li><a href="#argo-cd">Argo CD</a></li><li><a href="#flux">Flux</a></li><li><a href="#cmp">Argo CD and Flux</a></li></ul></nav>'
            f'<div>{arts}<section class="entry cmp" id="cmp"><h2>{esc(c["title"])}</h2><table><thead><tr><th></th>{head}</tr></thead><tbody>{rows}</tbody></table></section></div></div></main>')
    return page("GitOps · Atlas specimen", HEAD, body, CSS)


def lenses():
    markup, js = lenses_markup()
    body = (top() + '<main class="wrap"><nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Atlas</a><span>/</span><a href="index.html#views">Views</a><span>/</span><span>Lenses</span></nav>'
            f'<div class="hero"><h1>Lenses</h1><p class="lede">Where does a service go? One picture of an application, five lenses.</p></div>{markup}</main>{js}')
    return page("Lenses · Atlas specimen", HEAD, body, CSS)

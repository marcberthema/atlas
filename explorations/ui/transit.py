"""World F: transit diagram. Families are coloured lines, topics are stations, views are interchanges."""
from common import *

LINE = {"iac": ("#0057B8", "#fff"), "cicd": ("#D6001C", "#fff"), "development": ("#00843D", "#fff"), "enterprise": ("#F28C00", "#14181F")}

CSS = """
:root{--ink:#14181F;--ground:#FFFFFF;--soft:#F2F4F7;--mut:#4A5260;--rule:#D5DAE1;--g:'Red Hat Display','Helvetica Neue',Arial,sans-serif}
body{background:var(--ground);color:var(--ink);font:500 1.0625rem/1.6 var(--g)}
::selection{background:#0057B8;color:#fff}
:focus-visible{outline:3px solid var(--ink);outline-offset:3px}
a{text-decoration:none;color:inherit}
.wrap{max-width:1120px;margin:0 auto;padding:1.2rem clamp(1rem,3vw,2rem) 4rem}
.brand{display:flex;align-items:center;gap:.8rem;margin-bottom:1.6rem}
.brand .bar{display:inline-flex;align-items:center;height:2.2rem;padding:0 1rem;background:var(--ink);color:#fff;font-weight:900;letter-spacing:.02em;border-radius:6px}
.brand span{color:var(--mut);font-size:.95rem}
h1{font:900 clamp(3.2rem,11vw,6rem)/.95 var(--g);letter-spacing:-.04em;margin:0 0 .8rem;text-wrap:balance}
.tag{font-size:1.25rem;max-width:44ch;color:var(--mut);margin:0 0 1.6rem;text-wrap:pretty}
.plan{display:flex;align-items:center;gap:1rem;max-width:680px;background:var(--soft);border:3px solid var(--ink);border-radius:999px;padding:.3rem 1.4rem}
.plan svg{flex:none}.plan input{flex:1;min-width:0;font:700 1.3rem var(--g);border:0;background:transparent;color:var(--ink);padding:.8rem 0}.plan input:focus-visible{outline:0}.plan:focus-within{outline:3px solid #0057B8;outline-offset:3px}
.hint{font-size:.95rem;color:var(--mut);margin:.6rem 0 0}
.line{margin:3rem 0 0}
.lname{display:inline-block;margin:0;padding:.2rem 1.1rem;border-radius:999px;background:var(--c);color:var(--cf);font:900 1.2rem var(--g);letter-spacing:.02em}
.line>p{margin:.5rem 0 1.4rem;color:var(--mut);max-width:60ch}
.route{list-style:none;margin:0;padding:0;display:flex;position:relative}
.route::before{content:"";position:absolute;left:13px;right:0;top:7px;height:12px;background:var(--c);border-radius:0 6px 6px 0}
.stn{display:block;flex:1;min-width:0;padding-right:1.2rem;position:relative}
.dot{display:block;width:26px;height:26px;border-radius:50%;background:#fff;border:6px solid var(--c);margin-bottom:.8rem;transition:transform .2s}
.stn a{display:block;border-radius:8px}.stn:hover .dot,.stn a:focus-visible .dot{transform:scale(1.25);background:var(--c)}
.stn b{display:block;font:900 1.4rem/1.15 var(--g);letter-spacing:-.02em}.stn small{display:block;color:var(--mut);font-weight:700;font-variant-numeric:tabular-nums}
.stn span.d{display:block;color:var(--mut);font-size:.98rem;line-height:1.4;margin-top:.3rem;max-width:30ch}
.inter{margin-top:3.4rem;border-top:3px solid var(--ink);padding-top:1.2rem}
.inter h2{margin:0;font:900 1.2rem var(--g)}.inter>p{margin:.4rem 0 1rem;color:var(--mut)}
.inter ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:1rem 2.5rem}
.xing{display:flex;align-items:center;gap:.8rem}.xing i{width:30px;height:30px;border-radius:50%;border:6px solid var(--ink);background:#fff;flex:none}.xing b{font:900 1.4rem var(--g);letter-spacing:-.02em}.xing:hover i{background:var(--ink)}
.board{display:grid;gap:3px;margin:1.6rem 0;background:var(--ink);padding:3px;border-radius:8px}
.hit{display:grid;grid-template-columns:1fr auto;gap:0 1rem;padding:.7rem 1.1rem;background:#1D2430;color:#fff}.hit:hover,.hit:focus-visible{background:#2B3547}
.hit b{font:900 1.35rem var(--g)}.hit small{font-weight:700;color:#FFD23F;align-self:center}.hit span{grid-column:1/-1;color:#C8CFDA}
.none{background:var(--soft);padding:1rem 1.2rem;border-radius:8px}.none button{font:inherit;font-weight:900;border:2px solid var(--ink);background:#fff;border-radius:999px;padding:.1rem .9rem;cursor:pointer}
/* topic */
.pill{display:inline-block;padding:.1rem .9rem;border-radius:999px;background:var(--c);color:var(--cf);font-weight:900;font-size:.95rem}
.crumb{display:flex;align-items:center;gap:.6rem;flex-wrap:wrap;margin-bottom:1.2rem;font-weight:700;color:var(--mut)}.crumb a:hover{color:var(--ink)}
.strip{position:sticky;top:0;z-index:5;background:var(--ground);padding:.8rem 0;border-bottom:1px solid var(--rule);margin:1.5rem 0}
.strip ol{list-style:none;margin:0;padding:0;display:flex;position:relative}
.strip ol::before{content:"";position:absolute;left:10px;right:10px;top:7px;height:8px;background:var(--c);border-radius:4px}
.strip li{flex:1;position:relative}.strip a{display:block;font-weight:700;font-size:.95rem}.strip a i{display:block;width:22px;height:22px;border-radius:50%;background:#fff;border:5px solid var(--c);margin-bottom:.3rem}
.strip a:hover i{background:var(--c)}.strip li:last-child{flex:none}
.stops{position:relative;padding-left:64px}
.stops::before{content:"";position:absolute;left:19px;top:20px;bottom:0;width:12px;background:var(--c);border-radius:6px 6px 0 0}
.stop{position:relative;padding-bottom:3rem}
.stop::before{content:"";position:absolute;left:-64px;top:6px;width:26px;height:26px;margin-left:7px;border-radius:50%;background:#fff;border:6px solid var(--c)}
.stop h2{font:900 clamp(2.2rem,5.5vw,3.2rem)/1.05 var(--g);letter-spacing:-.035em;margin:0 0 .6rem;text-wrap:balance}
.chips{display:flex;flex-wrap:wrap;gap:.5rem;margin:.4rem 0 1rem}.chips span{border-radius:999px;padding:.1rem .9rem;font-weight:700;font-size:.95rem;font-variant-numeric:tabular-nums;border:2px solid var(--ink)}
.chips .v{background:var(--ink);color:#fff}
.sum{font-size:1.3rem;line-height:1.5;max-width:58ch;margin:0 0 1rem;text-wrap:pretty}
.stop ul{max-width:64ch;padding-left:1.2rem}.stop li{margin:.4rem 0}
code{font:.88em ui-monospace,Menlo,monospace;background:var(--soft);padding:.05em .3em;border-radius:4px}
.gotcha{border:3px solid #D6001C;border-radius:12px;padding:.7rem 1.1rem;margin:1.1rem 0;max-width:64ch}.gotcha b{background:#D6001C;color:#fff;border-radius:999px;padding:0 .7rem;margin-right:.6rem;font-size:.9rem}
.srcs{display:flex;flex-wrap:wrap;gap:.5rem}.srcs a{border:2px solid var(--ink);border-radius:999px;padding:.1rem .9rem;font-weight:700}.srcs a:hover{background:var(--ink);color:#fff}
.cmp h2{font:900 2.4rem var(--g);letter-spacing:-.03em;margin:0 0 .8rem}
table{border-collapse:collapse;width:100%;font-size:1rem}th,td{text-align:left;vertical-align:top;padding:.8rem .8rem .8rem 0;border-bottom:1px solid var(--rule)}
thead th{font-weight:900;border-bottom:3px solid var(--ink)}tbody th{width:7rem;font-weight:900}
/* lenses */
.lensbar{display:flex;flex-wrap:wrap;gap:.5rem;margin:0 0 .6rem}
.lensbtn{font:900 1rem var(--g);padding:.4rem 1.2rem;border:3px solid var(--ink);border-radius:999px;background:#fff;color:var(--ink);cursor:pointer}.lensbtn[aria-pressed=true]{background:var(--ink);color:#fff}
.about{max-width:60ch;min-height:3.3em;color:var(--mut);margin:0 0 1rem}
.lane{padding:.8rem 0;border-top:1px solid var(--rule)}
.lane h2{margin:0 0 .5rem;display:inline-block;font:900 .95rem var(--g);padding:0 .8rem;border-radius:999px;background:var(--ink);color:#fff}
.cells{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:.6rem}
.role{font:700 1rem/1.15 var(--g);padding:.75rem .4rem;min-height:3.4rem;border-radius:10px;background:#fff;color:var(--ink);border:4px solid var(--ink);cursor:pointer;transition:opacity .2s}
.c-edge{border-color:#F28C00}.c-run{border-color:#0057B8}.c-data{border-color:#00843D}.c-ops{border-color:#D6001C}
.role.dim{opacity:.25}.role[aria-pressed=true]{background:var(--ink);color:#fff}
.legend{display:flex;flex-wrap:wrap;gap:.4rem 1.2rem;font-weight:700;font-size:.95rem;margin:0 0 1rem}.legend span::before{content:"";display:inline-block;width:14px;height:14px;border-radius:50%;border:4px solid var(--k);margin-right:.4rem;vertical-align:-1px}
.panel{margin-top:1.5rem;background:var(--soft);border-radius:12px;padding:1rem 1.3rem;max-width:62ch}.panel h2{font:900 1.8rem var(--g);letter-spacing:-.03em;margin:0 0 .3rem}.panel p{margin:.4rem 0}
.wires{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;overflow:visible;color:#5C6675;z-index:0}
.w{opacity:.85;stroke-width:3;transition:opacity .2s}.w.on{opacity:1;stroke-width:4;color:var(--ink)}.w.off{opacity:.1}.role,.lane h2{position:relative;z-index:1}
.wl{font:700 .85rem var(--g);fill:var(--ink);paint-order:stroke;stroke:#fff;stroke-width:5px;stroke-linejoin:round}
@media(max-width:760px){.route{flex-direction:column;gap:1.2rem}.route::before{left:7px;right:auto;top:13px;bottom:13px;width:12px;height:auto;border-radius:6px}
.stn a{display:grid;grid-template-columns:26px 1fr;gap:0 1rem}.dot{grid-row:1/4;margin:0}.strip ol{overflow-x:auto}.cells{grid-template-columns:repeat(3,1fr)}.gap{display:none}}
"""
HEAD = gfont("family=Red+Hat+Display:wght@500;700;900")
PIN = '<svg width="22" height="22" viewBox="0 0 22 22" aria-hidden="true"><circle cx="11" cy="11" r="8" fill="#fff" stroke="#14181F" stroke-width="4"/></svg>'


def brand(sub="A reference you can ride"):
    return f'<div class="brand"><a class="bar" href="index.html">ATLAS</a><span>{sub}</span></div>'


def landing():
    lines = ""
    for f in families():
        c, cf = LINE[f["id"]]
        st = "".join(f'<li class="stn"><a href="topic.html"><i class="dot"></i><b>{esc(t["label"])}</b><small>{t["count"]} entries</small><span class="d">{esc(t["description"])}</span></a></li>' for t in f["topics"])
        lines += f'<section class="line" style="--c:{c};--cf:{cf}"><h2 class="lname">{esc(f["label"])}</h2><p>{esc(f["description"])}</p><ol class="route">{st}</ol></section>'
    xs = "".join(f'<li><a class="xing" href="{"lenses" if v["id"] == "lenses" else "topic"}.html"><i></i><b>{esc(v["label"])}</b></a></li>' for v in T["views"])
    body = (f'<div class="wrap">{brand()}<h1>{esc(T["name"])}</h1><p class="tag">{esc(T["tagline"])}</p>'
            f'<label class="plan"><span class="sr">Search every entry</span>{PIN}<input id="q" type="search" placeholder="Where to? Search every entry" autocomplete="off"></label>'
            '<p class="hint">Press / to search, Esc to clear, the down arrow to reach the results.</p><p id="st" class="sr" role="status"></p>'
            f'<main><div id="res" class="board" role="region" aria-label="Search results" hidden></div><div id="fams">{lines}'
            f'<section class="inter" id="views"><h2>Interchanges</h2><p>Views that cut across the lines; they are not topics themselves.</p><ul>{xs}</ul></section></div></main></div>')
    return page("Atlas · transit", HEAD, body + search_block(), CSS)


def topic():
    c, cf = LINE["iac"]
    stops = ""
    for eid in ("opengitops", "argo-cd", "flux"):
        e = entry(eid)
        v = e["version"]
        li = "".join(f"<li>{md(b)}</li>" for b in e["bullets"])
        g = f'<p class="gotcha"><b>Gotcha</b>{md(e["gotcha"])}</p>' if e["gotcha"] else ""
        src = "".join(f'<a href="{esc(l["url"])}">{esc(l["label"])}</a>' for l in e["links"])
        stops += (f'<article class="stop" id="{eid}"><h2>{esc(e["name"])}</h2><div class="chips"><span class="v">analysed {esc(v["analysed"])}</span><span>checked {esc(v["checked"])}</span>'
                  f'<span>{esc(e["status"])}</span><span>{esc(e["license"])}</span></div><p class="sum">{esc(e["summary"])}</p><ul>{li}</ul>{g}<p class="srcs">{src}</p></article>')
    cm = comparison()
    head = "".join(f"<th>{esc(x)}</th>" for x in cm["columns"])
    rows = "".join(f'<tr><th scope="row">{esc(r["label"])}</th>' + "".join(f"<td>{md(x)}</td>" for x in r["cells"]) + "</tr>" for r in cm["rows"])
    strip = "".join(f'<li><a href="#{i}"><i></i>{n}</a></li>' for i, n in (("opengitops", "Principles"), ("argo-cd", "Argo CD"), ("flux", "Flux"), ("cmp", "Compare")))
    body = (f'<div class="wrap" style="--c:{c};--cf:{cf}">{brand()}<nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Atlas</a><span>›</span><span class="pill">IaC line</span><span>›</span><span>GitOps</span></nav>'
            f'<h1>{esc(G["title"])}</h1><p class="tag">{esc(G["intro"])}</p><nav class="strip" aria-label="Stops on this page"><ol>{strip}</ol></nav>'
            f'<main><div class="stops">{stops}</div><section class="cmp" id="cmp"><h2>{esc(cm["title"])}</h2><table><thead><tr><th></th>{head}</tr></thead><tbody>{rows}</tbody></table></section></main></div>')
    return page("GitOps · Atlas transit", HEAD, body, CSS)


def lenses():
    markup, js = lenses_markup()
    legend = '<p class="legend"><span style="--k:#F28C00">Edge</span><span style="--k:#0057B8">Runs the app</span><span style="--k:#00843D">Data</span><span style="--k:#D6001C">Operations</span></p>'
    body = (f'<div class="wrap">{brand()}<nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Atlas</a><span>›</span><a href="index.html#views">Interchanges</a><span>›</span><span>Lenses</span></nav>'
            f'<h1>Lenses</h1><p class="tag">Where does a service go? One picture of an application, five lenses.</p>{legend}<main>{markup}</main></div>{js}')
    return page("Lenses · Atlas transit", HEAD, body, CSS)

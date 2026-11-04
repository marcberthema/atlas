"""World A: field guide. Entries are species accounts; families are colour-tabbed edge-index tabs."""
from common import *

TAB = {"iac": ("#E9A21B", "#13211B"), "cicd": ("#C93A1F", "#fff"), "development": ("#2E6FD2", "#fff"), "enterprise": ("#7B4FB8", "#fff")}

CSS = """
:root{--cloth:#0E4B3B;--page:#F3F7F4;--ink:#13211B;--mut:#46594F;--rule:#C9D6CE;--read:'Literata',Georgia,serif;--lab:'Barlow Semi Condensed','Arial Narrow',sans-serif}
body{background:var(--page);color:var(--ink);font:1.0625rem/1.65 var(--read)}
::selection{background:#E9A21B;color:#13211B}
:focus-visible{outline:3px solid #E9A21B;outline-offset:2px}
.mast :focus-visible{outline-color:#fff}
.mast{background:var(--cloth);color:#F3F7F4;padding:1.2rem max(1.25rem,calc(50vw - 500px)) 1.6rem;padding-right:max(4rem,calc(50vw - 460px))}
.mast a{text-decoration:none}
.crumb{font:600 .95rem var(--lab);letter-spacing:.06em;text-transform:uppercase;display:flex;gap:.6rem;flex-wrap:wrap}
.crumb a:hover{text-decoration:underline}
.mark{font:700 clamp(2.6rem,8vw,5rem)/1 var(--read);letter-spacing:-.02em;margin:.6rem 0 .3rem;text-wrap:balance}
.tag{font:500 1.15rem/1.4 var(--lab);max-width:44ch;margin:0 0 1.2rem;color:#CFE3D9;text-wrap:pretty}
.lede{max-width:62ch;margin:0;color:#DCEBE3;text-wrap:pretty}
#q{display:block;width:100%;max-width:640px;font:500 1.2rem var(--read);padding:.8rem 1rem;border:2px solid #F3F7F4;border-radius:8px;background:#fff;color:var(--ink)}
.keyhint{font:500 .95rem var(--lab);color:#CFE3D9;margin:.5rem 0 0;letter-spacing:.03em}
.wrap{max-width:1000px;margin:0 auto;padding:2rem 1.25rem 4rem;padding-right:4rem}
.tabs{position:fixed;right:0;top:34vh;display:grid;gap:6px;z-index:5}
.tabs a{writing-mode:vertical-rl;padding:16px 9px;background:var(--c);color:var(--cf);font:600 .95rem var(--lab);letter-spacing:.08em;text-transform:uppercase;text-decoration:none;border-radius:8px 0 0 8px;transition:padding .2s}
.tabs a:hover,.tabs a[aria-current]{padding-right:20px}
.fam{margin:0 0 3rem}
.fam h2{display:inline-block;margin:0;padding:.15rem .8rem;background:var(--c);color:var(--cf);font:700 1.05rem var(--lab);letter-spacing:.08em;text-transform:uppercase;border-radius:6px}
.fam>p{margin:.5rem 0 .6rem;color:var(--mut);max-width:60ch}
.acct{display:grid;grid-template-columns:1fr auto;gap:.1rem 1.5rem;padding:1rem .8rem;border-bottom:1px solid var(--rule);text-decoration:none;border-radius:6px}
.acct:hover{background:color-mix(in srgb,var(--c) 11%,transparent)}
.acct h3{margin:0;font:600 1.45rem/1.25 var(--read)}
.acct .id{grid-column:1;margin:0;color:var(--mut);max-width:60ch}
.acct .also{grid-column:1;margin:.2rem 0 0;font:500 .98rem var(--lab);letter-spacing:.02em;color:var(--mut)}
.acct .also b{color:var(--ink);font-weight:600}
.acct .n{grid-row:1/3;grid-column:2;text-align:right;font:600 2rem/1 var(--lab);font-variant-numeric:tabular-nums}
.acct .n small{display:block;font:500 .9rem var(--lab);color:var(--mut);text-transform:uppercase;letter-spacing:.06em}
.hit{display:block;padding:.8rem;border-bottom:1px solid var(--rule);text-decoration:none}
.hit:hover,.hit:focus-visible{background:#E4EEE8}
.hit b{display:block;font-size:1.2rem}.hit span{display:block;color:var(--mut)}.hit small{font:600 .9rem var(--lab);text-transform:uppercase;letter-spacing:.06em;color:var(--cloth)}
.none button{font:inherit;color:var(--cloth);background:none;border:0;text-decoration:underline;cursor:pointer;padding:0}
.crossing{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1rem}
.crossing a{display:block;border:1.5px solid var(--cloth);border-radius:8px;padding:1rem;text-decoration:none}
.crossing a:hover{background:#E4EEE8}.crossing b{font-size:1.25rem}.crossing span{display:block;color:var(--mut)}
/* topic */
.layout{display:grid;grid-template-columns:200px minmax(0,1fr);gap:2.5rem;max-width:1100px;margin:0 auto;padding:2rem 1.25rem 4rem;padding-right:4rem}
.key{position:sticky;top:1rem;align-self:start;font:500 1rem/1.4 var(--lab)}
.key h2{font:700 .95rem var(--lab);letter-spacing:.08em;text-transform:uppercase;color:var(--mut);margin:0 0 .5rem}
.key ul{list-style:none;margin:0 0 1.5rem;padding:0;display:grid;gap:.3rem}.key a{text-decoration:none;display:block;padding:.2rem .5rem;border-radius:4px}.key a:hover{background:#E4EEE8}
.account{padding:0 0 2.5rem;margin:0 0 2.5rem;border-bottom:1px solid var(--rule)}
.account header{display:flex;flex-wrap:wrap;align-items:baseline;gap:.4rem 1rem}
.account h2{margin:0;font:700 2rem/1.2 var(--read);text-wrap:balance}
.grp{font:600 .9rem var(--lab);letter-spacing:.06em;text-transform:uppercase;background:var(--c);color:var(--cf);padding:.1rem .6rem;border-radius:4px}
.account .sum{font-size:1.2rem;font-weight:500;margin:.4rem 0 1.2rem;max-width:62ch;text-wrap:pretty}
.cols{display:grid;grid-template-columns:200px minmax(0,1fr);gap:1.5rem 2rem}
dl.marks{margin:0;font:500 1rem/1.35 var(--lab);display:grid;gap:.6rem;align-content:start;background:#E8F0EB;border-radius:8px;padding:1rem}
.marks dt{font-weight:700;font-size:.85rem;letter-spacing:.08em;text-transform:uppercase;color:var(--mut)}
.marks dd{margin:0;font-variant-numeric:tabular-nums;font-size:1.05rem}
.prose{max-width:64ch}.prose ul{padding-left:1.2rem;margin:0 0 1rem}.prose li{margin:.35rem 0}
code{font:.9em ui-monospace,SFMono-Regular,Menlo,monospace;background:#E4EEE8;padding:.05em .3em;border-radius:3px}
.gotcha{border:1.5px solid #C93A1F;background:#FDF1EE;border-radius:8px;padding:.8rem 1rem;margin:1rem 0}
.gotcha b{font:700 .9rem var(--lab);letter-spacing:.08em;text-transform:uppercase;color:#9A2A14;margin-right:.5rem}
.src{font:500 1rem var(--lab);margin:1rem 0 0}.src a{margin-right:1rem}
.confused h2{font:700 1.8rem var(--read);margin:0 0 .3rem}.confused p{color:var(--mut);margin:0 0 1rem}
table{border-collapse:collapse;width:100%;font-size:1rem}
th,td{text-align:left;vertical-align:top;padding:.7rem .8rem;border-bottom:1px solid var(--rule)}
thead th{font:700 .95rem var(--lab);letter-spacing:.08em;text-transform:uppercase;border-bottom:2px solid var(--cloth)}
tbody th{font:600 1rem var(--lab);width:7rem;color:var(--mut)}
/* lenses */
.lensbar{display:flex;flex-wrap:wrap;gap:6px;margin:1rem 0 .4rem}
.lensbtn{font:600 1rem var(--lab);letter-spacing:.06em;text-transform:uppercase;padding:.5rem 1rem;border:1.5px solid var(--cloth);background:#fff;color:var(--cloth);border-radius:6px;cursor:pointer}
.lensbtn[aria-pressed=true]{background:var(--cloth);color:#fff}
.about{color:var(--mut);max-width:62ch;min-height:3.3em;margin:0 0 1rem}
.lane{display:grid;grid-template-columns:150px 1fr;gap:.5rem 1rem;align-items:center;padding:.5rem 0;border-bottom:1px solid var(--rule)}
.lane h2{margin:0;font:600 1rem var(--lab);letter-spacing:.05em;text-transform:uppercase;color:var(--mut)}
.cells{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:6px}
.role{font:600 .95rem/1.2 var(--lab);padding:.7rem .4rem;border-radius:6px;border:1.5px solid var(--cloth);background:#fff;color:var(--ink);cursor:pointer;min-height:3.2rem;transition:opacity .2s}
.c-edge{background:#FBEBC8}.c-run{background:#DCE7F8}.c-data{background:#D6EBDD}.c-ops{background:#E7DCF4}
.role.dim{opacity:.3}.role[aria-pressed=true]{outline:3px solid var(--cloth);outline-offset:1px}
.panel{margin-top:1.5rem;border:1.5px solid var(--cloth);border-radius:8px;padding:1rem 1.2rem;max-width:62ch}.panel h2{margin:0 0 .3rem;font:700 1.5rem var(--read)}.panel p{margin:.4rem 0}
@media(max-width:800px){.tabs{position:static;display:flex;flex-wrap:wrap;padding:.6rem 1.25rem;background:var(--cloth)}.tabs a{writing-mode:horizontal-tb;padding:.35rem .8rem;border-radius:6px}.tabs a:hover,.tabs a[aria-current]{padding-right:.8rem}
.mast,.wrap,.layout{padding-right:1.25rem}.layout{grid-template-columns:1fr}.key{position:static}.cols{grid-template-columns:1fr}.acct{grid-template-columns:1fr}.acct .n{grid-row:auto;grid-column:1;text-align:left}
.lane{grid-template-columns:1fr}.cells{grid-template-columns:repeat(3,1fr)}.gap{display:none}}
"""
HEAD = gfont("family=Literata:opsz,wght@7..72,400;7..72,500;7..72,600;7..72,700&family=Barlow+Semi+Condensed:wght@500;600;700")


def tabs(cur=None):
    a = "".join(f'<a href="index.html#{f["id"]}" style="--c:{TAB[f["id"]][0]};--cf:{TAB[f["id"]][1]}"{" aria-current=page" if f["id"] == cur else ""}>{esc(f["label"])}</a>' for f in T["families"])
    return f'<nav class="tabs" aria-label="Families">{a}</nav>'


def landing():
    fams = ""
    for f in families():
        c, cf = TAB[f["id"]]
        rows = "".join(
            f'<a class="acct" href="topic.html" style="--c:{c}"><h3>{esc(t["label"])}</h3><p class="id">{esc(t["description"])}</p>'
            f'<p class="also"><b>Includes</b> {esc(", ".join(t["samples"]))}</p><span class="n">{t["count"]}<small>entries</small></span></a>'
            for t in f["topics"])
        fams += f'<section class="fam" id="{f["id"]}" style="--c:{c};--cf:{cf}"><h2>{esc(f["label"])}</h2><p>{esc(f["description"])}</p>{rows}</section>'
    views = "".join(f'<a href="{"lenses" if v["id"] == "lenses" else "topic"}.html"><b>{esc(v["label"])}</b><span>{esc(v["description"])}</span></a>' for v in T["views"])
    body = (f'<header class="mast"><h1 class="mark">{esc(T["name"])}</h1><p class="tag">{esc(T["tagline"])}</p>'
            '<label class="sr" for="q">Search every entry</label>'
            '<input id="q" type="search" placeholder="Name an entry, a tool or a word" autocomplete="off">'
            '<p class="keyhint">Press / to search. Esc clears. The arrow key moves into the results.</p><p id="st" class="sr" role="status"></p></header>'
            f'{tabs()}<main class="wrap"><div id="res" role="region" aria-label="Search results" hidden></div>'
            f'<div id="fams">{fams}<section class="fam" id="views" style="--c:#0E4B3B;--cf:#fff"><h2>Views</h2><p>Pictures that cut across the topics; they are not topics themselves.</p><div class="crossing">{views}</div></section></div></main>')
    return page("Atlas · field guide", HEAD, body + search_block(), CSS)


def topic():
    c, cf = TAB["iac"]
    marks = lambda e: ("<dl class=marks>"
        f'<dt>Status</dt><dd>{esc(e["status"])}</dd><dt>Depth</dt><dd>{esc(e["level"])}</dd>'
        f'<dt>Version analysed</dt><dd>{esc(e["version"]["analysed"])}</dd><dt>Released</dt><dd>{esc(e["version"].get("released", ""))}</dd>'
        f'<dt>Checked</dt><dd>{esc(e["version"]["checked"])}</dd><dt>Licence</dt><dd>{esc(e["license"])}</dd></dl>')
    grp = {"opengitops": "Principles", "argo-cd": "GitOps operators", "flux": "GitOps operators"}
    arts = ""
    for eid in ("opengitops", "argo-cd", "flux"):
        e = entry(eid)
        li = "".join(f"<li>{md(b)}</li>" for b in e["bullets"])
        g = f'<p class="gotcha"><b>Gotcha</b>{md(e["gotcha"])}</p>' if e["gotcha"] else ""
        src = "".join(f'<a href="{esc(l["url"])}">{esc(l["label"])}</a>' for l in e["links"])
        arts += (f'<article class="account" id="{eid}" style="--c:{c};--cf:{cf}"><header><h2>{esc(e["name"])}</h2><span class="grp">{grp[eid]}</span></header>'
                 f'<p class="sum">{esc(e["summary"])}</p><div class="cols">{marks(e)}<div class="prose"><ul>{li}</ul>{g}<p class="src">Sources {src}</p></div></div></article>')
    cmp = comparison()
    head = "".join(f"<th>{esc(x)}</th>" for x in cmp["columns"])
    rows = "".join(f'<tr><th scope="row">{esc(r["label"])}</th>' + "".join(f"<td>{md(x)}</td>" for x in r["cells"]) + "</tr>" for r in cmp["rows"])
    body = (f'<header class="mast"><nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Atlas</a><span>/</span><a href="index.html#iac">IaC</a></nav>'
            f'<h1 class="mark">{esc(G["title"])}</h1><p class="lede">{esc(G["intro"])}</p></header>{tabs("iac")}'
            '<div class="layout"><nav class="key" aria-label="On this page"><h2>Accounts</h2><ul><li><a href="#opengitops">OpenGitOps principles</a></li><li><a href="#argo-cd">Argo CD</a></li><li><a href="#flux">Flux</a></li></ul>'
            '<h2>Easily confused</h2><ul><li><a href="#confused">Argo CD and Flux</a></li></ul></nav>'
            f'<main>{arts}<section class="confused" id="confused"><h2>{esc(cmp["title"])}</h2><p>Look-alikes: how to tell the two operators apart.</p>'
            f'<table><thead><tr><th></th>{head}</tr></thead><tbody>{rows}</tbody></table></section></main></div>')
    return page("GitOps · Atlas field guide", HEAD, body, CSS)


def lenses():
    markup, js = lenses_markup()
    body = (f'<header class="mast"><nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Atlas</a><span>/</span><a href="index.html#views">Views</a></nav>'
            f'<h1 class="mark">Lenses</h1><p class="lede">Where does a service go? One picture of an application, five lenses.</p></header>{tabs()}'
            f'<main class="wrap">{markup}</main>{js}')
    return page("Lenses · Atlas field guide", HEAD, body, CSS)

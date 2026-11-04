"""World F: transit diagram. Families are coloured lines, topics are stations, views are interchanges."""
import sys
from common import *
sys.path.insert(0, str(R / "shared"))
from atlas import DISCLAIMER, repo_url, ref

LINE = {"iac": ("var(--iac)", "var(--iacf)"), "cicd": ("var(--cic)", "var(--cicf)"), "development": ("var(--dev)", "var(--devf)"), "enterprise": ("var(--ent)", "var(--entf)")}

CSS = """
:root{color-scheme:light;--ink:#14181F;--ground:#FFFFFF;--soft:#F2F4F7;--mut:#4A5260;--rule:#D5DAE1;--iac:#0057B8;--iacf:#fff;--cic:#D6001C;--cicf:#fff;--dev:#00843D;--devf:#fff;--ent:#F28C00;--entf:#14181F;--wire:#5C6675;--boardline:#14181F;--d1:#3C8EE2;--d1f:#14181F;--d2:#1D6FCB;--d2f:#fff;--d3:#0057B8;--d3f:#fff;--d4:#003D87;--d4f:#fff;--o1:#E8505F;--o1f:#14181F;--o2:#D6001C;--o2f:#fff;--o3:#A60019;--o3f:#fff;--o4:#760012;--o4f:#fff;--g:'Red Hat Display','Helvetica Neue',Arial,sans-serif}
html[data-theme=dark]{color-scheme:dark;--ink:#EEF1F5;--ground:#0F131A;--soft:#1A202B;--mut:#A9B3C1;--rule:#2C3543;--iac:#4C9AFF;--iacf:#0F131A;--cic:#FF6B7A;--cicf:#0F131A;--dev:#3DC878;--devf:#0F131A;--ent:#F5A524;--entf:#0F131A;--wire:#8793A5;--boardline:#2C3543;--d1:#9CCBFF;--d2:#76B4FF;--d3:#4C9AFF;--d4:#2E80EC;--o1:#FFB0B8;--o2:#FF8E9B;--o3:#FF6B7A;--o4:#EA4A5D;--d1f:#0F131A;--d2f:#0F131A;--d3f:#0F131A;--d4f:#0F131A;--o1f:#0F131A;--o2f:#0F131A;--o3f:#0F131A;--o4f:#0F131A}
body{background:var(--ground);color:var(--ink);font:500 1.0625rem/1.6 var(--g)}
::selection{background:var(--iac);color:var(--iacf)}
:focus-visible{outline:3px solid var(--ink);outline-offset:3px}
a{text-decoration:none;color:inherit}
.wrap{max-width:1120px;margin:0 auto;padding:1.2rem clamp(1rem,3vw,2rem) 4rem}
.brand{display:flex;align-items:center;flex-wrap:wrap;gap:.6rem .8rem;margin-bottom:1.6rem}
.brand .bar{display:inline-flex;align-items:center;height:2.2rem;padding:0 1rem;background:var(--ink);color:var(--ground);font-weight:900;letter-spacing:.02em;border-radius:6px}
.brand span{color:var(--mut);font-size:.95rem}
h1{font:900 clamp(3.2rem,11vw,6rem)/.95 var(--g);letter-spacing:-.04em;margin:0 0 .8rem;text-wrap:balance}
.tag{font-size:1.25rem;max-width:44ch;color:var(--mut);margin:0 0 1.6rem;text-wrap:pretty}
.plan{display:flex;align-items:center;gap:1rem;max-width:680px;background:var(--soft);border:3px solid var(--ink);border-radius:999px;padding:.3rem 1.4rem}
.plan svg{flex:none}.plan input{flex:1;min-width:0;font:700 1.3rem var(--g);border:0;background:transparent;color:var(--ink);padding:.8rem 0}.plan input:focus-visible{outline:0}.plan:focus-within{outline:3px solid var(--iac);outline-offset:3px}
.hint{font-size:.95rem;color:var(--mut);margin:.6rem 0 0}
.line{margin:3rem 0 0}
.lname{display:inline-block;margin:0;padding:.2rem 1.1rem;border-radius:999px;background:var(--c);color:var(--cf);font:900 1.2rem var(--g);letter-spacing:.02em}
.line>p{margin:.5rem 0 1.4rem;color:var(--mut);max-width:60ch}
.route{list-style:none;margin:0;padding:0;display:flex;position:relative}
.route::before{content:"";position:absolute;left:13px;right:0;top:7px;height:12px;background:var(--c);border-radius:0 6px 6px 0}
.stn{display:block;flex:1;min-width:0;padding-right:1.2rem;position:relative}
.dot{display:block;width:26px;height:26px;border-radius:50%;background:var(--ground);border:6px solid var(--c);margin-bottom:.8rem;transition:transform .2s}
.stn a{display:block;border-radius:8px}.stn:hover .dot,.stn a:focus-visible .dot{transform:scale(1.25);background:var(--c)}
.stn b{display:block;font:900 1.4rem/1.15 var(--g);letter-spacing:-.02em}.stn small{display:block;color:var(--mut);font-weight:700;font-variant-numeric:tabular-nums}
.stn span.d{display:block;color:var(--mut);font-size:.98rem;line-height:1.4;margin-top:.3rem;max-width:30ch}
.inter{margin-top:3.4rem;border-top:3px solid var(--ink);padding-top:1.2rem}
.inter h2{margin:0;font:900 1.2rem var(--g)}.inter>p{margin:.4rem 0 1rem;color:var(--mut)}
.inter ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:1rem 2.5rem}
.xing{display:flex;align-items:center;gap:.8rem}.xing i{width:30px;height:30px;border-radius:50%;border:6px solid var(--ink);background:var(--ground);flex:none}.xing b{font:900 1.4rem var(--g);letter-spacing:-.02em}.xing:hover i{background:var(--ink)}
.board{display:grid;gap:3px;margin:1.6rem 0;background:var(--boardline);padding:3px;border-radius:8px}
.hit{display:grid;grid-template-columns:1fr auto;gap:0 1rem;padding:.7rem 1.1rem;background:#1D2430;color:#fff}.hit:hover,.hit:focus-visible{background:#2B3547}
.hit b{font:900 1.35rem var(--g)}.hit small{font-weight:700;color:#FFD23F;align-self:center}.hit span{grid-column:1/-1;color:#C8CFDA}
.none{background:var(--soft);padding:1rem 1.2rem;border-radius:8px}.none button{font:inherit;font-weight:900;border:2px solid var(--ink);background:var(--ground);color:var(--ink);border-radius:999px;padding:.1rem .9rem;cursor:pointer}
.brand .acts{margin-left:auto;display:flex;gap:.5rem}
.btn{font:900 .95rem var(--g);border:3px solid var(--ink);border-radius:999px;background:var(--ground);color:var(--ink);padding:.1rem 1rem;cursor:pointer}.btn:hover{background:var(--ink);color:var(--ground)}
dialog.ai{max-width:min(560px,92vw);border:3px solid var(--ink);border-radius:14px;background:var(--ground);color:var(--ink);padding:1.4rem 1.6rem;font:500 1rem/1.55 var(--g)}
dialog.ai::backdrop{background:rgba(10,12,16,.6)}dialog.ai h2{margin:0 2.5rem .6rem 0;font:900 1.7rem var(--g);letter-spacing:-.02em}dialog.ai p{margin:.6rem 0}
dialog.ai .cl{position:absolute;top:1rem;right:1rem}
.dx{display:flex;gap:.7rem;align-items:flex-start;margin:1rem 0;font-weight:700}.dx input{width:1.3rem;height:1.3rem;margin-top:.2rem;accent-color:var(--iac)}.dx small{display:block;font-weight:500;color:var(--mut)}
.vr{font-size:.9rem;color:var(--mut);word-break:break-all}.vr a{color:inherit}
.foot{max-width:1120px;margin:0 auto;padding:1.6rem clamp(1rem,3vw,2rem) 3rem;border-top:1px solid var(--rule);color:var(--mut);font-size:.9rem}.foot p{margin:.4rem 0;max-width:80ch}
.chips .xd{display:none}html[data-details] .chips .xd,.stop.open .chips .xd{display:inline}
.srcs.xd{display:none}html[data-details] .srcs.xd,.stop.open .srcs.xd{display:flex}
.more{font:700 .9rem var(--g);border:0;background:none;color:var(--mut);text-decoration:underline;cursor:pointer;padding:0 .3rem}
.tw{overflow-x:auto}.tw table{min-width:560px}
.inter-nav{display:flex;align-items:center;flex-wrap:wrap;gap:.2rem 1.2rem}.il{font-weight:700;font-size:.9rem;color:var(--mut)}
.xl{display:inline-flex;align-items:center;gap:.45rem;font-weight:900}.xl i{width:18px;height:18px;border-radius:50%;border:5px solid var(--ink);background:var(--ground)}
.xl:hover i,.xl[aria-current] i{background:var(--ink)}
/* azure */
.tools{display:flex;flex-wrap:wrap;align-items:center;gap:.8rem 1rem;margin:1.4rem 0 .4rem}
.tools .plan{flex:1 1 320px;max-width:520px}
.tierbar{display:flex;flex-wrap:wrap;gap:.5rem}
.tier{font:900 .95rem var(--g);border:3px solid var(--c);border-radius:999px;background:var(--ground);color:var(--ink);padding:.25rem 1rem;cursor:pointer}
.tier[aria-pressed=true]{background:var(--c);color:var(--cf)}
.zone{margin-top:2.6rem}.zone>p{margin:.4rem 0 .6rem;color:var(--mut);max-width:60ch}
.cat h3{font:900 1.15rem var(--g);margin:1.6rem 0 .6rem}
.stns{list-style:none;margin:0;padding:0 0 0 48px;position:relative}
.stns::before{content:"";position:absolute;left:14px;top:12px;bottom:12px;width:10px;background:var(--c);border-radius:5px}
.svc{position:relative;padding:0 0 1.5rem}
.svc::before{content:"";position:absolute;left:-48px;top:4px;width:24px;height:24px;margin-left:5px;border-radius:50%;background:var(--ground);border:6px solid var(--c)}
.svc b{font:900 1.35rem/1.2 var(--g);letter-spacing:-.02em}.svc p{margin:.1rem 0 .4rem;max-width:62ch;color:var(--mut)}
.svc .chips{margin:.2rem 0 0}.svc .chips span{font-size:.9rem}
.svc .det.xd{display:none;margin-top:.6rem}html[data-details] .svc .det.xd,.svc.open .det.xd{display:block}
.svc.open .chips .xd{display:inline}
.det ul{max-width:64ch;padding-left:1.2rem;margin:.2rem 0 .6rem}.det li{margin:.3rem 0}
.empty{background:var(--soft);padding:1rem 1.2rem;border-radius:8px}.empty button{font:inherit;font-weight:900;border:2px solid var(--ink);background:var(--ground);color:var(--ink);border-radius:999px;padding:.1rem .9rem;cursor:pointer}
/* loop */
.loopsvg{width:100%;height:auto;margin:1rem 0 2rem}
.loopsvg .bg{fill:none;stroke-width:14;stroke-linecap:butt}
.loopsvg .st{fill:var(--ground);stroke-width:7}.loopsvg a:hover .st,.loopsvg a:focus-visible .st{fill:var(--sc)}
.loopsvg text{font:900 17px var(--g);fill:var(--ink);paint-order:stroke;stroke:var(--ground);stroke-width:5px;stroke-linejoin:round}
.loopsvg .lobe{font:900 20px var(--g);fill:var(--mut);stroke:none;text-anchor:middle}
.loopsvg a:focus-visible{outline:none}.loopsvg a:focus-visible .st{stroke:var(--ink)}
.grp2{margin-top:2.4rem}.grp2 .stops::before{background:transparent}.stage::after{content:"";position:absolute;left:-45px;top:19px;bottom:-19px;width:12px;background:var(--c)}.stage:last-child::after{display:none}
.stage h3{font:900 1.7rem/1.1 var(--g);letter-spacing:-.03em;margin:0 0 .2rem}.stage h3 small{font:900 .95rem var(--g);background:var(--c);color:var(--cf);border-radius:999px;padding:.05rem .6rem;margin-right:.6rem;vertical-align:.2rem}
.stage>p{margin:.1rem 0 .6rem;color:var(--mut)}
.pills{display:flex;flex-wrap:wrap;gap:.5rem;margin:0;padding:0;list-style:none}.pills a{display:inline-block;border:2px solid var(--ink);border-radius:999px;padding:.1rem .9rem;font-weight:900}.pills a:hover{background:var(--ink);color:var(--ground)}.pills .none{color:var(--mut);border:0;padding:0;font-weight:500}
@media(max-width:560px){.loopsvg{display:none}}
/* topic */
.pill{display:inline-block;padding:.1rem .9rem;border-radius:999px;background:var(--c);color:var(--cf);font-weight:900;font-size:.95rem}
.crumb{display:flex;align-items:center;gap:.6rem;flex-wrap:wrap;margin-bottom:1.2rem;font-weight:700;color:var(--mut)}.crumb a:hover{color:var(--ink)}
.strip{position:sticky;top:0;z-index:5;background:var(--ground);padding:.8rem 0;border-bottom:1px solid var(--rule);margin:1.5rem 0}
.strip ol{list-style:none;margin:0;padding:0;display:flex;position:relative}
.strip ol::before{content:"";position:absolute;left:10px;right:10px;top:7px;height:8px;background:var(--c);border-radius:4px}
.strip li{flex:1;position:relative}.strip a{display:block;font-weight:700;font-size:.95rem}.strip a i{display:block;width:22px;height:22px;border-radius:50%;background:var(--ground);border:5px solid var(--c);margin-bottom:.3rem}
.strip a:hover i{background:var(--c)}.strip li:last-child{flex:none}
.stops{position:relative;padding-left:64px}
.stops::before{content:"";position:absolute;left:19px;top:20px;bottom:0;width:12px;background:var(--c);border-radius:6px 6px 0 0}
.stop{position:relative;padding-bottom:3rem}
.stop::before{content:"";position:absolute;left:-64px;top:6px;width:26px;height:26px;margin-left:7px;border-radius:50%;background:var(--ground);border:6px solid var(--c)}
.stop h2{font:900 clamp(2.2rem,5.5vw,3.2rem)/1.05 var(--g);letter-spacing:-.035em;margin:0 0 .6rem;text-wrap:balance}
.chips{display:flex;flex-wrap:wrap;gap:.5rem;margin:.4rem 0 1rem}.chips span{border-radius:999px;padding:.1rem .9rem;font-weight:700;font-size:.95rem;font-variant-numeric:tabular-nums;border:2px solid var(--ink)}
.chips .v{background:var(--ink);color:var(--ground)}
.sum{font-size:1.3rem;line-height:1.5;max-width:58ch;margin:0 0 1rem;text-wrap:pretty}
.stop ul{max-width:64ch;padding-left:1.2rem}.stop li{margin:.4rem 0}
code{font:.88em ui-monospace,Menlo,monospace;background:var(--soft);padding:.05em .3em;border-radius:4px}
.gotcha{border:3px solid var(--cic);border-radius:12px;padding:.7rem 1.1rem;margin:1.1rem 0;max-width:64ch}.gotcha b{background:var(--cic);color:var(--cicf);border-radius:999px;padding:0 .7rem;margin-right:.6rem;font-size:.9rem}
.srcs{display:flex;flex-wrap:wrap;gap:.5rem}.srcs a{border:2px solid var(--ink);border-radius:999px;padding:.1rem .9rem;font-weight:700}.srcs a:hover{background:var(--ink);color:var(--ground)}
.cmp h2{font:900 2.4rem var(--g);letter-spacing:-.03em;margin:0 0 .8rem}
table{border-collapse:collapse;width:100%;font-size:1rem}th,td{text-align:left;vertical-align:top;padding:.8rem .8rem .8rem 0;border-bottom:1px solid var(--rule)}
thead th{font-weight:900;border-bottom:3px solid var(--ink)}tbody th{width:7rem;font-weight:900}
/* lenses */
.lensbar{display:flex;flex-wrap:wrap;gap:.5rem;margin:0 0 .6rem}
.lensbtn{font:900 1rem var(--g);padding:.4rem 1.2rem;border:3px solid var(--ink);border-radius:999px;background:var(--ground);color:var(--ink);cursor:pointer}.lensbtn[aria-pressed=true]{background:var(--ink);color:var(--ground)}
.about{max-width:60ch;min-height:3.3em;color:var(--mut);margin:0 0 1rem}
.lane{padding:.8rem 0;border-top:1px solid var(--rule)}
.lane h2{margin:0 0 .5rem;display:inline-block;font:900 .95rem var(--g);padding:0 .8rem;border-radius:999px;background:var(--ink);color:var(--ground)}
.cells{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:.6rem}
.role{font:700 1rem/1.15 var(--g);padding:.75rem .4rem;min-height:3.4rem;border-radius:10px;background:var(--ground);color:var(--ink);border:4px solid var(--ink);cursor:pointer;transition:opacity .2s}
.c-edge{border-color:var(--ent)}.c-run{border-color:var(--iac)}.c-data{border-color:var(--dev)}.c-ops{border-color:var(--cic)}
.role.dim{opacity:.25}.role[aria-pressed=true]{background:var(--ink);color:var(--ground)}
.legend{display:flex;flex-wrap:wrap;gap:.4rem 1.2rem;font-weight:700;font-size:.95rem;margin:0 0 1rem}.legend span::before{content:"";display:inline-block;width:14px;height:14px;border-radius:50%;border:4px solid var(--k);margin-right:.4rem;vertical-align:-1px}
.panel{margin-top:1.5rem;background:var(--soft);border-radius:12px;padding:1rem 1.3rem;max-width:62ch}.panel h2{font:900 1.8rem var(--g);letter-spacing:-.03em;margin:0 0 .3rem}.panel p{margin:.4rem 0}
.wires{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;overflow:visible;color:var(--wire);z-index:0}
.w{opacity:.85;stroke-width:3;transition:opacity .2s}.w.on{opacity:1;stroke-width:4;color:var(--ink)}.w.off{opacity:.1}.role,.lane h2{position:relative;z-index:1}
.wl{font:700 .85rem var(--g);fill:var(--ink);paint-order:stroke;stroke:var(--ground);stroke-width:5px;stroke-linejoin:round}
@media(max-width:760px){.route{flex-direction:column;gap:1.2rem}.route::before{left:7px;right:auto;top:13px;bottom:13px;width:12px;height:auto;border-radius:6px}
.stn a{display:grid;grid-template-columns:26px 1fr;gap:0 1rem}.dot{grid-row:1/4;margin:0}.strip ol{overflow-x:auto}.cells{grid-template-columns:repeat(3,1fr)}.gap{display:none}}
"""
THEME = "<script>try{var t=localStorage.getItem('atlas-theme')}catch(e){}document.documentElement.dataset.theme=t||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light')</script>"
HEAD = THEME + gfont("family=Red+Hat+Display:wght@500;700;900")
PIN = '<svg width="22" height="22" viewBox="0 0 22 22" aria-hidden="true"><circle cx="11" cy="11" r="8" stroke-width="4" style="fill:var(--ground);stroke:var(--ink)"/></svg>'


def brand(cur=None):
    xs = "".join(f'<a class="xl" href="{h}.html"{" aria-current=page" if h == cur else ""}><i></i>{n}</a>' for h, n in (("lenses", "Lenses"), ("loop", "DevOps loop")))
    return ('<div class="brand"><a class="bar" href="index.html">ATLAS</a><nav class="inter-nav" aria-label="Interchanges"><span class="il">Interchanges</span>' + xs + '</nav><span class="acts">'
            '<button type="button" class="btn" id="abt" aria-haspopup="dialog">About</button>'
            '<button type="button" class="btn" id="thm" aria-pressed="false">Dark</button></span></div>')


def chrome(details=False):
    url, r = repo_url(), ref()
    where = f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(url)}</a>' if url else "not available"
    sw = ('<label class="dx"><input type="checkbox" id="dxs"><span>Show entry details<small>Release and check dates, status, licence, and every source. The version analysed is always shown.</small></span></label>' if details else "")
    dlg = ('<dialog class="ai" id="ai" aria-labelledby="ai-t"><button type="button" class="btn cl" id="acl">Close</button><h2 id="ai-t">About Atlas</h2>'
           + "".join(f"<p>{x}</p>" for x in DISCLAIMER) + sw + f'<p class="vr">Version <code>{esc(r)}</code><br>Source {where}</p></dialog>')
    foot = '<footer class="foot">' + "".join(f"<p>{x}</p>" for x in DISCLAIMER) + "</footer>"
    js = """<script>
const root=document.documentElement,thm=document.getElementById('thm'),ai=document.getElementById('ai');
const store=(k,v)=>{try{v==null?localStorage.removeItem(k):localStorage.setItem(k,v)}catch(e){}};
function paint(){const d=root.dataset.theme==='dark';thm.setAttribute('aria-pressed',d);thm.textContent=d?'Light':'Dark';thm.setAttribute('aria-label',d?'Switch to the light theme':'Switch to the dark theme')}
thm.addEventListener('click',()=>{root.dataset.theme=root.dataset.theme==='dark'?'light':'dark';store('atlas-theme',root.dataset.theme);paint()});paint();
document.getElementById('abt').addEventListener('click',()=>ai.showModal());document.getElementById('acl').addEventListener('click',()=>ai.close());
ai.addEventListener('click',e=>{if(e.target===ai)ai.close()});
const dxs=document.getElementById('dxs');
if(dxs){const on=()=>{try{return localStorage.getItem('atlas-details')==='1'}catch(e){return false}};dxs.checked=on();root.toggleAttribute('data-details',dxs.checked);
  dxs.addEventListener('change',()=>{root.toggleAttribute('data-details',dxs.checked);store('atlas-details',dxs.checked?'1':null)})}
document.addEventListener('click',e=>{const b=e.target.closest('.more');if(!b)return;const st=b.closest('.stop,.svc'),o=st.classList.toggle('open');b.textContent=o?'hide details':'show details';b.setAttribute('aria-expanded',o)});
</script>"""
    return dlg + foot + js


def landing():
    lines = ""
    for f in families():
        c, cf = LINE[f["id"]]
        st = "".join(f'<li class="stn"><a href="{"azure" if t["id"] == "azure" else "topic"}.html"><i class="dot"></i><b>{esc(t["label"])}</b><small>{t["count"]} entries</small><span class="d">{esc(t["description"])}</span></a></li>' for t in f["topics"])
        lines += f'<section class="line" style="--c:{c};--cf:{cf}"><h2 class="lname">{esc(f["label"])}</h2><p>{esc(f["description"])}</p><ol class="route">{st}</ol></section>'
    body = (f'<div class="wrap">{brand()}<h1>{esc(T["name"])}</h1><p class="tag">{esc(T["tagline"])}</p>'
            f'<label class="plan"><span class="sr">Search every entry</span>{PIN}<input id="q" type="search" placeholder="Where to? Search every entry" autocomplete="off"></label>'
            '<p class="hint">Press / to search, Esc to clear, the down arrow to reach the results.</p><p id="st" class="sr" role="status"></p>'
            f'<main><div id="res" class="board" role="region" aria-label="Search results" hidden></div><div id="fams">{lines}</div></main></div>')
    return page("Atlas · transit", HEAD, body + chrome() + search_block(), CSS)


def topic():
    c, cf = LINE["iac"]
    stops = ""
    for eid in ("opengitops", "argo-cd", "flux"):
        e = entry(eid)
        v = e["version"]
        li = "".join(f"<li>{md(b)}</li>" for b in e["bullets"])
        g = f'<p class="gotcha"><b>Gotcha</b>{md(e["gotcha"])}</p>' if e["gotcha"] else ""
        src = "".join(f'<a href="{esc(l["url"])}">{esc(l["label"])}</a>' for l in e["links"])
        stops += (f'<article class="stop" id="{eid}"><h2>{esc(e["name"])}</h2><div class="chips"><span class="v">analysed {esc(v["analysed"])}</span><span class="xd">checked {esc(v["checked"])}</span>'
                  f'<span class="xd">{esc(e["status"])}</span><span class="xd">{esc(e["license"])}</span><button type="button" class="more" aria-expanded="false">show details</button></div><p class="sum">{esc(e["summary"])}</p><ul>{li}</ul>{g}<p class="srcs xd">{src}</p></article>')
    cm = comparison()
    head = "".join(f"<th>{esc(x)}</th>" for x in cm["columns"])
    rows = "".join(f'<tr><th scope="row">{esc(r["label"])}</th>' + "".join(f"<td>{md(x)}</td>" for x in r["cells"]) + "</tr>" for r in cm["rows"])
    strip = "".join(f'<li><a href="#{i}"><i></i>{n}</a></li>' for i, n in (("opengitops", "Principles"), ("argo-cd", "Argo CD"), ("flux", "Flux"), ("cmp", "Compare")))
    body = (f'<div class="wrap" style="--c:{c};--cf:{cf}">{brand()}<nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Atlas</a><span>›</span><span class="pill">IaC line</span><span>›</span><span>GitOps</span></nav>'
            f'<h1>{esc(G["title"])}</h1><p class="tag">{esc(G["intro"])}</p><nav class="strip" aria-label="Stops on this page"><ol>{strip}</ol></nav>'
            f'<main><div class="stops">{stops}</div><section class="cmp" id="cmp"><h2>{esc(cm["title"])}</h2><div class="tw"><table><thead><tr><th></th>{head}</tr></thead><tbody>{rows}</tbody></table></div></section></main></div>')
    return page("GitOps · Atlas transit", HEAD, body + chrome(True), CSS)


def lenses():
    markup, js = lenses_markup()
    legend = '<p class="legend"><span style="--k:var(--ent)">Edge</span><span style="--k:var(--iac)">Runs the app</span><span style="--k:var(--dev)">Data</span><span style="--k:var(--cic)">Operations</span></p>'
    body = (f'<div class="wrap">{brand("lenses")}<nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Atlas</a><span>›</span><span>Interchanges</span><span>›</span><span>Lenses</span></nav>'
            f'<h1>Lenses</h1><p class="tag">Where does a service go? One picture of an application, five lenses.</p>{legend}<main>{markup}</main></div>{chrome()}{js}')
    return page("Lenses · Atlas transit", HEAD, body, CSS)


AZ = json.loads((R / "dist/azure/services.resolved.json").read_text())


def azure():
    cost = {c["level"]: c["label"] for c in AZ["cost_scale"]}
    cn = {c["level"]: c["label"] for c in AZ["cloud_native_scale"]}
    tinfo = {t["tier"]: t for t in AZ["tiers"]}
    tc = {0: ("var(--iac)", "var(--iacf)"), 1: ("var(--dev)", "var(--devf)")}
    zones = ""
    for tier in (0, 1):
        cats = ""
        for cat in AZ["categories"]:
            svcs = [x for x in AZ["services"] if x["tier"] == tier and x["category"] == cat]
            if not svcs:
                continue
            li = ""
            for x in svcs:
                docs = sorted(x.get("docs", []), key=lambda d: d.get("page_date", ""), reverse=True)
                links = "".join(f'<a href="{esc(d["url"])}">{esc(d["url"].rstrip("/").split("/")[-1])} ({esc(d.get("page_date", ""))})</a>' for d in docs)
                facts = "".join(f"<li>{md(f)}</li>" for f in x["facts"])
                cnl = cn.get(x["cloud_native"]["level"], "Not rated")
                tf = (x.get("terraform") or {}).get("status", "")
                q = esc(f'{x["name"]} {x["purpose"]} {x["category"]}'.lower())
                li += (f'<li class="svc" data-tier="{tier}" data-q="{q}"><b>{esc(x["name"])}</b><p>{esc(x["purpose"])}</p>'
                       f'<div class="chips"><span>{esc(cost.get(x["cost"]["level"], x["cost"]["level"]))}</span>' + (f'<span>Terraform {esc(tf)}</span>' if tf else "") +
                       f'<span class="xd">{esc(cnl)}</span><span class="xd">{esc(x["review"]["status"])}</span>'
                       '<button type="button" class="more" aria-expanded="false">show details</button></div>'
                       f'<div class="det xd"><ul>{facts}</ul><p class="srcs">{links}</p></div></li>')
            cats += f'<section class="cat"><h3>{esc(cat)}</h3><ul class="stns">{li}</ul></section>'
        c, cf = tc[tier]
        zones += (f'<section class="zone" style="--c:{c};--cf:{cf}"><h2 class="lname">{esc(tinfo[tier]["label"])}</h2><p>{esc(tinfo[tier]["description"])}</p>{cats}</section>')
    chips = "".join(f'<button type="button" class="tier" data-t="{t}" aria-pressed="true" style="--c:{tc[t][0]};--cf:{tc[t][1]}">{esc(tinfo[t]["label"])}</button>' for t in (0, 1))
    js = r"""<script>
const q=document.getElementById('q'),st=document.getElementById('st'),empty=document.getElementById('empty'),svcs=[...document.querySelectorAll('.svc')],tiers=[...document.querySelectorAll('.tier')];
function run(){const w=q.value.toLowerCase().split(/\s+/).filter(Boolean),on=new Set(tiers.filter(t=>t.getAttribute('aria-pressed')==='true').map(t=>t.dataset.t));let n=0;
  svcs.forEach(s=>{const ok=on.has(s.dataset.tier)&&w.every(x=>s.dataset.q.includes(x));s.hidden=!ok;if(ok)n++});
  document.querySelectorAll('.cat').forEach(c=>c.hidden=!c.querySelector('.svc:not([hidden])'));document.querySelectorAll('.zone').forEach(z=>z.hidden=!z.querySelector('.svc:not([hidden])'));
  empty.hidden=n>0;st.textContent=n?n+' services':'No services';document.getElementById('en').textContent=q.value.trim()}
q.addEventListener('input',run);tiers.forEach(t=>t.addEventListener('click',()=>{t.setAttribute('aria-pressed',t.getAttribute('aria-pressed')!=='true');run()}));
q.addEventListener('keydown',e=>{if(e.key==='Escape'){q.value='';run()}});
document.getElementById('clr').addEventListener('click',()=>{q.value='';tiers.forEach(t=>t.setAttribute('aria-pressed','true'));run();q.focus()});
addEventListener('keydown',e=>{if(e.key==='/'&&!/INPUT|TEXTAREA/.test(document.activeElement.tagName)&&!document.querySelector('dialog[open]')){e.preventDefault();q.focus()}});
</script>"""
    body = (f'<div class="wrap">{brand()}<nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Atlas</a><span>›</span><span class="pill" style="--c:var(--iac);--cf:var(--iacf)">IaC line</span><span>›</span><span>Azure with Terraform</span></nav>'
            '<h1>Azure</h1><p class="tag">What an Azure service provides, what it requires, how it relates to other services, and how to build it with Terraform. Tiers 0 and 1 for now.</p>'
            f'<div class="tools"><label class="plan"><span class="sr">Filter services</span>{PIN}<input id="q" type="search" placeholder="Filter the {len(AZ["services"])} services" autocomplete="off"></label><div class="tierbar" role="group" aria-label="Tiers">{chips}</div></div>'
            '<p id="st" class="sr" role="status"></p><main>'
            f'<div id="empty" class="empty" hidden>No service matches “<span id="en"></span>”. <button type="button" id="clr">Clear the filters</button> to see every service.</div>{zones}</main></div>')
    return page("Azure · Atlas transit", HEAD, body + chrome(True) + js, CSS)


def loop():
    import math
    W, H = 940, 330
    lem = lambda t, a=330: (W / 2 + a * math.cos(t) / (1 + math.sin(t) ** 2), H / 2 - a * .95 * math.sin(t) * math.cos(t) / (1 + math.sin(t) ** 2))
    st, n = T["stages"], len(T["stages"])
    half = n // 2
    def path(t0, t1):
        return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in (lem(t0 + (t1 - t0) * i / 120) for i in range(121)))
    base = ("var(--iac)", "var(--cic)")
    shade = lambda i: f"var(--{'do'[i // half]}{i % half + 1})"
    nodes = ""
    for i, sg in enumerate(st):
        lobe, k = divmod(i, half)
        x, y = lem(math.pi / 2 + math.pi * lobe + (k + .5) * math.pi / half)
        ly = y - 26 if y < H / 2 else y + 36
        nodes += (f'<a href="#stage-{sg["id"]}" aria-label="Stage {i + 1}: {esc(sg["label"])}"><g style="--sc:{shade(i)}"><circle class="st" cx="{x:.1f}" cy="{y:.1f}" r="15" style="stroke:{shade(i)}"/>'
                  f'<text x="{x:.1f}" y="{ly:.1f}" text-anchor="middle">{i + 1} {esc(sg["label"])}</text></g></a>')
    segs = ""
    for i in range(n):
        lobe, k = divmod(i, half)
        t0 = math.pi / 2 + math.pi * lobe + k * math.pi / half
        segs += f'<path class="bg" d="{path(t0, t0 + math.pi / half)}" style="stroke:{shade(i)}"/>'
    svg = (f'<svg class="loopsvg" viewBox="0 0 {W} {H}" role="group" aria-label="The DevOps loop: {", ".join(s_["label"] for s_ in st)}, then back to {st[0]["label"]}">'
           f'{segs}<text class="lobe" x="{W * .25}" y="{H / 2 + 6}">Dev</text><text class="lobe" x="{W * .75}" y="{H / 2 + 6}">Ops</text>{nodes}</svg>')
    fam = {f["id"]: f["label"] for f in T["families"]}
    groups = ""
    for lobe, name in ((0, "Dev"), (1, "Ops")):
        items = ""
        for i, sg in enumerate(st):
            if i // half != lobe:
                continue
            mine = [t for t in T["topics"] if not t.get("draft") and sg["id"] in t.get("stages", [])]
            pills = "".join(f'<li><a href="{"azure" if t["id"] == "azure" else "topic"}.html">{esc(t["label"])}</a></li>' for t in mine) or '<li class="none">No Atlas topic covers this stage yet.</li>'
            items += f'<article class="stop stage" id="stage-{sg["id"]}" style="--c:{shade(i)};--cf:var(--{"do"[lobe]}{i % half + 1}f)"><h3><small>{i + 1}</small>{esc(sg["label"])}</h3><p>{esc(sg["about"])}</p><ul class="pills">{pills}</ul></article>'
        groups += f'<section class="grp2" style="--c:{base[lobe]};--cf:{"var(--iacf)" if lobe == 0 else "var(--cicf)"}"><h2 class="lname">{name}</h2><div class="stops">{items}</div></section>'
    body = (f'<div class="wrap">{brand("loop")}<nav class="crumb" aria-label="Breadcrumb"><a href="index.html">Atlas</a><span>›</span><span>Interchanges</span><span>›</span><span>DevOps loop</span></nav>'
            f'<h1>DevOps loop</h1><p class="tag">The eight stages, and where each topic fits. A topic can belong to several stages.</p>{svg}<main>{groups}'
            '<p class="hint">Which stages a topic belongs to is a judgement recorded in the topic\'s spec, not something a source states.</p></main></div>')
    return page("DevOps loop · Atlas transit", HEAD, body + chrome(), CSS)

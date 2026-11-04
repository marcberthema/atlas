"""Real Atlas content for the mocks. Reads the repo; writes nothing."""
import html, json, re
from pathlib import Path

R = Path(__file__).resolve().parents[2]
esc = html.escape
T = json.loads((R / "topics.json").read_text())
G = json.loads((R / "topics/gitops/data/gitops.json").read_text())
L = json.loads((R / "views/lenses/data/lenses.json").read_text())
IDX = json.loads(re.search(r'<script id="idx" type="application/json">(.*?)</script>',
                           (R / "dist/index.html").read_text(), re.S).group(1))
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')


def gfont(spec):
    return FONTS + f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{spec}&display=swap">'


def md(s):
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", esc(s))


def families():
    """Families with their published topics, entry counts and sample entry names."""
    out = []
    for f in T["families"]:
        ts = []
        for t in T["topics"]:
            if t.get("draft") or t["family"] != f["id"]:
                continue
            rows = [r for r in IDX if r[0] == t["id"]]
            ts.append({**t, "count": len(rows), "samples": [r[3] for r in rows[:4]]})
        out.append({**f, "topics": ts})
    return out


def entry(eid):
    e = next(x for x in G["entries"] if x["id"] == eid)
    bullets = next(([i for i in s["items"] if isinstance(i, str)] for s in e["sections"]
                    if any(isinstance(i, str) for i in s["items"])), [])
    gotcha = next((i["text"] for s in e["sections"] for i in s["items"]
                   if isinstance(i, dict) and i.get("type") == "callout"), "")
    return {"id": e["id"], "name": e["name"], "summary": e["summary"], "status": e.get("status", ""),
            "level": e.get("level", ""), "version": e["version"], "license": e.get("license", ""),
            "links": e.get("links", []), "bullets": bullets[:3], "gotcha": gotcha}


def comparison():
    c = G["comparisons"][0]
    return {"title": c["title"], "columns": c["columns"], "rows": c["rows"][:5]}


def search_block(idx_json=True):
    """Shared search script. Markup contract: #q input, #st status, #res results, #fams hidden while searching."""
    data = json.dumps(IDX, separators=(",", ":")).replace("</", "<\\/")
    return f"""<script id="idx" type="application/json">{data}</script>
<script>
const I=JSON.parse(document.getElementById('idx').textContent),q=document.getElementById('q'),res=document.getElementById('res'),st=document.getElementById('st'),fams=document.getElementById('fams');
const esc=s=>String(s).replace(/[&<>"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]));
function run(){{
  const w=q.value.toLowerCase().split(/\\s+/).filter(Boolean);
  fams.hidden=w.length>0;res.hidden=!w.length;
  if(!w.length){{st.textContent='';return}}
  const hits=I.filter(r=>w.every(x=>(r[3]+' '+r[4]).toLowerCase().includes(x))).slice(0,12);
  st.textContent=hits.length?hits.length+' results':'No results';
  res.innerHTML=hits.length?hits.map(r=>'<a class="hit" href="topic.html"><b>'+esc(r[3])+'</b><span>'+esc(r[4])+'</span><small>'+esc(r[1])+'</small></a>').join('')
    :'<p class="none">No match for “'+esc(q.value.trim())+'”. <button type="button" id="clr">Clear the search</button> to browse every topic.</p>';
}}
q.addEventListener('input',run);
q.addEventListener('keydown',e=>{{if(e.key==='Escape'){{q.value='';run()}}else if(e.key==='ArrowDown'){{const h=res.querySelector('a.hit');if(h){{e.preventDefault();h.focus()}}}}}});
res.addEventListener('keydown',e=>{{const hs=[...res.querySelectorAll('a.hit')],i=hs.indexOf(document.activeElement);if(i<0)return;
  if(e.key==='ArrowDown'&&hs[i+1]){{e.preventDefault();hs[i+1].focus()}}else if(e.key==='ArrowUp'){{e.preventDefault();(hs[i-1]||q).focus()}}}});
res.addEventListener('click',e=>{{if(e.target.id==='clr'){{q.value='';run();q.focus()}}}});
addEventListener('keydown',e=>{{if(e.key==='/'&&!e.ctrlKey&&!e.metaKey&&!/INPUT|TEXTAREA/.test(document.activeElement.tagName)){{e.preventDefault();q.focus()}}}});
</script>"""


def lenses_markup():
    """Shared lens diagram markup; each world styles .lensbar, .lane, .role, .dim, .panel."""
    lenses = "".join(f'<button type="button" class="lensbtn" data-l="{l["id"]}" aria-pressed="{"true" if i == 0 else "false"}">{esc(l["label"])}</button>'
                     for i, l in enumerate(L["lenses"]))
    lanes = ""
    for ln in L["lanes"]:
        cells = ""
        for col in range(6):
            r = next((x for x in L["roles"] if x.get("at") == {"lane": ln["id"], "col": col}), None)
            cells += (f'<button type="button" class="role c-{r["category"]}" data-id="{r["id"]}" data-lenses="{" ".join(r["lenses"])}">{esc(r["name"])}</button>'
                      if r else '<span class="gap"></span>')
        lanes += f'<div class="lane" role="group" aria-label="{esc(ln["label"])}"><h2>{esc(ln["label"])}</h2><div class="cells">{cells}</div></div>'
    roles = {r["id"]: {k: r.get(k, "") for k in ("name", "full", "what", "where", "why")} for r in L["roles"]}
    about = {l["id"]: l["about"] for l in L["lenses"]}
    edges = [e for e in L["edges"] if not e["to"].startswith("@") and not e["from"].startswith("@")]
    js = f"""<script>
const R={json.dumps(roles)},A={json.dumps(about)},E={json.dumps(edges)};
const btns=[...document.querySelectorAll('.lensbtn')],roles=[...document.querySelectorAll('.role')],panel=document.getElementById('panel'),live=document.getElementById('live');
function lens(id){{btns.forEach(b=>b.setAttribute('aria-pressed',b.dataset.l===id));let n=0;
  roles.forEach(r=>{{const on=r.dataset.lenses.split(' ').includes(id);r.classList.toggle('dim',!on);if(on)n++}});
  document.getElementById('about').textContent=A[id];draw(id);live.textContent=btns.find(b=>b.dataset.l===id).textContent+' lens: '+n+' roles';}}
btns.forEach(b=>b.addEventListener('click',()=>lens(b.dataset.l)));
roles.forEach(r=>r.addEventListener('click',()=>{{const d=R[r.dataset.id];roles.forEach(x=>x.setAttribute('aria-pressed',x===r));
  panel.innerHTML='<h2>'+d.full+'</h2><p>'+d.what+'</p><p><b>Where</b> '+d.where+'</p><p><b>Why</b> '+d.why+'</p>';}}));
const lanesEl=document.getElementById('lanes'),svg=document.getElementById('wires');let cur='app',hov=null;
function rp(p,r){{let d='M'+p[0][0]+' '+p[0][1];for(let i=1;i<p.length-1;i++){{const [x0,y0]=p[i-1],[x1,y1]=p[i],[x2,y2]=p[i+1],l1=Math.hypot(x1-x0,y1-y0),l2=Math.hypot(x2-x1,y2-y1),k=Math.min(r,l1/2,l2/2);
  d+='L'+(x1-(x1-x0)/l1*k)+' '+(y1-(y1-y0)/l1*k)+'Q'+x1+' '+y1+' '+(x1+(x2-x1)/l2*k)+' '+(y1+(y2-y1)/l2*k)}}
  return d+'L'+p[p.length-1][0]+' '+p[p.length-1][1]}}
function draw(id){{cur=id||cur;const o=lanesEl.getBoundingClientRect();
  const sel=document.querySelector('.role[aria-pressed=true]'),act=hov||(sel&&sel.dataset.id)||null;
  const box=i=>{{const b=document.querySelector('.role[data-id="'+i+'"]');if(!b)return null;const r=b.getBoundingClientRect();return {{l:r.left-o.left,r:r.right-o.left,t:r.top-o.top,b:r.bottom-o.top,w:r.width,h:r.height,cx:(r.left+r.right)/2-o.left,cy:(r.top+r.bottom)/2-o.top}}}};
  const ed=E.filter(e=>e.lenses.includes(cur)).map(e=>({{e,a:box(e.from),b:box(e.to)}})).filter(x=>x.a&&x.b);
  ed.forEach(x=>{{if(Math.abs(x.a.cy-x.b.cy)<4){{x.sa=x.a.cx<x.b.cx?'r':'l';x.sb=x.a.cx<x.b.cx?'l':'r'}}else{{const dn=x.b.cy>x.a.cy;x.sa=dn?'b':'t';x.sb=dn?'t':'b'}}}});
  const slots={{}};ed.forEach(x=>{{[['from','sa','b'],['to','sb','a']].forEach(([w,sd,oth])=>{{(slots[x.e[w]+x[sd]]=slots[x.e[w]+x[sd]]||[]).push([x,w,sd,oth])}})}});
  Object.values(slots).forEach(L=>{{const hz='lr'.includes(L[0][2]==='sa'?L[0][0].sa:L[0][0].sb);
    L.sort((p,q)=>hz?p[0][p[3]].cy-q[0][q[3]].cy:p[0][p[3]].cx-q[0][q[3]].cx);
    L.forEach(([x,w,sd],k)=>{{const bx=w==='from'?x.a:x.b,side=x[sd],f=(k+1)/(L.length+1);
      x[w==='from'?'pa':'pb']=side==='b'?[bx.l+bx.w*f,bx.b]:side==='t'?[bx.l+bx.w*f,bx.t]:side==='r'?[bx.r,bx.t+bx.h*f]:[bx.l,bx.t+bx.h*f]}})}});
  let h='<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 1L9 5L0 9" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>';
  ed.forEach(x=>{{const [ax,ay]=x.pa,[bx,by]=x.pb,hz=x.sa==='r'||x.sa==='l',on=act&&(x.e.from===act||x.e.to===act);
    const pts=hz?(Math.abs(ay-by)<2?[[ax,ay],[bx,by]]:[[ax,ay],[(ax+bx)/2,ay],[(ax+bx)/2,by],[bx,by]]):(Math.abs(ax-bx)<2?[[ax,ay],[bx,by]]:[[ax,ay],[ax,(ay+by)/2],[bx,(ay+by)/2],[bx,by]]);
    const cls='w'+(act?(on?' on':' off'):'');
    h+='<path class="'+cls+'" d="'+rp(pts,9)+'" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" marker-end="url(#ah)"'+(x.e.style==='dash'?' stroke-dasharray="6 5"':x.e.style==='dot'?' stroke-dasharray="1 5"':'')+'/>';
    if(x.e.label&&(!act||on)){{const mx=hz?(ax+bx)/2:(ax+bx)/2,my=hz?ay-7:(ay+by)/2-6;h+='<text x="'+mx+'" y="'+my+'" text-anchor="middle" class="wl">'+x.e.label+'</text>'}}}});
  svg.setAttribute('viewBox','0 0 '+o.width+' '+o.height);svg.innerHTML=h;}}
roles.forEach(r=>{{['mouseenter','focus'].forEach(ev=>r.addEventListener(ev,()=>{{hov=r.dataset.id;draw()}}));['mouseleave','blur'].forEach(ev=>r.addEventListener(ev,()=>{{hov=null;draw()}}));r.addEventListener('click',()=>draw())}});
addEventListener('resize',()=>draw());if(document.fonts)document.fonts.ready.then(()=>draw());
lens('app');
</script>"""
    return (f'<div class="lensbar" role="group" aria-label="Lens">{lenses}</div><p id="about" class="about"></p>'
            f'<div class="lanes" id="lanes" style="position:relative">{lanes}<svg class="wires" id="wires" aria-hidden="true"></svg></div><aside id="panel" class="panel" aria-live="polite"><h2>Pick a role</h2>'
            f'<p>Select a role in the picture to read what it is, where it sits and why it exists.</p></aside>'
            f'<p id="live" class="sr" role="status"></p>', js)


BASE_CSS = """*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}body{margin:0}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
[hidden]{display:none!important}a{color:inherit}img,svg{max-width:100%}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important;scroll-behavior:auto!important}}
"""


def page(title, head, body, css):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{esc(title)}</title>{head}<style>{BASE_CSS}{css}</style></head><body>{body}</body></html>')

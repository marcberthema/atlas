"""What every Atlas page shares: the topic registry, the top banner and the footer disclaimer.

Templates carry two markers, filled in at build time so the page stays plain static HTML:
  <!--__BANNER__-->      right after <body>
  /*__BANNER_CSS__*/     inside <style>
  <!--__FOOTER__-->      just before </body>
Links are relative and name index.html, so they also work from file://.
"""
import html
import json
import os
import re
import subprocess
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
DIST = SITE / "dist"
BANNER_MARK = "<!--__BANNER__-->"
CSS_MARK = "/*__BANNER_CSS__*/"
FOOTER_MARK = "<!--__FOOTER__-->"
PUBLIC = "https://atlas.marcberthelette.com/"  # only for pages outside dist/, which cannot link to it relatively

CSS = """
.atlas{display:flex;gap:6px;align-items:center;flex-wrap:wrap;border-bottom:1px solid var(--rule);padding:0 0 8px;margin:0 0 12px}
.atlas a{color:var(--fg);text-decoration:none;padding:4px 12px;border-radius:8px;border:1px solid transparent}
.atlas a:hover{border-color:var(--rule)}
.atlas a:focus-visible{outline:3px solid var(--acc);outline-offset:2px}
.atlas-foot{border-top:1px solid var(--rule);margin-top:28px;padding-top:10px;color:var(--mut);font-size:.85rem}
.atlas-foot p{margin:0 0 4px}
.atlas.two{display:block;position:sticky;top:0;z-index:5;background:var(--bg);margin:0 0 12px;padding:0 0 8px}
.atlas .fams{display:flex;align-items:center;gap:8px;background:var(--card);border:1px solid var(--rule);border-radius:12px;padding:5px 8px}
.atlas .fams::before{content:"";flex:0 0 170px}
.atlas .fb,.atlas .tops{display:flex;gap:6px;align-items:center;overflow-x:auto;scrollbar-width:none}
.atlas .fb{flex:1}
.atlas .fb>:first-child{margin-left:auto}
.atlas .fb>:last-child{margin-right:auto}
.atlas .tops>div{margin-inline:auto}
.atlas .fb{padding:0 2px}
.atlas .tops{margin-top:8px}
.atlas .tops>div{display:flex;gap:6px;flex:none}
.atlas.none .tops{display:none}
.atlas button{font:inherit;font-weight:600;white-space:nowrap;color:var(--fg);background:none;padding:5px 16px;border-radius:8px;border:1px solid transparent;cursor:pointer}
.atlas button:hover{border-color:var(--rule);background:var(--bg)}
.atlas button:focus-visible{outline:3px solid var(--acc);outline-offset:2px}
.atlas button[aria-pressed=true]{background:var(--acc);color:var(--bg)}
.atlas .tops a{white-space:nowrap;font-size:.94rem}
.atlas .rt{display:flex;align-items:center;justify-content:flex-end;gap:2px;flex:0 0 170px}
.atlas .fams .home{margin:0;padding:4px 8px;white-space:nowrap}
.atlas .tg{display:inline-flex;padding:5px 8px;color:var(--acc)}
.atlas dialog.ai{width:min(460px,calc(100vw - 24px));max-height:calc(100vh - 24px);border:1px solid var(--rule);border-radius:12px;background:var(--bg);color:var(--fg);padding:16px 18px;font-size:.92rem}
.atlas dialog.ai::backdrop{background:rgba(0,0,0,.5)}
.atlas dialog.ai h2{font-size:1.05rem;color:var(--acc);margin:0 0 8px;border:0;padding:0}
.atlas dialog.ai p{margin:0 0 8px}
.atlas dialog.ai .vr{border-top:1px solid var(--rule);padding-top:8px;color:var(--mut)}
.atlas dialog.ai .vr code{color:var(--fg)}
.atlas dialog.ai .dx{display:flex;gap:8px;align-items:flex-start;border-top:1px solid var(--rule);padding-top:8px;margin-bottom:8px;cursor:pointer}
.atlas dialog.ai .dx small{display:block;color:var(--mut)}
.atlas dialog.ai a{padding:0;text-decoration:underline;color:var(--acc)}
.atlas dialog.ai .cl{float:right;padding:4px 14px;border-color:var(--rule)}
.atlas .tg svg{width:18px;height:18px;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
@media(max-width:560px){.atlas .fams::before{display:none}.atlas .rt{flex:none}}
:root[data-theme=light]{color-scheme:light}
:root[data-theme=dark]{color-scheme:dark}
.atlas .skip{position:absolute;left:-9999px}
.atlas .skip:focus{left:8px;top:8px;z-index:10;background:var(--bg);border-color:var(--acc)}
.atlas [hidden]{display:none!important}
.atlas .home{font-weight:700;color:var(--acc);margin-right:6px}
.atlas a[aria-current=page]{background:var(--acc);color:var(--bg);font-weight:600}
"""


DISCLAIMER = [
    "Everything here is collected with AI assistance from public sources, and it changes. Always check the real source (the links and dates on each entry) before relying on it. "
    "Entries marked <b>?</b> or \"unconfirmed\" haven't been verified yet.",
    "This is a personal project, not an official resource of Microsoft, HashiCorp, Argo CD or any other product named here.",
]
FOOTER = '<footer class="atlas-foot">' + "".join(f"<p>{x}</p>" for x in DISCLAIMER) + "</footer>"


def repo_url():
    """The https address of the git remote, or "" when there is none (the build never fails for it)."""
    try:
        u = subprocess.run(["git", "remote", "get-url", "origin"], cwd=SITE, capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return ""
    m = re.match(r"(?:git@|ssh://git@|https://)([^:/]+)[:/](.+?)(?:\.git)?/?$", u)
    return f"https://{m[1]}/{m[2]}" if m else ""


def ref():
    """The version shown in the About window: ATLAS_REF if set (`make deploy`), else the release tag in the VERSION file, else "dev".
    The file changes only when a release is cut, so committed pages do not change on every commit."""
    v = SITE / "VERSION"
    return os.environ.get("ATLAS_REF", "").strip() or (v.read_text(encoding="utf-8").strip() if v.exists() else "") or "dev"


def load():
    return json.loads((SITE / "topics.json").read_text(encoding="utf-8"))


def published():
    """Topics that are built and shown. An entry with "draft": true is an idea: it never reaches dist/."""
    return [t for t in load()["topics"] if not t.get("draft")]


def views():
    """Generated pages that cut across topics (docs/views.md). They are shown as a last family, Views."""
    return [dict(v, family="views") for v in load().get("views", [])]


def check():
    """Exit 1 when topics.json is inconsistent: ids, published topics need a folder, drafts must not leak into dist/."""
    bad, seen = [], set()
    families = [f.get("id") for f in load().get("families", [])]
    if not families or len(set(families)) != len(families) or not all(f.get("label") for f in load()["families"]):
        bad.append("families need unique ids and labels")
    stages = [x.get("id") for x in load().get("stages", [])]
    if len(set(stages)) != len(stages) or not all(x.get("label") for x in load().get("stages", [])):
        bad.append("stages need unique ids and labels")
    for t in load()["topics"]:
        i = t.get("id", "")
        if not t.get("draft") and t.get("family") not in families:
            bad.append(f"published topic {i} needs a family from {families}")
        if t.get("draft") and t.get("family") not in (None, *families):
            bad.append(f"draft topic {i} names an unknown family: {t['family']}")
        if any(x not in stages for x in t.get("stages", [])):
            bad.append(f"topic {i} names an unknown stage: {t['stages']}")
        if not i or not t.get("label"):
            bad.append(f"topic needs an id and a label: {t}")
        if i in seen:
            bad.append(f"duplicate topic id: {i}")
        seen.add(i)
        if t.get("draft"):
            if (DIST / i).exists():
                bad.append(f"draft topic {i} has a dist/{i} folder: remove it")
        elif not (SITE / "topics" / i / "Makefile").exists() or not t.get("description"):
            bad.append(f"published topic {i} needs topics/{i}/Makefile and a description (or set \"draft\": true)")
    for v in load().get("views", []):
        if not v.get("id") or not v.get("label") or not v.get("description"):
            bad.append(f"view needs an id, a label and a description: {v}")
        if v.get("id") in seen:
            bad.append(f"view id clashes with a topic id: {v.get('id')}")
    for x in load().get("stages", []):
        if not x.get("about"):
            bad.append(f"stage {x.get('id')} needs an about line")
    for line in bad:
        print("bad:", line)
    print(f"topics {len(seen)} published {len(published())} drafts {len(seen) - len(published())} bad {len(bad)}")
    return 1 if bad else 0


def by_family():
    """[(family, [published topics])] in the order of "families"; families without a published topic are left out. The views come last, as a family."""
    topics = published()
    groups = [(f, [t for t in topics if t.get("family") == f["id"]]) for f in load()["families"]]
    groups = [(f, ts) for f, ts in groups if ts]
    return groups + ([({"id": "views", "label": "Views", "description": "Pictures that cut across the topics; they are not topics themselves."}, views())] if views() else [])


def banner(current, prefix):
    """Two rows: the families (and the home icon), then the topics of the selected family.
    `current` is a topic id or None for the landing page; `prefix` is "../" from a topic page, "" from the landing.
    On a topic page its family starts selected; on the landing nothing is, and a family filters the cards (sections with data-fam)."""
    reg = load()
    groups = by_family()
    cur_fam = next((t["family"] for _, ts in groups for t in ts if t["id"] == current), "")
    buttons = "".join(
        '<button type="button" data-fam="{id}" aria-pressed="false">{label}</button>'.format(id=f["id"], label=html.escape(f["label"]))
        for f, _ in groups)
    panels = "".join(
        '<div data-fam="{id}" aria-label="{label}">{links}</div>'.format(
            id=f["id"], label=html.escape(f["label"]),
            links="".join(
                '<a href="{p}{id}/index.html"{cur}>{label}</a>'.format(
                    p=prefix, id=t["id"], label=html.escape(t["label"]), cur=' aria-current="page"' if t["id"] == current else "")
                for t in ts))
        for f, ts in groups)
    return ('<nav class="atlas two" aria-label="Atlas" data-current="{cur}"><a class="skip" href="#">Skip to content</a>'
            '<div class="fams"><div class="fb" role="group" aria-label="Families">{b}</div>'
            '<div class="rt"><button type="button" class="tg th">{icons}</button>'
            '<button type="button" class="tg ab" aria-label="About Atlas" title="About Atlas">{help}</button>'
            '<a class="home" href="{p}index.html" aria-label="{name} home" title="{name} home">&#8962; {name}</a></div></div>'
            '<div class="tops">{panels}</div>{about}<script>{js}</script></nav>').format(
        cur=cur_fam, b=buttons, p=prefix, name=html.escape(reg["name"]), panels=panels, js=JS, icons=ICONS, help=HELP, about=about())


HELP = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M9.1 9a3 3 0 0 1 5.8 1c0 2-3 3-3 3M12 17h.01"/></svg>'


def about():
    """The About window: disclaimer, where this version came from, and the switch that shows the low-value details of every entry."""
    url, r = repo_url(), ref()
    sha = r.removesuffix("-dirty")
    where = '<a href="{u}" target="_blank" rel="noopener">{u}</a>'.format(u=html.escape(url)) if url else "not available"
    commit = ('<a href="{u}/commit/{s}" target="_blank" rel="noopener"><code>{r}</code></a>'.format(u=html.escape(url), s=html.escape(sha), r=html.escape(r))
              if url and r != "dev" else "<code>{}</code>".format(html.escape(r)))
    return ('<dialog class="ai" aria-labelledby="ai-t"><button type="button" class="cl">Close</button><h2 id="ai-t">About Atlas</h2>{d}'
            '<label class="dx" hidden><input type="checkbox"><span>Show entry details<small>Release and check dates, status, CNCF, licence, and every source. '
            'The version analysed is always shown.</small></span></label>'
            '<p class="vr">Version {c}<br>Source {w}</p></dialog>').format(d="".join(f"<p>{x}</p>" for x in DISCLAIMER), c=commit, w=where)


# Sun (shown in dark mode: click for light) and moon (shown in light mode: click for dark).
ICONS = ('<svg class="sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
         '<svg class="moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 13.5A8.5 8.5 0 0 1 10.5 3 8.5 8.5 0 1 0 21 13.5z"/></svg>')

# The banner is sticky: --atlash is its height, so a page's own sticky bars can sit below it.
JS = """(function(){var n=document.currentScript.parentNode,bs=n.querySelectorAll('button[data-fam]'),ps=n.querySelectorAll('.tops [data-fam]'),keep=n.dataset.current,sel='';
function h(){document.documentElement.style.setProperty('--atlash',n.offsetHeight+'px')}
function show(f){sel=f;n.classList.toggle('none',!f);bs.forEach(function(b){b.setAttribute('aria-pressed',b.dataset.fam===f)});ps.forEach(function(p){p.hidden=p.dataset.fam!==f});document.querySelectorAll('main [data-fam]').forEach(function(c){c.hidden=!!f&&c.dataset.fam!==f});h()}
bs.forEach(function(b){b.addEventListener('click',function(){show(sel===b.dataset.fam&&!keep?'':b.dataset.fam)})});
n.querySelector('.skip').addEventListener('click',function(e){var m=document.querySelector('main');if(m){e.preventDefault();m.tabIndex=-1;m.focus()}});
var root=document.documentElement,mq=matchMedia('(prefers-color-scheme:dark)'),tg=n.querySelector('.th');
function eff(){return root.dataset.theme||(mq.matches?'dark':'light')}
function paint(){var d=eff()==='dark';tg.querySelector('.sun').toggleAttribute('hidden',!d);tg.querySelector('.moon').toggleAttribute('hidden',d);tg.setAttribute('aria-label',d?'Switch to light mode':'Switch to dark mode');tg.title=tg.getAttribute('aria-label')}
try{var st=localStorage.getItem('atlas-theme');if(st)root.dataset.theme=st}catch(e){}
tg.addEventListener('click',function(){var t=eff()==='dark'?'light':'dark';root.dataset.theme=t;try{localStorage.setItem('atlas-theme',t)}catch(e){}paint()});
if(mq.addEventListener)mq.addEventListener('change',paint);
var dl=n.querySelector('dialog.ai'),dx=dl.querySelector('.dx'),cb=dx.querySelector('input');
try{root.dataset.details=localStorage.getItem('atlas-details')==='1'?'show':'hide'}catch(e){root.dataset.details='hide'}
n.querySelector('.ab').addEventListener('click',function(){dx.hidden=!root.dataset.xd;cb.checked=root.dataset.details==='show';dl.showModal()});
cb.addEventListener('change',function(){root.dataset.details=cb.checked?'show':'hide';try{localStorage.setItem('atlas-details',cb.checked?'1':'0')}catch(e){}});
dl.querySelector('.cl').addEventListener('click',function(){dl.close()});
dl.addEventListener('click',function(e){if(e.target===dl)dl.close()});
paint();addEventListener('resize',h);show(keep)})();"""


DARK = re.compile(r"@media\(prefers-color-scheme:dark\)\{:root\{(.*?)\}\}", re.S)


def themed(page):
    """Let the banner's toggle override the OS setting: the dark variables also apply under html[data-theme=dark], and not under light."""
    assert len(DARK.findall(page)) == 1, "template needs one prefers-color-scheme:dark block"
    return DARK.sub(lambda m: "@media(prefers-color-scheme:dark){:root:not([data-theme=light]){%s}}:root[data-theme=dark]{%s}" % (m[1], m[1]), page)


def apply(page, current):
    """Fill the banner markers of a topic page."""
    assert all(page.count(m) == 1 for m in (BANNER_MARK, CSS_MARK, FOOTER_MARK)), "template needs one banner, one banner css and one footer marker"
    return themed(page).replace(BANNER_MARK, banner(current, "../")).replace(CSS_MARK, CSS).replace(FOOTER_MARK, FOOTER)


def apply_standalone(page, label):
    """Fill the markers of a page kept in git but not published: the banner names only that page and links to the public site."""
    assert all(page.count(m) == 1 for m in (BANNER_MARK, CSS_MARK, FOOTER_MARK)), "template needs one banner, one banner css and one footer marker"
    nav = '<nav class="atlas" aria-label="Topics"><a class="home" href="{}">{}</a><a href="index.html" aria-current="page">{}</a></nav>'.format(
        PUBLIC, html.escape(load()["name"]), html.escape(label))
    return page.replace(BANNER_MARK, nav).replace(CSS_MARK, CSS).replace(FOOTER_MARK, FOOTER)


if __name__ == "__main__":
    import sys
    if sys.argv[1:] == ["ids"]:
        print(" ".join(t["id"] for t in published()))
    elif sys.argv[1:] == ["check"]:
        sys.exit(check())
    else:
        sys.exit("usage: atlas.py ids|check")

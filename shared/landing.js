// Rows are [topic id, topic label, entry id, name, summary]; a hit opens the entry in its topic.
const I=JSON.parse(document.getElementById('idx').textContent),q=document.getElementById('q'),res=document.getElementById('res'),st=document.getElementById('st'),fams=document.getElementById('fams');
const H=window.ATLAS_HREF||(id=>id+'/index.html');
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function run(){
  const w=q.value.toLowerCase().split(/\s+/).filter(Boolean);
  fams.hidden=w.length>0;res.hidden=!w.length;
  if(!w.length)return;
  const hits=I.map(r=>{const n=r[3].toLowerCase(),all=(n+' '+r[4].toLowerCase());
    return w.every(x=>all.includes(x))?[w.every(x=>n.includes(x))?0:1,r]:null}).filter(Boolean).sort((a,b)=>a[0]-b[0]).slice(0,40);
  const n=hits.length,label=n+(n===40?'+':'')+' result'+(n===1?'':'s');
  st.textContent=n?label:'No results';
  res.innerHTML=n?'<p class="count">'+label+'</p>'
    +hits.map(h=>{const r=h[1];return '<a class="hit" href="'+H(r[0])+'#'+encodeURIComponent(r[2])+'"><small>'+esc(r[1])+'</small><b>'+esc(r[3])+'</b><span>'+esc(r[4])+'</span></a>'}).join('')
    :'<p class="count">No match for “'+esc(q.value.trim())+'”.</p><p class="hint">Searches entry names and summaries. Try fewer or shorter words, or <a href="#" id="clr">clear the search</a> to browse every topic.</p>';
}
const first=()=>res.hidden?null:res.querySelector('a.hit');
q.addEventListener('input',run);
q.addEventListener('keydown',e=>{
  if(e.key==='Escape'){q.value='';run()}
  else if(e.key==='ArrowDown'&&first()){e.preventDefault();first().focus()}
  else if(e.key==='Enter'&&first())first().click();
});
res.addEventListener('keydown',e=>{
  const hs=[...res.querySelectorAll('a.hit')],i=hs.indexOf(document.activeElement);
  if(i<0)return;
  if(e.key==='ArrowDown'&&hs[i+1]){e.preventDefault();hs[i+1].focus()}
  else if(e.key==='ArrowUp'){e.preventDefault();(hs[i-1]||q).focus()}
});
res.addEventListener('click',e=>{if(e.target.id==='clr'){e.preventDefault();q.value='';run();q.focus()}});
addEventListener('keydown',e=>{if(e.key==='/'&&!e.ctrlKey&&!e.metaKey&&!e.altKey&&!(e.target.closest&&e.target.closest('input,textarea,select,dialog,[contenteditable]'))){e.preventDefault();q.focus()}});

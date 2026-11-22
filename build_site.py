"""Build docs/: a static site for GitHub Pages with the voiced prologue and Act 1, both built into index.html.

Run:  python3 build_site.py
Then publish the docs/ folder (GitHub: Settings > Pages > Deploy from a branch > main, /docs).

docs/
  index.html      the title page, with both chapters built in (#prologue, #act1).
                  The voiced prologue is rebuilt from mockups/prologue.html first.
                  The prologue's recorded voices are built in too, so the one file plays with sound.
  .nojekyll       tells GitHub Pages to serve the files as they are
The originals in mockups/ are never modified.
"""
import os, re, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
MOCK = os.path.join(ROOT, "mockups")
OUT = os.path.join(ROOT, "docs")
VOICES_SRC = os.path.join(ROOT, "voices", "samples", "office")

# 1. rebuild the voiced prologue so it matches the current prologue.html
subprocess.run([sys.executable, os.path.join(ROOT, "voices", "build_voiced.py")], check=True)

if os.path.isdir(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT)

def must(s, old, new):
    assert s.count(old) == 1, f"expected exactly one {old[:60]!r}"
    return s.replace(old, new)

# 2. the prologue: voices next to the page, and the end card leads on to Act 1
pro = open(os.path.join(MOCK, "prologue-voiced.html"), encoding="utf-8").read()
used = sorted(set(re.findall(r"\.\./voices/samples/office/([\w.-]+\.mp3)", pro)))
# the recorded voices go inside the page as data, so index.html plays with sound on its own
import base64
def _inline(m):
    with open(os.path.join(VOICES_SRC, m.group(1)), "rb") as fh:
        return "data:audio/mpeg;base64," + base64.b64encode(fh.read()).decode()
pro = re.sub(r"\.\./voices/samples/office/([\w.-]+\.mp3)", _inline, pro)
pro = must(pro, '<a class="btn" href="painterly-scene.html">Visit Cwm Du (scene mockup)</a>',
           '<a class="btn" href="index.html#act1" target="_top">Continue to Act 1</a><a class="btn" href="index.html#" target="_top">Title page</a>')
pro = re.sub(r"<title>[^<]*</title>", "<title>Black Seam · Prologue</title>", pro, count=1)

# 3. Act 1 as it is, with a way back to the title page from its end card
act = open(os.path.join(MOCK, "act1.html"), encoding="utf-8").read()
act = re.sub(r"<title>[^<]*</title>", "<title>Black Seam · Act 1</title>", act, count=1)
m = re.search(r'(<div class="row">)(.*?id="again".*?</div>)', act)
if m:
    act = act[:m.start(1)] + m.group(1) + '<a class="btn" href="index.html#" target="_top">Title page</a>' + act[m.end(1):]
# the chapel mockup isn't part of the site
act = act.replace('<a class="btn" href="chapel-scene.html">Visit Bethel, 1869 and 1871</a>', '')

# 4. the title page
INDEX = """<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Black Seam</title>
<meta name="description" content="A Victorian adventure about coal, lies and a Welsh valley. 1869.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=Inter:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{--bg:#120d09;--card:#1c140e;--line:rgba(233,184,106,.22);--gold:#e9b86a;--cream:#f3e3c4;--muted:#b9a68a}
*{box-sizing:border-box;margin:0}
html,body{background:var(--bg);color:var(--cream)}
body{min-height:100vh;font-family:Inter,system-ui,sans-serif;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:48px 16px;
 background:radial-gradient(ellipse at 50% 30%,rgba(233,184,106,.10),transparent 60%),var(--bg)}
header{text-align:center;max-width:640px}
small{letter-spacing:.32em;text-transform:uppercase;font-size:11px;color:var(--gold)}
h1{font-family:"Cormorant Garamond",serif;font-weight:400;font-size:clamp(52px,11vw,96px);line-height:1;margin:14px 0 12px}
header p{font-family:"Cormorant Garamond",serif;font-style:italic;font-size:clamp(18px,2.6vw,22px);color:var(--muted);line-height:1.45}
.chapters{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;width:min(720px,100%);margin-top:40px}
a.chapter{display:block;text-decoration:none;color:inherit;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:22px 22px 20px;transition:border-color .2s,transform .2s}
a.chapter:hover,a.chapter:focus-visible{border-color:var(--gold);transform:translateY(-2px)}
a.chapter.locked{opacity:.42;filter:grayscale(1);cursor:not-allowed;pointer-events:none}
a.chapter.locked:hover{transform:none}
a.chapter small{font-size:10px}
a.chapter h2{font-family:"Cormorant Garamond",serif;font-weight:500;font-size:30px;margin:6px 0 8px}
a.chapter p{font-size:14px;line-height:1.55;color:var(--muted)}
a.chapter span{display:inline-block;margin-top:14px;font-size:13px;color:var(--gold)}
#game{position:fixed;inset:0;width:100%;height:100%;border:0;background:#000;z-index:10}
body.playing{overflow:hidden}
footer a{color:var(--gold)}
footer{margin-top:36px;font-size:12px;color:var(--muted);text-align:center;max-width:520px;line-height:1.6}
@media (prefers-reduced-motion:reduce){a.chapter{transition:none}}
</style>
</head>
<body>
<header>
 <small>A Victorian adventure</small>
 <h1>Black Seam</h1>
 <p>London and the valleys of Glamorgan, 1869. A draughtsman, a dead man’s notebook, and six feet of coal nobody else knows about.</p>
</header>
<main class="chapters">
 <a class="chapter" href="#prologue">
  <small>Prologue · voiced</small>
  <h2>Bevan’s box</h2>
  <p>London, September 1869. Josiah Bevan is dead at his desk, and his notebook is in Elias Crane’s pocket.</p>
  <span>Play the prologue →</span>
 </a>
 <a class="chapter" id="act1card" href="#act1">
  <small>Act 1</small>
  <h2>The survey</h2>
  <p>Cwm Du, September 1869. A government surveyor gets off the train with a forged letter and a theodolite.</p>
  <span id="act1cta">Play Act 1 →</span>
 </a>
</main>
<footer>Best with sound on. Your progress in each chapter is saved in this browser. <a href="#" id="reset">Start over</a></footer>
<iframe id="game" title="Black Seam" allow="autoplay; fullscreen" hidden></iframe>
<script>
/* both chapters live in this one file; the address (#prologue, #act1) says which is playing */
const CHAPTERS=__CHAPTERS__;
const NAMES={prologue:'Black Seam · Prologue',act1:'Black Seam · Act 1'};
const frame=document.getElementById('game');
/* Act 1 opens once the prologue has been played to the end */
function prologueDone(){try{return !!localStorage.getItem('blackseam-game-prologue-complete')}catch(_){return false}}
function lockAct1(){const done=prologueDone(),c=document.getElementById('act1card');c.classList.toggle('locked',!done);c.setAttribute('aria-disabled',String(!done));c.tabIndex=done?0:-1;
 document.getElementById('act1cta').textContent=done?'Play Act 1 →':'Finish the prologue to unlock'}
function route(){
 let id=location.hash.slice(1);
 if(id==='act1'&&!prologueDone()){history.replaceState(null,'',location.pathname);id=''}
 lockAct1();
 if(CHAPTERS[id]){if(frame.dataset.ch!==id){frame.srcdoc=CHAPTERS[id];frame.dataset.ch=id}frame.hidden=false;document.body.classList.add('playing');document.title=NAMES[id];frame.focus()}
 else{frame.hidden=true;frame.removeAttribute('srcdoc');frame.dataset.ch='';document.body.classList.remove('playing');document.title='Black Seam'}}
addEventListener('hashchange',route);route();
/* start over: forget both chapters' saves and lock Act 1 again */
document.getElementById('reset').onclick=e=>{e.preventDefault();if(!confirm('Start over? This forgets your progress in both chapters.'))return;
 try{for(const k of['blackseam-game-prologue-complete','blackseam-prologue-v2','blackseam-act1-v1'])localStorage.removeItem(k)}catch(_){}lockAct1()};
</script>
</body>
</html>
"""
import json
chapters = json.dumps({"prologue": pro, "act1": act}, ensure_ascii=False).replace("</", "<\\/")
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(INDEX.replace("__CHAPTERS__", chapters))
open(os.path.join(OUT, ".nojekyll"), "w").close()

size = sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(OUT) for f in fs)
print(f"built docs/: index.html with the prologue, Act 1 and {len(used)} voice lines built in · {size/1e6:.1f} MB")

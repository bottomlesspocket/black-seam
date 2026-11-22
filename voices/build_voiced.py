"""Build mockups/prologue-voiced.html: an exact copy of mockups/prologue.html
with voice playback added to the dialogue function. Art, layout and all other
code are untouched; the original file is never modified.

Run:  python3 voices/build_voiced.py   (re-run whenever new lines are rendered)
"""
import json, os, sys
WEB = "--web" in sys.argv  # artifact build: page + office/*.mp3 side by side

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "mockups", "prologue.html")
OUT = os.path.join(ROOT, "mockups", "prologue-voiced.html")
if WEB:
    OUT = sys.argv[sys.argv.index("--web") + 1]
MANIFEST = os.path.join(ROOT, "voices", "samples", "office", "manifest.json")
WHO = {"Crane": "Elias Crane"}  # manifest speaker -> on-screen name

html = open(SRC, encoding="utf-8").read()
man = json.load(open(MANIFEST, encoding="utf-8"))
voice = {
    WHO.get(l["speaker"], l["speaker"]) + "|" + l["text"]: ("office/" if WEB else "../voices/samples/office/") + l["file"]
    for l in man["lines"] if l["file"]
}

OLD = """function line(who,text){return new Promise(res=>{
 clearInterval(typing);whoEl.textContent=who;lineEl.textContent='';choicesEl.innerHTML='';subEl.classList.add('on');
 let i=0,done=false,auto;const finish=()=>{if(done)return;done=true;clearInterval(typing);lineEl.textContent=text;auto=setTimeout(go,1600+text.length*42)};
 const go=()=>{clearTimeout(auto);clearInterval(typing);adv=null;res()};"""

NEW = """const VOICE=%s;
/* one reusable element, unlocked on the first tap, so iPhone Safari lets later lines play without a tap */
const voEl=new Audio();voEl.preload='auto';let voOn=false;
addEventListener('pointerdown',function u(){removeEventListener('pointerdown',u,true);voEl.src='data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEAQB8AAIA+AAACABAAZGF0YQAAAAA=';voEl.play().catch(()=>{})},true);
function stopVoice(){if(voOn){voEl.onended=null;voEl.pause();voOn=false}}
function line(who,text){return new Promise(res=>{
 clearInterval(typing);whoEl.textContent=who;lineEl.textContent='';choicesEl.innerHTML='';subEl.classList.add('on');
 stopVoice();const vf=VOICE[who+'|'+text];let voEnded=true;
 if(vf&&audio.started&&!audio.muted){voEnded=false;voOn=true;voEl.onended=()=>{voEnded=true;voOn=false;if(done){clearTimeout(auto);auto=setTimeout(go,600)}};voEl.src=vf;voEl.play().catch(()=>{voEnded=true;voOn=false})}
 let i=0,done=false,auto;const finish=()=>{if(done)return;done=true;clearInterval(typing);lineEl.textContent=text;auto=setTimeout(go,voEnded?1600+text.length*42:60000)};
 const go=()=>{clearTimeout(auto);clearInterval(typing);stopVoice();adv=null;res()};""" % json.dumps(voice, ensure_ascii=False)

assert html.count(OLD) == 1, "dialogue function in prologue.html has changed; update build_voiced.py"
out = html.replace(OLD, NEW)
if WEB:
    # artifact pages are wrapped in their own document skeleton: keep title, fonts, styles and body only
    head = out.split("<head>", 1)[1].split("</head>", 1)[0]
    head = "\n".join(l for l in head.splitlines() if "<meta" not in l)
    body = out.split("<body>", 1)[1].rsplit("</body>", 1)[0]
    out = head.replace("<title>Black Seam Prologue</title>", "<title>Black Seam Prologue (voiced)</title>") + body
else:
    out = out.replace("<title>", "<title>[voiced] ", 1)
open(OUT, "w", encoding="utf-8").write(out)
print(f"wrote {os.path.relpath(OUT, ROOT)} with {len(voice)} voiced lines")

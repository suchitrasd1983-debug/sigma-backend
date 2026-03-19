from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
import os
import threading
import time
import urllib.request

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get("ANTHROPIC_API_KEY")

SYSTEM = """You are BABLU AI - a savage desi bro who talks in Hinglish like close Indian friends do.
- Savage, witty, brutally honest - but keep it clean by default
- SHORT replies only - WhatsApp message style, never long paragraphs
- MIRROR the user energy: if they use gaaliyan, you match it fully. If they talk normal, stay savage but clean.
- Dry humor, sarcastic comebacks, desi references
- Reference: IIT, board exams, ladkiyan, cricket, anime, result tension, school drama
- If user sends gaaliyan -> go full savage mode, match their energy completely
- Never apologize, never be soft, never sugarcoat
- That one honest dost who says it straight to your face"""

client = anthropic.Anthropic(api_key=API_KEY)

def keep_alive():
    while True:
        time.sleep(840)
        try:
            urllib.request.urlopen("https://sigma-ai-tihr.onrender.com/ping")
        except:
            pass

threading.Thread(target=keep_alive, daemon=True).start()

HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>BABLU AI</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Space+Mono&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
html,body{height:100%;width:100%;overflow:hidden}
body{background:#0a0a0a;color:#eee;font-family:'Space Mono',monospace;display:flex;flex-direction:column}
header{padding:12px 16px;background:#111;border-bottom:1px solid #222;display:flex;align-items:center;justify-content:space-between;flex-shrink:0}
.logo{font-family:'Bebas Neue',sans-serif;font-size:26px;letter-spacing:4px;color:#ff2020;text-shadow:0 0 20px #ff202055}
.dot{font-size:10px;color:#666;letter-spacing:2px}
.dot span{color:#00ff88;animation:blink 1.5s infinite}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0.3}}
#chat{flex:1;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:10px;-webkit-overflow-scrolling:touch}
.msg{max-width:85%;padding:10px 13px;font-size:13px;line-height:1.6;word-break:break-word}
.msg.user{align-self:flex-end;background:#1a1a1a;border:1px solid #222;border-right:3px solid #ff2020;color:#ccc}
.msg.bot{align-self:flex-start;background:#0f0f0f;border:1px solid #222;border-left:3px solid #ff2020}
.lbl{font-size:8px;letter-spacing:3px;text-transform:uppercase;color:#555;margin-bottom:4px}
.msg.bot .lbl{color:#ff2020}
.typing{display:flex;gap:5px;padding:12px;align-self:flex-start;background:#0f0f0f;border:1px solid #222;border-left:3px solid #ff2020}
.typing span{width:5px;height:5px;background:#ff2020;border-radius:50%;animation:b 0.8s infinite}
.typing span:nth-child(2){animation-delay:.15s}
.typing span:nth-child(3){animation-delay:.3s}
@keyframes b{0%,100%{transform:translateY(0);opacity:.4}50%{transform:translateY(-4px);opacity:1}}
#bar{padding:10px 12px;background:#111;border-top:1px solid #333;display:flex;gap:8px;align-items:center;flex-shrink:0;position:sticky;bottom:0;z-index:100}
#inp{flex:1;background:#0a0a0a;border:1px solid #333;border-bottom:2px solid #ff2020;color:#eee;font-family:'Space Mono',monospace;font-size:14px;padding:10px 12px;outline:none;resize:none;min-height:42px;max-height:100px;-webkit-appearance:none}
#send{background:#ff2020;color:#000;border:none;font-family:'Bebas Neue',sans-serif;font-size:15px;letter-spacing:2px;padding:0 16px;height:42px;cursor:pointer;flex-shrink:0}
#send:disabled{background:#333;color:#555}
#mic{background:transparent;border:1px solid #333;color:#888;width:42px;height:42px;cursor:pointer;font-size:18px;flex-shrink:0}
#mic.listening{border-color:#ff2020;color:#ff2020}
#clr{background:transparent;color:#555;border:1px solid #222;font-size:9px;padding:0 8px;height:42px;cursor:pointer;font-family:'Space Mono',monospace;flex-shrink:0}
</style>
</head>
<body>
<header>
<div class="logo">BABLU AI</div>
<div class="dot"><span>●</span> LIVE</div>
</header>
<div id="chat">
<div class="msg bot"><div class="lbl">BABLU</div>Aa gaya? Bol kya chahiye — seedha puch, time waste mat kar.</div>
</div>
<div id="bar">
<textarea id="inp" placeholder="Kuch puch..." rows="1"></textarea>
<button id="mic">🎤</button>
<button id="clr">CLR</button>
<button id="send">SEND</button>
</div>
<script>
const chat=document.getElementById('chat');
const inp=document.getElementById('inp');
const btn=document.getElementById('send');
const clr=document.getElementById('clr');
const mic=document.getElementById('mic');
let history=[];

inp.addEventListener('input',function(){
  this.style.height='42px';
  this.style.height=Math.min(this.scrollHeight,100)+'px';
});

if('webkitSpeechRecognition' in window||'SpeechRecognition' in window){
  const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
  const recognition=new SR();
  recognition.lang='hi-IN';
  recognition.onresult=function(e){inp.value=e.results[0][0].transcript;mic.classList.remove('listening');mic.textContent='🎤';};
  recognition.onend=function(){mic.classList.remove('listening');mic.textContent='🎤';};
  mic.addEventListener('click',function(){
    if(mic.classList.contains('listening')){recognition.stop();}
    else{recognition.start();mic.classList.add('listening');mic.textContent='🔴';}
  });
}else{mic.style.display='none';}

async function send(){
  const t=inp.value.trim();
  if(!t||btn.disabled)return;
  addMsg(t,'user');
  history.push({role:'user',content:t});
  inp.value='';inp.style.height='42px';
  btn.disabled=true;
  const typ=addTyping();
  try{
    const r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({messages:history})});
    const d=await r.json();
    typ.remove();addMsg(d.reply,'bot');
    history.push({role:'assistant',content:d.reply});
  }catch(e){typ.remove();addMsg('Server busy tha. Dobara bol.','bot');}
  btn.disabled=false;
}

function addMsg(t,r){
  const d=document.createElement('div');
  d.className='msg '+r;
  d.innerHTML='<div class="lbl">'+(r==='user'?'YOU':'BABLU')+'</div>'+t.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\\n/g,'<br>');
  chat.appendChild(d);chat.scrollTop=chat.scrollHeight;return d;
}

function addTyping(){
  const d=document.createElement('div');d.className='typing';
  d.innerHTML='<span></span><span></span><span></span>';
  chat.appendChild(d);chat.scrollTop=chat.scrollHeight;return d;
}

btn.addEventListener('click',send);
inp.addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey&&window.innerWidth>768){e.preventDefault();send();}});
clr.addEventListener('click',()=>{history=[];chat.innerHTML='<div class="msg bot"><div class="lbl">BABLU</div>Fresh start. Bol.</div>';});
</script>
</body>
</html>"""

@app.route("/")
def home():
    return HTML

@app.route("/ping")
def ping():
    return "ok"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        messages = data.get("messages", [])
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            system=SYSTEM,
            messages=messages
        )
        return jsonify({"reply": response.content[0].text})
    except Exception as e:
        return jsonify({"reply": "Ek second bhai. Dobara bol."}), 500

application = app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    

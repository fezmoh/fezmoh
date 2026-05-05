from flask import Flask, render_template_string, request, jsonify
from groq import Groq
import os
import sqlite3

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def init_db():
    conn = sqlite3.connect("memory.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS memory
                 (id INTEGER PRIMARY KEY, role TEXT, content TEXT)''')
    conn.commit()
    conn.close()

def save_message(role, content):
    conn = sqlite3.connect("memory.db")
    c = conn.cursor()
    c.execute("INSERT INTO memory (role, content) VALUES (?, ?)", (role, content))
    conn.commit()
    conn.close()

def load_history():
    conn = sqlite3.connect("memory.db")
    c = conn.cursor()
    c.execute("SELECT role, content FROM memory ORDER BY id DESC LIMIT 20")
    rows = c.fetchall()
    conn.close()
    rows.reverse()
    return [{"role": r[0], "content": r[1]} for r in rows]

HTML = '''
<!DOCTYPE html>
<html>
<head>
<title>Fezmoh AI</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0a0a0a;color:#fff;font-family:Arial;display:flex;flex-direction:column;height:100vh}
#header{background:#1a1a2e;padding:15px;text-align:center;border-bottom:2px solid #6200ea}
#header h1{color:#6200ea;font-size:22px}
#header p{color:#aaa;font-size:11px}
#chat{flex:1;overflow-y:auto;padding:15px;display:flex;flex-direction:column;gap:12px}
.msg-user{background:#6200ea;padding:10px 15px;border-radius:18px 18px 4px 18px;max-width:78%;align-self:flex-end;font-size:14px}
.msg-bot{background:#1e1e1e;padding:10px 15px;border-radius:18px 18px 18px 4px;max-width:78%;align-self:flex-start;border:1px solid #333;font-size:14px}
.bot-label{color:#6200ea;font-weight:bold;font-size:11px;margin-bottom:4px}
#footer{background:#1a1a2e;padding:12px;display:flex;gap:8px;border-top:2px solid #6200ea;align-items:center}
#msg{flex:1;padding:12px 16px;background:#0d0d0d;color:#fff;border:1px solid #6200ea;border-radius:25px;outline:none;font-size:14px}
#send{padding:12px 20px;background:#6200ea;color:#fff;border:none;border-radius:25px;cursor:pointer;font-size:14px;font-weight:bold}
#send:hover{background:#7c00ff}
#clear{padding:10px 12px;background:#222;color:#aaa;border:1px solid #333;border-radius:25px;cursor:pointer;font-size:16px}
#clear:hover{background:#333}
.typing{color:#aaa;font-size:13px;font-style:italic}
</style>
</head>
<body>
<div id="header">
  <h1>🤖 🤖 Fezmoh AI</h1>
  <p>Your intelligent assistant • Always here for you</p>
</div>
<div id="chat">
  <div class="msg-bot"><div class="bot-label">Fezmoh</div>Hey! I am Fezmoh, your AI assistant. How can I help you today? 😊</div>
</div>
<div id="footer">
  <input id="msg" placeholder="Message Fezmoh..."/>
  <button id="clear" onclick="clearChat()" title="Clear chat">🗑</button>
  <button id="send" onclick="send()">Send</button>
</div>
<script>
let history=[];
async function send(){
  let msg=document.getElementById("msg").value.trim();
  if(!msg)return;
  let chat=document.getElementById("chat");
  chat.innerHTML+="<div class='msg-user'>"+msg+"</div>";
  document.getElementById("msg").value="";
  chat.innerHTML+="<div class='msg-bot typing' id='typing'><div class='bot-label'>Fezmoh</div>typing...</div>";
  chat.scrollTop=chat.scrollHeight;
  history.push({role:"user",content:msg});
  let res=await fetch("/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({history,message:msg})});
  let data=await res.json();
  history.push({role:"assistant",content:data.reply});
  document.getElementById("typing").remove();
  chat.innerHTML+="<div class='msg-bot'><div class='bot-label'>Fezmoh</div>"+data.reply+"</div>";
  chat.scrollTop=chat.scrollHeight;
}
function clearChat(){
  document.getElementById("chat").innerHTML="<div class='msg-bot'><div class='bot-label'>Fezmoh</div>Hey! I am Fezmoh, your AI assistant. How can I help you today? 😊</div>";
  history=[];
}
document.getElementById("msg").addEventListener("keypress",function(e){if(e.key=="Enter")send();});
</script>
</body>
</html>
'''

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message")
    history = load_history()
    save_message("user", message)
    history.append({"role": "user", "content": message})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": "You are Fezmoh, an incredible AI assistant. You are friendly, funny, smart, motivating and professional. Your creator is Austine Baraka but only mention this if someone asks."}] + history
    )
    reply = response.choices[0].message.content
    save_message("assistant", reply)
    return jsonify({"reply": reply})

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

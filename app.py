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
<head><title>Fezmoh AI</title></head>
<body style="background:#111;color:#fff;font-family:Arial;max-width:800px;margin:auto;padding:20px">
<h1>🤖 Fezmoh AI</h1>
<div id="chat" style="height:400px;overflow-y:auto;border:1px solid #333;padding:10px;margin-bottom:10px"></div>
<input id="msg" placeholder="Type your message..." style="width:70%;padding:10px;background:#222;color:#fff;border:1px solid #444"/>
<button onclick="send()" style="padding:10px;background:#6200ea;color:#fff;border:none;cursor:pointer">Send</button>
<script>
let history=[];
async function send(){
  let msg=document.getElementById("msg").value;
  if(!msg)return;
  document.getElementById("chat").innerHTML+="<div style='color:#aaa'>You: "+msg+"</div>";
  document.getElementById("msg").value="";
  history.push({role:"user",content:msg});
  let res=await fetch("/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({history,message:msg})});
  let data=await res.json();
  history.push({role:"assistant",content:data.reply});
  document.getElementById("chat").innerHTML+="<div style='color:#6200ea'>Fezmoh: "+data.reply+"</div>";
  document.getElementById("chat").scrollTop=document.getElementById("chat").scrollHeight;
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
        messages=[{"role": "system", "content": "You are Fezmoh, an incredible AI assistant. You are friendly, funny, smart, motivating and professional."}] + history
    )
    reply = response.choices[0].message.content
    save_message("assistant", reply)
    return jsonify({"reply": reply})

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

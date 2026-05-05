import os
from flask import Flask, request, jsonify, render_template_string
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

HTML = '''
<!DOCTYPE html>
<html>
<head><title>Fezmoh AI</title>
<style>
body{background:#0a0a0a;color:#fff;font-family:Arial;display:flex;flex-direction:column;align-items:center;padding:20px;}
h1{color:#00ff88;}
#chat{width:700px;height:400px;background:#111;border-radius:10px;padding:20px;overflow-y:auto;margin-bottom:10px;}
.user{color:#00ff88;margin:10px 0;}
.bot{color:#fff;margin:10px 0;}
input{width:600px;padding:10px;border-radius:5px;border:none;background:#222;color:#fff;}
button{padding:10px 20px;background:#00ff88;color:#000;border:none;border-radius:5px;cursor:pointer;font-weight:bold;}
</style></head>
<body>
<h1>🤖 Fezmoh AI</h1>
<div id="chat"></div>
<div><input id="msg" placeholder="Type your message..."/><button onclick="send()">Send</button></div>
<script>
let history=[];
async function send(){
  let msg=document.getElementById("msg").value;
  if(!msg)return;
  document.getElementById("chat").innerHTML+="<div class='user'>You: "+msg+"</div>";
  document.getElementById("msg").value="";
  let res=await fetch("/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:msg,history:history})});
  let data=await res.json();
  history.push({role:"user",content:msg});
  history.push({role:"assistant",content:data.reply});
  document.getElementById("chat").innerHTML+="<div class='bot'>Fezmoh: "+data.reply+"</div>";
  document.getElementById("chat").scrollTop=document.getElementById("chat").scrollHeight;
}
document.getElementById("msg").addEventListener("keypress",function(e){if(e.key==="Enter")send();});
</script>
</body></html>
'''

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    history = data.get("history", [])
    message = data.get("message", "")
    history.append({"role": "user", "content": message})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": "You are Fezmoh, an incredible AI assistant. You are friendly, funny, smart, motivating and professional. You were created by Austine Baraka."}] + history
    )
    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

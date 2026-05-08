from flask import Flask, jsonify, request
import hashlib
import time
app=Flask(__name__)
blockchain=[]
wallets={}
circulating=0
@app.route('/')
def home():
    return jsonify({"coin":"FEZMOH","symbol":"FZM","origin":"Kenya","status":"LIVE"})
@app.route('/rates')
def rates():
    return jsonify({"FZM/USD":0.005,"FZM/KES":0.65,"FZM/EUR":0.0046})
@app.route('/chain')
def chain():
    return jsonify({"chain":blockchain,"length":len(blockchain)})
if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000,debug=False)

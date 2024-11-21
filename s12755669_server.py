#server side flask application
import os, time
from flask import Flask, request, jsonify
import random

app = Flask(__name__)

#localhost and port:5000
HOST, PORT = "0.0.0.0", 5000

app = Flask(__name__)

#R4
def login(username, password):
    # username string must be digit
    if type(username) != str: return False
    if not(username.isdigit()): return False
    # password string must be username-pw
    if type(password) != str: return False
    if password != f"{username}-pw": return False
    return True
    
#Testing    
@app.get("/")
def index():
    return jsonify({"message": "Hello, World!"})

#R1
@app.post("/pi")
def pi():
    #login is required
    get_json = request.get_json()
    username = get_json.get("username")
    password = get_json.get("password")
    if not login(username, password):
        return jsonify({"error": "user info error"})
    #get request data
    simulations = get_json.get("simulations")
    concurrency = get_json.get("concurrency")
    #process part of the service
    start = time.time() #start execturion time
    pi = 3.14
    time.sleep(1)
    end = time.time() #end execturion time
    #send response
    return jsonify({"simulations": simulations, "concurrency": concurrency, "pi": pi, "execution_time": end-start})

#R2
@app.post("/legacy_pi")
def legacy_pi():
    #login is required
    get_json = request.get_json()
    username = get_json.get("username")
    password = get_json.get("password")
    if not login(username, password):
        return jsonify({"error": "user info error"})
    return jsonify({"message": "legacy_pi"})

#R3
@app.post("/statistics")
def statistics():
    #login is required
    get_json = request.get_json()
    username = get_json.get("username")
    password = get_json.get("password")
    if not login(username, password):
        return jsonify({"error": "user info error"})
    return jsonify({"message": "statistics"})

if __name__ == "__main__":
    app.run(host=HOST, port=PORT,debug=True)
    
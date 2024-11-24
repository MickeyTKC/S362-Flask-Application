#server side flask application
import os, time
from flask import Flask, request, jsonify
from random import random
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import socket
import regex as re

#config
app = Flask(__name__)
HOST, PORT = "0.0.0.0", 5000
app = Flask(__name__)
LEGACY_HOST, LEGACY_PORT = "localhost", 31416
#functions

#R4
def login(username, password):
    # username string must be digit
    if type(username) != str: return False
    if not(username.isdigit()): return False
    # password string must be username-pw
    if type(password) != str: return False
    if password != f"{username}-pw": return False
    return True

#R1 
def compute_count(simulations):
    count = 0
    for _ in range(simulations):
        x = random()
        y = random()
        if x * x + y * y < 1:
            count += 1
    return count

#R2
def compute_legacy_pi(protocol):
    global socket, LEGACY_HOST, LEGACY_PORT
    types = { "tcp":socket.SOCK_STREAM, "udp":socket.SOCK_DGRAM }
    with socket.socket(socket.AF_INET, types[protocol]) as s:
        # Connect the socket to the server's address and port
        print(f"Connecting to {LEGACY_HOST}:{LEGACY_PORT}, Type:{types[protocol]}")  # debug
        if protocol == "tcp":
            s.connect((LEGACY_HOST, LEGACY_PORT))
            s.sendall(b"")  # Using sendall for TCP
            response = s.recv(1024)  # Buffer size is 1024 bytes
        elif protocol == "udp":
            s.sendto(b"", (LEGACY_HOST, LEGACY_PORT))
            response, addr = s.recvfrom(1024)  # Use recvfrom for UDP
        return response.decode()
#R2
def tcp_legacy_pi(i):
    global socket, LEGACY_HOST, LEGACY_PORT    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Connect the socket to the server's address and port
        s.connect((LEGACY_HOST, LEGACY_PORT))
        s.sendall(b"")  # Using sendall for TCP
        response = s.recv(1024)  # Buffer size is 1024 bytes
    return response.decode()

#R2
def udp_legacy_pi(i):
    global socket, LEGACY_HOST, LEGACY_PORT
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # Connect the socket to the server's address and port
        s.sendto(b"", (LEGACY_HOST, LEGACY_PORT))
        response, addr = s.recvfrom(1024)  # Use recvfrom for UDP
    return response.decode()

#R2
def is_valid_pi(pi_string):
    # Regex to check if the string is a valid float representation
    return bool(re.match(r'^\d+(\.\d+)?$', pi_string))

#R2
def average_pi(results):
    valid_results = []
    print(f"{results=}")
    for result in results:
        print(f"{result=}")
        if is_valid_pi(result):
            valid_results.append(float(result))  # Convert valid strings to float
            
    valid_count = len(valid_results)
    average_pi = sum(valid_results) / valid_count if valid_count > 0 else 0
    
    return average_pi

#routing   
    
#testing flask server   
@app.get("/")
def index():
    return jsonify({"application": "PI Calculator"})

#R1
@app.post("/pi")
def pi():
    #login is required
    get_json = request.get_json()
    username = get_json.get("username")
    password = get_json.get("password")
    if not login(username, password):
        return jsonify({"error": "user info error"}), 401
    #get request data
    simulations = get_json.get("simulations")
    concurrency = get_json.get("concurrency")
    #invalid field handling
    if simulations < 100 or simulations > 100000000: return jsonify({"error": "invalid field simulations"}), 400
    if concurrency < 1 or concurrency > 8: return jsonify({"error": "invalid field concurrency"}), 400
    #process part of the service
    start = time.time() #start execturion time
    if concurrency > 1:
        with ProcessPoolExecutor(max_workers=concurrency) as executor:
            futures = [executor.submit(compute_count, simulations // concurrency) for _ in range(concurrency)]
            total_count = sum(future.result() for future in futures)
    else:
        total_count = compute_count(simulations)
    pi_estimate = total_count / simulations * 4
    end = time.time() #end execturion time
    #send response
    return jsonify({"simulations": simulations, "concurrency": concurrency, "pi": pi_estimate, "execution_time": end-start})

#R2
@app.post("/legacy_pi")
def legacy_pi():
    #login is required
    get_json = request.get_json()
    username = get_json.get("username")
    password = get_json.get("password")
    if not login(username, password):
        return jsonify({"error": "user info error"}), 401
    protocol = get_json.get("protocol")
    concurrency = get_json.get("concurrency")
    #invalid field handling
    if not isinstance(protocol, str) or (protocol != "tcp" and protocol != "udp"):
        return jsonify({"error": "invalid field protocol"}), 400
    if concurrency < 1 or concurrency > 8: return jsonify({"error": "invalid field concurrency"}), 400
    #process part of the service
    pi = 0
    start = time.time() #start execturion time
    if concurrency == 1:
        if protocol == "tcp": pi = tcp_legacy_pi(None)
        elif protocol == "udp": pi = udp_legacy_pi(None)
        if not is_valid_pi(pi): pi = 0
    else:
        with ProcessPoolExecutor(max_workers=concurrency) as executor:
            futures = []
            if protocol == "tcp": 
                result = list(executor.map(tcp_legacy_pi, range(concurrency)))
            elif protocol == "udp": 
                result = list(executor.map(udp_legacy_pi, range(concurrency)))
            pi = average_pi(result)
    end = time.time() #end execturion time
    return jsonify({"protocol": protocol, "concurrency": concurrency, "pi": pi, "execution_time": end-start})

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
    
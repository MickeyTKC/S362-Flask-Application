#server side flask application
import os, time, timeit
from flask import Flask, request, jsonify
from random import random
import threading
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import socket
import regex as re

#config
app = Flask(__name__)
HOST, PORT = "0.0.0.0", 5000
app = Flask(__name__)
LEGACY_HOST, LEGACY_PORT = "localhost", 31416
TEXT_FILE = 'request_statistics.txt' # Text file for storing request statistics in CSV format
lock = threading.Lock() # Create a lock for mutual exclusion
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

#R5
def init_file():
    if not os.path.exists(TEXT_FILE):
        with open(TEXT_FILE, mode='w') as file:
            file.write('username,request_count\n')  # Write the header

#R5
def update_request_statistics(username):
    with lock:
        # Read existing data
        records = []
        user_found = False
        
        with open(TEXT_FILE, mode='r') as file:
            next(file)  # Skip the header
            for line in file:
                row = line.strip().split(',')
                if row[0] == username:
                    user_found = True
                    row[1] = str(int(row[1]) + 1)  # Increment the count
                records.append(row)

        # If user not found, add a new record
        if not user_found:
            records.append([username, '1'])
        
        # Write updated records back to the text file
        with open(TEXT_FILE, mode='w') as file:
            file.write('username,request_count\n')  # Write the header
            for record in records:
                file.write(','.join(record) + '\n')  # Write all records

#R3
def get_request_statistics():
    with lock:  # Ensure mutual exclusion
        stats = []
        with open(TEXT_FILE, mode='r') as file:
            next(file)  # Skip header
            for line in file:
                row = line.strip().split(',')
                stats.append((row[0], int(row[1])))  # Convert count to int
        return stats

#routing   
    
#testing flask server   
@app.get("/")
def index():
    return jsonify({"application": "PI Calculator"})

#R1
@app.post("/pi")
def pi():
    #start execturion time
    start = timeit.default_timer()
    #login is required
    get_json = request.get_json()
    username = get_json.get("username")
    password = get_json.get("password")
    if not login(username, password):
        return jsonify({"error": "user info error"}), 401
    update_request_statistics(username)
    #get request data
    simulations = get_json.get("simulations")
    concurrency = get_json.get("concurrency") or 1
    #invalid field handling
    if simulations < 100 or simulations > 100000000: return jsonify({"error": "invalid field simulations"}), 400
    if type(concurrency) != int or concurrency < 1 or concurrency > 8: return jsonify({"error": "invalid field concurrency"}), 400
    #process part of the service
    if concurrency > 1:
        with ProcessPoolExecutor(max_workers=concurrency) as executor:
            futures = [executor.submit(compute_count, simulations // concurrency) for _ in range(concurrency)]
            total_count = sum(future.result() for future in futures)
    else:
        total_count = compute_count(simulations)
    pi_estimate = total_count / simulations * 4
    #end execturion time
    end = timeit.default_timer() 
    #send response
    return jsonify({"simulations": simulations, "concurrency": concurrency, "pi": float(pi_estimate), "execution_time": end-start})

#R2
@app.post("/legacy_pi")
def legacy_pi():
    #start execturion time
    start = timeit.default_timer()
    #login is required
    get_json = request.get_json()
    username = get_json.get("username")
    password = get_json.get("password")
    if not login(username, password):
        return jsonify({"error": "user info error"}), 401
    update_request_statistics(username)
    protocol = get_json.get("protocol")
    concurrency = get_json.get("concurrency") or 1
    #invalid field handling
    if not isinstance(protocol, str) or (protocol != "tcp" and protocol != "udp"):
        return jsonify({"error": "invalid field protocol"}), 400
    if type(concurrency) != int or concurrency < 1 or concurrency > 8: return jsonify({"error": "invalid field concurrency"}), 400
    #process part of the service
    pi = 0
    
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
    #end execturion time
    end = timeit.default_timer() 
    return jsonify({"protocol": protocol, "concurrency": concurrency, "pi": float(pi), "execution_time": end-start})

#R3
@app.post("/statistics")
def statistics():
    #login is required
    get_json = request.get_json()
    username = get_json.get("username")
    password = get_json.get("password")
    if not login(username, password):
        return jsonify({"error": "user info error"})
    #get statistics
    stats = get_request_statistics()
    list = []
    for username, count in stats:
        list.append({"username": username, "count": count})
    return jsonify(list)

if __name__ == "__main__":
    init_file()
    app.run(host=HOST, port=PORT,debug=True)
    
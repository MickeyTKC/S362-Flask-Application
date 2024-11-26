import os, subprocess
import json, requests

USERNAME, PASSWORD = "1111", "1111-pw"
SIMULATIONS = 100000
CONCURRENCY = 2
PROTOCAL = "tcp"

def r1():
    req = {"username":USERNAME, "password":PASSWORD, "simulations":SIMULATIONS, "concurrency":CONCURRENCY}
    res = requests.post("http://localhost:5000/pi", json=req)
    return res.json()

def r2():
    req = {"username":USERNAME, "password":PASSWORD, "protocol":PROTOCAL, "concurrency":CONCURRENCY}
    res = requests.post("http://localhost:5000/legacy_pi", json=req)
    return res.json()

def r3():
    req = {"username":USERNAME, "password":PASSWORD}
    res = requests.post("http://localhost:5000/statistics", json=req)
    return res.json()


if __name__ == "__main__":
    print(r2())
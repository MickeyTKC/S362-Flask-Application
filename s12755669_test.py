
import os, subprocess
import unittest, time
import json, requests


class TestFlask(unittest.TestCase):
    """
    def test_failed_login(self):
        req = {"username":1234, "password":"s1234-pw", "simulations":0, "concurrency":1}
        res = requests.post("http://localhost:5000/pi", json=req)
        print(res.json())
        self.assertEqual(res.status_code, 401)
        req = {"username":"s1234", "password":"s1234-pw", "simulations":0, "concurrency":1}
        res = requests.post("http://localhost:5000/pi", json=req)
        print(res.json())
        self.assertEqual(res.status_code, 401)
    """
    
    """
    def test_pi(self):
        #success
        req = {"username":"1234", "password":"1234-pw", "simulations":100, "concurrency":1}
        res = requests.post("http://localhost:5000/pi", json=req)
        print(res.json())
        self.assertEqual(res.status_code, 200)
        #success
        req = {"username":"1234", "password":"1234-pw", "simulations":100000000, "concurrency":8}
        res = requests.post("http://localhost:5000/pi", json=req)
        print(res.json())
        self.assertEqual(res.status_code, 200)
        #invlid simulations
        req = {"username":"1234", "password":"1234-pw", "simulations":0, "concurrency":8}
        res = requests.post("http://localhost:5000/pi", json=req)
        print(res.json())
        self.assertEqual(res.status_code, 400)
        #success concurrency
        req = {"username":"1234", "password":"1234-pw", "simulations":100000000, "concurrency":0}
        res = requests.post("http://localhost:5000/pi", json=req)
        print(res.json())
        self.assertEqual(res.status_code, 400)
    """
    def test_legacy_pi(self):
        #success tcp
        req = {"username":"1234", "password":"1234-pw", "protocol":"tcp", "concurrency":1}
        res = requests.post("http://localhost:5000/legacy_pi", json=req)
        print(res.json())
        self.assertEqual(res.status_code, 200)
        #success udp
        req = {"username":"1234", "password":"1234-pw", "protocol":"udp", "concurrency":1}
        res = requests.post("http://localhost:5000/legacy_pi", json=req)
        print(res.json())
        self.assertEqual(res.status_code, 200)
        #success tcp concurrency 8
        req = {"username":"1234", "password":"1234-pw", "protocol":"tcp", "concurrency":8}
        res = requests.post("http://localhost:5000/legacy_pi", json=req)
        print(res.json())
        self.assertEqual(res.status_code, 200)
        #success udp concurrency 8
        req = {"username":"1234", "password":"1234-pw", "protocol":"udp", "concurrency":8}
        res = requests.post("http://localhost:5000/legacy_pi", json=req)
        print(res.json())
        self.assertEqual(res.status_code, 200)

if __name__ == '__main__':
    unittest.main()
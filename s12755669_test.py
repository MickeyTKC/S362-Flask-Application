
import os, subprocess
import unittest, time
import json, requests


class TestFlask(unittest.TestCase):

    def test_userinfo_error(self):
        req = {"username":1111, "password":"s1111-pw", "simulations":0, "concurrency":1}
        res = requests.post("http://localhost:5000/pi", json=req)
        self.assertEqual(res.status_code, 401)
        req = {"username":"s1111", "password":"s1111-pw", "simulations":0, "concurrency":1}
        res = requests.post("http://localhost:5000/pi", json=req)
        self.assertEqual(res.status_code, 401)
    def test_invalid_simulations(self):
        pass
    def test_invalid_concurrency(self):
        pass
    def test_invalid_protocol(self):
        pass

    def test_legacy_pi(self):
        #success tcp
        req = {"username":"1111", "password":"1111-pw", "protocol":"tcp", "concurrency":1}
        res = requests.post("http://localhost:5000/legacy_pi", json=req)
        self.assertEqual(res.status_code, 200)
        #success udp
        req = {"username":"1111", "password":"1111-pw", "protocol":"udp", "concurrency":1}
        res = requests.post("http://localhost:5000/legacy_pi", json=req)
        self.assertEqual(res.status_code, 200)
        #success tcp concurrency 8
        req = {"username":"1111", "password":"1111-pw", "protocol":"tcp", "concurrency":8}
        res = requests.post("http://localhost:5000/legacy_pi", json=req)
        
        self.assertEqual(res.status_code, 200)
        #success udp concurrency 8
        req = {"username":"1111", "password":"1111-pw", "protocol":"udp", "concurrency":8}
        res = requests.post("http://localhost:5000/legacy_pi", json=req)
        
        self.assertEqual(res.status_code, 200)
        #failed protocol
        req = {"username":"1111", "password":"1111-pw", "protocol":"aaa", "concurrency":1}
        res = requests.post("http://localhost:5000/legacy_pi", json=req)
        
        self.assertEqual(res.status_code, 400)
        #failed protocol 2
        req = {"username":"1111", "password":"1111-pw", "protocol":0, "concurrency":1}
        res = requests.post("http://localhost:5000/legacy_pi", json=req)
        
        self.assertEqual(res.status_code, 400)
        #failed concurrency
        req = {"username":"1111", "password":"1111-pw", "protocol":"tcp", "concurrency":9}
        res = requests.post("http://localhost:5000/legacy_pi", json=req)
        
        self.assertEqual(res.status_code, 400)

    def test_pi(self):
        #success
        req = {"username":"2222", "password":"2222-pw", "simulations":100, "concurrency":1}
        res = requests.post("http://localhost:5000/pi", json=req)
        
        self.assertEqual(res.status_code, 200)
        #success
        req = {"username":"2222", "password":"2222-pw", "simulations":100000000, "concurrency":8}
        res = requests.post("http://localhost:5000/pi", json=req)
        
        self.assertEqual(res.status_code, 200)
        #invlid simulations
        req = {"username":"2222", "password":"2222-pw", "simulations":0, "concurrency":8}
        res = requests.post("http://localhost:5000/pi", json=req)
        
        self.assertEqual(res.status_code, 400)
        #success concurrency
        req = {"username":"2222", "password":"2222-pw", "simulations":100000000, "concurrency":0}
        res = requests.post("http://localhost:5000/pi", json=req)
        
        self.assertEqual(res.status_code, 400)
        
    def test_stats(self):
        req = {"username":"1111", "password":"1111-pw"}
        res = requests.post("http://localhost:5000/statistics", json=req)
        
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
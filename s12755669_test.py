
import os, subprocess
import unittest, time
import json, requests


class TestFlask(unittest.TestCase):
    
    def test_failed_login(self):
        req = {"username":1234, "password":"s1234-pw", "simulations":0, "concurrency":1}
        res = requests.post("http://localhost:5000/pi", json=req)
        print(res.json())
        self.assertEqual(res.status_code, 200)
        req = {"username":"s1234", "password":"s1234-pw", "simulations":0, "concurrency":1}
        res = requests.post("http://localhost:5000/pi", json=req)
        print(res.json())
        self.assertEqual(res.status_code, 200)

    def test_pi(self):
        req = {"username":"1234", "password":"1234-pw", "simulations":0, "concurrency":1}
        res = requests.post("http://localhost:5000/pi", json=req)
        print(res.json())
        #self.assertEqual(res.status_code, 200)

if __name__ == '__main__':
    unittest.main()
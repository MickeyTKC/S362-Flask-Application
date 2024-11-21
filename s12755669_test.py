
import os, subprocess
import unittest, time
import json, requests


class TestFlask(unittest.TestCase):

    def test_pi(self):
        #json req = {username:"1234", password:"1234-pw", simulations:0, concurrency, 1}
        req = {"username":"1234", "password":"1234-pw", "simulations":0, "concurrency":1}
        #send request to server
        res = requests.post("http://localhost:5000/pi", json=req)
        #check if response is correct
        print(res.json())
        self.assertEqual(res.status_code, 200)

if __name__ == '__main__':
    unittest.main()

import os, subprocess
import unittest, time
import json, requests


class TestFlask(unittest.TestCase):
    user1 = "1111"
    user2 = "2222"
    user_count = {"1111":0,"2222":0}

    def test_userinfo_error(self):
        #R1
        req = {"username":1111, "password":"s1111-pw", "simulations":0, "concurrency":1}
        res = requests.post("http://localhost:5000/pi", json=req)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.json()["error"], "user info error")
        req = {"username":"s1111", "password":"s1111-pw", "simulations":0, "concurrency":1}
        res = requests.post("http://localhost:5000/pi", json=req)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.json()["error"], "user info error")
        #R2
        req = {"username":1111, "password":"s1111-pw", "simulations":0, "concurrency":1}
        res = requests.post("http://localhost:5000/legacy_pi", json=req)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.json()["error"], "user info error")
        req = {"username":"s1111", "password":"s1111-pw", "simulations":0, "concurrency":1}
        res = requests.post("http://localhost:5000/legacy_pi", json=req)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.json()["error"], "user info error")
        #R3
        req = {"username":1111, "password":"s1111-pw"}
        res = requests.post("http://localhost:5000/statistics", json=req)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.json()["error"], "user info error")
        req = {"username":"s1111", "password":"s1111-pw"}
        res = requests.post("http://localhost:5000/statistics", json=req)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.json()["error"], "user info error")
        
    def test_invalid_simulations(self):
        #R1
        req = {"username":"2222", "password":"2222-pw", "simulations":0, "concurrency":8}
        res = requests.post("http://localhost:5000/pi", json=req)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()["error"], "invalid field simulations")
        req = {"username":"2222", "password":"2222-pw", "simulations":100000001, "concurrency":8}
        res = requests.post("http://localhost:5000/pi", json=req)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()["error"], "invalid field simulations")
        req = {"username":"2222", "password":"2222-pw", "simulations":100000.1, "concurrency":8}
        res = requests.post("http://localhost:5000/pi", json=req)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()["error"], "invalid field simulations")
        
    def test_missing_simulations(self):
        req = {"username":"2222", "password":"2222-pw", "concurrency":8}
        res = requests.post("http://localhost:5000/pi", json=req)
        self.assertEqual(res.status_code, 400)
        #err msg
        self.assertEqual(res.json()["error"], "missing field simulations")
    
    def test_invalid_concurrency(self):
        #R1
        req = {"username":"2222", "password":"2222-pw", "simulations":100000000, "concurrency":0}
        res = requests.post("http://localhost:5000/pi", json=req)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()["error"], "invalid field concurrency")
        req = {"username":"2222", "password":"2222-pw", "simulations":100000000, "concurrency":9}
        res = requests.post("http://localhost:5000/pi", json=req)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()["error"], "invalid field concurrency")
        req = {"username":"2222", "password":"2222-pw", "simulations":100000000, "concurrency":2.2}
        res = requests.post("http://localhost:5000/pi", json=req)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()["error"], "invalid field concurrency")
        #R2
        req = {"username":"1111", "password":"1111-pw", "protocol":"tcp", "concurrency":0}
        res = requests.post("http://localhost:5000/legacy_pi", json=req)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()["error"], "invalid field concurrency")
        req = {"username":"1111", "password":"1111-pw", "protocol":"tcp", "concurrency":9}
        res = requests.post("http://localhost:5000/legacy_pi", json=req)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()["error"], "invalid field concurrency")
        req = {"username":"2222", "password":"2222-pw", "protocol":"tcp", "concurrency":2.2}
        res = requests.post("http://localhost:5000/legacy_pi", json=req)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()["error"], "invalid field concurrency")
        
    def test_default_concurrency(self):
        req = {"username":self.user1, "password":"1111-pw", "simulations":100000000}
        res = requests.post("http://localhost:5000/pi", json=req)
        self.user_count[self.user1] += 1
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["concurrency"], 1)
        req = {"username":self.user1, "password":"1111-pw", "protocol":"tcp"}
        res = requests.post("http://localhost:5000/legacy_pi", json=req)
        self.user_count[self.user1] += 1
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["concurrency"], 1)
        
    def test_invalid_protocol(self):
        #R2
        req = {"username":self.user1, "password":"1111-pw", "protocol":"aaa", "concurrency":1}
        res = requests.post("http://localhost:5000/legacy_pi", json=req)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()["error"], "invalid field protocol")
        req = {"username":self.user1, "password":"1111-pw", "concurrency":1}
        res = requests.post("http://localhost:5000/legacy_pi", json=req)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()["error"], "invalid field protocol")

    def test_legacy_pi(self):
        #R2 TCP
        req = {"username":self.user1, "password":"1111-pw", "protocol":"tcp", "concurrency":1}
        res = requests.post("http://localhost:5000/legacy_pi", json=req)
        self.user_count[self.user1] += 1
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["concurrency"], 1)
        self.assertEqual(res.json()["protocol"], "tcp")
        self.assertIsInstance(res.json()["execution_time"], float)
        self.assertGreater(res.json()["execution_time"], 0)
        self.assertTrue(res.json()["pi"]==0 or(res.json()["pi"] >= 2 and res.json()["pi"] <= 4))
        req = {"username":self.user1, "password":"1111-pw", "protocol":"tcp", "concurrency":8}
        res = requests.post("http://localhost:5000/legacy_pi", json=req)
        self.user_count[self.user1] += 1
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["concurrency"], 8)
        self.assertEqual(res.json()["protocol"], "tcp")
        self.assertIsInstance(res.json()["execution_time"], float)
        self.assertGreater(res.json()["execution_time"], 0)
        self.assertTrue(res.json()["pi"]==0 or(res.json()["pi"] >= 3 and res.json()["pi"] <= 3.5))
        #R2 UDP
        req = {"username":self.user1, "password":"1111-pw", "protocol":"udp", "concurrency":1}
        res = requests.post("http://localhost:5000/legacy_pi", json=req)
        self.user_count[self.user1] += 1
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["concurrency"], 1)
        self.assertEqual(res.json()["protocol"], "udp")
        self.assertIsInstance(res.json()["execution_time"], float)
        self.assertGreater(res.json()["execution_time"], 0)
        self.assertTrue(res.json()["pi"]==0 or(res.json()["pi"] >= 2 and res.json()["pi"] <= 4))
        req = {"username":self.user1, "password":"1111-pw", "protocol":"udp", "concurrency":8}
        res = requests.post("http://localhost:5000/legacy_pi", json=req)
        self.user_count[self.user1] += 1
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["concurrency"], 8)
        self.assertEqual(res.json()["protocol"], "udp")
        self.assertIsInstance(res.json()["execution_time"], float)
        self.assertGreater(res.json()["execution_time"], 0)
        self.assertTrue(res.json()["pi"]==0 or(res.json()["pi"] >= 3 and res.json()["pi"] <= 3.5))

    def test_pi(self):
        #R1
        req = {"username":self.user2, "password":"2222-pw", "simulations":100, "concurrency":1}
        res = requests.post("http://localhost:5000/pi", json=req)
        self.user_count[self.user2] += 1
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["simulations"], 100)
        self.assertEqual(res.json()["concurrency"], 1)
        self.assertIsInstance(res.json()["execution_time"], float)
        self.assertGreater(res.json()["execution_time"], 0)
        self.assertTrue(res.json()["pi"]==0 or(res.json()["pi"] >= 2 and res.json()["pi"] <= 4))
        req = {"username":self.user2, "password":"2222-pw", "simulations":100000000, "concurrency":8}
        self.user_count[self.user2] += 1
        res = requests.post("http://localhost:5000/pi", json=req)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["simulations"], 100000000)
        self.assertEqual(res.json()["concurrency"], 8)
        self.assertIsInstance(res.json()["execution_time"], float)
        self.assertGreater(res.json()["execution_time"], 0)
        self.assertTrue(res.json()["pi"]==0 or(res.json()["pi"] >= 3 and res.json()["pi"] <= 3.5))
        
    def test_stats(self):
        req = {"username":"1111", "password":"1111-pw"}
        res = requests.post("http://localhost:5000/statistics", json=req)
        self.assertEqual(res.status_code, 200)
        #return list of username and request_count
        #username has "1111" and "2222"
        results = res.json()
        has_user1 = False
        has_user2 = False
        for result in results:
            self.assertIsInstance(result["request_count"], int)
            if(result["username"] == self.user1):
                has_user1 = True
                self.assertGreaterEqual(result["request_count"], self.user_count[self.user1])
            elif(result["username"] == self.user2):
                has_user2 = True
                self.assertGreaterEqual(result["request_count"], self.user_count[self.user2])
        self.assertTrue(has_user1 and has_user2)


if __name__ == '__main__':
    unittest.main()
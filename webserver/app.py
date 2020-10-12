from flask import Flask, flash, jsonify, render_template, request, session, redirect, url_for
import mysql.connector
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import datetime
import sys
import os
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import shutil
import json
import time
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin


time.sleep(25)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder='templates')

def connection():
    conn = mysql.connector.connect(host = "database",
                  user = 'root',
                  password = 'samplePassword',
                  database = 'db',
                  auth_plugin='caching_sha2_password')

    c = conn.cursor(buffered=True)
    return c , conn

def getBoard(cursor, conn):
    cursor.execute("SELECT challengeName, category, status, lastCheck, lastUp FROM challenges")
    data = cursor.fetchall()
    temp = []
    for row in data:
        row = list(row)
        if row[2]:
            row[2] = "Up"
        else:
            row[2] = "Down"
        row = tuple(row)
        temp.append(row)
    return temp

@app.route("/", methods=['GET'])
def home():
    c, conn = connection()
    data = getBoard(c, conn)
    print(data, flush=True)
    return render_template("index.html", data=data)

@app.after_request
def gnu_terry_pratchett(resp):
  resp.headers.add("X-Clacks-Overhead", "GNU Terry Pratchett")
  return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

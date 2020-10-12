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



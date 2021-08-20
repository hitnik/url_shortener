import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from flask import Flask


app = Flask(__name__)

from app import routes


import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from flask import Flask



app = Flask(__name__)

from db import DB_PATH, init_app

app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, DB_PATH),
    )
init_app(app)

from app import routes


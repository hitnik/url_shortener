import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from flask import Flask

from config import DB_PATH


def create_app(test_config=None):
    
    app = Flask(__name__)

    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_mapping(
                SECRET_KEY=os.environ.get("SECRET_KEY", "foo"),
                DATABASE=DB_PATH,
            ) 

    from db import init_app

    init_app(app)


    from app import routes

    app.register_blueprint(routes.bp)

    app.register_error_handler(400, routes.bad_request)
    app.register_error_handler(404, routes.page_not_found)

    return app


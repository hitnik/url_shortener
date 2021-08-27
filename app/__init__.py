import os
import sys

from flask import Flask
from flask_migrate import Migrate, migrate
from flask_sqlalchemy import SQLAlchemy

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

db = SQLAlchemy()
migrate = Migrate()

from config import BASEDIR, DB_PATH


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config:
        app.config.from_mapping(test_config)
    else:
        db_type = os.environ.get('DATABASE', 'sqlite')
        if db_type == 'postgres':
            user = os.environ["POSTGRES_USER"]
            pswd = os.environ["POSTGRES_PASSWORD"]
            host = os.environ['PG_HOST']
            port = os.environ.get('PG_PORT', 5432)
            pg_db = os.environ['POSTGRES_DB']
            db_uri = f'postgresql://{user}:{pswd}@{host}:{port}/{pg_db}'
        else:
            db_uri = 'sqlite:///' + DB_PATH
        app.config.from_mapping(
                SECRET_KEY=os.environ.get("SECRET_KEY", "foo"),
                SQLALCHEMY_DATABASE_URI=db_uri,
            )
    app.config.update(SQLALCHEMY_TRACK_MODIFICATIONS=False)

    db.init_app(app)
    migrate.init_app(app, db, directory=os.path.join(BASEDIR, 'migrations'))

    from app import models, routes

    app.register_blueprint(routes.bp)

    app.register_error_handler(400, routes.bad_request)
    app.register_error_handler(404, routes.page_not_found)

    return app

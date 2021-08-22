import os
import tempfile

import pytest
from app.db import init_db
from app.utils import parser
from app import app as create_app
import shutil
from flask import template_rendered

@pytest.fixture
def db_path():
    db_path = os.path.join(tempfile.mkdtemp(), 'db1.sqlite3')
    try:
        yield db_path
    finally:
        try:
            shutil.rmtree(db_path)
        except IOError:
            pass

@pytest.fixture
def db_mock(db_path):
    return init_db(db_path)


@pytest.fixture
def argparser():
    return parser()


@pytest.fixture
def app(db_path):
    create_app.config.from_mapping(
        SERVER_NAME = 'localhost.localdomain',
        TESTING = True,
        DATABASE = db_path,
    )
    app = create_app
    with app.app_context():
        init_db(db_path)
    return app

@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)
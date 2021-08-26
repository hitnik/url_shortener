import os
import shutil
import tempfile

import pytest
from app import create_app
from app.db_utils import init_db
from app.utils import parser
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
    app = create_app({
                        'SERVER_NAME':'localhost.localdomain',
                        'TESTING': True,
                        'DATABASE': db_path,
                        'SECRET_KEY': 'test'
                        })
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


def pytest_addoption(parser):
    parser.addoption("--docker", action="store_true", default=False,
                     help="run docker tests")


@pytest.fixture(scope='session')
def skip_docker(request):
    return not request.config.option.docker

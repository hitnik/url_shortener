import os
import shutil
import tempfile

import pytest
from flask import template_rendered
from flask_migrate import upgrade

from app import create_app, db
from app.models import LongUrls, ShortUrls


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
def app(db_path):
    app = create_app({
                        'SERVER_NAME': 'localhost.localdomain',
                        'TESTING': True,
                        'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + db_path,
                        'SECRET_KEY': 'test'
                        })
    with app.app_context():
        upgrade()
        l1 = LongUrls(long_url='https://www.google.com/')
        l2 = LongUrls(long_url='https://www.youtube.com')
        sh1 = ShortUrls(short='goo.gl', long=l1)
        sh2 = ShortUrls(short='yu.tu', long=l2)
        db.session.add_all((l1, l2, sh1, sh2))
        db.session.commit()
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

import os
import tempfile
import pytest
from app.db import init_db
from app.utils import parser


@pytest.fixture
def db_path():
    db_path = os.path.join(tempfile.mkdtemp(), 'db1.sqlite3')
    return db_path


@pytest.fixture
def db_mock(db_path):
    return init_db(db_path)

@pytest.fixture
def argparser():
    return parser()

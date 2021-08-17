import os
import tempfile
import pytest



@pytest.fixture
def db_path():
    db_path = os.path.join(tempfile.mkdtemp(),'db.sqlite3')
    return db_path


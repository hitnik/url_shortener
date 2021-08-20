from app.db import (
  init_db, close_db, get_db, insert_long_url, insert_short_url,
  long_url_exist, get_short_url, short_url_exist, get_long_url_from_db,
  get_short_url_by_long
  )
from unittest import mock
from contextlib import contextmanager
import sqlite3
import pytest

script = """
INSERT INTO long_urls (id, long_url)
VALUES
  (1, 'https://www.google.com/'),
  (2, 'https://www.youtube.com');
INSERT INTO short_urls (id, long_id, short)
VALUES
  (1, 1, 'goo.gl'),
  (2, 2, 'yu.tu');
"""


@contextmanager
def manager_mock(db_mock, init_db, db_manager):
    with mock.patch(init_db) as get_db:
        get_db.return_value = db_mock
        with mock.patch(db_manager) as manager:
            manager.return_value = db_mock
            yield lambda: manager


def test_init_db(db_path):
    db = init_db(db_path)
    db.executescript(script)
    cur = db.cursor()
    sql = 'SELECT * FROM short_urls WHERE long_id = ? AND id = ?;'
    value_1 = cur.execute(sql, (1, 1)).fetchone()
    assert value_1 is not None
    assert value_1[2] == 'goo.gl'
    cur.close()
    close_db(db)


def test_get_db(db_path, app):
    init_db(db_path=db_path)
    with mock.patch('app.db.DB_PATH', db_path):
        db = get_db()
        db.executescript(script)
        cur = db.cursor()
        sql = 'SELECT * FROM short_urls WHERE long_id = ? AND id = ?;'
        value_1 = cur.execute(sql, (1, 1)).fetchone()
        assert value_1 is not None
        assert value_1[2] == 'goo.gl'
        close_db(db)
        with app.app_context():
            db = get_db()
            db.execute('SELECT 1')


def test_close_db(db_path, app):
    init_db(db_path=db_path)
    with mock.patch('app.db.DB_PATH', db_path):
        with app.app_context():
            db = get_db()
            db.execute('SELECT 1')
        
        with pytest.raises(sqlite3.ProgrammingError) as e:
            db.execute('SELECT 1')
        db = get_db()
        close_db(db)
        with pytest.raises(sqlite3.ProgrammingError) as e:
            db.execute('SELECT 1')


def test_long_url_exist(db_mock):
    db_mock.executescript(script)
    with manager_mock(db_mock, 'app.db.get_db', 'app.db.db_manager'):
        assert long_url_exist('') is False
        assert long_url_exist('https://www.youtube.com') is True


def test_insert(db_mock):
    with manager_mock(db_mock, 'app.db.get_db', 'app.db.db_manager'):
        assert insert_long_url('www.test.ru') == 1
        assert insert_short_url('short.ru/a23', 1) == 1


def test_get_short_url(db_mock):
    db_mock.executescript(script)
    with manager_mock(db_mock, 'app.db.get_db', 'app.db.db_manager'):
        assert type(get_short_url('goo.gl')) == tuple
        assert get_short_url('goo.gl')[0] == 1


def test_short_url_exist(db_mock):
    db_mock.executescript(script)
    with manager_mock(db_mock, 'app.db.get_db', 'app.db.db_manager'):
        assert short_url_exist('') is False
        assert short_url_exist('goo.gl') is True


def test_get_long_url(db_mock):
    db_mock.executescript(script)
    with manager_mock(db_mock, 'app.db.get_db', 'app.db.db_manager'):
        assert get_long_url_from_db() is None
        assert type(get_long_url_from_db(id=1)) == tuple
        assert get_long_url_from_db(id=1)[0] == 1
        assert type(get_long_url_from_db(
            url='https://www.google.com/')) == tuple
        assert get_long_url_from_db(url='https://www.google.com/')[0] == 1


def test_get_short_by_long(db_mock):
    db_mock.executescript(script)
    with manager_mock(db_mock, 'app.db.get_db', 'app.db.db_manager'):
        assert type(get_short_url_by_long(1)) == tuple
        assert get_short_url_by_long(2)[0] == 2
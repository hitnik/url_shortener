from app.db import (
  init_db, close_db, get_db, insert_long_url, insert_short_url,
  long_url_exist, get_short_url, short_url_exist, get_long_url
  )
from unittest import mock

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


def test_get_db(db_path):
    init_db(db_path=db_path)
    with mock.patch('app.db.DB_PATH', db_path):
        db = get_db()
        db.executescript(script)
        cur = db.cursor()
        sql = 'SELECT * FROM short_urls WHERE long_id = ? AND id = ?;'
        value_1 = cur.execute(sql, (1, 1)).fetchone()
        assert value_1 is not None
        assert value_1[2] == 'goo.gl'
        cur.close()
        close_db(db)


def test_long_url_exist(db_mock):
    db_mock.executescript(script)
    with mock.patch('app.db.get_db') as get_db:
        get_db.return_value = db_mock
        with mock.patch('app.db.db_manager') as manager:
            manager.return_value = db_mock
            assert long_url_exist('') is False
            assert long_url_exist('https://www.youtube.com') is True


def test_insert(db_mock):
    with mock.patch('app.db.get_db') as get_db:
        get_db.return_value = db_mock
        with mock.patch('app.db.db_manager') as manager:
            manager.return_value = db_mock
            assert insert_long_url('www.test.ru') == 1
            assert insert_short_url('short.ru/a23', 1) == 1


def test_get_short_url(db_mock):
    with mock.patch('app.db.get_db') as get_db:
        get_db.return_value = db_mock
        with mock.patch('app.db.db_manager') as manager:
            manager.return_value = db_mock
            db_mock.executescript(script)
            assert type(get_short_url('goo.gl')) == tuple
            assert get_short_url('goo.gl')[0] == 1


def test_short_url_exist(db_mock):
    db_mock.executescript(script)
    with mock.patch('app.db.get_db') as get_db:
        get_db.return_value = db_mock
        with mock.patch('app.db.db_manager') as manager:
            manager.return_value = db_mock
            assert short_url_exist('') is False
            assert short_url_exist('goo.gl') is True

def test_get_long_url(db_mock):
    with mock.patch('app.db.get_db') as get_db:
        get_db.return_value = db_mock
        with mock.patch('app.db.db_manager') as manager:
            manager.return_value = db_mock
            db_mock.executescript(script)
            assert type(get_long_url(1)) == tuple
            assert get_long_url(1)[0] == 1
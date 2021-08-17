from app.db import init_db, close_db, get_db
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
    value_1 = cur.execute('SELECT * FROM short_urls WHERE long_id = ? AND id = ?;', (1,1)
      ).fetchone()
    assert value_1 != None  
    assert value_1[2] == 'goo.gl'
    cur.close()
    close_db(db)

def test_get_db(db_path):
    init_db(db_path=db_path)
    with mock.patch('app.db.DB_PATH', db_path) as path:
        db = get_db()
        db.executescript(script)
        cur = db.cursor()
        value_1 = cur.execute('SELECT * FROM short_urls WHERE long_id = ? AND id = ?;', (1,1)
          ).fetchone()
        assert value_1 != None  
        assert value_1[2] == 'goo.gl'
        cur.close()
        close_db(db)


import sqlite3
import os
from contextlib import contextmanager

BASEDIR = os.path.dirname(__file__)

DB_PATH = os.path.join(BASEDIR, 'db.sqlite3')


def init_db(db_path):
    """init sqlite database, create sqlite file if needed

    Args:
        db_path (str): sqlite db path
    Returns:
        sqlite3.Connection: sqlite3 connection
    """
    db = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    with open(os.path.join(BASEDIR, 'schema.sql'), 'rb') as file:
        db.executescript(file.read().decode('utf8'))
    return db


def get_db():
    """returns sqlite3 connection

    Returns:
        sqlite3.Connection
    """
    db = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    return db


def close_db(db):
    """ close sqlite3.Connection

    Args:
        db (sqlite3.Connection)
    """
    if db is not None:
        db.close()


@contextmanager
def db_manager():
    db = get_db()
    try:
        yield db
    finally:
        close_db(db)


@contextmanager
def cur_manager(db):
    cur = db.cursor()
    try:
        yield cur
    finally:
        cur.close()


def long_url_exist(url):
    """ checks if row with long_rurl = url exists

    Args:
        url (str): url to check

    Returns:
        [bool]: returns True when exists
    """
    with db_manager() as db:
        cur = db.cursor()
        exist = cur.execute(f"""SELECT EXISTS(SELECT * FROM long_urls
                                WHERE long_url = '{url}')"""
                            ).fetchone()
    if exist[0] > 0:
        return True
    return False


def insert_long_url(url):
    """ insert long_url to long_urls table

    Args:
        url (str): url to insert into table

    Returns:
        int or None: returns id of row
        or if IntegrityError raised then returns None
    """
    sql = "INSERT INTO long_urls(long_url) VALUES(?);"
    with db_manager() as db:
        cur = db.cursor()
        try:
            cur.execute(sql, (url,))
        except sqlite3.IntegrityError:
            return None
        db.commit()
        return cur.lastrowid


def insert_short_url(url, long_id):
    """insert short_url to short_urls table
    Args:
        url (str): short url
        long_id (int): Foreign key id

    Returns:
        int or None: returns id of row
        or if IntegrityError raised then returns None
    """
    sql = "INSERT INTO short_urls(long_id, short) VALUES(?, ?);"
    with db_manager() as db:
        cur = db.cursor()
        try:
            -cur.execute(sql, (long_id, url))
        except sqlite3.IntegrityError:
            return None
        db.commit()
        return cur.lastrowid

def get_short_url(url_long):
    pass


if __name__ == '__main__':
    db = init_db(DB_PATH)
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
    db.executescript(script)
    close_db(db)
    long_id = insert_long_url('https://www.tut.by')
    print(insert_short_url('http://ex.com/asd', long_id))
    print(insert_short_url('http://ex.com/asd', long_id))

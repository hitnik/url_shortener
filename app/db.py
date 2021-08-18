import sqlite3
import os

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

def long_url_exist(url, db):
    """ checks if row with long_rurl = url exists

    Args:
        url (str): url to check
        db (sqlite3.Connection): db connection

    Returns:
        [bool]: returns True when exists
    """
    cur = db.cursor()
    exist = cur.execute(f"SELECT EXISTS(SELECT * FROM long_urls WHERE long_url = '{url}')"
        ).fetchone()
    if exist[0] > 0:
        return True
    return False


def insert_long_url(url):
    pass

def insert_short_url(url, long_url):
    pass

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
    print(long_url_exist('https://www.google.com/', db))

import sqlite3
import os
from contextlib import contextmanager
from flask import g, current_app
from config import DB_PATH, BASEDIR
from flask.cli import with_appcontext
import click


def init_db(db_path=DB_PATH):
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
    try:
        current_app
        if 'db' not in g:
            g.db = db
            g.db.row_factory = sqlite3.Row
            return g.db
    except RuntimeError:
        pass
    finally:
        return db


def close_db(db=None):
    """ close sqlite3.Connection

    Args:
        db (sqlite3.Connection)
    """
    if db is None:
        try:
            current_app
            db = g.pop('db', None)
        except RuntimeError:
            pass
    if db is not None:
        try:
            db.close()
        except AttributeError:
            pass


@contextmanager
def db_manager():
    db = get_db()
    try:
        yield db
    finally:
        close_db(db)


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
            cur.execute(sql, (long_id, url))
        except sqlite3.IntegrityError:
            return None
        db.commit()
        return cur.lastrowid


def short_url_exist(url):
    """ checks if row with short = url exists

    Args:
        url (str): url to check

    Returns:
        [bool]: returns True when exists
    """
    sql = "SELECT EXISTS(SELECT * FROM short_urls WHERE short = ?);"
    with db_manager() as db:
        cur = db.cursor()
        exist = cur.execute(sql, (url,)).fetchone()
    if exist[0] > 0:
        return True
    return False


def get_short_url(short):
    """ get short_url instance by url

    Args:
        short (str): short_url

    Returns:
        [tuple]: short_url instance
    """
    sql = "SELECT * FROM short_urls WHERE short = ?;"
    with db_manager() as db:
        cur = db.cursor()
        short = cur.execute(sql, (short,)).fetchone()
    return short


def get_short_url_by_long(long_id):
    """ get short_url instance by long id

    Args:
        long_id (int): long id

    Returns:
        [tuple]: short_url instance
    """
    sql = "SELECT * FROM short_urls WHERE long_id = ?;"
    with db_manager() as db:
        cur = db.cursor()
        short = cur.execute(sql, (long_id,)).fetchone()
    return short


def get_long_url_from_db(id=None, url=None):
    """ get long_url instance by id

    Args:
        id (int): long_url id

    Returns:
        [tuple]: long_url instance
    """

    sql_id = "SELECT * FROM long_urls WHERE id = ?;"
    sql_url = "SELECT * FROM long_urls WHERE long_url = ?;"
    instance = None
    with db_manager() as db:
        cur = db.cursor()
        if id and not url:
            instance = cur.execute(sql_id, (id,)).fetchone()
        elif url and not id:
            instance = cur.execute(sql_url, (url,)).fetchone()
    return instance


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

if __name__ == '__main__':
    db = init_db(DB_PATH)

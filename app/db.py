import sqlite3
import os

BASEDIR = os.path.dirname(__file__)

DB_PATH = os.path.join(BASEDIR, 'db.sqlite3')

def init_db(db_path):
    db = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    with open(os.path.join(BASEDIR, 'schema.sql'), 'rb') as file:
        db.executescript(file.read().decode('utf8'))
    return db

def get_db():
    db = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    return db

def close_db(db):
    if db is not None:
        db.close()

if __name__ == '__main__':
    init_db(DB_PATH)
    

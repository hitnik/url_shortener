import os

BASEDIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASEDIR, 'db.sqlite3')

SCHEME = os.environ.get("API_SCHEME", "http")
NETLOC = os.environ.get("API_NETLOC", "ex.com")


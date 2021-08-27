from app import db
from app.models import LongUrls, ShortUrls


def long_url_exist(url):
    """ checks if row with long_rurl = url exists"""
    query = LongUrls.query.filter(LongUrls.long_url == url).exists()
    return db.session.query(query).scalar()


def insert_long_url(url):
    """ insert long_url to long_urls table """
    long_inst = LongUrls(long_url=url)
    db.session.add(long_inst)
    db.session.commit()
    return long_inst


def insert_short_url(url, long_inst):
    """insert short_url to short_urls table"""
    sh = ShortUrls(short=url, long=long_inst)
    db.session.add(sh)
    db.session.commit()
    return sh


def short_url_exist(url):
    """ checks if row with short = url exists  """
    query = ShortUrls.query.filter(ShortUrls.short == url).exists()
    return db.session.query(query).scalar()


def get_short_url(short):
    """ get short_url instance by url"""
    return ShortUrls.query.filter_by(short=short).first()


def get_short_url_by_long(long_inst):
    """ get short_url instance by long id"""
    return ShortUrls.query.filter_by(long=long_inst).first()


def get_long_url_from_db(url):
    """ get long_url instance by id"""
    return LongUrls.query.filter_by(long_url=url).first()

from app.db_utils import (get_short_url, insert_long_url, insert_short_url,
                          long_url_exist, short_url_exist)
from app.models import LongUrls, ShortUrls


def test_long_url_exist(app):
    with app.app_context():
        assert long_url_exist('') is False
        assert long_url_exist('https://www.youtube.com') is True


def test_insert_long(app):
    with app.app_context():
        long_inst = insert_long_url('www.test.ru')
        assert isinstance(long_inst, LongUrls)
        assert long_inst.long_url == 'www.test.ru'


def test_insert_short(app):
    with app.app_context():
        long_inst = LongUrls.query.filter_by(id=1).first()
        sh = insert_short_url('123', long_inst)
        assert isinstance(sh, ShortUrls)
        assert sh.long.id == 1


def test_short_url_exist(app):
    with app.app_context():
        assert short_url_exist('') is False
        assert short_url_exist('goo.gl') is True


def test_get_short_url(app):
    with app.app_context():
        sh = get_short_url('goo.gl')
        assert isinstance(sh, ShortUrls)
        assert sh.id == 1


def test_get_short_by_long(app):
    with app.app_context():
        long_inst = LongUrls.query.first()
        sh = ShortUrls.query.filter_by(long=long_inst).first()
        assert isinstance(sh, ShortUrls)
        assert sh.id == 1


def test_get_long_url(app):
    with app.app_context():
        long_inst = LongUrls.query.filter_by(
            long_url='https://www.google.com/').first()
        assert isinstance(long_inst, LongUrls)
        assert long_inst.id == 1

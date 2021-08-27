from urllib.parse import urlunsplit
import pytest

from app.config import NETLOC, SCHEME
from app.utils import Shortener, URLExistsError, URLNotFoundError


def build_url(path):
    return urlunsplit((SCHEME, NETLOC, path, '', ''))


def test_get_long_url(app):
    with app.app_context():
        with pytest.raises(URLNotFoundError):
            Shortener.get_long_url('raise')
        short = Shortener.get_long_url('goo.gl')
        assert isinstance(short, str)
        assert short == 'https://www.google.com/'


def test_get_short_url(app):
    with app.app_context():
        inst = Shortener.gen_short_url('https://www.google.com/')
        assert isinstance(inst, str)
        assert inst == urlunsplit((SCHEME, NETLOC, 'goo.gl', '', ''))
        inst = Shortener.gen_short_url('http://www.onliner.by')
        assert isinstance(inst, str)


def test_save_url(app):
    with app.app_context():
        with pytest.raises(URLExistsError):
            Shortener.save_url('goo.gl', 'https://www.google.com/')
        short = Shortener.save_url('onl', 'http://www.onliner.by')
        assert short == build_url('onl')
        assert Shortener.get_long_url(
            build_url('onl')) == 'http://www.onliner.by'

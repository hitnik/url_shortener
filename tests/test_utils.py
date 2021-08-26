from urllib.parse import urlunsplit

import pytest
from app.config import NETLOC, SCHEME
from app.utils import Shortener, URLExistsError, URLNotFoundError

from tests.test_db import manager_mock, script

def build_url(path):
    return urlunsplit((SCHEME, NETLOC, path, '', ''))

def test_get_long_url(db_mock):
    db_mock.executescript(script)
    with manager_mock(db_mock, 'db_utils.get_db', 'db_utils.db_manager'):
        with pytest.raises(URLNotFoundError):
            Shortener.get_long_url('raise')
        inst = Shortener.get_long_url('goo.gl')
        assert isinstance(inst, str)
        assert inst == 'https://www.google.com/'


def test_get_short_url(db_mock):
    db_mock.executescript(script)
    with manager_mock(db_mock, 'db_utils.get_db', 'db_utils.db_manager'):
        inst = Shortener.gen_short_url('https://www.google.com/')
        assert isinstance(inst, str)
        assert inst == urlunsplit((SCHEME, NETLOC, 'goo.gl', '', ''))
        inst = Shortener.gen_short_url('http://www.onliner.by')
        assert isinstance(inst, str)


def test_save_url(db_mock):
    db_mock.executescript(script)
    with manager_mock(db_mock, 'db_utils.get_db', 'db_utils.db_manager'):
        with pytest.raises(URLExistsError):
            Shortener.save_url('goo.gl', 'https://www.google.com/')
        short = Shortener.save_url('onl', 'http://www.onliner.by')
        assert short == build_url('onl')
        assert Shortener.get_long_url(
            build_url('onl')) == 'http://www.onliner.by'

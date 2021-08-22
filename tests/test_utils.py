from app.utils import Shortener, URLNotFoundError, URLExistsError
from tests.test_db import script, manager_mock
import pytest
from urllib.parse import urlunsplit
from app.config import NETLOC, SCHEME


def test_get_long_url(db_mock):
    db_mock.executescript(script)
    with manager_mock(db_mock, 'db.get_db', 'db.db_manager'):
        with pytest.raises(URLNotFoundError):
            Shortener.get_long_url('raise')
        inst = Shortener.get_long_url('goo.gl')
        assert type(inst) is str
        assert inst == 'https://www.google.com/'


def test_get_short_url(db_mock):
    db_mock.executescript(script)
    with manager_mock(db_mock, 'db.get_db', 'db.db_manager'):
        inst = Shortener.gen_short_url('https://www.google.com/')
        assert type(inst) is str
        assert inst == urlunsplit((SCHEME, NETLOC, 'goo.gl', '', ''))
        inst = Shortener.gen_short_url('http://www.onliner.by')
        assert type(inst) is str


def test_save_url(db_mock):
    db_mock.executescript(script)
    with manager_mock(db_mock, 'db.get_db', 'db.db_manager'):
        with pytest.raises(URLExistsError):
            Shortener.save_url('goo.gl', 'https://www.google.com/')
        short = Shortener.save_url('on.by/ptrer', 'http://www.onliner.by')
        assert short == 'on.by/ptrer'
        assert Shortener.get_long_url('on.by/ptrer') == 'http://www.onliner.by'

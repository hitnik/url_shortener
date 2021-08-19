from os import name
from urllib.parse import urlencode
from app.utils import Shortener
from tests.test_db import script, manager_mock
import pytest
from unittest import mock


def  test_get_long_url(db_mock):
    db_mock.executescript(script)
    with manager_mock(db_mock, 'db.get_db', 'db.db_manager'):
        with pytest.raises(Exception, match=r".* URL does .*"):
            Shortener.get_long_url('raise')
        inst = Shortener.get_long_url('goo.gl')
        assert type(inst) is str
        assert inst == 'https://www.google.com/'

def test_get_long_url(db_mock):
    db_mock.executescript(script)
    with manager_mock(db_mock, 'db.get_db', 'db.db_manager'):
        inst = Shortener.gen_short_url('https://www.google.com/')
        assert type(inst) is str
        assert inst == 'goo.gl'
        inst = Shortener.gen_short_url('http://www.onliner.by')
        assert type(inst) is str

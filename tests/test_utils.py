from app.utils import Shortener
from tests.test_db import script
import pytest
from unittest import mock


def  test_get_long_url(db_mock):
    db_mock.executescript(script)
    with mock.patch('db.get_db') as get_db:
        get_db.return_value = db_mock
        with mock.patch('db.db_manager') as manager:
            manager.return_value = db_mock
            with pytest.raises(Exception, match=r".* URL does .*"):
                Shortener.get_long_url('raise')
            inst = Shortener.get_long_url('goo.gl')
            assert type(inst) is str
            assert inst == 'https://www.google.com/'

def test_get_long_url(db_mock):
    db_mock.executescript(script)
    with mock.patch('db.get_db') as get_db:
        get_db.return_value = db_mock
        with mock.patch('db.db_manager') as manager:
            manager.return_value = db_mock
            inst = Shortener.gen_short_url('https://www.google.com/')
            assert type(inst) is str
            assert inst == 'goo.gl'

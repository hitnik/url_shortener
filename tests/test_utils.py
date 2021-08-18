from app.utils import get_long_url
from tests.test_db import script
import pytest
from unittest import mock


def  test_get_long_url(db_mock):
    db_mock.executescript(script)
    with mock.patch('app.db.get_db') as get_db:
        get_db.return_value = db_mock
        with mock.patch('app.db.db_manager') as manager:
            manager.return_value = db_mock
            with pytest.raises(Exception, match=r".* URL does .*"):
                get_long_url('raise')
            inst = get_long_url('goo.gl')
            assert type(inst) is str
            assert inst == 'https://www.google.com/'

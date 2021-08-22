from unittest import mock
from urllib.parse import urlunsplit

import pytest
import shortuuid
from app.config import NETLOC, SCHEME
from app.db import get_db, init_db
from main import main

from test_db import manager_mock, script


def get_short_url(url):
    uuid = shortuuid.uuid(name=url)[:7]
    return urlunsplit((SCHEME, NETLOC, uuid, '', ''))


def build_url(path):
    return urlunsplit((SCHEME, NETLOC, path, '', ''))


def test_main_noparams(db_path, mocker):
    mocker.patch('main.DB_PATH', db_path)
    with pytest.raises(SystemExit):
        main()


@pytest.mark.parametrize('args, output',
                         [(['on.ln'], "ERROR!!! URL does not exists"),
                          (['goo.gl'], 'https://www.google.com/'),
                          (['https://www.google.com/', '--generate'], build_url('goo.gl')),
                          (['https://www.onliner.by', '--generate'],
                           get_short_url('https://www.onliner.by')),
                          (['https://www.onliner.by', '--generate',
                            '--short_url', 'onl.by'], build_url('onl.by')),
                          (['https://www.google.com/', '--generate', '--short_url', 'goo.gl'],
                           "ERROR!!! This url already in database"),
                          ]
                         )
def test_main(db_path, argparser, mocker, capsys, args, output):
    mocker.patch('main.DB_PATH', db_path)
    init_db(db_path=db_path)
    with mock.patch('app.db.DB_PATH', db_path):
        db = get_db()
        db.executescript(script)
        args = argparser.parse_args(args)
        mocker.patch('argparse.ArgumentParser.parse_args', return_value=args)
        with manager_mock(db, 'db.get_db', 'db.db_manager'):
            main()
            captured = capsys.readouterr()
            assert output+'\n' == captured.out

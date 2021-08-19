from main import main
import pytest
from test_db import script, manager_mock
from unittest import mock
from app.db import get_db,  init_db
import shortuuid
from urllib.parse import urlunsplit
from app.config import SCHEME, NETLOC


def get_short_url(url):
    uuid = shortuuid.uuid(name=url)[:7]
    return urlunsplit((SCHEME, NETLOC, uuid, '', ''))


def test_main_noparams(db_path, mocker):
    mocker.patch('main.DB_PATH', db_path)
    with pytest.raises(SystemExit):
        main()


@pytest.mark.parametrize('args, output',
                                [(['on.ln'], "ERROR!!! URL does not exists"),
                                    (['goo.gl'], 'https://www.google.com/'), (['https://www.google.com/', '--generate'],
                                     'goo.gl'),  
                                    (['https://www.onliner.by', '--generate'], get_short_url('https://www.onliner.by')),
                                    (['https://www.onliner.by', '--generate', '--short_url', 'onl.by'], 'onl.by'),
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
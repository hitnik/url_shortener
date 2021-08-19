from main import main
from pytest_mock import mocker
import pytest
from argparse import Namespace
from test_db import script
from unittest import mock
from app.db import get_db, close_db, init_db
from argparse import ArgumentParser
import re



def test_main_noparams(db_path, mocker):
    mocker.patch('main.DB_PATH', db_path)
    with pytest.raises(SystemExit):
        main()

def test_main_short_url(db_path, argparser, mocker, capsys):
    mocker.patch('main.DB_PATH', db_path)
    init_db(db_path=db_path)
    with mock.patch('app.db.DB_PATH', db_path):
        db = get_db()
        db.executescript(script)
        args = argparser.parse_args(['on.ln'])    
        parser = mocker.patch('argparse.ArgumentParser.parse_args', return_value=args)
        main()
        captured = capsys.readouterr()
        print(captured)
        assert 'URL does not exists\n' == captured.err
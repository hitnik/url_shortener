import argparse
import textwrap
from db import (insert_long_url, short_url_exist, get_short_url,
                get_long_url_from_db, long_url_exist,
                get_short_url_by_long, insert_short_url,
                insert_long_url
                )
import shortuuid
from urllib.parse import urlunsplit
from config import NETLOC, SCHEME


class URLExistsError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
        self.message = "This short URL already exists"


class URLNotFoundError(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)
        self.message = "This short URL does not exist"


def parser():
    parser = argparse.ArgumentParser(
        description="URL shortener app.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('url', metavar='URL', type=str,
                        help=textwrap.dedent("""
                                Provide URL here.\r
                                If you want to shorten URL, """ +
                                             """provide it with [--generate] argument.\r
                                If you want to get long URL, """ +
                                             """provide short URL without any other arguments.
                                """),
                        )
    parser.add_argument('--generate', action='store_true', default=False,
                        help="""If argument presented, URL param will be defined as long url and it wil be shorten."""
                        )
    parser.add_argument('--short_url', action='store', default=None,
                        help="""Use this argument and cpecify short URL, if you want to use custom short_url."""
                        )

    return parser


class Shortener:

    @staticmethod
    def get_long_url(short):
        """ get long url by short url 

        Args:
            short (str):  short url

        Raises:
            Exception: Raises Exception when short url does not exists

        Returns:
            [str]: short url
        """
        if short_url_exist(short):
            short_inst = get_short_url(short)
            long_inst = get_long_url_from_db(id=short_inst[1])
            return long_inst[1]
        else:
            raise URLNotFoundError

    @staticmethod
    def gen_short_url(long):
        """ Generates short url from long url.
            If long url exists in DB return existing short url,
            otherwise generate new short url

        Args:
            long (str): long url

        Returns:
            str: short url
        """
        if long_url_exist(long):
            long_inst = get_long_url_from_db(url=long)
            short_inst = get_short_url_by_long(long_inst[0])
            return short_inst[2]
        else:
            uuid = shortuuid.uuid(name=long)[:7]
            short_url = urlunsplit((SCHEME, NETLOC, uuid, '', ''))
            long_id = insert_long_url(long)
            insert_short_url(short_url, long_id)
            return short_url

    @staticmethod
    def save_url(short, long):
        if not short_url_exist(short):
            if long_url_exist(long):
                long_inst = get_long_url_from_db(url=long)
                insert_short_url(short, long_inst[0])
            return short
        else:
            raise URLExistsError

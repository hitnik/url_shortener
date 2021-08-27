import argparse
import textwrap
from posixpath import basename
from urllib.parse import urlsplit, urlunsplit

import shortuuid

from config import NETLOC, SCHEME
from db_utils import (get_long_url_from_db, get_short_url,
                      get_short_url_by_long, insert_long_url, insert_short_url,
                      long_url_exist, short_url_exist)


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
                        help="If argument presented, URL param will be " +
                        "defined as long url and it wil be shorten."
                        )
    parser.add_argument('--short_url', action='store', default=None,
                        help="Use this argument and cpecify short URL, " +
                        "if you want to use custom short_url."
                        )

    return parser


class Shortener:

    def __parse_short_url(self, url):
        short = urlsplit(url)
        return basename(short.path)

    @staticmethod
    def unparse_short_url(path):
        return urlunsplit((SCHEME, NETLOC, path, '', ''))

    @classmethod
    def get_long_url(cls, short):
        """ get long url by short url
        """
        short_path = cls().__parse_short_url(short)
        if short_url_exist(short_path):
            short_inst = get_short_url(short_path)
            long_inst = get_long_url_from_db(id=short_inst[1])
            return long_inst[1]
        else:
            raise URLNotFoundError

    @classmethod
    def gen_short_url(cls, long):
        """ Generates short url from long url.
            If long url exists in DB return existing short url,
            otherwise generate new short url
        """
        if long_url_exist(long):
            long_inst = get_long_url_from_db(url=long)
            short_inst = get_short_url_by_long(long_inst[0])
            return cls.unparse_short_url(short_inst[2])
        else:
            uuid = shortuuid.uuid(name=long)[:7]
            short_url = urlunsplit((SCHEME, NETLOC, uuid, '', ''))
            long_inst = insert_long_url(long)
            insert_short_url(uuid, long_inst)
            return short_url

    @staticmethod
    def save_url(short, long):
        if not short_url_exist(short):
            if long_url_exist(long):
                long_inst = get_long_url_from_db(url=long)
                insert_short_url(short, long_inst)
            else:
                long_inst = insert_long_url(long)
                insert_short_url(short, long_inst)
            return urlunsplit((SCHEME, NETLOC, short, '', ''))
        else:
            raise URLExistsError

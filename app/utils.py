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
            return short_inst.long.long_url
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
            short_inst = get_short_url_by_long(long_inst)
            return cls.unparse_short_url(short_inst.short)
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
                long_inst = get_long_url_from_db(long)
                insert_short_url(short, long_inst)
            else:
                long_inst = insert_long_url(long)
                insert_short_url(short, long_inst)
            return urlunsplit((SCHEME, NETLOC, short, '', ''))
        else:
            raise URLExistsError

import argparse
import textwrap
from db import ( short_url_exist, get_short_url,
                    get_long_url_from_db, init_db
                )


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


def get_long_url(short):
    if short_url_exist(short):
        short_inst = get_short_url(short)
        long_inst = get_long_url_from_db(short_inst[0])
        return long_inst[1]
    else:
        raise Exception("This short URL does not exist")



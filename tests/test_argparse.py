from argparse import Namespace


def test_parser(argparser):
    args = argparser.parse_args(['test_url', '--generate',
                                '--short_url', 'short']
                                )
    assert type(args) == Namespace
    assert args.url == 'test_url'
    assert args.generate is True
    assert args.short_url == 'short'

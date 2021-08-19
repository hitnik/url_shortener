import os
import sys
from app.utils import (
    parser, Shortener,
    URLExistsError, URLNotFoundError
)
from app.db import DB_PATH, init_db


def main():
    if not os.path.exists(DB_PATH):
        init_db(DB_PATH)
    args = parser().parse_args()
    print(args)
    if not args.generate:
        try:
            Shortener.get_long_url(args.url)
        except URLNotFoundError:
            print("URL does not exists", file=sys.stderr)


if __name__ == '__main__':
    main()

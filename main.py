import os
from app.utils import (
    parser, Shortener,
    URLExistsError, URLNotFoundError
)
from app.db import DB_PATH, init_db


def main():
    if not os.path.exists(DB_PATH):
        init_db(DB_PATH)
    args = parser().parse_args()
    if not args.generate:
        try:
            print(Shortener.get_long_url(args.url))
        except URLNotFoundError:
            print("ERROR!!! URL does not exists")
    elif args.short_url is None:
        print(Shortener.gen_short_url(args.url))
    else:
        try:
            print(Shortener.save_url(args.short_url, args.url))
        except URLExistsError:
            print("ERROR!!! This url already in database")


if __name__ == '__main__':
    main()

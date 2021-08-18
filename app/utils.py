from unittest.main import main
from db import ( short_url_exist, get_short_url,
                    get_long_url_from_db, init_db
                )

def get_long_url(short):
    if short_url_exist(short):
        short_inst = get_short_url(short)
        long_inst = get_long_url_from_db(short_inst[0])
        return long_inst[1]
    else:
        raise Exception("This short URL does not exist")



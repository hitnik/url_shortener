from app import app
from flask import render_template
from flask import request, abort
from utils import Shortener, URLExistsError
import sys

@app.route('/', methods=['GET', 'POST'])
def index():
    short_out = long_out = None
    if request.method == "POST":
        long = request.form.get('long')
        short = request.form.get('short')
        if long:
            if not short or len(short) == 0:
                short_out = Shortener.gen_short_url(long)
                long_out = long
            else:
                try:
                    short_out = Shortener.save_url(long=long, short=short)
                    long_out = long
                except URLExistsError as e:
                    abort(400, description="This short URL already exists")
        else:
            pass
    return render_template('index.html', long=long_out, short=short_out), 200


@app.errorhandler(400)
def page_not_found(e):
    return render_template('400.html', message=e), 400
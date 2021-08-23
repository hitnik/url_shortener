from app import app
from flask import (
                    render_template, flash,
                     request, abort, redirect
                    )
from utils import Shortener, URLExistsError, URLNotFoundError
from db import short_url_exist


@app.route('/', methods=['GET', 'POST'])
def index():
    """index view of url_shortener app"""

    short_out = long_out = None
    if request.method == "POST":
        long = request.form.get('long')
        short = request.form.get('short')
        if long:
            if short and len(short) > 0:
                try:
                    short_out = Shortener.save_url(long=long, short=short)
                    long_out = long
                except URLExistsError as e:
                    abort(400, description=e.message)
            else:
                short_out = Shortener.gen_short_url(long)
                long_out = long
        elif short:
            try:
                long_out = Shortener.get_long_url(short)
                short_out = Shortener.unparse_short_url(short)
            except URLNotFoundError as e:
                abort(400, description=e.message)
        else:
            flash('At least one field should be filled.')
    return render_template('index.html', long=long_out, short=short_out), 200


@app.errorhandler(400)
def page_not_found(e):
    """400 error handling view"""
    return render_template('400.html', message=e), 400


@app.route('/<short>')
def redirect_short(short):
    if short_url_exist(short):
        long_url = Shortener.get_long_url(short)
        return redirect(long_url)
    abort(400, description=URLNotFoundError().message)

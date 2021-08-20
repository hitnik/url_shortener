from logging import error
from app import app
from flask import render_template
from flask import request
from utils import Shortener
import sys

@app.route('/', methods=['GET', 'POST'])
def index():
    short_out = long_out = None
    errors = []
    if request.method == "POST":
        long = request.form.get('long')
        short = request.form.get('short')
        if long:
            if not short or len(short) == 0:
                short_out = Shortener.gen_short_url(long)
                long_out = long
    context={'short': short_out, 'long': long_out, "errors": errors}
    return render_template('index.html', context=context)
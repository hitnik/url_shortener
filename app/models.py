from datetime import datetime

from app import db


class LongUrls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String, unique=True, index=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.long_url}'


class ShortUrls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short = db.Column(db.String(16), unique=True, index=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    long_id = db.Column(db.Integer, db.ForeignKey('long_urls.id'))
    long = db.relationship('LongUrls',
                           backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return f'{self.short_url}'

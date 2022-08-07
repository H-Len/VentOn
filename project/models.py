from flask_login import UserMixin
from . import db
from datetime import datetime

class Author(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))

class Post(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    init_mood = db.Column(db.SmallInteger)
    final_mood = db.Column(db.SmallInteger)


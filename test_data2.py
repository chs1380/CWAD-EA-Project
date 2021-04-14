from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db
from app.models import User, Category, Post, Comment
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app


def my_function():
    with app.app_context():
        casual = Category(id=1, body='casual')
        relationship = Category(id=2, body='relationship')
        db.session.add(casual)
        db.session.add(relationship)
        db.session.commit()


casual = Category(id=1, body='casual')
relationship = Category(id=2, body='relationship')
db.session.add(casual)
db.session.add(relationship)
db.session.commit()

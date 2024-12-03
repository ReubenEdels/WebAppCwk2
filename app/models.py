from app import db
from flask_login import UserMixin

likes_table = db.Table('likes_table',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('review_id', db.Integer, db.ForeignKey('review.id'), primary_key=True)
)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    genre = db.Column(db.String(20))
    description = db.Column(db.String(1000))
    reviews = db.relationship('Review', backref='game')


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    review = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    likes = db.relationship('User', backref='review', secondary="likes_table")


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(15), nullable=False)
    reviews = db.relationship('Review', backref='user')
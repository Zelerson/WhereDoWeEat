from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Place(db.Model):
    __tablename__ = 'places'

    place_id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255))
    formatted_address = db.Column(db.String(255))
    editorial_summary = db.Column(db.String())
    rating = db.Column(db.Float)
    user_ratings_total = db.Column(db.Integer)
    url = db.Column(db.String(255))
    type = db.Column(db.JSON)
    location = db.Column(db.JSON)
    reviews = db.relationship('Review', back_populates='place')
    last_update = db.Column(db.DateTime, default=datetime.today(), onupdate=datetime.today())


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(255))
    author_url = db.Column(db.String(255))
    relative_time_description = db.Column(db.String(255))
    text = db.Column(db.String(255))
    rating = db.Column(db.Integer)
    place_id = db.Column(db.String(255), db.ForeignKey('places.place_id'))
    place = db.relationship('Place', back_populates='reviews')


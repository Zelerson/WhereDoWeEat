from flask import Blueprint, render_template, request, redirect, jsonify, session
from .api import get_nearby, get_details
from .models import Place, Review, db
from datetime import datetime, timedelta

bp = Blueprint('app', __name__, template_folder='../templates')


@bp.route('/places/')
def places_list():
    blacklist = ['Żabka']
    location = session.get('location')
    if location:
        result_places = get_nearby(location)
        places_nearby = [place for place in result_places if place.get('name') not in blacklist
                         and (place.get('user_ratings_total') and place.get('user_ratings_total') >= 100)]

        return render_template('places_list.html', places_nearby=places_nearby)
    else:
        error_message = 'Brak możliwości określenia lokalizacji'
        return render_template('error.html', error_message=error_message)


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/details/<place_id>')
def place_details(place_id):
    place = db.session.query(Place).filter(Place.place_id == place_id).first()

    if not place or place.last_update < datetime.today() - timedelta(days=5):
        get_details(place_id)
        db.session.commit()
        place = db.session.query(Place).filter(Place.place_id == place_id).first()

    reviews = db.session.query(Review).filter(Review.place_id == place_id).all()

    return render_template('details.html', place=place, reviews=reviews)


@bp.route('/receive_location', methods=['POST'])
def receive_location():
    data = request.get_json()
    session['location'] = data['latitude'], data['longitude']
    return jsonify({"status": "success"})

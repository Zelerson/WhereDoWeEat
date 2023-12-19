import os
import time
import googlemaps
from app.models import Place, Review, db
from dotenv import load_dotenv

load_dotenv('api_key.env')

API_KEY = os.environ.get('GOOGLE_API_KEY')
# LOCATION = (52.210948, 20.9751663)

gmaps = googlemaps.Client(key=API_KEY)


def get_details(place_id, client=gmaps):
    fields = ['name', 'formatted_address', 'rating', 'type', 'url', 'reviews', 'geometry/location', 'user_ratings_total', 'editorial_summary']

    details = client.place(place_id=place_id, fields=fields, language='pl')

    result_place = Place(
        place_id=place_id,
        name=details['result']['name'],
        formatted_address=details['result']['formatted_address'],
        rating=details['result']['rating'],
        user_ratings_total=details['result']['user_ratings_total'],
        url=details['result']['url'],
        type=details['result']['types'],
        location=details['result']['geometry']['location']
    )

    if details['result'].get('editorial_summary'):
        result_place.editorial_summary = details['result']['editorial_summary']['overview']

    db.session.add(result_place)

    for review_data in details.get('result', {}).get('reviews', []):
        review = Review(
            place=result_place,
            text=review_data['text'],
            rating=review_data['rating'],
            author_name=review_data['author_name'],
            author_url=review_data['author_url'],
            relative_time_description=review_data['relative_time_description'])
        db.session.add(review)


def get_nearby(location, client=gmaps, radius=500, types='restaurant'):
    all_results = []
    places_result = client.places_nearby(location=location, radius=radius, type=types)
    all_results.extend(places_result.get('results', []))

    next_page_token = places_result.get('next_page_token')
    while next_page_token:
        time.sleep(2)

        places_result = client.places_nearby(location=location, radius=radius, type=types, page_token=next_page_token)

        all_results.extend(places_result.get('results', []))

        next_page_token = places_result.get('next_page_token')

    return all_results

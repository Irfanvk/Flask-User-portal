from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
import geocoder
import urllib.request as urllib2
import json

# import os

# os.environ["GOOGLE_API_KEY"] = "api_key_from_google_cloud_platform"
# or
# export GOOGLE_API_KEY=api_key_from_google_cloud_platform

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    pwdhash = db.Column(db.String(54))

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)


class Place(object):
    """docstring for Place"""

    def meters_to_walking_time(self, meters):
        # 80 meters is one minute walking time
        return int(meter / 80)

    def wiki_path(self, slug):
        return urllib2.urlparse.urljoin("http://en.wikipedia.org/wiki/", slug.replace(' ', '_'))

    def address_to_latlng(self, address):

        g = geocoder.google(address)
        return (g.lat, g.lng)

    def query(self, address):
        lat, lng = self.address_to_latlng(address)
        print("lat and lng", lat, lng)

        query_url = 'https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gsradius=10000&gscoord={0}%7C{1}&gslimit=20&format=json'.format(
            lat, lng)
        g = urllib2.urlopen(query_url)
        print("querymodel g->", g)

        results = g.read()
        print('here is results***************',
              results,  "<--*****************")
        g.close()

        data = json.loads(results)
        print("data", data)

        places = []
        for place in data['query']['geosearch']:
            name = place['title']
            meters = place['dist']
            lat = place['lat']
            lng = place['lng']

            wiki_url = self.wiki_path(name)
            walking_time = self.meters_to_walking_time(meters)

            d = {
                'name': name,
                'url': wiki_url,
                'time': walking_time,
                'lat': lat,
                'lng': lng
            }

            places.append(d)
        return places

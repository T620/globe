#geocoding utilites
import globe
from globe import app
import geopy
from geopy.geocoders import Nominatim
geolocator = Nominatim(timeout=3)
import os

key = os.environ['MAPS_API_KEY']

def get(address):
	#returns the lat and long of a given address
	print address

	try:
		lat = str(geolocator.geocode(address).latitude)
		lo = str(geolocator.geocode(address).longitude)

		coordinates = {
			"lattitude:": lat,
			"longitude:": lo
		}
	except:
		return "geocoder timed out :("

	return lat

def getUserLocation():
	#grabs the user's location when access is granted
	import requests
	import json

	send_url = ''
	r = requests.get("http://freegeoip.net/json")
	j = json.loads(r.text)

	coordinates = {
		"lattitude": j['latitude'],
		"longitude": j['longitude']
	}


def reverse(coords):
	from geopy.geocoders import GoogleV3
	geolocator = GoogleV3(api_key=key, domain='maps.google.co.uk', timeout=3)
	address = geolocator.reverse(coords)
	print address
	return address

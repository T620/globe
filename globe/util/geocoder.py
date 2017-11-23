#geocoding utilites

def getCoordinates(address):
	#returns the lat and long of a given address
	from geopy.geocoders import Nominatim

	try:

		lat = str(geolocator.geocode(address).latitude)
		lo = str(geolocator.geocode(address).longitude)

		coordinates = {
			"lattitude": lat,
			"longitude": lo
		}

		return coordinates
	except:
		return "geocoder timed out :("


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

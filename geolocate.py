import sys
import json
import datetime
import googlemaps
from tempfile import mkdtemp
from joblib import Memory

memory = Memory(cachedir='.cache', verbose=0)

from blessings import Terminal
t = Terminal()

gmaps = googlemaps.Client(key='AIzaSyChd4ESsjuPQDQSuX11pLGrsca3_3XYmfI')

def find_nearest_weekday(now=datetime.datetime.now()):
    MONDAY = 0
    FRIDAY = 5
    current = now
    while current.weekday() > FRIDAY:
        current += datetime.timedelta(days=1)
    return current

@memory.cache
def geocode(address):
    return gmaps.geocode(address)

@memory.cache
def get_transit_directions(source, destination):
    departure_time = find_nearest_weekday().replace(hour=6) # 6 am nearest weekday
    try:
        directions_result = gmaps.directions(source,
                                             destination,
                                             mode="transit",
                                             departure_time=departure_time)
    except googlemaps.exceptions.ApiError as e:
        directions_result = []

    return directions_result

park_and_rides = {
    "West Milford": "Park & Ride, Old Rte 23, Newfoundland, NJ 07435"
}

# def get_directions(source, destination):
#     try:
#         directions_result = get_transit_directions(source, destination)
#     except googlemaps.exceptions.ApiError as e:
#         directions_result = []

#     if len(directions_result) == 0:
#         print(f"Unable to find directions directly from {t.yellow(source)} to {t.cyan(destination)}.")
#         geocode_result = geocode(source)

#         if len(geocode_result) == 0:
#             print(f"Unable to geocode {t.yellow(source)}.")
#             return None

#         try:
#             city = [x['short_name'] for x in geocode_result[0]['address_components'] if 'locality' in x['types']][0]
#         except IndexError:
#             print(f"Unable to get city from decoded address.")
#             return None

#         try:
#             park_and_ride_address = park_and_rides[city]
#         except KeyError:
#             print(f"No hardcoded park and ride address within {city}")
#             return None

#         print(f"Finding directions from park and ride within {t.magenta(city)} at {t.yellow(park_and_ride_address)} to {t.cyan(destination)}...")
#         directions_result = get_transit_directions(park_and_ride_address, destination)

#         if len(directions_result) == 0:
#             print(f"Unable to find directions directly from {t.yellow(park_and_ride_address)} to {t.cyan(destination)}.")
#             return None

#     return directions_result

def get_directions(source, destination):
    directions_result = get_transit_directions(source, destination)
    if not directions_result: return None
    leg = directions_result[0]['legs'][0]

    instructions = []
    for step in leg['steps']:
        instructions.append({
            "duration": step['duration']['text'],
            "distance": step['distance']['text'],
            "instructions": step['html_instructions'],
            "travel_mode": step['travel_mode']
            })

    return {
        "duration": leg['duration'],

        "instructions": instructions
    }

if __name__ == "__main__":

    from blessings import Terminal
    t = Terminal()

    source = "116 N 19th St, Hawthorne, NJ 07506"
    destination = "Port Authority Bus Terminal"

    legs = get_transit_directions(source, destination)[0]['legs']
    assert len(legs) == 1
    leg = legs[0]
    print("From", t.yellow(leg['start_address']), "at", leg['departure_time']['text'])
    print("To", t.cyan(leg['end_address']), "by", leg['arrival_time']['text'])
    print("In", leg['duration']['text'], "with a distance of", leg['distance']['text'])
    for i, step in enumerate(leg['steps']):
        print(i, step['duration']['text'], step['travel_mode'], step['distance']['text'], step['html_instructions'], sep=" | ")

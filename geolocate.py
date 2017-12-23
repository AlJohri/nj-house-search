import os
import sys
import json
import googlemaps
from joblib import Memory

from utils import find_nearest_weekday

memory = Memory(cachedir='.cache', verbose=0)

from blessings import Terminal
t = Terminal()

GOOGLE_MAPS_API_KEY = os.environ['GOOGLE_MAPS_API_KEY']

gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

@memory.cache
def geocode(address):
    return gmaps.geocode(address)

# rm -rf .cache/joblib/geolocate/get_driving_directions
@memory.cache
def get_driving_directions(source, destination):
    departure_time = find_nearest_weekday().replace(hour=6) # 6 am nearest weekday
    directions_result = gmaps.directions(source,
                                         destination,
                                         mode="driving",
                                         departure_time=departure_time)
    # ApiError: INVALID_REQUEST (departure_time is in the past. Traffic information is only available for future and current times.)
    # *** googlemaps.exceptions.ApiError: INVALID_REQUEST
    # (departure_time is in the past. Traffic information is only available for future and current times.)
    return directions_result

@memory.cache
def get_transit_directions(source, destination):
    departure_time = find_nearest_weekday().replace(hour=6) # 6 am nearest weekday
    # try:
    directions_result = gmaps.directions(source,
                                         destination,
                                         mode="transit",
                                         departure_time=departure_time)
    # except googlemaps.exceptions.ApiError as e:
    #     directions_result = []

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

def get_directions(source, destination, mode='transit'):
    if mode == 'transit':
        directions_result = get_transit_directions(source, destination)
    elif mode == 'driving':
        directions_result = get_driving_directions(source, destination)
    else:
        raise Exception(f'unknown mode {mode}')
    if not directions_result: return None
    leg = directions_result[0]['legs'][0]

    instructions = []
    for step in leg['steps']:
        instructions.append({
            "duration": step['duration']['text'],
            "distance": step['distance']['text'],
            "instructions": step['html_instructions'],
            "transit_details": step['transit_details'] if step.get('transit_details') else None,
            "travel_mode": step['travel_mode']
            })

    return {
        "duration": leg['duration'],
        "instructions": instructions
    }

def add_geocode_to_listing(listing):
    source = listing['address'] + ' ' + listing['city'] + ', ' + 'NJ'
    geocoded = geocode(source)
    if len(geocoded) == 0:
        source2 = listing['address'] + ' ' + listing['city'].replace(' City', '').replace(' Boro Twp.', '').replace(' Boro', '') + ', ' + 'NJ'
        geocoded = geocode(source2)
        if len(geocoded) == 0:
            print(f"could not geocode: {source} or {source2}")
            return listing
    listing['lat'] = geocoded[0]['geometry']['location']['lat']
    listing['lng'] = geocoded[0]['geometry']['location']['lng']
    listing['formatted_address'] = geocoded[0]['formatted_address']
    try:
        listing['city'] = [x['long_name'] for x in geocoded[0]['address_components'] if 'locality' in x['types']][0]
    except IndexError:
        try:
            listing['city'] = [x['long_name'] for x in geocoded[0]['address_components'] if 'administrative_area_level_3' in x['types']][0]
        except IndexError:
            print("could not find city for", listing['formatted_address'], geocoded[0]['address_components'])
    try:
        listing['county'] = [x['long_name'] for x in geocoded[0]['address_components'] if 'administrative_area_level_2' in x['types']][0].replace(' County', '')
    except IndexError:
        print("could not find county for", listing['id'], listing['formatted_address'], geocoded[0]['address_components'])
    return listing

if __name__ == "__main__":

    from blessings import Terminal
    t = Terminal()

    source = "408 Pine St Boonton Town, NJ"
    destination = "Port Authority Bus Terminal"

    legs = get_transit_directions(source, destination)[0]['legs']
    assert len(legs) == 1
    leg = legs[0]
    print("From", t.yellow(leg['start_address']), "at", leg['departure_time']['text'])
    print("To", t.cyan(leg['end_address']), "by", leg['arrival_time']['text'])
    print("In", leg['duration']['text'], "with a distance of", leg['distance']['text'])
    for i, step in enumerate(leg['steps']):
        print(i, step['duration']['text'], step['travel_mode'], step['distance']['text'], step['html_instructions'], sep=" | ")
        if 'transit_details' in step:
            print(step['transit_details']['line']['name'], step['transit_details']['line']['short_name'], step['transit_details']['departure_stop']['name'], step['transit_details']['arrival_stop']['name'])

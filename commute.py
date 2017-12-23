import json
import numpy as np
from geopy.distance import vincenty
from geolocate import get_directions

with open('park_and_rides.json') as f:
    park_and_rides = json.load(f)

# TODO: find the closest BUS vs TRAIN park and ride separately?
def add_closest_park_and_ride_to_listing(listing):
    if not listing.get('lat') or not listing.get('lng'):
        return listing

    distances = [vincenty(pr['location'], (listing['lat'], listing['lng'],)).miles for pr in park_and_rides]
    closest_index = np.argmin(distances)
    listing['park_and_ride'] = park_and_rides[closest_index]
    listing['park_and_ride_name'] = park_and_rides[closest_index]['name']
    listing['park_and_ride_type'] = park_and_rides[closest_index]['type']
    listing['park_and_ride_distance'] = distances[closest_index]
    
    park_and_rides_bus = [x for x in park_and_rides if x['type'] == 'bus']
    distances_bus = [vincenty(pr['location'], (listing['lat'], listing['lng'],)).miles for pr in park_and_rides_bus]
    closest_index_bus = np.argmin(distances_bus)
    listing['park_and_ride_bus'] = park_and_rides_bus[closest_index_bus]
    listing['park_and_ride_bus_name'] = park_and_rides_bus[closest_index_bus]['name']
    listing['park_and_ride_bus_type'] = park_and_rides_bus[closest_index_bus]['type']
    listing['park_and_ride_bus_distance'] = distances_bus[closest_index_bus]
    return listing

def add_commute_to_listing(listing):
    if not listing.get('formatted_address'):
        return listing

    # get walking/transit destination from source to port authority
    source = listing['formatted_address']
    destination = 'Port Authority Bus Terminal'
    try:
        directions = get_directions(source, destination, mode='transit')
    except Exception as e:
        pass
    else:
        listing['nyc_duration'] = directions['duration']['value'] if directions else None
        listing['nyc_duration_text'] = directions['duration']['text'] if directions else None
        listing['nyc_instructions'] = directions['instructions'] if directions else None
    
    # get walking/transit destination from source to 94 Old Short Hills Road, Livingston, NJ
    source = listing['formatted_address']
    destination = '94 Old Short Hills Road, Livingston, NJ'
    try:
        directions = get_directions(source, destination, mode='driving')
    except Exception as e:
        pass
    else:
        listing['barnabas_duration'] = directions['duration']['value'] if directions else None
        listing['barnabas_duration_text'] = directions['duration']['text'] if directions else None
        listing['barnabas_instructions'] = directions['instructions'] if directions else None

    if listing.get('park_and_ride'):

        # calculate time from home -> park and ride
        source = listing['formatted_address']
        destination = str(tuple(listing['park_and_ride']['location']))[1:-1]
        directions = get_directions(source, destination, mode='driving')
        if directions is None:
            print(f"unable to find driving directions from home ({source}) to park and ride ({destination})")
        listing['park_and_ride_duration1'] = directions['duration']['value'] if directions else None
        listing['park_and_ride_duration_text1'] = directions['duration']['text'] if directions else None
        # listing['park_and_ride_instructions1'] = directions['instructions'] if directions else None

        # calculate time from home -> park and ride
        source = listing['formatted_address']
        destination = str(tuple(listing['park_and_ride']['location']))[1:-1]
        directions = get_directions(source, destination, mode='driving')
        if directions is None:
            print(f"unable to find driving directions from home ({source}) to park and ride ({destination})")
        listing['park_and_ride_duration1'] = directions['duration']['value'] if directions else None
        listing['park_and_ride_duration_text1'] = directions['duration']['text'] if directions else None
        # listing['park_and_ride_instructions1'] = directions['instructions'] if directions else None

        # calculate time from park and ride -> NY
        if listing['park_and_ride']['type'] == 'rail':
            destination = 'New York Penn Station'
        else:
            destination = 'Port Authority Bus Terminal'
        source = str(tuple(listing['park_and_ride']['location']))[1:-1]
        directions = get_directions(source, destination, mode='transit')
        if directions is None:
            print(f"unable to find transit directions from park and ride ({source}) to NY ({destination})")
        listing['park_and_ride_duration2'] = directions['duration']['value'] if directions else None
        listing['park_and_ride_duration_text2'] = directions['duration']['text'] if directions else None
        # listing['park_and_ride_instructions2'] = directions['instructions'] if directions else None
    
        if not listing.get('park_and_ride_duration1') or not listing.get('park_and_ride_duration2'):
            print(listing)

        # sum total time from home -> NY
        listing['park_and_ride_duration'] = listing['park_and_ride_duration1'] + listing['park_and_ride_duration2']
        listing['park_and_ride_duration_text'] = ', '.join([listing['park_and_ride_duration_text1'], listing['park_and_ride_duration_text2']])

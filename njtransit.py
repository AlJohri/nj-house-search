# http://www.njtransit.com/sf/sf_servlet.srv?hdnPageAction=TripPlannerTo
# http://www.njtransit.com/sf/sf_servlet.srv?hdnPageAction=TripPlannerServiceNearTo

import lxml.html
import requests
from joblib import Memory
from geolocate import geocode

from utils import find_nearest_weekday

# http://www.njtransit.com/rg/rg_servlet.srv?hdnPageAction=StationParkRideTo

memory = Memory(cachedir='.cache', verbose=0)

@memory.cache
def plan_trip_inner(source, destination):

    source_geocoded = geocode(source)
    destination_geocoded = geocode(destination)

    departure_time = find_nearest_weekday().replace(hour=6, minute=0) # 6 am nearest weekday

    response = requests.post("http://www.njtransit.com/sf/sf_servlet.srv?hdnPageAction=TripPlannerItineraryFrom", data={
        "starting_street_address": source,
        "dest_street_address": destination,
        "datepicker": departure_time.strftime('%x'),
        "time": "D",
        "Time": departure_time.strftime('%I:%M'),
        "Suffix": "AM",
        "mode": "BCTLXR", # bus, rail, right rail, all
        "min": "T", # minimize travel time,
        "Walk": "0.25", # max 0.25 mile walk
        "Hour": departure_time.strftime('%I'),
        "Minute": departure_time.strftime('%M'),
        "TravelToLatLong": str(destination_geocoded[0]['geometry']['location']['lat']) + "," + str(destination_geocoded[0]['geometry']['location']['lng']),
        "TravelFromLatLong": str(source_geocoded[0]['geometry']['location']['lat']) + "," + str(source_geocoded[0]['geometry']['location']['lng']),
    })

    return response

def plan_trip(source, destination):

    response = plan_trip_inner(source, destination)
    doc = lxml.html.fromstring(response.text)

    if "We're sorry. We are unable to provide trip results based on the information you provided." in response.text:
        return None

    if "We're sorry. We were unable to find a trip between your origin and destination without an excessive walking distance." in response.text:
        row = doc.cssselect('form[name="frm_itinerary_planning_inaccurate"] table tr td table tr')[0]
        text = row.cssselect('td:nth-child(3) > font')[0].text
        full = row.cssselect('td input')[0].get('value')

        try:
            name, city_town, distance = text.split(' - ')
            return plan_trip(name + ", " + city_town, destination)
        except ValueError:
            name, distance = text.split(' - ')
            return plan_trip(name, destination)

    panel = doc.cssselect("#Accordion1 > .AccordionPanel > .AccordionPanelContent > table")[0]

    steps = []
    step = {}
    for i, el in enumerate(panel.cssselect('tr td[align="left"] font')):
        instruction_type, instructions = el.text_content().strip().split(' : ')
        instruction_type = instruction_type.strip()
        instructions = instructions.strip()
        if instruction_type == "Depart":
            step['depart'] = instructions
        elif instruction_type == "Board":
            step['board'] = instructions
        elif instruction_type == "Arrive":
            step['arrive'] = instructions
            steps.append(step)
            step = {}
        else:
            raise Exception(f"unknown instruction type {instruction_type}")

    for step in steps:
        print(step)

def find_service_near(address):
    pass

if __name__ == "__main__":
    plan_trip("115 Dumont Ave, Clifton, NJ 07013", "Port Authority Bus Terminal")
    # plan_trip("170 Schofield Rd, West Milford, NJ 07480", "Port Authority Bus Terminal")

    """
    # from itertools import islice
    # from njtransit import plan_trip
    # for listing in islice(listings.values(), 100):
    #     address = listing['address'] + ' ' + listing['city/town'] + ', ' + 'NJ'
    #     print(address)
    #     print("NJTransit")
    #     plan_trip(address, 'Port Authority Bus Terminal')
    #     print("Google")
    #     if listing.get('nyc_duration_text'):
    #         print(listing['nyc_duration_text'])
    #         for x in listing['nyc_instructions']:
    #             print(x['duration'], x['distance'],  x['instructions'], x['travel_mode'], x['transit_details'])
    #     print('---------------')
    # plan_trip('17 Highland Ave, Netcong, NJ', 'Port Authority Bus Terminal')
    """
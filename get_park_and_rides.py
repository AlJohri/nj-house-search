#!/usr/bin/env python3

"""
Links

Train Schedule from `orig` to `dest`
http://www.njtransit.com/sf/sf_servlet.srv?hdnPageAction=TrainSchedulesTo&orig=Rutherford&dest=New%20York%20Penn%20Station

http://www.njtransit.com/rg/rg_servlet.srv?hdnPageAction=StationParkRideTo
"""

import re
import json
import requests

counties = [
    {"code": "1" ,  "name": "Atlantic"},
    {"code": "2" ,  "name": "Bergen"},
    {"code": "4" ,  "name": "Camden"},
    {"code": "5" ,  "name": "Cape May"},
    {"code": "6" ,  "name": "Cumberland"},
    {"code": "7" ,  "name": "Essex"},
    {"code": "9" ,  "name": "Hudson"},
    {"code": "11",  "name": "Mercer"},
    {"code": "12",  "name": "Middlesex"},
    {"code": "13",  "name": "Monmouth"},
    {"code": "23",  "name": "New York (NY)"},
    {"code": "15",  "name": "Ocean"},
    {"code": "22",  "name": "Orange (NY)"},
    {"code": "16",  "name": "Passaic"},
    {"code": "24",  "name": "Philadelphia (PA)"},
    {"code": "18",  "name": "Somerset"},
    {"code": "19",  "name": "Sussex"},
    {"code": "20",  "name": "Union"},]

light_rail_lines = [
    {"code": "HBLR", "name": "Hudson-Bergen Light Rail"},
    {"code": "7", "name": "Newark Light Rail/City Subway"},
    {"code": "343", "name": "River Line"},]

light_rail_stations = [
    {'id': '38229', 'line': 'HBLR', 'name': '22nd Street (Bayonne)'},
    {'id': '38441', 'line': 'HBLR', 'name': '2nd Street (Hoboken)'},
    {'id': '37005', 'line': 'HBLR', 'name': '34th Street (Bayonne)'},
    {'id': '38306', 'line': '343', 'name': '36th Street'},
    {'id': '37004', 'line': 'HBLR', 'name': '45th Street (Bayonne)'},
    {'id': '42673', 'line': 'HBLR', 'name': '8th Street (Bayonne)'},
    {'id': '38442', 'line': 'HBLR', 'name': '9th Street - Congress Street'},
    {'id': '38309', 'line': '343', 'name': 'Aquarium'},
    {'id': '39133', 'line': '7', 'name': 'Atlantic Street'},
    {'id': '38578', 'line': 'HBLR', 'name': 'Bergenline Avenue'},
    {'id': '38299', 'line': '343', 'name': 'Beverly/Edgewater Park'},
    {'id': '14984', 'line': '7', 'name': 'Bloomfield Ave'},
    {'id': '38294', 'line': '343', 'name': 'Bordentown'},
    {'id': '26316', 'line': '7', 'name': 'Branch Brook Park'},
    {'id': '39130', 'line': '7', 'name': 'Broad Street'},
    {'id': '38298', 'line': '343', 'name': 'Burlington South'},
    {'id': '38297', 'line': '343', 'name': 'Burlington Towne Centre'},
    {'id': '38293', 'line': '343', 'name': 'Cass Street'},
    {'id': '38302', 'line': '343', 'name': 'Cinnaminson'},
    {'id': '38308', 'line': '343', 'name': 'Cooper St/Rutgers'},
    {'id': '37003', 'line': 'HBLR', 'name': 'Danforth Avenue'},
    {'id': '6907', 'line': '7', 'name': 'Davenport Ave'},
    {'id': '38300', 'line': '343', 'name': 'Delanco'},
    {'id': '38310', 'line': '343', 'name': 'Entertainment Center'},
    {'id': '36995', 'line': 'HBLR', 'name': 'Essex Street'},
    {'id': '36994', 'line': 'HBLR', 'name': 'Exchange Place'},
    {'id': '38296', 'line': '343', 'name': 'Florence'},
    {'id': '36999', 'line': 'HBLR', 'name': 'Garfield Avenue'},
    {'id': '38065', 'line': '7', 'name': 'Grove Street'},
    {'id': '38292', 'line': '343', 'name': 'Hamilton Avenue'},
    {'id': '37376', 'line': 'HBLR', 'name': 'Harborside'},
    {'id': '37377', 'line': 'HBLR', 'name': 'Harsimus Cove'},
    {'id': '39348', 'line': 'HBLR', 'name': 'Hoboken'},
    {'id': '36997', 'line': 'HBLR', 'name': 'Jersey Avenue'},
    {'id': '36998', 'line': 'HBLR', 'name': 'Liberty State Park'},
    {'id': '17699', 'line': 'HBLR', 'name': 'Lincoln Harbor'},
    {'id': '36996', 'line': 'HBLR', 'name': 'Marin Boulevard'},
    {'id': '37000', 'line': 'HBLR', 'name': 'Martin Luther King Drive'},
    {'id': '6900', 'line': '7', 'name': 'Military Park'},
    {'id': '39134', 'line': '7', 'name': 'NJPAC/Center Street'},
    {'id': '26326', 'line': '7', 'name': 'Newark Penn Station'},
    {'id': '37378', 'line': 'HBLR', 'name': 'Newport'},
    {'id': '6957', 'line': '7', 'name': 'Norfolk St'},
    {'id': '14986', 'line': '7', 'name': 'Orange St'},
    {'id': '38304', 'line': '343', 'name': 'Palmyra'},
    {'id': '6966', 'line': '7', 'name': 'Park Ave'},
    {'id': '43288', 'line': '343', 'name': 'Pennsauken Transit Center'},
    {'id': '38305', 'line': '343', 'name': 'Pennsauken/Route 73'},
    {'id': '9878', 'line': 'HBLR', 'name': 'Port Imperial'},
    {'id': '37002', 'line': 'HBLR', 'name': 'Richard St'},
    {'id': '39131', 'line': '7', 'name': 'Riverfront Stadium'},
    {'id': '38301', 'line': '343', 'name': 'Riverside'},
    {'id': '38303', 'line': '343', 'name': 'Riverton'},
    {'id': '38295', 'line': '343', 'name': 'Roebling'},
    {'id': '38064', 'line': '7', 'name': 'Silver Lake'},
    {'id': '38579', 'line': 'HBLR', 'name': 'Tonnelle Avenue'},
    {'id': '38291', 'line': '343', 'name': 'Trenton Transit Center'},
    {'id': '38307', 'line': '343', 'name': 'Walter Rand Trans. Center'},
    {'id': '6995', 'line': '7', 'name': 'Warren St'},
    {'id': '39132', 'line': '7', 'name': 'Washington Park'},
    {'id': '6997', 'line': '7', 'name': 'Washington St'},
    {'id': '37001', 'line': 'HBLR', 'name': 'West Side Avenue'}]

# http://www.njtransit.com/rg/rg_servlet.srv?hdnPageAction=BusTerminalLookupFrom&selCounty=2&selStation=700&x=40&y=14
# http://www.njtransit.com/rg/rg_servlet.srv?hdnPageAction=BusTerminalLookupFrom&selCounty=16&selStation=4098&x=19&y=15
bus_stations = [
    {'id': '38104', 'county': '13', 'name': 'Aldrich Road'},
    {'id': '4098', 'county': '16', 'name': 'Allwood Road'},
    {'id': '297', 'county': '1', 'name': 'Atlantic City Bus Terminal'},
    {'id': '1582', 'county': '4', 'name': 'Avandale'},
    {'id': '4643', 'county': '20', 'name': 'Bonnel Court - Union Twp'},
    {'id': '3625', 'county': '15', 'name': 'Brick'},
    {'id': '3897', 'county': '16', 'name': 'Broadway Bus Terminal - Paterson'},
    {'id': '23216', 'county': '5', 'name': 'Cape May Bus Terminal'},
    {'id': '37509', 'county': '12', 'name': 'Carteret'},
    {'id': '4137', 'county': '16', 'name': 'Clifton Commons'},
    {'id': '27345', 'county': '13', 'name': 'Craig Road'},
    {'id': '37008', 'county': '15', 'name': 'Dorado'},
    {'id': '700', 'county': '2', 'name': 'Dumont A'},
    {'id': '688', 'county': '2', 'name': 'Dumont B - West Shore'},
    {'id': '850', 'county': '2', 'name': 'Fairlawn DPW'},
    {'id': '1033', 'county': '2', 'name': 'Fort Lee'},
    {'id': '9729', 'county': '13', 'name': 'Freehold Center'},
    {'id': '27394', 'county': '13', 'name': 'Freehold Mall'},
    {'id': '17392', 'county': '12', 'name': 'Garden State Parkway Exit 120'},
    {'id': '37234', 'county': '2', 'name': 'Garden State Parkway Exit 165 - Paramus'},
    {'id': '3512', 'county': '23', 'name': 'George Washington Bridge Terminal'},
    {'id': '3277', 'county': '22', 'name': 'Greenwood Lake'},
    {'id': '237', 'county': '24', 'name': 'Greyhound Bus Terminal'},
    {'id': '1252', 'county': '2', 'name': 'Hackensack Terminal'},
    {'id': '17082', 'county': '9', 'name': 'Hoboken Terminal Bus Lanes'},
    {'id': '27400', 'county': '13', 'name': 'Howell'},
    {'id': '27358', 'county': '12', 'name': 'Inverness'},
    {'id': '28555', 'county': '7', 'name': 'Irvington Bus Terminal'},
    {'id': '27363', 'county': '12', 'name': 'Jake Brown'},
    {'id': '2916', 'county': '9', 'name': 'Journal Square Transportation Center'},
    {'id': '37607', 'county': '15', 'name': 'Lakewood Terminal'},
    {'id': '38455', 'county': '13', 'name': 'Lloyd Road - Aberdeen'},
    {'id': '17360', 'county': '13', 'name': 'Marlboro'},
    {'id': '29037', 'county': '2', 'name': 'Midland Park'},
    {'id': '38063', 'county': '16', 'name': 'Mothers Park & Ride'},
    {'id': '2275', 'county': '7', 'name': 'Newark Penn Station Bus Lanes'},
    {'id': '37801', 'county': '16', 'name': 'Newfoundland - West Milford NJ'},
    {'id': '2935', 'county': '9', 'name': 'North Bergen'},
    {'id': '1851', 'county': '5', 'name': 'Ocean City Transportation Center'},
    {'id': '27367', 'county': '12', 'name': 'Old Bridge'},
    {'id': '3942', 'county': '16', 'name': 'Passaic Bus Terminal'},
    {'id': '43282', 'county': '4', 'name': 'Pennsauken Bus Terminal'},
    {'id': '4622', 'county': '20', 'name': 'Pine Avenue - Union Twp'},
    {'id': '3511', 'county': '23', 'name': 'Port Authority Bus Terminal'},
    {'id': '37730', 'county': '2', 'name': 'Ridgewood Bus Terminal'},
    {'id': '27578', 'county': '16', 'name': 'Ringwood'},
    {'id': '16619', 'county': '20', 'name': 'Rutgers Lane Hospital - Union Twp'},
    {'id': '40358', 'county': '12', 'name': 'Sayreville'},
    {'id': '27344', 'county': '13', 'name': 'Schibanoff'},
    {'id': '4575', 'county': '20', 'name': 'Springfield Center - Springfield Twp'},
    {'id': '38360', 'county': '19', 'name': 'Stockholm - Hardyston'},
    {'id': '27439', 'county': '13', 'name': 'Symmes Drive - Manalapan Mall'},
    {'id': '27354', 'county': '13', 'name': 'Texas Road'},
    {'id': '3603', 'county': '15', 'name': 'Toms River Park & Ride'},
    {'id': '25104', 'county': '11', 'name': 'Trenton Transit Center'},
    {'id': '4633', 'county': '20', 'name': 'Union Center - Union Twp'},
    {'id': '27427', 'county': '13', 'name': 'Union Hill'},
    {'id': '615', 'county': '2', 'name': 'Vince Lombardi'},
    {'id': '197', 'county': '6', 'name': 'Vineland Terminal'},
    {'id': '11519', 'county': '4', 'name': 'Walter Rand Transportation Center'},
    {'id': '27561', 'county': '22', 'name': 'Warwick - NY'},
    {'id': '1813', 'county': '18', 'name': 'Watchung Park & Ride'},
    {'id': '39635', 'county': '16', 'name': 'Wayne/Route 23 Transit Center'},
    {'id': '38407', 'county': '16', 'name': 'West Milford - Greenwood Lake NJ'},
    {'id': '2076', 'county': '5', 'name': 'Wildwood Terminal'},
    {'id': '3921', 'county': '16', 'name': 'Willowbrook Mall'}]

train_stations = [
    {"id": "37169", "name": "Aberdeen Matawan"},
    {"id": "2", "name": "Absecon"},
    {"id": "3", "name": "Allendale"},
    {"id": "4", "name": "Allenhurst"},
    {"id": "5", "name": "Anderson Street"},
    {"id": "6", "name": "Annandale"},
    {"id": "8", "name": "Asbury Park"},
    {"id": "9", "name": "Atco"},
    {"id": "10", "name": "Atlantic City"},
    {"id": "11", "name": "Avenel"},
    {"id": "12", "name": "Basking Ridge"},
    {"id": "13", "name": "Bay Head"},
    {"id": "14", "name": "Bay Street"},
    {"id": "15", "name": "Belmar"},
    {"id": "17", "name": "Berkeley Heights"},
    {"id": "18", "name": "Bernardsville"},
    {"id": "19", "name": "Bloomfield"},
    {"id": "20", "name": "Boonton"},
    {"id": "21", "name": "Bound Brook"},
    {"id": "22", "name": "Bradley Beach"},
    {"id": "23", "name": "Brick Church"},
    {"id": "24", "name": "Bridgewater"},
    {"id": "25", "name": "Broadway"},
    {"id": "26", "name": "Campbell Hall"},
    {"id": "27", "name": "Chatham"},
    {"id": "28", "name": "Cherry Hill"},
    {"id": "29", "name": "Clifton"},
    {"id": "30", "name": "Convent Station"},
    {"id": "32", "name": "Cranford"},
    {"id": "33", "name": "Delawanna"},
    {"id": "34", "name": "Denville"},
    {"id": "35", "name": "Dover"},
    {"id": "36", "name": "Dunellen"},
    {"id": "37", "name": "East Orange"},
    {"id": "38", "name": "Edison"},
    {"id": "39", "name": "Egg Harbor City"},
    {"id": "40", "name": "Elberon"},
    {"id": "41", "name": "Elizabeth"},
    {"id": "42", "name": "Emerson"},
    {"id": "43", "name": "Essex Street"},
    {"id": "44", "name": "Fanwood"},
    {"id": "45", "name": "Far Hills"},
    {"id": "46", "name": "Garfield"},
    {"id": "47", "name": "Garwood"},
    {"id": "48", "name": "Gillette"},
    {"id": "49", "name": "Gladstone"},
    {"id": "50", "name": "Glen Ridge"},
    {"id": "51", "name": "Glen Rock Boro Hall"},
    {"id": "52", "name": "Glen Rock Main Line"},
    {"id": "54", "name": "Hackettstown"},
    {"id": "32905", "name": "Hamilton"},
    {"id": "55", "name": "Hammonton"},
    {"id": "57", "name": "Harriman"},
    {"id": "58", "name": "Hawthorne"},
    {"id": "59", "name": "Hazlet"},
    {"id": "60", "name": "High Bridge"},
    {"id": "61", "name": "Highland Avenue"},
    {"id": "62", "name": "Hillsdale"},
    {"id": "64", "name": "Ho-Ho-Kus"},
    {"id": "63", "name": "Hoboken"},
    {"id": "32906", "name": "Jersey Avenue"},
    {"id": "66", "name": "Kingsland"},
    {"id": "67", "name": "Lake Hopatcong"},
    {"id": "68", "name": "Lebanon"},
    {"id": "69", "name": "Lincoln Park"},
    {"id": "70", "name": "Linden"},
    {"id": "71", "name": "Lindenwold"},
    {"id": "72", "name": "Little Falls"},
    {"id": "73", "name": "Little Silver"},
    {"id": "74", "name": "Long Branch"},
    {"id": "75", "name": "Lyndhurst"},
    {"id": "76", "name": "Lyons"},
    {"id": "77", "name": "Madison"},
    {"id": "78", "name": "Mahwah"},
    {"id": "79", "name": "Manasquan"},
    {"id": "81", "name": "Maplewood"},
    {"id": "40570", "name": "Meadowlands Sports Complex"},
    {"id": "83", "name": "Metropark"},
    {"id": "84", "name": "Metuchen"},
    {"id": "85", "name": "Middletown New Jersey"},
    {"id": "86", "name": "Middletown New York"},
    {"id": "87", "name": "Millburn"},
    {"id": "88", "name": "Millington"},
    {"id": "31696", "name": "Monmouth Park"},
    {"id": "89", "name": "Montclair Heights"},
    {"id": "38081", "name": "Montclair State University"},
    {"id": "90", "name": "Montvale"},
    {"id": "91", "name": "Morris Plains"},
    {"id": "92", "name": "Morristown"},
    {"id": "39472", "name": "Mount Arlington"},
    {"id": "93", "name": "Mount Olive"},
    {"id": "94", "name": "Mount Tabor"},
    {"id": "95", "name": "Mountain Avenue"},
    {"id": "96", "name": "Mountain Lakes"},
    {"id": "97", "name": "Mountain Station"},
    {"id": "98", "name": "Mountain View"},
    {"id": "99", "name": "Murray Hill"},
    {"id": "100", "name": "Nanuet"},
    {"id": "101", "name": "Netcong"},
    {"id": "102", "name": "Netherwood"},
    {"id": "110", "name": "New Bridge Landing"},
    {"id": "103", "name": "New Brunswick"},
    {"id": "104", "name": "New Providence"},
    {"id": "105", "name": "New York Penn Station"},
    {"id": "37953", "name": "Newark Airport"},
    {"id": "106", "name": "Newark Broad Street"},
    {"id": "107", "name": "Newark Penn Station"},
    {"id": "108", "name": "North Branch"},
    {"id": "109", "name": "North Elizabeth"},
    {"id": "111", "name": "Oradell"},
    {"id": "112", "name": "Orange"},
    {"id": "113", "name": "Otisville"},
    {"id": "114", "name": "Park Ridge"},
    {"id": "115", "name": "Passaic"},
    {"id": "116", "name": "Paterson"},
    {"id": "117", "name": "Peapack"},
    {"id": "118", "name": "Pearl River"},
    {"id": "43298", "name": "Pennsauken Transit Center"},
    {"id": "119", "name": "Perth Amboy"},
    {"id": "1", "name": "Philadelphia 30th Street"},
    {"id": "120", "name": "Plainfield"},
    {"id": "121", "name": "Plauderville"},
    {"id": "122", "name": "Point Pleasant Beach"},
    {"id": "123", "name": "Port Jervis"},
    {"id": "124", "name": "Princeton"},
    {"id": "125", "name": "Princeton Junction"},
    {"id": "126", "name": "Radburn"},
    {"id": "127", "name": "Rahway"},
    {"id": "128", "name": "Ramsey"},
    {"id": "38417", "name": "Ramsey Route 17"},
    {"id": "129", "name": "Raritan"},
    {"id": "130", "name": "Red Bank"},
    {"id": "131", "name": "Ridgewood"},
    {"id": "132", "name": "River Edge"},
    {"id": "31", "name": "Roselle Park"},
    {"id": "134", "name": "Rutherford"},
    {"id": "135", "name": "Salisbury Mills Cornwall"},
    {"id": "38174", "name": "Secaucus Junction"},
    {"id": "136", "name": "Short Hills"},
    {"id": "137", "name": "Sloatsburg"},
    {"id": "138", "name": "Somerville"},
    {"id": "139", "name": "South Amboy"},
    {"id": "140", "name": "South Orange"},
    {"id": "141", "name": "Spring Lake"},
    {"id": "142", "name": "Spring Valley"},
    {"id": "143", "name": "Stirling"},
    {"id": "144", "name": "Suffern"},
    {"id": "145", "name": "Summit"},
    {"id": "146", "name": "Teterboro"},
    {"id": "147", "name": "Towaco"},
    {"id": "148", "name": "Trenton Transit Center"},
    {"id": "149", "name": "Tuxedo"},
    {"id": "38105", "name": "Union"},
    {"id": "150", "name": "Upper Montclair"},
    {"id": "151", "name": "Waldwick"},
    {"id": "152", "name": "Walnut Street"},
    {"id": "153", "name": "Watchung Avenue"},
    {"id": "154", "name": "Watsessing Avenue"},
    {"id": "39635", "name": "Wayne/Route 23 Transit Center"},
    {"id": "43599", "name": "Wesmont "},
    {"id": "155", "name": "Westfield"},
    {"id": "156", "name": "Westwood"},
    {"id": "157", "name": "White House"},
    {"id": "160", "name": "Wood Ridge"},
    {"id": "158", "name": "Woodbridge"},
    {"id": "159", "name": "Woodcliff Lake"},]

def get_location(station_id):
    response = requests.get(f"http://www.njtransit.com/rg/rg_servlet.srv?hdnPageAction=TrainStationLookupFrom&selStation={station_id}")
    match = re.search(r"var stationPoint = new google.maps.LatLng\(([-+]?\d+\.\d+),([-+]?\d+\.\d+)\);", response.text)
    latitude, longitude = [float(x) for x in match.groups()]
    return (latitude, longitude,)

if __name__ == "__main__":

    stations = []

    for station in light_rail_stations:
        station_id = station['id']
        station['location'] = get_location(station_id)
        station['type'] = 'light_rail'
        stations.append(station)

    for station in train_stations:
        station_id = station['id']
        station['location'] = get_location(station_id)
        station['type'] = 'rail'
        stations.append(station)

    for station in bus_stations:
        station_id = station['id']
        station['location'] = get_location(station_id)
        station['type'] = 'bus'
        stations.append(station)

    with open('park_and_rides.json', 'w') as f:
        json.dump(stations, f)
import os
import json
import datetime
import shapefile
from json import dumps

def shape2json(fname, outfile):
    reader = shapefile.Reader(fname)
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]

    buffer = []
    for sr in reader.shapeRecords():
        atr = dict(zip(field_names, sr.record))
        geom = sr.shape.__geo_interface__
        buffer.append(dict(type="Feature", geometry=geom, properties=atr))
            
    for record in buffer:
        for key in record['properties']:
            if type(record['properties'][key]) is datetime.date:
                record['properties'][key] = record['properties'][key].isoformat()

    with open(outfile, "w") as geojson:
       geojson.write(dumps({"type": "FeatureCollection",
                            "features": buffer}, indent=2) + "\n")

if __name__ == "__main__":

    shape2json('NJ_Rail_shp/Tran_railroad_passenger.shp',
                outfile='Tran_railroad_passenger.json')

    shape2json('NJ_Rail_shp/Tran_railroad_station.shp',
                outfile='Tran_railroad_station.json')

import os
import json
import datetime
import pyproj
import shapefile
from json import dumps

# http://spatialreference.org/ref/esri/nad-1983-stateplane-new-jersey-fips-2900-feet/proj4/

# http://proj4.org/parameters.html#false-easting-northing
# Note that these values are always expressed in meters even
# if the coordinate system is some other units.

pnj = pyproj.Proj(
    proj='tmerc',
    datum='NAD83',
    ellps='GRS80',
    units='us-ft',
    lon_0=-74.5, # longitude of the central meridian
    lat_0=38.83333333333334, # latitude of projection origin
    x_0=150000, # false easting (492125.0 ft to m = 150000)
    y_0=0.0, # false northing
    k_0=0.9999, # scaling factor at central meridian
    preserve_units=True, # do not force to be meters,
    no_defs=True, # don't use defaults file
    )


def shape2json(fname, outfile):
    reader = shapefile.Reader(fname)
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]

    buffer = []
    for sr in reader.shapeRecords():
        atr = dict(zip(field_names, sr.record))
        geom = sr.shape.__geo_interface__
        if geom['type'] in ['Point']:
            geom['coordinates'] = pnj(geom['coordinates'][0], geom['coordinates'][1], inverse=True)
        elif geom['type'] in ['LineString']:
            geom['coordinates'] = [pnj(x, y, inverse=True) for (x, y,) in geom['coordinates']]
        elif geom['type'] == 'MultiLineString':
            new_coordinates = []
            for points in geom['coordinates']:
                new_points = [pnj(x, y, inverse=True) for (x, y,) in points]
                new_coordinates.append(new_points)
            geom['coordinates'] = new_coordinates
        else:
            raise Exception(f'unknown geojson type {geom["type"]}')
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

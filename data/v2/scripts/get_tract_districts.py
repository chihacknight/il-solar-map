import csv
import json
import requests_cache
import tqdm
from shapely.geometry import shape, Point
from shapely.geometry.polygon import Polygon

session = requests_cache.CachedSession('geocoding_cache')

centroids = []

with open("../raw/unique-tracts.csv", 'r') as csvfile:
    tracts = csv.DictReader(csvfile)
    for tract in tqdm.tqdm(tracts):
        tract_id = tract['census_tract']

        url = f"https://tigerweb.geo.census.gov/arcgis/rest/services/Census2020/tigerWMS_Census2020/MapServer/6/query?where=GEOID%3D%27{tract_id}%27&text=&objectIds=&time=&timeRelation=esriTimeRelationOverlaps&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&distance=&units=esriSRUnit_Foot&relationParam=&outFields=CENTLON%2CCENTLAT&returnGeometry=false&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&havingClause=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&historicMoment=&returnDistinctValues=false&resultOffset=&resultRecordCount=&returnExtentOnly=false&sqlFormat=none&datumTransformation=&parameterValues=&rangeValues=&quantizationParameters=&featureEncoding=esriDefault&f=pjson"
        
        response = session.get(url)
        data = response.json()

        try:
          centroid = data['features'][0]['attributes']
          centroid['GEOID'] = tract_id
          centroids.append(centroid)
        except IndexError:
          print(f"Error looking up: {tract_id}")
          continue

print(len(centroids),"centroids found")

house_districts = {}
with open("../raw/il_house_2023.geojson", "r") as geojsonfile: 
    house_geojson_src = json.load(geojsonfile)["features"]
    for h in house_geojson_src:
        house_districts[h["properties"]["DISTRICT"]] = shape(h["geometry"])

print(len(house_districts), "house districts found")

senate_districts = {}
with open("../raw/il_senate_2023.geojson", "r") as geojsonfile: 
    senate_geojson_src = json.load(geojsonfile)["features"]
    for h in senate_geojson_src:
        senate_districts[h["properties"]["DISTRICT"]] = shape(h["geometry"])

print(len(senate_districts), "house districts found")

for centroid in centroids:
    point = (centroid['CENTLON'], centroid['CENTLAT'])
    for district in house_districts:
        if house_districts[district].contains(Point([point])):
            centroid['house_district'] = district
            break
    for district in senate_districts:
        if senate_districts[district].contains(Point([point])):
            centroid['senate_district'] = district
            break

output = []
# write out to projects csv
with open("../final/all-projects.csv", 'r') as csvfile:
    projects = csv.DictReader(csvfile)
    for row in projects:
        tract_id = row["census_tract"]
        for centroid in centroids:
            if centroid['GEOID'] == tract_id:
                o = dict(row)
                o['house_district'] = centroid.get('house_district',None)
                o['senate_district'] = centroid.get('senate_district',None)
                output.append(o)
                break

with open("../final/all-projects-w-districts.csv", "w") as outfile:    
    writer = csv.writer(outfile)
    writer.writerow(output[0].keys())
    for r in output:
        writer.writerow([r[field] for field in r.keys()])
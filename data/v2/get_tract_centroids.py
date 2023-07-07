import csv
import json
import requests
import tqdm

data = {}

tract_geojson = { 
    "type": "FeatureCollection",
    "features": [] }
features = tract_geojson['features']

with open("raw/unique-tracts.csv", 'r') as csvfile:
    tracts = csv.DictReader(csvfile)
    for tract in tqdm.tqdm(tracts):
        tract_id = tract['census_tract']

        url = f"https://tigerweb.geo.census.gov/arcgis/rest/services/Census2020/tigerWMS_Census2020/MapServer/6/query?where=GEOID%3D%27{tract_id}%27&text=&objectIds=&time=&timeRelation=esriTimeRelationOverlaps&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&distance=&units=esriSRUnit_Foot&relationParam=&outFields=CENTLON%2CCENTLAT&returnGeometry=false&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&havingClause=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&historicMoment=&returnDistinctValues=false&resultOffset=&resultRecordCount=&returnExtentOnly=false&sqlFormat=none&datumTransformation=&parameterValues=&rangeValues=&quantizationParameters=&featureEncoding=esriDefault&f=pjson"
        
        response = requests.get(url)
        data = response.json()

        try:
          centroid = data['features'][0]['attributes']
        except IndexError:
          print(f"Error looking up: {tract_id}")
          continue

        feature = { 
          "type": "Feature",
          "geometry": {"type": "Point", "coordinates": [float(centroid['CENTLON']), float(centroid['CENTLAT'])]},
          "properties": {"census_tract": tract_id}
          }

        features.append(feature)

with open("raw/census_tract_centroids.geojson", 'w') as f:
    json.dump(tract_geojson, f)
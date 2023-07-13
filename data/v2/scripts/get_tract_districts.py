import csv
import requests_cache
import tqdm

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
          centroids.append(centroid)
        except IndexError:
          print(f"Error looking up: {tract_id}")
          continue

print(len(centroids,"centroids found"))
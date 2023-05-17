import csv
import json

data = {}
county_index = 15
ac_kwh_index = 8

jsonreader = ""

with open('data/report-3-census-tract-rev.csv', "r") as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:

        raw_county_name = row[county_index]

        county_name = raw_county_name.upper().replace(" COUNTY", "")

        if(county_name=="COUNTY"):
            continue

        if county_name in data:
            data[county_name][0] += 1
            data[county_name][1] += float(row[ac_kwh_index])
        else:
            data[county_name] = [1, float(row[ac_kwh_index])]


with open("data/boundaries/il_counties.geojson") as jsonfile:
    jsonreader = json.load(jsonfile)

    for key, arr in data.items():
        for county in jsonreader["features"]:
            if county["properties"]["COUNTY_NAM"] == key:
                county["properties"]["NUM_SOLAR"] = arr[0]
                county["properties"]["TOTAL_KWH"] = arr[1]

with open("data/boundaries/il_counties_with_solar_info.geojson", "w") as outfile:
    json.dump(jsonreader, outfile)

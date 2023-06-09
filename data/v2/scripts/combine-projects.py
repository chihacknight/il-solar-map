import csv
import json
import requests_cache
import tqdm

session = requests_cache.CachedSession('geocoding_cache')

def get_category(size_str):
    try:
        size = float(size_str)
    except ValueError:
        size = 0

    if size <= 25:
        return "Small_DG"
    else:
        return "Large_DG"


def get_census_tract(lat, long):
    try:
        r = session.get(
            f"https://geocoding.geo.census.gov/geocoder/geographies/coordinates?benchmark=4&format=json&vintage=4&x={lat}&y={long}")

        json_val = r.json()
        return json_val["result"]["geographies"]["Census Tracts"][0]["GEOID"]

    except TypeError:
        print("Failed to find census tract")
        return "00000"


projects = []

jsonreader_eia = ""

with open('../raw/report-3-census-tract-rev.csv', "r") as report_3_file:
    datareader_report_3 = csv.DictReader(report_3_file)

    for row in datareader_report_3:
        cur_project = {}

        cur_project["source_file"] = "report-3-census-tract-rev.csv"
        cur_project["kw"] = float(row["Project Size AC kW"])
        cur_project["census_tract"] = row["Census Tract"]
        cur_project["category"] = row["CEJA Category"]

        if row["CEJA Category"] == "CS":
            cur_project["category"] = "CS"
        else:
            cur_project["category"] = get_category(row["Project Size AC kW"])

        cur_project["county"] = row["County FIPS"][2:]

        projects.append(cur_project)

with open('../raw/ilsfa-2023-05-07.csv', "r") as ilsfa_file:
    datareader_ilsfa = csv.DictReader(ilsfa_file)

    for row in datareader_ilsfa:
        cur_project = {}

        cur_project["source_file"] = "ilsfa-2023-05-07.csv"
        cur_project["kw"] = float(row["Project Size (AC kW) (P2F)"])
        cur_project["census_tract"] = row["Census Tract"]
        cur_project["county"] = row["Census Tract"][2:5]
        cur_project["category"] = get_category(
            row["Project Size (AC kW) (P2F)"])

        projects.append(cur_project)

with open("../raw/solar-eia-plants_1677797680150.geojson") as eiafile:
    jsonreader_eia = json.load(eiafile)

    for row in tqdm.tqdm(jsonreader_eia["features"]):
        cur_project = {}

        if row["properties"]["StateName"] != "Illinois":
            continue

        lat, long = row["geometry"]["coordinates"]

        cur_project["source_file"] = "solar-eia-plants_1677797680150.geojson"
        cur_project["kw"] = row["properties"]["Total_MW"]
        cur_project["census_tract"] = get_census_tract(lat, long)
        cur_project["county"] = cur_project["census_tract"][2:5]
        cur_project["category"] = "Utility"

        projects.append(cur_project)

with open("../final/all-projects.csv", "w") as projectfile:
    fields = ["source_file", "kw", "census_tract", "county", "category"]
    writer = csv.DictWriter(projectfile, fieldnames=fields)
    writer.writeheader()
    for vals in projects:
        writer.writerow(vals)

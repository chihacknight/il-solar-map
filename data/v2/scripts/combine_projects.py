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

    except KeyError:
        print("Failed to find census tract", lat, long)
        return "00000"


projects = []

jsonreader_eia = ""

with open('../raw/report-3-census-tract-rev.csv', "r") as report_3_file:
    datareader_report_3 = csv.DictReader(report_3_file)

    for row in datareader_report_3:
        if row["Census Tract"] == "N/A":
            continue
        
        cur_project = {}

        cur_project["source_file"] = "report-3-census-tract-rev.csv"
        cur_project["kw"] = float(row["Project Size AC kW"])
        cur_project["census_tract"] = row["Census Tract"]
        cur_project["category"] = row["CEJA Category"]
        cur_project["energization_date"] = row["Part II Application Verification/ Energization Date"]

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
        cur_project["energization_date"] = row["Date of System Energization"]

        projects.append(cur_project)

with open("../raw/EIA-860M-2023-may-solar-IL.csv") as eiafile:
    datareader_eia = csv.DictReader(eiafile)

    for row in datareader_eia:
        cur_project = {}

        cur_project["source_file"] = "EIA-860M-2023-may-solar-IL.csv"
        cur_project["kw"] = round(float(row["Nameplate Capacity (MW)"])) * 1000 # Convert MW to kW
        # note that the EIA data has lat/long columns swapped
        cur_project["census_tract"] = get_census_tract(row['Longitude'], row['Latitude'])
        cur_project["county"] = cur_project["census_tract"][2:5]
        cur_project["category"] = "Utility"
        cur_project["energization_date"] = f"{row['Operating Month']}/1/{row['Operating Year']}"

        projects.append(cur_project)

with open("../final/all-projects.csv", "w") as projectfile:
    fields = ["source_file", "kw", "census_tract", "county", "category", "energization_date"]
    writer = csv.DictWriter(projectfile, fieldnames=fields)
    writer.writeheader()
    for vals in projects:
        writer.writerow(vals)

# search for duplicates
print("Searching for duplicates...")
for p in projects:
    if p["category"] in ["CS", "Utility"]:
        for p2 in projects:
            if p2["category"] in ["CS", "Utility"]:
                if p["census_tract"] == p2["census_tract"] \
                and p["kw"] == p2["kw"] \
                and p["energization_date"] == p2["energization_date"] \
                and p["source_file"] != p2["source_file"]:
                    print("Potential duplicate:", p, p2)

print("Done combining files")
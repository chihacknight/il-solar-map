import csv
import json

data = {}
projects_dict = {}

# key: type (ilsfa, eia, report-3) value: array of projects
# project id, source file, kw, census tract, category, county


def get_category(size_str):
    try:
        size = float(size_str)
    except ValueError:
        size = 0

    if size <= 25:
        return "Small_DG"
    else:
        return "Large_DG"


projects = []

jsonreader_eia = ""

with open('raw/report-3-census-tract-rev.csv', "r") as report_3_file:
    datareader_report_3 = csv.DictReader(report_3_file)

    for row in datareader_report_3:
        cur_project = {}

        cur_project["source_file"] = "report-3-census-tract-rev.csv"
        cur_project["kw"] = row["Project Size AC kW"]
        cur_project["census_tract"] = row["Census Tract"]
        cur_project["category"] = row["CEJA Category"]

        if row["CEJA Category"] == "CS":
            cur_project["category"] = "CS"
        else:
            cur_project["category"] = get_category(row["Project Size AC kW"])

        cur_project["county"] = row["County FIPS"]

        projects.append(cur_project)

with open('raw/ilsfa-2023-05-07.csv', "r") as ilsfa_file:
    datareader_ilsfa = csv.DictReader(ilsfa_file)

    for row in datareader_ilsfa:
        cur_project = {}

        cur_project["source_file"] = "ilsfa-2023-05-07.csv"
        cur_project["kw"] = row["Project Size (AC kW) (P2F)"]
        cur_project["census_tract"] = row["Census Tract"]
        cur_project["county"] = row["Census Tract"][2:5]
        cur_project["category"] = get_category(
            row["Project Size (AC kW) (P2F)"])

        projects.append(cur_project)

with open("raw/solar-eia-plants_1677797680150.geojson") as eiafile:
    jsonreader_eia = json.load(eiafile)

    for row in jsonreader_eia["features"]:
        cur_project = {}

        if row["properties"]["StateName"] != "Illinois":
            continue

        cur_project["source_file"] = "solar-eia-plants_1677797680150.geojson"
        cur_project["kw"] = row["properties"]["Total_MW"]
        cur_project["census_tract"] = ""
        cur_project["county"] = ""
        cur_project["category"] = "Utility"

        projects.append(cur_project)


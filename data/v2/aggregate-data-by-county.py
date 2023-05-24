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

jsonreader = ""

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

print(projects.__len__())
# with open("data/raw/il_counties.geojson") as jsonfile:
#     jsonreader = json.load(jsonfile)

#     for key, arr in data.items():
#         for county in jsonreader["features"]:
#             if county["properties"]["COUNTY_NAM"] == key:
#                 county["properties"]["NUM_SOLAR"] = arr[0]
#                 county["properties"]["TOTAL_KWH"] = arr[1]

# with open("data/final/il_counties_with_solar_info.geojson", "w") as outfile:
#     json.dump(jsonreader, outfile)

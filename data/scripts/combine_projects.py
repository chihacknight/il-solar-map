import csv
import requests_cache

IL_ABP_FILE = "ilabp"
IL_SFA_FILE = "ilsfa"
EIA_FILE = "eia860"

session = requests_cache.CachedSession('geocoding_cache')

def get_category(size_str):
    """The source data categories are unreliable, so we assign a category 
    based on the kW size of the project. 25 kW and smaller is Small 
    Distributed Distribution."""
    try:
        size = float(size_str)
    except ValueError:
        size = 0

    if size <= 25:
        return "Small_DG"
    else:
        return "Large_DG"
    

def clean_number(num_str):
    """remove number formatting and convert nulls to 0"""
    try:
        num_str = num_str.replace(',', '')
        num = float(num_str)
    except ValueError:
        num = 0

    return num


def get_census_tract(lat, long):
    """use the census geocoder to find a tract based on lat/long"""
    try:
        r = session.get(
            f"https://geocoding.geo.census.gov/geocoder/geographies/coordinates?benchmark=4&format=json&vintage=4&x={lat}&y={long}")

        json_val = r.json()
        return json_val["result"]["geographies"]["Census Tracts"][0]["GEOID"]

    except KeyError:
        print("Failed to find census tract", lat, long)
        return "00000"


projects = []
energized_project_ids = set()
planned_projects = []

jsonreader_eia = ""

for project_type in ("energized", "planned"):
    print("combining", project_type, "projects")
    print("Reading ABP data...")

    file_suffix = ""
    if project_type == "planned":
        file_suffix = "_planned"

    with open(f"../raw/{IL_ABP_FILE}{file_suffix}.csv") as report_3_file:
        datareader_report_3 = csv.DictReader(report_3_file)

        for row in datareader_report_3:
            
            # energized projects are not removed from the planned report, so skip them here
            if project_type == "planned":
                if row["Application ID"] in energized_project_ids:
                    continue
            else:
                energized_project_ids.add(row["Application ID"])

            if row["Census Tract Code"] == "N/A" or row["Project Size AC kW"] == "":
                continue
            
            cur_project = {}

            cur_project["source_file"] = IL_ABP_FILE
            cur_project["kw"] = clean_number(row["Project Size AC kW"])
            cur_project["census_tract"] = row["Census Tract Code"]
            if project_type == "planned":
                cur_project["energization_date"] = row["Scheduled Energization Date"]
            else:
                cur_project["energization_date"] = row["Part II Application Verification/ Energization Date"]

            if "CEJA Category" in row.keys() and row["CEJA Category"] == "CS":
                cur_project["category"] = "CS"
            else:
                cur_project["category"] = get_category(row["Project Size AC kW"])

            cur_project["county"] = row["Census Tract Code"][2:5]

            if project_type == "planned":
                planned_projects.append(cur_project)
            else:
                projects.append(cur_project)

    print("Reading IL SFA data...")
    with open(f"../raw/{IL_SFA_FILE}{file_suffix}.csv") as ilsfa_file:
        datareader_ilsfa = csv.DictReader(ilsfa_file)

        for row in datareader_ilsfa:
            
            # energized projects are not removed from the planned report, so skip them here
            if project_type == "planned":
                if row["Project ID"] in energized_project_ids:
                    continue
            else:
                energized_project_ids.add(row["Project ID"])

            cur_project = {}

            cur_project["source_file"] = IL_SFA_FILE
            cur_project["kw"] = clean_number(row["Project Size AC kW"])
            cur_project["census_tract"] = row["Census Tract"]
            cur_project["county"] = row["Census Tract"][2:5]
            cur_project["category"] = get_category(
                row["Project Size AC kW"])
            if project_type == "planned":
                cur_project["energization_date"] = row["Scheduled Energization Deadline"]
            else:
                cur_project["energization_date"] = row["Date of System Energization"]

            if project_type == "planned":
                planned_projects.append(cur_project)
            else:
                projects.append(cur_project)

    print("Reading EIA data...")
    with open(f"../raw/{EIA_FILE}{file_suffix}.csv") as eiafile:
        datareader_eia = csv.DictReader(eiafile)

        # print out top 10 largest by KW
        eia_list = list(datareader_eia)
        sorted_eia_list = sorted(eia_list, key=lambda x: clean_number(x['Nameplate Capacity (MW)']), reverse=True)
        cnt = 1
        top_entries = []
        for r in sorted_eia_list:
            if r["Plant State"] == "IL" and r["Technology"] == "Solar Photovoltaic" and cnt <= 10:
                te = {
                    "Entity Name": r["Entity Name"],
                    "Plant Name": r["Plant Name"],
                    "County": r["County"],
                    "Nameplate Capacity (MW)": clean_number(r["Nameplate Capacity (MW)"]),
                    "Energization Date": "",
                }
                if project_type == "planned":
                    te["Energization Date"] = f"{r['Planned Operation Month']}/1/{r['Planned Operation Year']}"
                else:
                    te["Energization Date"] = f"{r['Operating Month']}/1/{r['Operating Year']}"

                top_entries.append(te)
                cnt += 1

        print(f'writing to top-10-projects{file_suffix}.csv')
        with open(f"../final/top-10-projects{file_suffix}.csv", "w") as projectfile:
            fieldnames = ["Plant Name", "Entity Name", "County", "Nameplate Capacity (MW)", "Energization Date"]
            writer = csv.DictWriter(projectfile, fieldnames=fieldnames)
            writer.writeheader()
            for vals in top_entries:
                writer.writerow(vals)

        for row in eia_list:
            
            # data is for entire US, so filter to IL
            if row["Plant State"] == "IL" and row["Technology"] == "Solar Photovoltaic":
                cur_project = {}

                cur_project["source_file"] = EIA_FILE
                cur_project["kw"] = round(clean_number(row["Nameplate Capacity (MW)"]) * 1000) # Convert MW to kW
                # note that the EIA data has lat/long columns swapped
                cur_project["census_tract"] = get_census_tract(row['Longitude'], row['Latitude'])
                cur_project["county"] = cur_project["census_tract"][2:5]
                cur_project["category"] = "Utility"
                if project_type == "planned":
                    cur_project["energization_date"] = f"{row['Planned Operation Month']}/1/{row['Planned Operation Year']}"
                else:
                    cur_project["energization_date"] = f"{row['Operating Month']}/1/{row['Operating Year']}"

                if project_type == "planned":
                    planned_projects.append(cur_project)
                else:
                    projects.append(cur_project)

    print(f'writing to all-projects{file_suffix}.csv')
    with open(f"../final/all-projects{file_suffix}.csv", "w") as projectfile:
        fields = ["source_file", "kw", "census_tract", "county", "category", "energization_date"]
        writer = csv.DictWriter(projectfile, fieldnames=fields)
        writer.writeheader()
        if project_type == "planned":
            for vals in planned_projects:
                writer.writerow(vals)
        else:
            for vals in projects:
                writer.writerow(vals)

    print("Done combining files")
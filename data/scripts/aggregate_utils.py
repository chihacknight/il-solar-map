import csv
import json
import pandas as pd
import hashlib

def init_aggregate(row):
    """initialize an aggregate row"""
    agg = {}
    agg["dg_small_kw"] = 0
    agg["dg_small_count"] = 0
    agg["dg_large_kw"] = 0
    agg["dg_large_count"] = 0
    agg["cs_kw"] = 0
    agg["cs_count"] = 0
    agg["utility_kw"] = 0
    agg["utility_count"] = 0
    agg["total_kw"] = 0
    agg["total_count"] = 0

    agg["planned_dg_small_kw"] = 0
    agg["planned_dg_small_count"] = 0
    agg["planned_dg_large_kw"] = 0
    agg["planned_dg_large_count"] = 0
    agg["planned_cs_kw"] = 0
    agg["planned_cs_count"] = 0
    agg["planned_utility_kw"] = 0
    agg["planned_utility_count"] = 0
    agg["planned_total_kw"] = 0
    agg["planned_total_count"] = 0
    
    prefix = ""
    if row["type"] == "planned":
        prefix = "planned_"
        
    if row["category"] == "Small_DG":
        agg[f"{prefix}dg_small_kw"] = round(float(row["kw"]))
        agg[f"{prefix}dg_small_count"] = 1
    elif row["category"] == "Large_DG":
        agg[f"{prefix}dg_large_kw"] = round(float(row["kw"]))
        agg[f"{prefix}dg_large_count"] = 1
    elif row["category"] == "CS":
        agg[f"{prefix}cs_kw"] = round(float(row["kw"]))
        agg[f"{prefix}cs_count"] = 1
    elif row["category"] == "Utility":
        agg[f"{prefix}utility_kw"] = round(float(row["kw"]))
        agg[f"{prefix}utility_count"] = 1
    
    agg[f"{prefix}total_kw"] = round(float(row["kw"]))
    agg[f"{prefix}total_count"] = 1

    return agg

def increment_aggregate(agg, row):
    """increment values for an aggregate row"""
    prefix = ""
    if row["type"] == "planned":
        prefix = "planned_"
    
    if row["category"] == "Small_DG":
        agg[f"{prefix}dg_small_kw"] += round(float(row["kw"]))
        agg[f"{prefix}dg_small_count"] += 1
    elif row["category"] == "Large_DG":
        agg[f"{prefix}dg_large_kw"] += round(float(row["kw"]))
        agg[f"{prefix}dg_large_count"] += 1
    elif row["category"] == "CS":
        agg[f"{prefix}cs_kw"] += round(float(row["kw"]))
        agg[f"{prefix}cs_count"] += 1
    elif row["category"] == "Utility":
        agg[f"{prefix}utility_kw"] += round(float(row["kw"]))
        agg[f"{prefix}utility_count"] += 1
    
    agg[f"{prefix}total_kw"] += round(float(row["kw"]))
    agg[f"{prefix}total_count"] += 1

    return agg

def aggregate_projects(items, index, index_name):
    """iterates through all projects and aggregates by a given geography"""
    projects = []
    planned_projects = []
    
    with open("../final/all-projects-w-districts.csv", 'r') as csvfile:
        projects = list(csv.DictReader(csvfile))

    with open("../final/all-projects_planned-w-districts.csv", 'r') as csvfile:
        planned_projects = list(csv.DictReader(csvfile))
        
    all_projects = projects + planned_projects
        
    for row in all_projects:
        if index == "county":
            try:
                idx = int(row["county"])
            except ValueError:
                continue
        else:
            idx = row[index]
        
        if idx not in items:
            i = init_aggregate(row)
            i[index_name] = idx
            items[idx] = i
        else:
            i = items[idx]
            i = increment_aggregate(i, row)
            continue

def write_csv(items, fields, filename):
    """output aggregates as a csv file"""
    with open(filename, "w") as outfile:    
        writer = csv.writer(outfile)
        writer.writerow(fields)
        for key, value in items.items():
            writer.writerow([value[field] for field in fields])

def text_to_int(text):
    # Use SHA-256 hash to ensure a deterministic and stable hash value
    hash_object = hashlib.sha256(text.encode('utf-8'))
    hash_hex = hash_object.hexdigest()
    # Convert the hexadecimal hash to an integer
    return int(hash_hex, 16) % 100000

def write_geojson(geosource, key, items, geoout):
    """output aggregates as a geojson file"""
    out_geojson = { 
        "type": "FeatureCollection",
        "features": [] }
    out_features = out_geojson['features']

    with open(geosource, "r") as geojsonfile: 
        geojson_src = json.load(geojsonfile)["features"]
        for g in geojson_src:
            item = g["properties"][key]
            id_key = item
            # for places, convert the NAMELSAD20 field to a number id
            # todo - make this deterministic
            if key == "NAMELSAD20":
                id_key = text_to_int(item)

            if item in items:
                item_data = items[item]
            else:
                item_data = init_aggregate({"kw": 0, "category": "None", "type": "energized"})
                item_data["total_count"] = 0
                if key == "GEOID10":
                    item_data["census_tract"] = item

            feature = { 
                "type": "Feature",
                "geometry": g["geometry"],
                "id": id_key,
                "properties": item_data
            }
            out_features.append(feature)

    with open(geoout, "w") as outfile:
        json.dump(out_geojson, outfile)

def aggregate_all_projects(type):
    """calculate totals across the entire state for about page"""

    prefix = ""
    file_prefix = ""
    if type == "planned":
        prefix = "planned_"
        file_prefix = "_planned"

    all_projects = {}
    with open(f"../final/all-projects{file_prefix}-w-districts.csv", 'r') as csvfile:
        projects = csv.DictReader(csvfile)
        for cnt, row in enumerate(projects):
          row["type"] = type  
          if cnt == 0:
              all_projects = init_aggregate(row)
          else:
              increment_aggregate(all_projects, row)

    print(all_projects)

    all_projects[f"{prefix}dg_small_pct"] = round(all_projects[f"{prefix}dg_small_kw"] / all_projects[f"{prefix}total_kw"] * 100, 1)
    all_projects[f"{prefix}dg_large_pct"] = round(all_projects[f"{prefix}dg_large_kw"] / all_projects[f"{prefix}total_kw"] * 100, 1)
    all_projects[f"{prefix}cs_pct"] = round(all_projects[f"{prefix}cs_kw"] / all_projects[f"{prefix}total_kw"] * 100, 1)
    all_projects[f"{prefix}utility_pct"] = round(all_projects[f"{prefix}utility_kw"] / all_projects[f"{prefix}total_kw"] * 100, 1)

    # convert to MW
    all_projects[f"{prefix}dg_small_mw"] = int(str(round(all_projects[f"{prefix}dg_small_kw"],-3))[:-3])
    all_projects[f"{prefix}dg_large_mw"] = int(str(round(all_projects[f"{prefix}dg_large_kw"],-3))[:-3])
    if all_projects[f"{prefix}cs_kw"] > 0:
      all_projects[f"{prefix}cs_mw"] = int(str(round(all_projects[f"{prefix}cs_kw"],-3))[:-3])
    else:
        all_projects[f"{prefix}cs_mw"] = 0
    all_projects[f"{prefix}utility_mw"] = int(str(round(all_projects[f"{prefix}utility_kw"],-3))[:-3])
    all_projects[f"{prefix}total_mw"] = int(str(round(all_projects[f"{prefix}total_kw"],-3))[:-3])

    with open(f"../final/all_projects{file_prefix}_summary.csv", "w") as outfile:    
        writer = csv.writer(outfile)
        writer.writerow(["Category", f"MW {type}", "Percent", "Project count"])
        writer.writerow(["Utility", f'{all_projects[f"{prefix}utility_mw"]:,d} MW', f'{all_projects[f"{prefix}utility_pct"]}%', f'{all_projects[f"{prefix}utility_count"]:,d}'])
        writer.writerow(["Small DG", f'{all_projects[f"{prefix}dg_small_mw"]:,d} MW', f'{all_projects[f"{prefix}dg_small_pct"]}%', f'{all_projects[f"{prefix}dg_small_count"]:,d}'])
        writer.writerow(["Large DG", f'{all_projects[f"{prefix}dg_large_mw"]:,d} MW', f'{all_projects[f"{prefix}dg_large_pct"]}%', f'{all_projects[f"{prefix}dg_large_count"]:,d}'])
        writer.writerow(["Community Solar", f'{all_projects[f"{prefix}cs_mw"]:,d} MW', f'{all_projects[f"{prefix}cs_pct"]}%', f'{all_projects[f"{prefix}cs_count"]:,d}'])
        writer.writerow(["Total", f'{all_projects[f"{prefix}total_mw"]:,d} MW', '100%', f'{all_projects[f"{prefix}total_count"]:,d}'])
        
def generate_monthly_kw_time_series():
    """calculate aggregated solar by category over time"""
    print("Generating monthly time series...")
    # load csv into pandas dataframe
    all_files = ["../final/all-projects-w-districts.csv", "../final/all-projects_planned-w-districts.csv"]
    df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)

    # set energization_date column to datetime
    df["energization_date"] = pd.to_datetime(df["energization_date"], format='mixed')

    # convert energization_date to first of month
    df["energization_date"] = df["energization_date"].dt.to_period("M").dt.to_timestamp()
    
    # aggregate projects by month and category
    monthly_aggregate = df.groupby(["energization_date", "category"]).agg({"kw": "sum"}).reset_index().sort_values(by=["energization_date"])

    # pivot table to get category columns
    monthly_aggregate = monthly_aggregate.pivot(index="energization_date", columns="category", values="kw").reset_index().fillna(0)

    # calculate cumulative sum of MW by month
    # round to nearest 1000, convert to int to remove decimal value, convert to string, then slice off the last 3 digits
    monthly_aggregate["CS"] = monthly_aggregate["CS"].cumsum().round(-3).astype(int).astype(str).str.slice(0,-3)
    monthly_aggregate["Large_DG"] = monthly_aggregate["Large_DG"].cumsum().round(-3).astype(int).astype(str).str.slice(0,-3)
    monthly_aggregate["Small_DG"] = monthly_aggregate["Small_DG"].cumsum().round(-3).astype(int).astype(str).str.slice(0,-3)
    monthly_aggregate["Utility"] = monthly_aggregate["Utility"].cumsum().round(-3).astype(int).astype(str).str.slice(0,-3)

    # export to csv
    monthly_aggregate.to_csv("../final/monthly-aggregate.csv", index=False)
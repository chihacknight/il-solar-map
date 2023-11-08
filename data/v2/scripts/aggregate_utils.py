import csv
import json

def init_aggregate(row):
    agg = {}
    agg["dg_small_kw"] = 0
    agg["dg_small_count"] = 0
    agg["dg_large_kw"] = 0
    agg["dg_large_count"] = 0
    agg["cs_kw"] = 0
    agg["cs_count"] = 0
    agg["utility_kw"] = 0
    agg["utility_count"] = 0
    
    if row["category"] == "Small_DG":
        agg["dg_small_kw"] = round(float(row["kw"]))
        agg["dg_small_count"] = 1
    elif row["category"] == "Large_DG":
        agg["dg_large_kw"] = round(float(row["kw"]))
        agg["dg_large_count"] = 1
    elif row["category"] == "CS":
        agg["cs_kw"] = round(float(row["kw"]))
        agg["cs_count"] = 1
    elif row["category"] == "Utility":
        agg["utility_kw"] = round(float(row["kw"]))
        agg["utility_count"] = 1
    
    agg["total_kw"] = round(float(row["kw"]))
    agg["total_count"] = 1

    return agg

def increment_aggregate(agg, row):
    if row["category"] == "Small_DG":
        agg["dg_small_kw"] += round(float(row["kw"]))
        agg["dg_small_count"] += 1
    elif row["category"] == "Large_DG":
        agg["dg_large_kw"] += round(float(row["kw"]))
        agg["dg_large_count"] += 1
    elif row["category"] == "CS":
        agg["cs_kw"] += round(float(row["kw"]))
        agg["cs_count"] += 1
    elif row["category"] == "Utility":
        agg["utility_kw"] += round(float(row["kw"]))
        agg["utility_count"] += 1
    
    agg["total_kw"] += round(float(row["kw"]))
    agg["total_count"] += 1

    return agg

def aggregate_projects(items, index, index_name):
    with open("../final/all-projects-w-districts.csv", 'r') as csvfile:
        projects = csv.DictReader(csvfile)
        for row in projects:
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
    with open(filename, "w") as outfile:    
        writer = csv.writer(outfile)
        writer.writerow(fields)
        for key, value in items.items():
            writer.writerow([value[field] for field in fields])

def write_geojson(geosource, key, items, geoout):
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
            if key == "NAMELSAD20":
                id_key = abs(hash(item)) % (10 ** 8)

            if item in items:
                item_data = items[item]
            else:
                item_data = init_aggregate({"kw": 0, "category": "None"})
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

def aggregate_all_projects():
    all_projects = {}
    with open("../final/all-projects-w-districts.csv", 'r') as csvfile:
        projects = csv.DictReader(csvfile)
        for cnt, row in enumerate(projects):     
          if cnt == 0:
              all_projects = init_aggregate(row)
          else:
              increment_aggregate(all_projects, row)

    all_projects["dg_small_pct"] = round(all_projects["dg_small_kw"] / all_projects["total_kw"] * 100, 1)
    all_projects["dg_large_pct"] = round(all_projects["dg_large_kw"] / all_projects["total_kw"] * 100, 1)
    all_projects["cs_pct"] = round(all_projects["cs_kw"] / all_projects["total_kw"] * 100, 1)
    all_projects["utility_pct"] = round(all_projects["utility_kw"] / all_projects["total_kw"] * 100, 1)

    with open("../final/all_projects_summary.csv", "w") as outfile:    
        writer = csv.writer(outfile)
        writer.writerow(["Category", "kW installed", "Percent", "Project count"])
        writer.writerow(["Utility", f'{all_projects["utility_kw"]:,d} kW', f'{all_projects["utility_pct"]}%', f'{all_projects["utility_count"]:,d}'])
        writer.writerow(["Small DG", f'{all_projects["dg_small_kw"]:,d} kW', f'{all_projects["dg_small_pct"]}%', f'{all_projects["dg_small_count"]:,d}'])
        writer.writerow(["Large DG", f'{all_projects["dg_large_kw"]:,d} kW', f'{all_projects["dg_large_pct"]}%', f'{all_projects["dg_large_count"]:,d}'])
        writer.writerow(["Community Solar", f'{all_projects["cs_kw"]:,d} kW', f'{all_projects["cs_pct"]}%', f'{all_projects["cs_count"]:,d}'])
        
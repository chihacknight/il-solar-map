import csv
import json

counties = {}

with open("../final/all-projects.csv", 'r') as csvfile:
    projects = csv.DictReader(csvfile)
    for row in projects:
        try:
            county_index = int(row["county"])
        except ValueError:
            continue
        if county_index not in counties:
            county = {}
            county["county_fips"] = county_index
            county["dg_small_kw"] = 0
            county["dg_small_count"] = 0
            county["dg_large_kw"] = 0
            county["dg_large_count"] = 0
            county["cs_kw"] = 0
            county["cs_count"] = 0
            county["utility_kw"] = 0
            county["utility_count"] = 0
            
            if row["category"] == "Small_DG":
                county["dg_small_kw"] = round(float(row["kw"]))
                county["dg_small_count"] = 1
            elif row["category"] == "Large_DG":
                county["dg_large_kw"] = round(float(row["kw"]))
                county["dg_large_count"] = 1
            elif row["category"] == "CS":
                county["cs_kw"] = round(float(row["kw"]))
                county["cs_count"] = 1
            elif row["category"] == "Utility":
                county["utility_kw"] = round(float(row["kw"]))
                county["utility_count"] = 1
            
            county["total_kw"] = round(float(row["kw"]))
            county["total_count"] = 1

            counties[county_index] = county
        else:
            c = counties[county_index]

            if row["category"] == "Small_DG":
                c["dg_small_kw"] += round(float(row["kw"]))
                c["dg_small_count"] += 1
            elif row["category"] == "Large_DG":
                c["dg_large_kw"] += round(float(row["kw"]))
                c["dg_large_count"] += 1
            elif row["category"] == "CS":
                c["cs_kw"] += round(float(row["kw"]))
                c["cs_count"] += 1
            elif row["category"] == "Utility":
                c["utility_kw"] += round(float(row["kw"]))
                c["utility_count"] += 1
            
            c["total_kw"] += round(float(row["kw"]))
            c["total_count"] += 1
            continue


# save to csv
with open("../final/solar-projects-by-county.csv", "w") as outfile:    
    fields = ["county_fips", "dg_small_kw", "dg_small_count", "dg_large_kw", "dg_large_count", "cs_kw", "cs_count", "utility_kw", "utility_count", "total_kw", "total_count"]
    writer = csv.writer(outfile)
    writer.writerow(fields)
    for key, value in counties.items():
        writer.writerow([value[field] for field in fields])

# save to geojson
county_geojson = { 
    "type": "FeatureCollection",
    "features": [] }
county_features = county_geojson['features']

with open("../raw/il_counties.geojson", "r") as geojsonfile: 
    counties_geojson_src = json.load(geojsonfile)["features"]
    for c in counties_geojson_src:
        county = c["properties"]["CO_FIPS"]
        if county in counties:
            county_data = counties[county]
            feature = { 
                "type": "Feature",
                "geometry": c["geometry"],
                "properties": county_data
            }
            county_features.append(feature)

    
with open("../final/solar-projects-by-county.geojson", "w") as outfile:
    json.dump(county_geojson, outfile)

      

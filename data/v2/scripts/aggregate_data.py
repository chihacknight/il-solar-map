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

def write_csv(items, fields, filename):
    with open(filename, "w") as outfile:    
        writer = csv.writer(outfile)
        writer.writerow(fields)
        for key, value in items.items():
            writer.writerow([value[field] for field in fields])

counties = {}

with open("../final/all-projects-w-districts.csv", 'r') as csvfile:
    projects = csv.DictReader(csvfile)
    for row in projects:
        try:
            county_index = int(row["county"])
        except ValueError:
            continue
        
        # aggregate by county
        if county_index not in counties:
            county = init_aggregate(row)
            county["county_fips"] = county_index
            counties[county_index] = county
        else:
            c = counties[county_index]
            c = increment_aggregate(c, row)
            continue

print("aggregated", len(counties), "counties")

tracts = {}

with open("../final/all-projects.csv", 'r') as csvfile:
    projects = csv.DictReader(csvfile)
    for row in projects:
        tract_index = row["census_tract"]

        # aggregate by tract
        if tract_index not in tracts:
            tract = init_aggregate(row)
            tract["census_tract"] = tract_index
            tracts[tract_index] = tract
        else:
            t = tracts[tract_index]
            t = increment_aggregate(t, row)
            continue

print("aggregated", len(tracts), "tracts")

# save counties to csv
fields = ["county_fips", "dg_small_kw", "dg_small_count", "dg_large_kw", "dg_large_count", "cs_kw", "cs_count", "utility_kw", "utility_count", "total_kw", "total_count"]
write_csv(counties, fields, "../final/solar-projects-by-county.csv")
print('saved counties to csv')

# save counties to geojson
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

print('saved counties to geojson')

# save tracts to csv
fields = ["census_tract", "dg_small_kw", "dg_small_count", "dg_large_kw", "dg_large_count", "cs_kw", "cs_count", "utility_kw", "utility_count", "total_kw", "total_count"]
write_csv(tracts, fields, "../final/solar-projects-by-tract.csv")
print('saved tracts to csv')

# save tracts to geojson
tract_geojson = { 
    "type": "FeatureCollection",
    "features": [] }
tract_features = tract_geojson['features']

with open("../raw/il_2020_census_tracts.geojson", "r") as geojsonfile: 
    tract_geojson_src = json.load(geojsonfile)["features"]
    for t in tract_geojson_src:
        tract = t["properties"]["GEOID10"]
        if tract in tracts:
            tract_data = tracts[tract]
        else:
            tract_data = init_aggregate({"kw": 0, "category": "None"})
        
        feature = { 
            "type": "Feature",
            "geometry": t["geometry"],
            "properties": tract_data
        }
        tract_features.append(feature)

with open("../final/solar-projects-by-tract.geojson", "w") as outfile:
    json.dump(tract_geojson, outfile)

print('saved tracts to geojson')
print('done!')
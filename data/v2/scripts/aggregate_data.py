import csv
import json
import hashlib

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

# aggregate all projects in the state
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
print(all_projects)

# aggregate projects by each geography
counties = {}
aggregate_projects(counties, "county", "county_fips")
print("aggregated", len(counties), "counties")

# create list of County / FIPS lookups and add them to counties
county_fips = {}
with open("../raw/il_counties.geojson", "r") as geojsonfile: 
    geojson_src = json.load(geojsonfile)["features"]
    for g in geojson_src:
        county_fips[g["properties"]["CO_FIPS"]] = g["properties"]["COUNTY_NAM"]

for c in counties:
    counties[c]["county_name"] = county_fips[c]

tracts = {}
aggregate_projects(tracts, "census_tract", "census_tract")
print("aggregated", len(tracts), "tracts")

places = {}
aggregate_projects(places, "place", "place")
print("aggregated", len(tracts), "places")

house_districts = {}
aggregate_projects(house_districts, "house_district", "house_district")
print("aggregated", len(house_districts), "house districts")

# populate house districts with legislators
with open("../raw/il_house_2023_members.csv", "r") as housefile: 
    district_info = csv.DictReader(housefile)
    for h in house_districts:
        house_districts[h]["legislator"] = ""
        house_districts[h]["party"] = ""
        house_districts[h]["date_assumed_office"] = ""
        for di in district_info:
            if di['Office'] == f"Illinois House of Representatives District {h}":
                house_districts[h]["legislator"] = di['Name']
                house_districts[h]["party"] = di['Party']
                house_districts[h]["date_assumed_office"] = di['Date assumed office']
        housefile.seek(0)

senate_districts = {}
aggregate_projects(senate_districts, "senate_district", "senate_district")
print("aggregated", len(senate_districts), "senate districts")

# populate senate districts with legislators
with open("../raw/il_senate_2023_members.csv", "r") as senatefile: 
    district_info = csv.DictReader(senatefile)
    for s in senate_districts:
        senate_districts[s]["legislator"] = ""
        senate_districts[s]["party"] = ""
        senate_districts[s]["date_assumed_office"] = ""
        for di in district_info:
            if di['Office'] == f"Illinois State Senate District {s}":
                senate_districts[s]["legislator"] = di['Name']
                senate_districts[s]["party"] = di['Party']
                senate_districts[s]["date_assumed_office"] = di['Date assumed office']
        senatefile.seek(0)

# save counties to csv
fields = ["county_name", "county_fips", "dg_small_kw", "dg_small_count", "dg_large_kw", "dg_large_count", "cs_kw", "cs_count", "utility_kw", "utility_count", "total_kw", "total_count"]
write_csv(counties, fields, "../final/solar-projects-by-county.csv")
print('saved counties to csv')

# save counties to geojson
write_geojson("../raw/il_counties.geojson", "CO_FIPS", counties, "../final/solar-projects-by-county.geojson")
print('saved counties to geojson')

# save tracts to csv
fields = ["census_tract", "dg_small_kw", "dg_small_count", "dg_large_kw", "dg_large_count", "cs_kw", "cs_count", "utility_kw", "utility_count", "total_kw", "total_count"]
write_csv(tracts, fields, "../final/solar-projects-by-tract.csv")
print('saved tracts to csv')

# save tracts to geojson
write_geojson("../raw/il_2020_census_tracts.geojson", "GEOID10", tracts, "../final/solar-projects-by-tract.geojson")
print('saved tracts to geojson')

# save places to csv
fields = ["place", "dg_small_kw", "dg_small_count", "dg_large_kw", "dg_large_count", "cs_kw", "cs_count", "utility_kw", "utility_count", "total_kw", "total_count"]
write_csv(places, fields, "../final/solar-projects-by-place.csv")
print('saved places to csv')

# save places to geojson
write_geojson("../raw/il_places.geojson", "NAMELSAD20", places, "../final/solar-projects-by-place.geojson")
print('saved places to geojson')

# save house to csv
fields = ["house_district", "legislator", "party", "date_assumed_office", "dg_small_kw", "dg_small_count", "dg_large_kw", "dg_large_count", "cs_kw", "cs_count", "utility_kw", "utility_count", "total_kw", "total_count"]
write_csv(house_districts, fields, "../final/solar-projects-by-il-house.csv")
print('saved house districts to csv')

# save house to geojson
write_geojson("../raw/il_house_2023.geojson", "DISTRICT", house_districts, "../final/solar-projects-by-il-house.geojson")
print('saved house districts to geojson')

# save senate to csv
fields = ["senate_district", "legislator", "party", "date_assumed_office", "dg_small_kw", "dg_small_count", "dg_large_kw", "dg_large_count", "cs_kw", "cs_count", "utility_kw", "utility_count", "total_kw", "total_count"]
write_csv(senate_districts, fields, "../final/solar-projects-by-il-senate.csv")
print('saved senate districts to csv')

# save senate to geojson
write_geojson("../raw/il_senate_2023.geojson", "DISTRICT", senate_districts, "../final/solar-projects-by-il-senate.geojson")
print('saved senate districts to geojson')

print('done!')
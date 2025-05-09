import csv
import json
from aggregate_utils import *

# aggregate all projects in the state
aggregate_all_projects("energized")
aggregate_all_projects("planned")
generate_monthly_kw_time_series()

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

# aggregate by US Census Tract
tracts = {}
aggregate_projects(tracts, "census_tract", "census_tract")
print("aggregated", len(tracts), "tracts")

# aggregate by US Census Place
places = {}
aggregate_projects(places, "place", "place")
print("aggregated", len(places), "places")

# aggregate by IL House
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

# aggregate by IL Senate
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

# each aggregate shares a common set of fields including:
# energized vs planned
# categories (dg_small, dg_large, cs, utility, total)
# kw totals and project counts
common_field_names = [ "dg_small_kw",
                       "dg_small_count", 
                       "dg_large_kw", 
                       "dg_large_count", 
                       "cs_kw", 
                       "cs_count", 
                       "utility_kw", 
                       "utility_count", 
                       "total_kw", 
                       "total_count",
                       "planned_dg_small_kw",
                       "planned_dg_small_count", 
                       "planned_dg_large_kw", 
                       "planned_dg_large_count", 
                       "planned_cs_kw", 
                       "planned_cs_count", 
                       "planned_utility_kw", 
                       "planned_utility_count", 
                       "planned_total_kw", 
                       "planned_total_count"]

# save counties to csv
fields = ["county_name", "county_fips"] + common_field_names
write_csv(counties, fields, "../final/solar-projects-by-county.csv")
print('saved counties to csv')

# save counties to geojson
write_geojson("../raw/il_counties.geojson", "CO_FIPS", counties, "../final/solar-projects-by-county.geojson")
print('saved counties to geojson')

# save tracts to csv
fields = ["census_tract"] + common_field_names
write_csv(tracts, fields, "../final/solar-projects-by-tract.csv")
print('saved tracts to csv')

# save tracts to geojson
write_geojson("../raw/il_2020_census_tracts.geojson", "GEOID10", tracts, "../final/solar-projects-by-tract.geojson")
print('saved tracts to geojson')

# save places to csv
fields = ["place"] + common_field_names
write_csv(places, fields, "../final/solar-projects-by-place.csv")
print('saved places to csv')

# save places to geojson
write_geojson("../raw/il_places.geojson", "NAMELSAD20", places, "../final/solar-projects-by-place.geojson")
print('saved places to geojson')

# save house to csv
fields = ["house_district", "legislator", "party", "date_assumed_office"] + common_field_names
write_csv(house_districts, fields, "../final/solar-projects-by-il-house.csv")
print('saved house districts to csv')

# save house to geojson
write_geojson("../raw/il_house_2023.geojson", "DISTRICT", house_districts, "../final/solar-projects-by-il-house.geojson")
print('saved house districts to geojson')

# save senate to csv
fields = ["senate_district", "legislator", "party", "date_assumed_office"] + common_field_names
write_csv(senate_districts, fields, "../final/solar-projects-by-il-senate.csv")
print('saved senate districts to csv')

# save senate to geojson
write_geojson("../raw/il_senate_2023.geojson", "DISTRICT", senate_districts, "../final/solar-projects-by-il-senate.geojson")
print('saved senate districts to geojson')

print('done!')
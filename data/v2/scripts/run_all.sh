# /bin/bash

# combine 3 source files into one
python combine_projects.py

# assign il house and senate districts based on tract centroids
python get_tract_districts.py

# aggregate data by county, tract and legilsative districts
python aggregate_data.py

# format the csv files
csvcut ../final/solar-projects-by-county.csv -c "county_name,total_kw,utility_kw,cs_kw,dg_large_kw,dg_small_kw" > ../final/solar-projects-by-county-formatted.csv

csvcut ../final/solar-projects-by-place.csv -c "place,total_kw,utility_kw,cs_kw,dg_large_kw,dg_small_kw" > ../final/solar-projects-by-place-formatted.csv

csvcut ../final/solar-projects-by-il-house.csv -c "house_district,legislator,party,total_kw,utility_kw,cs_kw,dg_large_kw,dg_small_kw" > ../final/solar-projects-by-il-house-formatted.csv

csvcut ../final/solar-projects-by-il-senate.csv -c "senate_district,legislator,party,total_kw,utility_kw,cs_kw,dg_large_kw,dg_small_kw" > ../final/solar-projects-by-il-senate-formatted.csv

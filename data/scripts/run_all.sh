# /bin/bash

# convert energized project data to csv
echo "extracting energized project data"
in2csv ../raw/eia860.xlsx > ../raw/eia860_raw.csv
sed 1,2d ../raw/eia860_raw.csv > ../raw/eia860.csv

in2csv ../raw/ilabp.xlsx > ../raw/ilabp.csv

in2csv ../raw/ilsfa.xlsx > ../raw/ilsfa_raw.csv
sed 1,2d ../raw/ilsfa_raw.csv > ../raw/ilsfa.csv

# convert planned projects to csv
echo "extracting planned project data"
in2csv ../raw/eia860.xlsx --sheet "Planned" > ../raw/eia860_planned_raw.csv
# chop the first 2 lines and last 8 lines (requires reversing chopping and un-reversing)
sed 1,2d ../raw/eia860_planned_raw.csv | tail -r | sed 1,8d | tail -r > ../raw/eia860_planned.csv

in2csv ../raw/ilabp_report_2.xlsx > ../raw/ilabp_planned.csv

in2csv ../raw/ilsfa_report_2.xlsx > ../raw/ilsfa_planned_raw.csv
sed 1,2d ../raw/ilsfa_planned_raw.csv > ../raw/ilsfa_planned.csv

# combine 3 source files into one
python combine_projects.py

# assign il house and senate districts based on tract centroids
python get_tract_districts.py

# aggregate data by county, tract and legilsative districts
python aggregate_data.py

# format the csv files
csvcut ../final/solar-projects-by-county.csv -c "county_name,total_kw,utility_kw,cs_kw,dg_large_kw,dg_small_kw,planned_total_kw,planned_utility_kw,planned_cs_kw,planned_dg_large_kw,planned_dg_small_kw" > ../final/solar-projects-by-county-formatted.csv
sed 1d ../final/solar-projects-by-county-formatted.csv > tmp.txt
sed '1 s/^/county,total,utility,cs,dg_large,dg_small,pl_total,pl_utility,pl_cs,pl_dg_large,pl_dg_small\n/' tmp.txt > ../final/solar-projects-by-county-formatted.csv

csvcut ../final/solar-projects-by-place.csv -c "place,total_kw,utility_kw,cs_kw,dg_large_kw,dg_small_kw,planned_total_kw,planned_utility_kw,planned_cs_kw,planned_dg_large_kw,planned_dg_small_kw" > ../final/solar-projects-by-place-formatted.csv
sed 1d ../final/solar-projects-by-place-formatted.csv > tmp.txt
sed '1 s/^/place,total,utility,cs,dg_large,dg_small,pl_total,pl_utility,pl_cs,pl_dg_large,pl_dg_small\n/' tmp.txt > ../final/solar-projects-by-place-formatted.csv

csvcut ../final/solar-projects-by-il-house.csv -c "house_district,legislator,party,total_kw,utility_kw,cs_kw,dg_large_kw,dg_small_kw,planned_total_kw,planned_utility_kw,planned_cs_kw,planned_dg_large_kw,planned_dg_small_kw" > ../final/solar-projects-by-il-house-formatted.csv
sed 1d ../final/solar-projects-by-il-house-formatted.csv > tmp.txt
sed '1 s/^/house_district,legislator,party,total,utility,cs,dg_large,dg_small,pl_total,pl_utility,pl_cs,pl_dg_large,pl_dg_small\n/' tmp.txt > ../final/solar-projects-by-il-house-formatted.csv

csvcut ../final/solar-projects-by-il-senate.csv -c "senate_district,legislator,party,total_kw,utility_kw,cs_kw,dg_large_kw,dg_small_kw,planned_total_kw,planned_utility_kw,planned_cs_kw,planned_dg_large_kw,planned_dg_small_kw" > ../final/solar-projects-by-il-senate-formatted.csv
sed 1d ../final/solar-projects-by-il-senate-formatted.csv > tmp.txt
sed '1 s/^/senate_district,legislator,party,total,utility,cs,dg_large,dg_small,pl_total,pl_utility,pl_cs,pl_dg_large,pl_dg_small\n/' tmp.txt > ../final/solar-projects-by-il-senate-formatted.csv

# cleanup
echo "cleanup temp data"
rm tmp.txt
rm ../raw/eia860*.csv
rm ../raw/ilabp*.csv
rm ../raw/ilsfa*.csv
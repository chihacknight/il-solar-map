import csv

data = {}
county_index = 15
ac_kwh_index = 8

with open('data/report-3-census-tract-rev.csv', "r") as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:

        raw_county_name = row[county_index]

        county_name = raw_county_name.upper().replace(" COUNTY", "")

        if(county_name=="COUNTY"):
            continue

        if county_name in data:
            data[county_name][0] += 1
            data[county_name][1] += float(row[ac_kwh_index])
        else:
            data[county_name] = [1, float(row[ac_kwh_index])]

print(data)
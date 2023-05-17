import csv

data = {}
county_index = 15
ac_kwh_index = 8

with open('data/report-3-census-tract-rev.csv', "r") as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        
        if(row[county_index]=="County"):
            continue

        if row[county_index] in data:
            data[row[county_index]][0] += 1
            data[row[county_index]][1] += float(row[ac_kwh_index])
        else:
            data[row[county_index]] = [1, float(row[ac_kwh_index])]

print(data)

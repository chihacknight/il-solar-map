import csv

data = {}

with open("raw/all-projects.csv", 'r') as csvfile:
    projects = csv.DictReader(csvfile)
    for project in projects:
        if project["county"] not in data:
            data[project["county"]] = [1, round(float(project["kw"]))]
        else:
            data[project["county"]][0] += 1
            data[project["county"]][1] += round(float(project["kw"]))

with open("final/solar-projects-by-county.csv", "w") as outfile:    
    fields = ["County", "Num Projects", "Total KW"]
    writer = csv.writer(outfile)
    # writer.writeheader()
    writer.writerow(fields)
    for key in data.keys():
        writer.writerow([key, data[key][0], data[key][1]])

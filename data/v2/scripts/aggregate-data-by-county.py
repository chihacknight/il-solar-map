import csv

counties = {}

with open("../final/all-projects.csv", 'r') as csvfile:
    projects = csv.DictReader(csvfile)
    for row in projects:
        if row["county"] not in counties:
            county = {}
            county["county_fips"] = row["county"]
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

            counties[row["county"]] = county
        else:
            c = counties[row["county"]]

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


with open("../final/solar-projects-by-county.csv", "w") as outfile:    
    fields = ["county_fips", "dg_small_kw", "dg_small_count", "dg_large_kw", "dg_large_count", "cs_kw", "cs_count", "utility_kw", "utility_count", "total_kw", "total_count"]
    writer = csv.writer(outfile)
    writer.writerow(fields)
    for key, value in counties.items():
        writer.writerow([value[field] for field in fields])

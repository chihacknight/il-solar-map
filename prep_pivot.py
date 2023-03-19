import csv

f_zips = open('data/il-zctas.csv', 'r')
reader_zips = csv.DictReader(f_zips)
il_zips = []
for row in reader_zips:
    il_zips.append(row)

f_zips.close()
print('zipcodes:', len(il_zips))

fieldnames = ['zipcode','cs','dg_large','dg_small','nonprofit_public','utility','grand_total']

f_pivot = open('data/il-solar-by-zip-pivot.csv', 'r')
reader_pivot = csv.DictReader(f_pivot, fieldnames=fieldnames)
il_solar = []
for row in reader_pivot:
    il_solar.append(row)
f_pivot.close()

print('zipcodes with data:', len(il_solar))

zip_rows = []
for z in il_zips:
    # fill with 0s
    new_row = {
        'zipcode': z['zipcode'],
        'cs': 0,
        'dg_large': 0,
        'dg_small': 0,
        'nonprofit_public': 0,
        'utility': 0,
        'grand_total': 0
    }

    # print('checking', z['zipcode'])
    for row in il_solar:
        # print (row)
        if row['zipcode'] == new_row['zipcode']:
            print ('found', row['zipcode'])
            for k,v in row.items():
                if v is not None and v is not '':
                    new_row[k] = int(round(float(v),0))
    
    zip_rows.append(new_row)

print(len(zip_rows))
# write output
outp = open('data/il-solar-by-zip-prepped.csv', 'w')
writer = csv.DictWriter(outp, fieldnames=fieldnames)
writer.writeheader()
writer.writerows(zip_rows)

# cleanup
outp.close()
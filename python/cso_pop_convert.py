# Written by Sharon Yang to convert CSO XLSX file to
# readable CSV file.
# Input: '../raw_data/raw_cso_pop_13_14.csv' (See below for how to get it.)
# Output: '../clean_data/cso_pop_fixed.csv' with schema 'province,
#         district, totalVotes'

import re


# Obtained raw CSO population data from:
# http://cso.gov.af/en/page/demography-and-socile-statistics/demograph-statistics/3897
# Delete the top two tables with province overview (no district info)
# Save as CSV file with filename 'raw_cso_pop_13_14.csv' in '../raw_data/'
with open('../raw_data/raw_cso_pop_13_14.csv', 'r') as f:
  data = f.read()

# Clean up some metadata not needed.
data = data.replace('Female,Male,Both Sexes,Female,Male,Both Sexes,'
    'Female,Male,Both Sexes,,,,,,,,,,,,,,,,,,,,,,,,,,,,', '')
data = data.replace(' Figures in  Thousand,,,,,,,,,,', '')
data = data.replace('Rural,,,Urban,,,Total  Urban and  Rural,,,Minor '
    'Civil Division,,NO,,,,,,,,,,,,,,,,,,,,,,,,,', '')
data = data.replace(',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,', '')

# Split data by province.
data_set = data.split('Province,,,,,,,,,,,,,,,,,,,,,,,,,,')

# Make a list of province names.
prov_list = []
for dat in data_set:
    test = dat[dat.rfind('\r\n') + 2:].strip()
    test = test.replace('Figures in  Thousand,,,,,,,,,,', '')
    prov_list.append(test)

# Truncate the header and footer.
data_set = data_set[1:]
prov_list = prov_list[:-1]

# Schema for our final product.
final_product = 'province,district,totalPop\n'

# Go through all district, save info.
for dat in range(len(data_set)):
    dist_set = data_set[dat].split(',,,,,,,,')
    for d in dist_set:
        # Find district names.
        reg = re.search('[A-Za-z ]+', d)
        if reg:
            dist_raw = reg.group(0)
            dist_name = dist_raw.strip()
            line = d[:d.find(',' + dist_raw)]
            dist_tot = line[line.rfind(',') + 1:]
            if dist_name != 'Total':
                output = prov_list[dat] + ',' + dist_name + ',' + dist_tot
                if output.find('Settled Population of') != -1:
                    continue
                # There are some "temporary" info districts.
                if output.find('temporary') != -1:
                    continue
                reg = re.search('[0-9]', output)
                if reg:
                    output = output.replace(dist_name + ',', '')
                    output = output.replace(dist_tot, '')
                    dist_name = dist_name.title().replace(' ', '')
                    dist_tot = str(int(float(dist_tot) * 1000))
                    output += dist_name + ',' + dist_tot
                    final_product += output + '\n'

# Output file is saved to '../clean_data/cso_pop_fixed.csv'.
with open('../clean_data/cso_pop_fixed.csv', 'w') as out:
    out.write(final_product)


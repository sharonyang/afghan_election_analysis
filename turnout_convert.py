# Written by Sharon Yang to use preliminary turnout data
# to output districts with "suspicious" voting stations.
# Input: 'turnout_raw.csv' (See below for how to get it.)
# Output: print out to stdout for districts with "suspicious"
#         voting stations sorted by highest count to lowest
#
# Output:
# Districts with stations with 0 vs. 600 votes
# ('Paktika,Paktika', 114)
# ('Paktya,Paktya', 44)
# ('Na,Na', 34)
# ('Wardak,Wardak', 25)
# ('Khost,Khost', 18)
# ('Ghor,Ghor', 16)
# ('Ghazni,Ghazni', 8)
# ('Kabul,Kabul', 4)
# ('Logar,Logar', 4)
# ('Zabul,Zabul', 3)
# ('Faryab,Faryab', 2)
# ('Herat,Herat', 2)
# ('Badghis,Badghis', 2)
# ('Kapisa,Kapisa', 1)
# ('Nooristan,Nooristan', 1)
# ('Badakhshan,Badakhshan', 1)

import operator

# The turnout raw data is obtained from Afghanistan Open Data Project
# which is located at https://github.com/developmentseed/aodp-data/tree/runoff
# The file specifically is at:
# https://github.com/developmentseed/aodp-data/blob/runoff/data/2014_president_election/results/preliminary-results/2014_afghanistan_preliminary_runoff_election_results.csv
with open('turnout_raw.csv', 'r') as ff:
    data = ff.read()

data_set = data.split('\n')

# Output dictionaries:
# 1. output_dict contains
#        {
#            "Province,District": [Abdullah, Ghanhi, Total]
#            ....
#        }
output_dict = {}

# 2. dist_flag contains
#        {
#            "Province,District": (# of stations with
#                                  0 vs. 600 votes)
#            ....
#        }
dist_flag = {}
first_line = True

# Go through each row.
for line in data_set:
    if first_line:
        first_line = False
        continue
    line_set = line.split(',')
    # Get important data from each station:
    # This includes province and district names,
    # Abdullah and Ghanhi vote counts, and total
    # vote count.
    prov = line_set[0].replace('\"', '')
    dist = line_set[0].replace('\"', '')
    key = prov.title() + ',' + dist.title()
    abdullah = int(line_set[4].replace('\"', ''))
    ghanhi = int(line_set[5].replace('\"', ''))
    total = int(line_set[6].replace('\"', ''))
    output = [abdullah, ghanhi, total]
    flag = False
    # Check if there is 0 vs. 600 situation.
    if (abdullah == 0 and ghanhi == 600) or \
       (ghanhi == 0 and abdullah == 600):
        flag = True
    if not output_dict.has_key(key):
        output_dict[key] = output
        if not flag:
            dist_flag[key] = 0
        else:
            dist_flag[key] = 1
    else:
        # Sum the station vote counts to
        # district's.
        output_dict[key][0] += abdullah
        output_dict[key][1] += ghanhi
        output_dict[key][2] += total
        if flag:
            dist_flag[key] += 1


sorted_dist = sorted(dist_flag.items(),
    key=operator.itemgetter(1), reverse=True)

print "Districts with stations with 0 vs. 600 votes"
for d in sorted_dist:
    if d[1] != 0:
        print d


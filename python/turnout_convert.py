# Written by Sharon Yang to use preliminary turnout data
# to output districts with "suspicious" voting stations.
# Input: '../raw_data/raw_votes_runoff.csv' (See below for how to get it.)
# Output: print out to stdout for districts with "suspicious"
#         voting stations sorted by highest count to lowest
#
# Output: printout to stdout. Stored in "../clean_data/turnout_convert.txt"

import operator

# The turnout raw data is obtained from Afghanistan Open Data Project
# which is located at https://github.com/developmentseed/aodp-data/tree/runoff
# The file specifically is at:
# https://github.com/developmentseed/aodp-data/blob/runoff/data/2014_president_election/results/preliminary-results/2014_afghanistan_preliminary_runoff_election_results.csv
with open('../raw_data/raw_votes_runoff.csv', 'r') as ff:
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
    dist = line_set[1].replace('\"', '')
    key = prov.title() + ',' + dist.title().replace(' ', '')
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
print "('Province,District', <station_count>)"
for d in sorted_dist:
    if d[1] != 0:
        print d

# Get population data from 2013-2014 CSO data
# converted by cso_pop_convert.py.
turnout_dict = {}
with open('../clean_data/cso_pop_fixed.csv', 'r') as population:
    pop_data = population.read()

pop_data = pop_data.split('\n')

# Go through population data along with turnout
# data to see if there are districts with SUPER
# high turnout rates.
extra_pop = []
missing_dist = []
ignore_flag = True
pop_dict = {}
for pop_line in pop_data:
    if ignore_flag:
        ignore_flag = False
        continue
    if pop_line == '':
    	continue
    curr = pop_line.split(',')
    key = curr[0] + ',' + curr[1]
    key = key.replace('Center', '')

    key = key.replace('Kunarha', 'Kunar')
    key = key.replace('-', '')

    # Note if there is missing population data.
    if not output_dict.has_key(key):
        extra_pop.append(key)
        continue
    pop_dict[key] = int(curr[2])

for key in output_dict:
    if not pop_dict.has_key(key):
        missing_dist.append(key)
        continue
    voted = output_dict[key][2]
    turnout_dict[key] = float(voted) / pop_dict[key]

# Sort by decreasing turnout rates.
sorted_turnout = sorted(turnout_dict.items(),
    key=operator.itemgetter(1), reverse=True)

# Print out result.
print ""
print ""
print "Districts with greater than 95% turnout"
print "'Province,District','PopulationVoted','TotalPopulation',<turnout %>"
for d in sorted_turnout:
    if d[1] - 0.95 > 0:
        print d[0] + ',' + str(output_dict[d[0]][2]) +\
            ',' + str(pop_dict[d[0]]) + ',' + str(d[1] * 100)

print ""
print "We are missing population from the following districts:"
print "[<Province,District>,... ]"
print ""
print "In turnout data but not in population data:"
print sorted(missing_dist)
print "count: " + str(len(missing_dist))
print ""

print "In population data but not in turnout data:"
print sorted(extra_pop)
print "count: " + str(len(extra_pop))
print ""


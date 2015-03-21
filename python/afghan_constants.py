# By: Laksh Bhasin
# Description: Useful constants for this election. Import this into other
# scripts.

# The total number of registered voters in Afghanistan, as well as the
# total population of Afghanistan. Both of these figures come from
# http://www.idea.int/vt/countryview.cfm?CountryCode=AF
NUM_REGISTERED_VOTERS = 20845988.0
AFGHAN_POPULATION = 31822848.0

# We will assume that the fraction of people who are eligible to vote in
# each district/province is just the ratio of the above two quantities.
# This homogeneity assumption might not always hold, but it's the best we
# can do.
VOTING_FRACTION = NUM_REGISTERED_VOTERS/float(AFGHAN_POPULATION)

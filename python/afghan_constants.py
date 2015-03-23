# By: Laksh Bhasin
# Description: Useful constants for this election. Import this into other
# scripts.

# The total voting age population of Afghanistan, as well as the total
# population of Afghanistan. Both of these figures come from
# http://www.idea.int/en/vt/countryview.cfm?CountryCode=AF
VOTING_AGE_POPULATION = 16208255.0
AFGHAN_POPULATION = 31822848.0

# We will assume that the fraction of people who are eligible to vote in
# each district/province is just the ratio of the above two quantities.
# This homogeneity assumption might not always hold, but it's the best we
# can do. Also, this is really a *maximum* voting-eligible fraction, based
# on how many people are of voting age (I'd imagine that prisoners can't
# vote).
VOTING_FRACTION = VOTING_AGE_POPULATION/float(AFGHAN_POPULATION)

# Colors to use for the two candidates' plots.
ABDULLAH_COLOR = "#FFAE19"
GHANI_COLOR = "#72AFE4"

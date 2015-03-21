# By: Laksh Bhasin
# Description: This script creates turnout distribution histograms for both
# the first round and runoff elections. Both of these are created using
# district level data (since that is the finest level at which we have
# population statistics).
#
# Inputs:
#       * ../raw_data/raw_votes_first_round.csv
#       * ../clean_data/runoff_votes_and_turnout.csv
#
# Outputs:
#       * ../clean_data/first_round_turnout_distrib_entire.png - The first
#         round turnout distribution, covering the entire data range (the
#         data goes up to like 1000%).
#       * ../clean_data/first_round_turnout_distrib_restricted.png - The
#         first round turnout distribution, but over a restricted range of
#         turnout percentages (e.g. 0% to 100%).
#       * ../clean_data/runoff_turnout_distrib_entire.png - The runoff
#         turnout distribution, over the entire data range.
#       * ../clean_data/runoff_turnout_distrib_restricted.png - The runoff
#         turnout distribution, but over a restricted range.
#

import csv
import numpy as np
import matplotlib.pyplot as plt

# Import convenience functions
from afghan_functions import *


# Constants

# VALUES
from afghan_constants import VOTING_FRACTION

# DIRECTORIES
RAW_DATA_DIR = "../raw_data/"
CLEAN_DATA_DIR = "../clean_data/"

# INPUT FILES

# CSV file for first round votes (by polling station)
FIRST_ROUND_VOTES_FILE = RAW_DATA_DIR + "raw_votes_first_round.csv"

# CSV file for runoff votes (by district).
RUNOFF_VOTES_FILE = CLEAN_DATA_DIR + "runoff_votes_and_turnout.csv"

# OUTPUT FILES

# Turnout distribution histogram for the first round, over the entire range
# of percentages.
FIRST_ROUND_TURNOUT_DISTRIB_ENTIRE = CLEAN_DATA_DIR +\
        "first_round_turnout_distrib_entire.png"

# The same as above, but over a restricted range of turnout percentages.
FIRST_ROUND_TURNOUT_DISTRIB_RESTR = CLEAN_DATA_DIR +\
        "first_round_turnout_distrib_restricted.png"

# Turnout distribution histogram for the runoff election, over the entire
# range of percentages.
RUNOFF_ELECTION_TURNOUT_DISTRIB_ENTIRE = CLEAN_DATA_DIR +\
        "runoff_turnout_distrib_entire.png"

# The same as above, but over a restricted range of turnout percentages.
RUNOFF_ELECTION_TURNOUT_DISTRIB_RESTR = CLEAN_DATA_DIR +\
        "runoff_turnout_distrib_restricted.png"


# Global variables

# Dicts to track district-level data (cached to avoid regeneration).
provinceDistrictToPop = None


# This function populates a dictionary that maps (Province, District)
# tuples to their populations.
#
def populateProvinceDistrictToPop():
    global provinceDistrictToPop

    # If it's already populated, just return.
    if provinceDistrictToPop != None:
        return

    provinceDistrictToPop = getProvinceDistrictToPop()


# This function returns a dictionary that maps (Province, District) tuples
# to their turnouts for the first round election.
#
def getProvinceDistrictToFirstRoundTurnout():
    global provinceDistrictToPop
    populateProvinceDistrictToPop()

    # Go through FIRST_ROUND_VOTES_FILE, add up all of the total vote
    # counts in each district, and divide by (that district's population *
    # VOTING_FRACTION). This will be stored in the dict below.
    provinceDistrictToFirstRoundTurnout = dict()

    with open(FIRST_ROUND_VOTES_FILE, 'rU') as csvFile:
        csvReader = csv.DictReader(csvFile)

        for row in csvReader:
            provinceName = row['province']
            districtName = row['district']
            totalVotes = float(row['Total'])

            # Fix the capitalization on province names. This just
            # capitalizes the first letter of each word and gets rid of
            # spaces (if any). This also includes capitalization around
            # dashes.
            provinceName = "".join(w.capitalize() for w in \
                                   provinceName.split())
            provinceName = provinceName.title()

            districtPop = provinceDistrictToPop[(provinceName,
                                                 districtName)]

            if (provinceName, districtName) in \
                    provinceDistrictToFirstRoundTurnout:

                provinceDistrictToFirstRoundTurnout[\
                        (provinceName, districtName)] += 100.0 *\
                        totalVotes / (VOTING_FRACTION * districtPop)

            else:
                provinceDistrictToFirstRoundTurnout[\
                        (provinceName, districtName)] = 100.0 *\
                        totalVotes / (VOTING_FRACTION * districtPop)

    return provinceDistrictToFirstRoundTurnout


# This function returns a dictionary that maps (Province, District) tuples
# to their turnouts for the runoff election.
#
def getProvinceDistrictToRunoffTurnout():
    global provinceDistrictToPop
    populateProvinceDistrictToPop()

    # Go through RUNOFF_VOTES_FILE, add up all of the total vote counts
    # in each district, and divide by (that district's population *
    # VOTING_FRACTION). This will be stored in the dict below.
    provinceDistrictToRunoffTurnout = dict()

    with open(RUNOFF_VOTES_FILE, 'rU') as csvFile:
        csvReader = csv.DictReader(csvFile)

        for row in csvReader:
            provinceName = row['Province']
            districtName = row['District']
            totalVotes = float(row['PopulationVoted'])

            districtPop = provinceDistrictToPop[(provinceName,
                                                 districtName)]

            if (provinceName, districtName) in \
                    provinceDistrictToRunoffTurnout:

                provinceDistrictToRunoffTurnout[\
                        (provinceName, districtName)] += 100.0 *\
                        totalVotes / (VOTING_FRACTION * districtPop)

            else:
                provinceDistrictToRunoffTurnout[\
                        (provinceName, districtName)] = 100.0 *\
                        totalVotes / (VOTING_FRACTION * districtPop)

    return provinceDistrictToRunoffTurnout


# Main code
if __name__ == "__main__":
    # Get the various dicts that contain turnout data.
    provinceDistrictToFirstRoundTurnout = \
            getProvinceDistrictToFirstRoundTurnout()
    provinceDistrictToRunoffTurnout = getProvinceDistrictToRunoffTurnout()

    # We only care about the dicts' values if we want to create histograms.
    firstRoundTurnouts = \
            np.array(provinceDistrictToFirstRoundTurnout.values())
    runoffTurnouts = \
            np.array(provinceDistrictToRunoffTurnout.values())

    # Plot histograms and save them to file. Do one histogram that extends
    # over all the data, and one from 0% to 100%.
    numBinsEntireRange = 100
    numBinsRestrictedRange = 30

    # Plot the two first-round histograms.
    fig, ax = plt.subplots()
    fig.set_facecolor('white')

    # In plotting the entire distribution, use different colors for
    # < 100% and >= 100% turnout.
    ax.hist(firstRoundTurnouts[firstRoundTurnouts < 100.0],
            numBinsEntireRange*100.0/max(firstRoundTurnouts),
            histtype = 'bar',
            range = None, color = 'b')
    ax.hist(firstRoundTurnouts[firstRoundTurnouts >= 100.0],
            numBinsEntireRange*(1.0 - 100.0/max(firstRoundTurnouts)),
            histtype = 'bar',
            range = None, color = 'r')
    plt.xlabel("Turnout Percentage")
    plt.ylabel("Number of Districts")
    plt.title("First Round Turnout Distribution")

    plt.savefig(FIRST_ROUND_TURNOUT_DISTRIB_ENTIRE,
                bbox_inches = "tight")
    print "Saved entire first-round turnout distribution to\n", \
            FIRST_ROUND_TURNOUT_DISTRIB_ENTIRE
    plt.close()

    fig = plt.figure()
    fig.set_facecolor('white')
    plt.hist(firstRoundTurnouts, numBinsRestrictedRange, histtype = 'bar',
             range = [0.0, 100.0])
    plt.xlabel("Turnout Percentage")
    plt.xlim([0.0, 100.0])
    plt.ylabel("Number of Districts")
    plt.title("First Round Turnout Distribution (Restricted Range)")

    plt.savefig(FIRST_ROUND_TURNOUT_DISTRIB_RESTR,
                bbox_inches = "tight")
    print "Saved restricted first-round turnout distribution to\n", \
            FIRST_ROUND_TURNOUT_DISTRIB_RESTR, "\n"
    plt.close()


    # Plot the two runoff-election histograms.
    fig, ax = plt.subplots()
    fig.set_facecolor('white')

    # In plotting the entire distribution, use different colors for
    # < 100% and >= 100% turnout.
    ax.hist(runoffTurnouts[runoffTurnouts < 100.0],
            numBinsEntireRange*100.0/max(runoffTurnouts),
            histtype = 'bar',
            range = None, color = 'b')
    ax.hist(runoffTurnouts[runoffTurnouts >= 100.0],
            numBinsEntireRange*(1.0 - 100.0/max(runoffTurnouts)),
            histtype = 'bar',
            range = None, color = 'r')
    plt.xlabel("Turnout Percentage")
    plt.ylabel("Number of Districts")
    plt.title("Runoff Election Turnout Distribution")

    plt.savefig(RUNOFF_ELECTION_TURNOUT_DISTRIB_ENTIRE,
                bbox_inches = "tight")
    print "Saved entire runoff turnout distribution to\n", \
            RUNOFF_ELECTION_TURNOUT_DISTRIB_ENTIRE
    plt.close()

    fig = plt.figure()
    fig.set_facecolor('white')
    plt.hist(runoffTurnouts, numBinsRestrictedRange, histtype = 'bar',
             range = [0.0, 100.0])
    plt.xlabel("Turnout Percentage")
    plt.ylabel("Number of Districts")
    plt.xlim([0.0, 100.0])
    plt.title("Runoff Election Turnout Distribution (Restricted)")

    plt.savefig(RUNOFF_ELECTION_TURNOUT_DISTRIB_RESTR,
                bbox_inches = "tight")
    print "Saved restricted runoff turnout distribution to\n", \
            RUNOFF_ELECTION_TURNOUT_DISTRIB_RESTR
    plt.close()

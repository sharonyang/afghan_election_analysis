# By: Laksh Bhasin
# Description: This script takes two arguments: a candidate's last name,
# and a province's name. It then creates a histogram of the vote share
# distribution for that candidate in that province. This is created by
# looking at all of the polling stations for that province and seeing how
# many of the total votes were won by the given candidate.
#
# Command-line arguments (in this order):
#       * Candidate's last name ("Ghani" or "Abdullah")
#       * Province name (must match the data).
#
# Inputs:
#       * ../raw_data/raw_votes_runoff.csv
#
# Outputs:
#       * ../figures/province_vote_share/<candidate>_<province>_
#         distrib.png - a histogram of the vote share distribution for
#         <candidate> in <province>, where both of these fields are
#         command-line arguments that are *made* lower case (even if the
#         inputs weren't).
#

import sys
import csv
import numpy as np
import matplotlib.pyplot as plt


# Constants

# VALUES
from afghan_constants import ABDULLAH_COLOR, GHANI_COLOR

# DIRECTORIES
RAW_DATA_DIR = "../raw_data/"
FIGURE_DIR = "../figures/province_vote_share/"

# INPUT FILES

# CSV file for runoff votes by polling station.
RUNOFF_VOTES_POLLING_STATION_FILE = RAW_DATA_DIR + "raw_votes_runoff.csv"


# This function gets the vote share (percentage) distribution for a given
# candidate in a given province. This involves looking at polling station
# level data for that province and finding the vote share percentage for
# the candidate at each polling station.
#
# Precondition: It is assumed that both "candidate" and "province" are
# valid parameters.
#
def getProvinceVoteShareDistrib(candidate, province):
    # Convert the province to lower case for easy comparison.
    lowercaseProvince = province.lower()

    # Set the column to look at in the CSV based on the candidate.
    candidateColumn = "Ghani"

    if candidate.lower() == "abdullah":
        candidateColumn = "Abdullah"

    # This array holds all of the polling-station level vote-share values
    # for this candidate in this province.
    candidateVoteSharesForProvince = list()

    with open(RUNOFF_VOTES_POLLING_STATION_FILE, 'rU') as csvFile:
        csvReader = csv.DictReader(csvFile)

        for row in csvReader:
            provinceName = row['Province'].lower()

            if provinceName != lowercaseProvince:
                continue

            candidateVotes = float(row[candidateColumn])
            totalVotes = float(row['Total'])

            candidateVoteSharesForProvince.append(100.0 *\
                    candidateVotes/totalVotes)

    candidateVoteSharesForProvince = \
            np.array(candidateVoteSharesForProvince)

    # If the array is empty, the province name was probably wrong.
    if len(candidateVoteSharesForProvince) == 0:
        raise ValueError("No provinces matching " + province +\
                " were found in " + RUNOFF_VOTES_POLLING_STATION_FILE)

    return candidateVoteSharesForProvince


# Main code
if __name__ == "__main__":

    # There should be two command-line arguments in addition to the script
    # name.
    if len(sys.argv) != 3:
        print "usage:", sys.argv[0], "candidate_last_name province_name"
        sys.exit(1)

    candidate = sys.argv[1].strip()
    provinceName = sys.argv[2]

    # Check the candidate. We won't check the province's spelling at this
    # point since that's too hard.
    if candidate.lower() != "abdullah" and candidate.lower() != "ghani":
        raise ValueError("The input candidate " + candidate + " was " +\
                "neither Abdullah nor Ghani!")

    # Configure the plot save files and the colors.
    plotColor = GHANI_COLOR

    if candidate.lower() == "abdullah":
        plotColor = ABDULLAH_COLOR

    plotSaveFile = FIGURE_DIR + candidate.lower() + "_" +\
            provinceName.lower() + "_distrib.png"

    # Get the distribution for this candidate.
    candidateVoteShareDistrib = getProvinceVoteShareDistrib(\
            candidate, provinceName)

    # Plot and save the histogram
    numBins = 25

    fig = plt.figure()
    fig.set_facecolor('white')
    plt.hist(candidateVoteShareDistrib, numBins, histtype = 'bar',
             range = [0.0, 100.0], color = plotColor)
    plt.xlabel(candidate + "'s Vote Share")
    plt.ylabel("Number of Polling Stations")
    plt.xlim([0.0, 100.0])
    plt.title(candidate + "'s Vote Share Distribution for " + provinceName)

    plt.savefig(plotSaveFile, bbox_inches = "tight")
    print "Saved " + candidate + "'s vote share distribution to\n" +\
            plotSaveFile
    plt.close()

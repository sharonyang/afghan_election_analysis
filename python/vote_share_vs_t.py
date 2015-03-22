# By: Laksh Bhasin
# Description: This script outputs plots of the vote share that each
# candidate received in the runoff election as a function of turnout.
# Individual points in the outputted plots represent districts.
#
# Input files:
#       * ../clean_data/runoff_votes_and_turnout.csv
#
# Output files:
#       * ../figures/vote_share_vs_t/runoff_abdullah_vote_share_vs_t.png -
#         The vote share vs T plot for Abdullah, accumulated at the
#         district level. This includes a linear fit on the data.
#       * ../figures/vote_share_vs_t/runoff_abdullah_vote_share_vs_t_
#         resid.png - The residual plot for a linear fit on the above data.
#       * ../figures/vote_share_vs_t/runoff_ghani_vote_share_vs_t.png - The
#         vote share vs T plot for Ghani, including a linear fit.
#       * ../figures/vote_share_vs_t/runoff_ghani_vote_share_vs_t_resid.png
#         - The residual plot for a linear fit on the above data.
#


import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Import convenience functions
from afghan_functions import *
from turnout_distrib import getProvinceDistrictToRunoffTurnout


# Constants

# VALUES
from afghan_constants import VOTING_FRACTION, ABDULLAH_COLOR, GHANI_COLOR

# DIRECTORIES
CLEAN_DATA_DIR = "../clean_data/"
FIGURE_DIR = "../figures/vote_share_vs_t/"

# INPUT FILES

# CSV file for runoff votes (by district).
RUNOFF_VOTES_FILE = CLEAN_DATA_DIR + "runoff_votes_and_turnout.csv"

# OUTPUT FILES

# The vote share vs T plot for Abdullah, using district-level data. This
# includes a linear fit on the data.
ABDULLAH_VOTE_SHARE_VS_T = FIGURE_DIR + \
        "runoff_abdullah_vote_share_vs_t.png"

# The residual plot for the above plot's linear fit.
ABDULLAH_VOTE_SHARE_VS_T_RESID = FIGURE_DIR +\
        "runoff_abdullah_vote_share_vs_t_resid.png"

# The vote share vs T plot for Ghani, using district-level data. This
# includes a linear fit on the data.
GHANI_VOTE_SHARE_VS_T = FIGURE_DIR + "runoff_ghani_vote_share_vs_t.png"

# The residual plot for the above plot's linear fit.
GHANI_VOTE_SHARE_VS_T_RESID = FIGURE_DIR +\
        "runoff_ghani_vote_share_vs_t_resid.png"


# This function takes a candidate (either "Abdullah" or "Ghani") and
# returns a mapping from (Province, District) tuples to the vote share for
# that candidate in that district. Note that the vote share is expressed as
# a percentage.
#
def getProvinceDistrictToVoteShare(candidate):
    if candidate is not "Abdullah" and candidate is not "Ghani":
        raise ValueError("The input candidate " + candidate + " was " +\
                "neither Abdullah nor Ghani!")

    # Set the column to look at in the CSV.
    voteColumn = "GhaniVotes"

    if candidate is "Abdullah":
        voteColumn = "AbdullahVotes"

    # Go through RUNOFF_VOTES_FILE, add up all of the votes for that
    # candidate, and store that information in the first dictionary below.
    # Then store the total number of votes cast in that district, in the
    # second dictionary below.
    provinceDistrictToCandidateVotes = dict()
    provinceDistrictToTotalVotes = dict()

    with open(RUNOFF_VOTES_FILE, 'rU') as csvFile:
        csvReader = csv.DictReader(csvFile)

        for row in csvReader:
            provinceName = row['Province']
            districtName = row['District']
            candidateVotes = float(row[voteColumn])
            totalVotes = float(row['PopulationVoted'])

            if (provinceName, districtName) in \
                    provinceDistrictToCandidateVotes:

                provinceDistrictToCandidateVotes[\
                        (provinceName, districtName)] += candidateVotes
                provinceDistrictToTotalVotes[\
                        (provinceName, districtName)] += totalVotes

            else:
                provinceDistrictToCandidateVotes[\
                        (provinceName, districtName)] = candidateVotes
                provinceDistrictToTotalVotes[\
                        (provinceName, districtName)] = totalVotes

    # Sanity check: both dictionaries should have the same keys.
    assert sorted(provinceDistrictToCandidateVotes.keys()) == \
            sorted(provinceDistrictToTotalVotes.keys())

    # For each district, take the ratio of the candidate's votes to the
    # total number of votes. This is the vote share.
    provinceDistrictToCandidateVoteShare = dict()

    for provinceDistrict in provinceDistrictToCandidateVotes:
        candidateVotes = provinceDistrictToCandidateVotes[provinceDistrict]
        totalVotes = provinceDistrictToTotalVotes[provinceDistrict]

        provinceDistrictToCandidateVoteShare[provinceDistrict] = 100.0 *\
                candidateVotes / totalVotes

    return provinceDistrictToCandidateVoteShare


# This function plots vote share vs T for a given candidate, as well as a
# residual plot for a linear fit. It takes a dictionary that maps
# (Province, District) tuples to that candidate's vote share, as well as
# another dictionary that maps (Province, District) tuples to turnout. The
# output plots are saved to plotSaveFile (just the vote share vs T plot
# with the linear fit) and residPlotSaveFile (for the residual plot).
#
def plotVoteShareVsT(candidate,
                     provinceDistrictToCandidateVoteShare,
                     provinceDistrictToTurnout,
                     plotTitle,
                     residPlotTitle,
                     plotColor,
                     plotSaveFile,
                     residPlotSaveFile):

    if candidate is not "Abdullah" and candidate is not "Ghani":
        raise ValueError("The input candidate " + candidate + " was " +\
                "neither Abdullah nor Ghani!")

    # Make sure that both the vote share and turnout dictionaries have the
    # same keys!
    assert sorted(provinceDistrictToCandidateVoteShare.keys()) == \
            sorted(provinceDistrictToTurnout.keys())

    # Get the x and y values for this plot by unpacking the dictionaries.
    xValues = list()
    yValues = list()

    for provinceDistrict in provinceDistrictToCandidateVoteShare:
        xValues.append(provinceDistrictToTurnout[provinceDistrict])
        yValues.append(\
                provinceDistrictToCandidateVoteShare[provinceDistrict])

    xValues = np.array(xValues)
    yValues = np.array(yValues)

    # Perform linear regression on the data.
    slope, intercept, rValue, pValue, stdErr = linregress(xValues, yValues)
    xValuesFitLine = np.arange(0.0, 210.0, 10.0)
    yValuesFitLine = slope * xValuesFitLine + intercept

    # Get the residuals
    residValues = yValues - (slope * xValues + intercept)

    # Plot vote share vs T with the linear fit.
    fig = plt.figure()
    fig.set_facecolor('white')
    plt.scatter(xValues, yValues, color = plotColor, s = 20)
    plt.plot(xValuesFitLine, yValuesFitLine, 'k', lw=1.5)
    plt.xlim([0.0, 200.0])
    plt.ylim([0.0, 100.0])
    plt.xlabel("Turnout Percentage")
    plt.ylabel("Vote Share for " + candidate)
    plt.title(plotTitle)

    # Include the fitted line's equation and r^2. Format the equation
    # correctly depending on the intercept's sign.
    if intercept >= 0:
        plt.text(120.0, 33.0, r"$VS \,= \," + str(slope)[0:6] +\
                 "T \,+\, " + str(intercept)[0:6] + r"$")
    else:
        plt.text(120.0, 33.0, r"$VS \,= \," + str(slope)[0:6] +\
                 "T \,-\, " + str(abs(intercept))[0:6] + r"$")

    plt.text(120.0, 28.0, r"$r^2 = \," + str(rValue**2.0)[0:6] + r"$")

    # Save to file and inform the user.
    plt.savefig(plotSaveFile, bbox_inches = "tight")
    plt.close()
    print "Saved vote share vs T plot for", candidate, "to\n", plotSaveFile

    # Plot the residual plot, with a flat line at y = 0 for reference.
    fig = plt.figure()
    fig.set_facecolor('white')
    plt.scatter(xValues, residValues, color = plotColor, s = 20)
    plt.plot([0.0, 250.0], [0.0, 0.0], 'k--')
    plt.xlim([0.0, 200.0])
    plt.ylim([-60.0, 60.0])
    plt.xlabel("Turnout Percentage")
    plt.ylabel("Vote Share Residuals")
    plt.title(residPlotTitle)

    # Save to file and inform the user.
    plt.savefig(residPlotSaveFile, bbox_inches = "tight")
    plt.close()
    print "Saved vote share vs T residual plot for", candidate, "to\n",\
            residPlotSaveFile, "\n"


# Main code
if __name__ == "__main__":
    # Get the necessary dictionaries for the runoff election data.
    provinceDistrictToTurnout = getProvinceDistrictToRunoffTurnout()
    provinceDistrictToAbdullahVoteShare = \
            getProvinceDistrictToVoteShare("Abdullah")
    provinceDistrictToGhaniVoteShare = \
            getProvinceDistrictToVoteShare("Ghani")

    # Plot vote share vs T (including linear fits and residuals) for both
    # candidates, using all district-level data. The following function
    # calls will also save the plots to file.
    plotVoteShareVsT("Abdullah",
                     provinceDistrictToAbdullahVoteShare,
                     provinceDistrictToTurnout,
                     "Vote Share vs T for Abdullah",
                     "Vote Share vs T Residuals for Abdullah",
                     ABDULLAH_COLOR,
                     ABDULLAH_VOTE_SHARE_VS_T,
                     ABDULLAH_VOTE_SHARE_VS_T_RESID)

    plotVoteShareVsT("Ghani",
                     provinceDistrictToGhaniVoteShare,
                     provinceDistrictToTurnout,
                     "Vote Share vs T for Ghani",
                     "Vote Share vs T Residuals for Ghani",
                     GHANI_COLOR,
                     GHANI_VOTE_SHARE_VS_T,
                     GHANI_VOTE_SHARE_VS_T_RESID)


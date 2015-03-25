# By: Laksh Bhasin
# Description: This script tries to see if provinces where Ghani won by a
# lot (in the runoff election) also happen to be places with relatively
# high turnout. If this is the case, then this suggests that Ghani engaged
# in country-wide vote-stuffing in order to win, and that Abdullah did not
# engage in as much vote stuffing or fraud. If this isn't the case, then we
# can't really say much; for all we know, Abdullah might also be engaging
# in vote stuffing, and this wouldn't show up in a winning margin analysis.
#
# Winning margin analysis (WMA) is conducted on a province level with
# histograms, and a district level with scatterplots (sort of like observer
# turnout trends).
#
# Inputs:
#       * ../clean_data/runoff_votes_and_turnout.csv
#
# Outputs:
#       * ../figures/winning_margin_analysis/wma_by_province.png - This is
#         a combination of two bar graphs, which shows both the turnout by
#         province *MINUS* 50% and the winning margin for Ghani in that
#         province.
#       * ../figures/winning_margin_analysis/wma_by_district.png - This is
#         a scatterplot that graphs Ghani's winning margin as a function of
#         turnout, using district level data.
#


import csv
import numpy as np
import matplotlib.pyplot as plt

# Import some convenience functions
from afghan_functions import *


# Constants

# VALUES
from afghan_constants import VOTING_FRACTION

# DIRECTORIES
RAW_DATA_DIR = "../raw_data/"
CLEAN_DATA_DIR = "../clean_data/"
FIGURE_DIR = "../figures/winning_margin_analysis/"

# INPUT FILES

# CSV file for runoff votes (by district).
RUNOFF_VOTES_FILE = CLEAN_DATA_DIR + "runoff_votes_and_turnout.csv"

# OUTPUT FILES

# Combined bar graph, showing the turnout by province *MINUS* 50% and the
# winning margin for Ghani in that province.
BAR_GRAPH_WMA_PROVINCE = FIGURE_DIR + "wma_by_province.png"

# A scatterplot of Ghani's WMA in various districts vs turnouts in those
# districts.
SCATTER_WMA_DISTRICT = FIGURE_DIR + "wma_by_district.png"


# Global variables

# Dicts to track province data (cached to avoid regeneration).
provinceNumToName = None


# This function returns a dictionary that maps province numbers to Ghani's
# winning margin in that province. The winning margin is defined as the %
# of votes for Ghani (in that province) minus the % of votes for Abdullah.
#
def getProvinceNumToGhaniWinningMargin():
    # Make sure provinceNumToName is populated.
    global provinceNumToName
    provinceNumToName = populateProvinceNumToName()

    # Go through RUNOFF_VOTES_FILE, add up all of the votes for Ghani minus
    # the votes for Abdullah (in each province). This information is stored
    # in the first dictionary below. Then store the total number of votes
    # cast in each province, in the second dictionary below.
    provinceNameToGhaniWinningMarginVotes = dict()
    provinceNameToTotalVotes = dict()

    with open(RUNOFF_VOTES_FILE, 'rU') as csvFile:
        csvReader = csv.DictReader(csvFile)

        for row in csvReader:
            provinceName = row['Province']
            ghaniVotes = float(row['GhaniVotes'])
            abdullahVotes = float(row['AbdullahVotes'])
            totalVotes = float(row['PopulationVoted'])

            ghaniWinningMarginVotes = ghaniVotes - abdullahVotes

            if provinceName in provinceNameToGhaniWinningMarginVotes:

                provinceNameToGhaniWinningMarginVotes[provinceName] += \
                        ghaniWinningMarginVotes
                provinceNameToTotalVotes[provinceName] += totalVotes

            else:
                provinceNameToGhaniWinningMarginVotes[provinceName] = \
                        ghaniWinningMarginVotes
                provinceNameToTotalVotes[provinceName] = totalVotes

    # Sanity check: both dictionaries should have the same keys.
    assert sorted(provinceNameToGhaniWinningMarginVotes.keys()) == \
            sorted(provinceNameToTotalVotes.keys())

    # For each province, take the ratio of Ghani's winning vote margin to
    # the total number of votes. This is Ghani's winning margin as a
    # *percentage*. Note that the following dictionary maps province
    # *numbers* to this winning margin percentage.
    provinceNumToGhaniWinningMarginPct = dict()

    for provinceNum in provinceNumToName:
        provinceName = provinceNumToName[provinceNum]
        ghaniWinningMarginVotes = \
                provinceNameToGhaniWinningMarginVotes[provinceName]
        totalVotes = provinceNameToTotalVotes[provinceName]

        provinceNumToGhaniWinningMarginPct[provinceNum] = \
                100.0 * ghaniWinningMarginVotes / totalVotes

    return provinceNumToGhaniWinningMarginPct


# This function returns a dictionary that maps (Province, District) tuples
# to Ghani's winning margin in that district. The winning margin is defined
# as the % of votes for Ghani (in that district) minus the % of votes for
# Abdullah.
#
def getProvinceDistrictToGhaniWinningMargin():
    # Go through RUNOFF_VOTES_FILE, add up all of the votes for Ghani minus
    # the votes for Abdullah (in each district). This information is stored
    # in the first dictionary below. Then store the total number of votes
    # cast in each district, in the second dictionary below.
    provinceDistrictToGhaniWinningMarginVotes = dict()
    provinceDistrictToTotalVotes = dict()

    with open(RUNOFF_VOTES_FILE, 'rU') as csvFile:
        csvReader = csv.DictReader(csvFile)

        for row in csvReader:
            provinceName = row['Province']
            districtName = row['District']
            ghaniVotes = float(row['GhaniVotes'])
            abdullahVotes = float(row['AbdullahVotes'])
            totalVotes = float(row['PopulationVoted'])

            ghaniWinningMarginVotes = ghaniVotes - abdullahVotes

            if (provinceName, districtName) in \
                    provinceDistrictToGhaniWinningMarginVotes:

                provinceDistrictToGhaniWinningMarginVotes[\
                        (provinceName, districtName)] += \
                        ghaniWinningMarginVotes
                provinceDistrictToTotalVotes[\
                        (provinceName, districtName)] += totalVotes

            else:
                provinceDistrictToGhaniWinningMarginVotes[\
                        (provinceName, districtName)] = \
                        ghaniWinningMarginVotes
                provinceDistrictToTotalVotes[\
                        (provinceName, districtName)] = totalVotes

    # Sanity check: both dictionaries should have the same keys.
    assert sorted(provinceDistrictToGhaniWinningMarginVotes.keys()) == \
            sorted(provinceDistrictToTotalVotes.keys())

    # For each district, take the ratio of Ghani's winning vote margin to
    # the total number of votes. This is Ghani's winning margin as a
    # *percentage*.
    provinceDistrictToGhaniWinningMarginPct = dict()

    for provinceDistrict in provinceDistrictToGhaniWinningMarginVotes:
        ghaniWinningMarginVotes = \
                provinceDistrictToGhaniWinningMarginVotes[provinceDistrict]
        totalVotes = provinceDistrictToTotalVotes[provinceDistrict]

        provinceDistrictToGhaniWinningMarginPct[provinceDistrict] = \
                100.0 * ghaniWinningMarginVotes / totalVotes

    return provinceDistrictToGhaniWinningMarginPct


# This function plots and saves two bar graphs that have the same x-axis.
# It also includes a legend. The two bars for each x-value are separated by
# "width" along the x-axis.
#
# Note: It is assumed that a figure has already been created via
# plt.figure(). The figure and axes are passed in as arguments.
#
def plotAndSaveCombinedBarGraphs(fig, ax, firstDict, secondDict, width,
        xLabel, yLabel, legendLabel1, legendLabel2, plotTitle, outputFile):

    # Unpack the first dictionary to get the common x-values
    keyValuePairs = np.array(firstDict.items())
    xValues = keyValuePairs[:, 0]
    firstBarGraphHeights = list()
    secondBarGraphHeights = list()

    for xVal in xValues:
        firstBarGraphHeights.append(firstDict[xVal])
        secondBarGraphHeights.append(secondDict[xVal])

    width = 0.4
    rects1 = ax.bar(xValues, firstBarGraphHeights, width,
                    color = '#DB1212')
    rects2 = ax.bar(xValues + width, secondBarGraphHeights,
                    width, color = '#1AC08E')
    ax.set_xlabel(xLabel)
    ax.set_ylabel(yLabel)
    ax.set_title(plotTitle)

    ax.legend((rects1[0], rects2[0]), \
              (legendLabel1, legendLabel2),
              loc = "upper left",
              prop = {"size": 10})

    plt.savefig(outputFile, bbox_inches = 'tight')
    print "Saved combined bar graph to\n", outputFile


# Main code
if __name__ == "__main__":
    # Get the various dicts we want.
    provinceNumToTurnout = getProvinceNumToTurnoutRunoff()
    provinceDistrictToTurnout = getProvinceDistrictToTurnoutRunoff()
    provinceNumToGhaniWinningMargin = getProvinceNumToGhaniWinningMargin()
    provinceDistrictToGhaniWinningMargin = \
            getProvinceDistrictToGhaniWinningMargin()

    # Subtract off 50% from the province-level turnout data for easy
    # viewing in the dual bar graph.
    provinceNumToTurnoutMinus50 = dict()

    for provinceNum in provinceNumToTurnout:
        turnout = provinceNumToTurnout[provinceNum]
        provinceNumToTurnoutMinus50[provinceNum] = turnout - 50

    # Plot and save a bar graph that combines the WMA data (on a province
    # level) with the turnout data *MINUS* 50% (on a province level).
    fig, ax = plt.subplots()
    fig.set_facecolor('white')
    plotAndSaveCombinedBarGraphs(fig, ax,
                                 provinceNumToTurnoutMinus50,
                                 provinceNumToGhaniWinningMargin,
                                 0.4,
                                 "Province Number",
                                 "Quantities",
                                 "Turnout Percentage Minus 50%",
                                 "Ghani's Winning Margin (%)",
                                 "Province-Level Ghani Winning " +\
                                         "Margin Analysis",
                                 BAR_GRAPH_WMA_PROVINCE)
    plt.close()

    # Plot and save a scatterplot of the district-level Ghani winning
    # margin data, as a function of turnout percentage.
    fig = plt.figure()
    fig.set_facecolor('white')

    # Get the x and y values for this scatterplot from our data dicts.
    xValues = list()
    yValues = list()
    for provinceDistrict in provinceDistrictToTurnout:
        xValues.append(provinceDistrictToTurnout[provinceDistrict])
        yValues.append(provinceDistrictToGhaniWinningMargin[\
                provinceDistrict])

    plt.scatter(xValues, yValues, s = 20, color = 'k')
    plt.xlim([0.0, 200.0])
    plt.ylim([-100.0, 100.0])
    plt.xlabel("Turnout Percentage")
    plt.ylabel("Ghani's Winning Margin")
    plt.title("District-Level Ghani Winning Margin Analysis")
    plt.savefig(SCATTER_WMA_DISTRICT, bbox_inches = 'tight')

    print "Saved scatterplot of district-level Ghani WMA " +\
            "to\n", SCATTER_WMA_DISTRICT
    plt.close()

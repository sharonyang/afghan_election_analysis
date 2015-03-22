# By: Laksh Bhasin
# Description: This script tries to answer the question of whether changing
# the number of election observers in a given province has an effect on
# changing the turnout. One way of doing this is comparing the data on
# election observer deployment between the first-round and runoff
# elections, and seeing if this matches any trends in turnout changes.
# Another way is to plot the runoff turnout percentages in each province as
# a function of the runoff "normalized observer deployment density"
# (which is defined below) for that province.
#
# Inputs:
#       * ../raw_data/raw_observers_first_round.csv
#       * ../raw_data/raw_observers_runoff.csv
#       * ../raw_data/raw_turnout_first_round.csv
#       * ../clean_data/runoff_votes_and_turnout.csv
#
# Outputs:
#       * ../figures/turnout_change.png - This is a bar graph showing
#         the percent change in turnout in each province between the two
#         elections. On the x-axis, each province is just assigned a
#         number.
#       * ../figures/obs_dep_change.png - This is a bar graph that shows
#         the percent change in the *relative* observer deployment density
#         between the two elections, for each province. The "relative" part
#         means we're subtracting off the median observer deployment
#         density change across all provinces (where the change is measured
#         between the two elections).
#       * ../figures/obs_dep_turnout_change.png - A combination of the
#         above two graphs, on the same set of axes.
#       * ../clean_data/num_to_province.csv - A CSV file that describes the
#         mapping between numbers (used in the above graphs) and actual
#         province names.
#       * ../figures/runoff_turnout_vs_norm_obs_dep.png - A scatterplot
#         of the turnout percentages in various provinces, as a function of
#         their "normalized observer deployment density (see below for a
#         definition of this).
#
# Precondition: there are 34 provinces, and it is essential that their
# names match across all of the input CSV files!
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
FIGURE_DIR = "../figures/"

# INPUT FILES

# CSV file for first-round election observer deployment
FIRST_ROUND_OBS_DEP_FILE = RAW_DATA_DIR + "raw_observers_first_round.csv"

# CSV file for runoff election observer deployment
RUNOFF_OBS_DEP_FILE = RAW_DATA_DIR + "raw_observers_runoff.csv"

# CSV file for first round turnout data (by province).
FIRST_ROUND_TURNOUT_FILE = RAW_DATA_DIR + "raw_turnout_first_round.csv"

# CSV file for runoff votes and turnout data (by district).
RUNOFF_TURNOUT_FILE = CLEAN_DATA_DIR + "runoff_votes_and_turnout.csv"

# OUTPUT FILES

# Bar graph for percent change in turnout vs province number
BAR_GRAPH_TURNOUT_CHANGE = FIGURE_DIR + "turnout_change.png"

# Bar graph for percent change in observer deployment density vs province
# number.
BAR_GRAPH_OBS_DEP_CHANGE = FIGURE_DIR + "obs_dep_change.png"

# Bar graph combining the above two bar graphs on the same axes.
BAR_GRAPH_TURNOUT_OBS_DEP_CHANGE = FIGURE_DIR +\
        "obs_dep_turnout_change.png"

# Scatterplot of the runoff turnout percentage in various provinces as a
# function of the "normalized observer deployment density".
SCATTER_TURNOUT_NORM_OBS_DEP = FIGURE_DIR +\
        "runoff_turnout_vs_norm_obs_dep.png"

# CSV file describing the mapping from numbers to actual province names.
NUM_TO_PROV_FILE = CLEAN_DATA_DIR + "num_to_province.csv"


# Global variables

# Dicts to track province data (cached to avoid regeneration).
provinceNumToName = None
provinceNameToPop = None


# This function populates a dictionary that maps province numbers to
# province names. This dictionary is stored in the global variable
# provinceNumToName.
#
# The number for each province is assigned by finding its index in a list
# of sorted province names. Note that this function uses the data in
# RUNOFF_TURNOUT_FILE.
#
def populateProvinceNumToName():
    global provinceNumToName

    # If it's already populated, there's nothing to do.
    if provinceNumToName != None:
        return

    provinceNumToName = getProvinceNumToName()

    return


# This function populates a dictionary that maps province names to their
# populations. This uses the data in RUNOFF_TURNOUT_FILE. The dictionary is
# then stored in the global variable provinceNameToPop.
#
def populateProvinceNameToPop():
    global provinceNameToPop

    # If it's already populated, there's nothing to do.
    if provinceNameToPop != None:
        return

    provinceNameToPop = getProvinceNameToPop()

    return


# This function returns a dictionary that maps province numbers to the
# percent change in turnout percentage, from the first-round election to
# the runoff election.
#
def getProvinceNumToTurnoutChange():
    # Make sure provinceNumToName and provinceNameToPop are populated.
    global provinceNumToName, provinceNameToPop
    populateProvinceNumToName()
    populateProvinceNameToPop()

    # Get the number of people who voted in each province in the first
    # round.
    provinceNameToNumVotesFirstRound = dict()

    with open(FIRST_ROUND_TURNOUT_FILE, 'rU') as csvFile:
        csvReader = csv.DictReader(csvFile)

        for row in csvReader:
            provinceName = row['province']
            numVoted = int(row['turnout_total'])

            if provinceName in provinceNameToNumVotesFirstRound:
                provinceNameToNumVotesFirstRound[provinceName] += \
                        numVoted
            else:
                provinceNameToNumVotesFirstRound[provinceName] = \
                        numVoted

    # Do the same thing for the runoff.
    provinceNameToNumVotesRunoff = dict()

    with open(RUNOFF_TURNOUT_FILE, 'rU') as csvFile:
        csvReader = csv.DictReader(csvFile)

        for row in csvReader:
            provinceName = row['Province']
            numVoted = int(row['PopulationVoted'])

            if provinceName in provinceNameToNumVotesRunoff:
                provinceNameToNumVotesRunoff[provinceName] += \
                        numVoted
            else:
                provinceNameToNumVotesRunoff[provinceName] = \
                        numVoted

    # Get the turnout in each province by dividing by (its population times
    # VOTING_FRACTION). Note that these are percentages.
    provinceNameToTurnoutFirstRound = dict()
    provinceNameToTurnoutRunoff = dict()

    for provinceName in provinceNameToNumVotesFirstRound:
        numVotesFirstRound = provinceNameToNumVotesFirstRound[provinceName]
        numVotesRunoff = provinceNameToNumVotesRunoff[provinceName]
        provincePop = provinceNameToPop[provinceName]

        provinceNameToTurnoutFirstRound[provinceName] = 100.0 * \
                numVotesFirstRound / (provincePop * VOTING_FRACTION)
        provinceNameToTurnoutRunoff[provinceName] = 100.0 * \
                numVotesRunoff / (provincePop * VOTING_FRACTION)

    # Now, map province numbers to the percent change in turnout percentage
    # between the two rounds.
    provinceNumToPctChangeTurnout = dict()

    for provinceNum in provinceNumToName:
        provinceName = provinceNumToName[provinceNum]

        firstRoundTurnout = provinceNameToTurnoutFirstRound[provinceName]
        runoffTurnout = provinceNameToTurnoutRunoff[provinceName]

        pctChangeTurnout = 100.0 * (runoffTurnout - firstRoundTurnout) / \
                           firstRoundTurnout

        provinceNumToPctChangeTurnout[provinceNum] = pctChangeTurnout

    return provinceNumToPctChangeTurnout


# This function returns a dictionary that maps province numbers to the
# relative change in the "observer deployment density", from the first-round
# election to the runoff election. This density is just the total number of
# observers in that province, divided by the population of that province.
# The relative change is found by taking the observer density change for a
# province and subtracting off the median density change between the two
# elections. This helps us see how the size of observer density changes
# correlates with turnout.
#
def getProvinceNumToRelObsDensChange():
    # Make sure provinceNumToName and provinceNameToPop are populated.
    global provinceNumToName, provinceNameToPop
    populateProvinceNumToName()
    populateProvinceNameToPop()

    # Get the observer density for the first round.
    provinceNameToObsDensityFirstRound = dict()

    with open(FIRST_ROUND_OBS_DEP_FILE, 'rU') as csvFile:
        csvReader = csv.DictReader(csvFile)

        for row in csvReader:
            provinceName = row['prov_name']
            provincePop = float(provinceNameToPop[provinceName])
            numObservers = int(row['all_observers'])

            if provinceName in provinceNameToObsDensityFirstRound:
                provinceNameToObsDensityFirstRound[provinceName] += \
                        numObservers / provincePop
            else:
                provinceNameToObsDensityFirstRound[provinceName] = \
                        numObservers / provincePop

    # Do the same thing for the runoff election.
    provinceNameToObsDensityRunoff = dict()

    with open(RUNOFF_OBS_DEP_FILE, 'rU') as csvFile:
        csvReader = csv.DictReader(csvFile)

        for row in csvReader:
            provinceName = row['prov_name']
            provincePop = float(provinceNameToPop[provinceName])
            numObservers = int(row['Total_Observers'])

            if provinceName in provinceNameToObsDensityRunoff:
                provinceNameToObsDensityRunoff[provinceName] += \
                        numObservers / provincePop
            else:
                provinceNameToObsDensityRunoff[provinceName] = \
                        numObservers / provincePop

    # Get the percent change in the observer deployment densities for each
    # province, and create a dictionary that maps from province *numbers*
    # to these percent changes.
    provinceNumToPctChangeObsDens = dict()

    for provinceNum in provinceNumToName:
        provinceName = provinceNumToName[provinceNum]

        firstRoundObsDensity = \
                provinceNameToObsDensityFirstRound[provinceName]
        runoffObsDensity = \
                provinceNameToObsDensityRunoff[provinceName]

        pctChangeObsDensity = 100.0 * \
                (runoffObsDensity - firstRoundObsDensity) / \
                firstRoundObsDensity

        provinceNumToPctChangeObsDens[provinceNum] = pctChangeObsDensity

    # Subtract off the median percent change in observer density, so we get
    # the relative changes in each province.
    provinceNumToRelPctChangeObsDens = dict()
    medianPctObsDensChange = np.median(
            provinceNumToPctChangeObsDens.values())

    for provinceNum in provinceNumToPctChangeObsDens:
        provinceNumToRelPctChangeObsDens[provinceNum] = \
                provinceNumToPctChangeObsDens[provinceNum] - \
                medianPctObsDensChange

    return provinceNumToRelPctChangeObsDens


# This function returns a mapping from the province number to the runoff
# election turnout percentage.
#
def getProvinceNumToRunoffTurnout():
    # Make sure provinceNumToName and provinceNameToPop are populated.
    global provinceNumToName, provinceNameToPop
    populateProvinceNumToName()
    populateProvinceNameToPop()

    # Get the number of people who voted in each province in the runoff.
    provinceNameToNumVotesRunoff = dict()

    with open(RUNOFF_TURNOUT_FILE, 'rU') as csvFile:
        csvReader = csv.DictReader(csvFile)

        for row in csvReader:
            provinceName = row['Province']
            numVoted = int(row['PopulationVoted'])

            if provinceName in provinceNameToNumVotesRunoff:
                provinceNameToNumVotesRunoff[provinceName] += \
                        numVoted
            else:
                provinceNameToNumVotesRunoff[provinceName] = \
                        numVoted

    # We want to return a mapping from the province number to the turnout
    # percentage in that province. This can be found by taking the number
    # of votes and dividing by (that province's population *
    # VOTING_FRACTION).
    provinceNumToRunoffTurnout = dict()

    for provinceNum in provinceNumToName:
        provinceName = provinceNumToName[provinceNum]
        numVotesRunoff = provinceNameToNumVotesRunoff[provinceName]
        provincePop = provinceNameToPop[provinceName]

        provinceNumToRunoffTurnout[provinceNum] = 100.0 * \
                numVotesRunoff / (provincePop * VOTING_FRACTION)

    return provinceNumToRunoffTurnout


# This function returns a mapping from the province number to the runoff
# election observer deployment density. This density is computed by taking
# the observer deployment, dividing by the population of that province, and
# then normalizing all the densities to a [0, 100] range.
#
def getProvinceNumToNormalizedRunoffObsDensity():
    # Make sure provinceNumToName and provinceNameToPop are populated.
    global provinceNumToName, provinceNameToPop
    populateProvinceNumToName()
    populateProvinceNameToPop()

    # This is a mapping from province names to the observer deployment in
    # that province, divided by the population of that province.
    provinceNameToObsRunoffDensity = dict()

    with open(RUNOFF_OBS_DEP_FILE, 'rU') as csvFile:
        csvReader = csv.DictReader(csvFile)

        for row in csvReader:
            provinceName = row['prov_name']
            provincePop = float(provinceNameToPop[provinceName])
            numObservers = int(row['Total_Observers'])

            if provinceName in provinceNameToObsRunoffDensity:
                provinceNameToObsRunoffDensity[provinceName] += \
                        numObservers/provincePop
            else:
                provinceNameToObsRunoffDensity[provinceName] = \
                        numObservers/provincePop

    # We want to normalize the above densities to a [0, 100] range, and
    # then we want to return a mapping from the province number to the
    # normalized densities.
    provinceNumToNormalizedRunoffObsDensity = dict()

    allObsDensities = np.array(provinceNameToObsRunoffDensity.values())
    minObsDensity = min(allObsDensities)
    relativeMaxObsDensity = max(allObsDensities) - minObsDensity

    for provinceNum in provinceNumToName:
        provinceName = provinceNumToName[provinceNum]

        normalizedObsDensity = 100.0 * \
                (provinceNameToObsRunoffDensity[provinceName] - \
                 minObsDensity) / relativeMaxObsDensity

        provinceNumToNormalizedRunoffObsDensity[provinceNum] = \
                normalizedObsDensity

    return provinceNumToNormalizedRunoffObsDensity


# This function plots the various kinds of bar graphs that this code
# produces. It takes a dictionary of data, and various plot-related
# parameters (e.g. axis labels), as well as the output file to which the
# plot will be saved.
#
# Note: It is assumed that a figure has already been created via
# plt.figure().
#
def plotAndSaveBarGraph(dataDict, xLabel, yLabel, plotTitle, outputFile):

    # Unpack the data into x and y (height).
    keyValuePairs = np.array(dataDict.items())
    xValues = keyValuePairs[:, 0]
    heights = keyValuePairs[:, 1]

    plt.bar(xValues, heights, 1.0, color = '#0000FF')
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(plotTitle)

    # Save plot and inform user.
    plt.savefig(outputFile, bbox_inches = 'tight')

    print "Saved bar graph to", outputFile


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
                    color = '#FFFF00')
    rects2 = ax.bar(xValues + width, secondBarGraphHeights,
                    width, color = '#3333FF')
    ax.set_xlabel(xLabel)
    ax.set_ylabel(yLabel)
    ax.set_title(plotTitle)

    ax.legend((rects1[0], rects2[0]), \
              (legendLabel1, legendLabel2),
              loc = "upper right",
              prop = {"size": 10})

    plt.savefig(outputFile, bbox_inches = 'tight')
    print "Saved combined bar graph to", outputFile


# Main code
if __name__ == "__main__":
    # Get the various dicts we want.
    provinceNumToPctChangeTurnout = getProvinceNumToTurnoutChange()
    provinceNumToRelPctChangeObsDens = getProvinceNumToRelObsDensChange()
    provinceNumToRunoffTurnout = getProvinceNumToRunoffTurnout()
    provinceNumToNormalizedRunoffObsDensity = \
            getProvinceNumToNormalizedRunoffObsDensity()

    # Plot and save the bar graphs. Create a separate figure for the ones
    # that should be separate.
    fig = plt.figure()
    fig.set_facecolor('white')
    plotAndSaveBarGraph(provinceNumToPctChangeTurnout,
                        "Province Number",
                        "% Change in Turnout",
                        "% Change in Turnout vs Province",
                        BAR_GRAPH_TURNOUT_CHANGE)
    plt.close()

    fig = plt.figure()
    fig.set_facecolor('white')
    plotAndSaveBarGraph(provinceNumToRelPctChangeObsDens,
                        "Province Number",
                        "% Change in Relative Observer Deployment Density",
                        "% Change in Relative Obs. Dep. Density " +\
                                "vs Province Number",
                        BAR_GRAPH_OBS_DEP_CHANGE)
    plt.close()

    # Plot and save a bar graph that combines the above two bar graphs.
    fig, ax = plt.subplots()
    fig.set_facecolor('white')
    plotAndSaveCombinedBarGraphs(fig, ax,
                                 provinceNumToPctChangeTurnout,
                                 provinceNumToRelPctChangeObsDens,
                                 0.4,
                                 "Province Number",
                                 "Quantities",
                                 "% Change in Turnout",
                                 "Relative Obs. Dep. Density % Change",
                                 "Turnout and Relative Obs. Dep. " +\
                                 "Density Changes",
                                 BAR_GRAPH_TURNOUT_OBS_DEP_CHANGE)
    plt.close()

    # Plot and save a scatterplot of the runoff turnout percentage vs the
    # runoff normalized observer deployment density.
    fig = plt.figure()
    fig.set_facecolor('white')

    # Get the x and y values for this scatterplot from our data dicts.
    xValues = list()
    yValues = list()
    for provinceNum in provinceNumToRunoffTurnout:
        xValues.append(provinceNumToNormalizedRunoffObsDensity[provinceNum])
        yValues.append(provinceNumToRunoffTurnout[provinceNum])

    plt.scatter(xValues, yValues, s = 40, color = 'k')
    plt.xlabel("Normalized Observer Deployment Density")
    plt.ylabel("Turnout Percentage")
    plt.title("Runoff Turnout vs. Normalized Obs. Dep. Density")
    plt.savefig(SCATTER_TURNOUT_NORM_OBS_DEP, bbox_inches = 'tight')

    print "Saved scatterplot of runoff turnout vs. normalized observer " +\
            "deployment density to", SCATTER_TURNOUT_NORM_OBS_DEP
    plt.close()

    # Output province num to province name dictionary
    csvWriter = csv.writer(open(NUM_TO_PROV_FILE, "w"))
    csvWriter.writerow(["ProvinceNum", "ProvinceName"])

    for key, val in provinceNumToName.items():
        csvWriter.writerow([key, val])

    print "Saved province num to name mapping to", NUM_TO_PROV_FILE

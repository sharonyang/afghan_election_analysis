# By: Laksh Bhasin
# Description: This script tries to answer the question of whether changing
# the number of election observers in a given province has an effect on
# changing the turnout. One way of doing this is comparing the data on
# election observer deployment between the first-round and runoff
# elections, and seeing if this matches any trends in turnout changes.
#
# Of course, we have to be careful to normalize the observer deployment
# counts since the number of election observers did go up between the two
# rounds. Thus, instead of comparing raw observer counts, we'll look at how
# the "observer deployment z-score" changed between the two elections. This
# is just defined by taking the observer count for a given province (in a
# given election), subtracting off the mean observer count (over all
# provinces for that election), and dividing by the std of observer counts
# (over all provinces for that election).
#
# Inputs:
#       * ../raw_data/raw_observers_first_round.csv
#       * ../raw_data/raw_observers_runoff.csv
#       * ../raw_data/raw_first_round_turnout.csv
#       * ../clean_data/runoff_votes_and_turnout.csv
#
# Outputs:
#       * ../clean_data/turnout_change.png - This is a bar graph showing
#         the percent change in turnout in each province between the two
#         elections. On the x-axis, each province is just assigned a
#         number.
#       * ../clean_data/obs_dep_change.png - This is a bar graph that shows
#         the percent change in the **observer deployment z-score** between
#         the two elections, for each province.
#       * ../clean_data/obs_dep_turnout_change.png - A combination of the
#         above two graphs, on the same set of axes.
#       * ../clean_data/num_to_province.csv - A CSV file that describes the
#         mapping between numbers (used in the above graphs) and actual
#         province names.
#
# Precondition: there are 34 provinces, and it is essential that their
# names match across all of the input CSV files!
#


import csv
import numpy as np
import matplotlib.pyplot as plt


# Constants

RAW_DATA_DIR = "../raw_data/"
CLEAN_DATA_DIR = "../clean_data/"

# INPUT FILES

# CSV file for first-round election observer deployment
FIRST_ROUND_OBS_DEP_FILE = RAW_DATA_DIR + "raw_observers_first_round.csv"

# CSV file for runoff election observer deployment
RUNOFF_OBS_DEP_FILE = RAW_DATA_DIR + "raw_observers_runoff.csv"

# CSV file for first round turnout data (by province).
FIRST_ROUND_TURNOUT_FILE = RAW_DATA_DIR + "raw_first_round_turnout.csv"

# CSV file for runoff votes and turnout data (by district). This is also
# what we'll use to get population data.
RUNOFF_TURNOUT_FILE = CLEAN_DATA_DIR + "runoff_votes_and_turnout.csv"

# OUTPUT FILES

# Bar graph for percent change in turnout vs province number
BAR_GRAPH_TURNOUT_CHANGE = CLEAN_DATA_DIR + "turnout_change.png"

# Bar graph for percent change in observer deployment z-score vs province
# number.
BAR_GRAPH_OBS_DEP_CHANGE = CLEAN_DATA_DIR + "obs_dep_change.png"

# Bar graph combining the above two bar graphs on the same axes.
BAR_GRAPH_TURNOUT_OBS_DEP_CHANGE = CLEAN_DATA_DIR +\
        "obs_dep_turnout_change.png"

# CSV file describing the mapping from numbers to actual province names.
NUM_TO_PROV_FILE = CLEAN_DATA_DIR + "num_to_province.csv"


# Global variables

# Dicts to track province data (cached to avoid regeneration).
provinceNumToName = None


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

    provinceSet = set()

    # Populate provinceSet by parsing RUNOFF_TURNOUT_FILE
    with open(RUNOFF_TURNOUT_FILE, 'rU') as csvFile:
        csvReader = csv.DictReader(csvFile)

        for row in csvReader:
            provinceSet.add(row['Province'])

    # Sort the list of provinces. Each province's number is just its index
    # in this sorted list.
    sortedProvinceList = sorted(list(provinceSet))

    provinceNumToName = dict()

    for i in range(len(sortedProvinceList)):
        provinceNumToName[i] = sortedProvinceList[i]

    return provinceNumToName


# This function returns a dictionary that maps province names to their
# populations. This uses the data in RUNOFF_TURNOUT_FILE.
#
def getProvinceNameToPop():
    # This dict will map from a province's name to its population.
    provinceNameToPop = dict()

    # Populate provinceNameToPop by parsing RUNOFF_TURNOUT_FILE
    with open(RUNOFF_TURNOUT_FILE, 'rU') as csvFile:
        csvReader = csv.DictReader(csvFile)

        for row in csvReader:
            provinceName = row['Province']
            districtPop = int(row['TotalPopulation'])

            if provinceName in provinceNameToPop:
                provinceNameToPop[provinceName] += districtPop
            else:
                provinceNameToPop[provinceName] = districtPop

    return provinceNameToPop


# This function returns a dictionary that maps province numbers to the
# percent change in turnout percentage, from the first-round election to
# the runoff election.
#
def getProvinceNumToTurnoutChange():
    # Make sure provinceNumToName is populated.
    global provinceNumToName
    populateProvinceNumToName()

    pass


# This function returns a dictionary that maps province numbers to the
# change in the "observer deployment z-score", from the first-round
# election to the runoff election.
#
def getProvinceNumToObsDepChange():
    # Make sure provinceNumToName is populated.
    global provinceNumToName
    populateProvinceNumToName()

    pass


# Main code
if __name__ == "__main__":
    provinceNameToPop = getProvinceNameToPop()

    print provinceNameToPop


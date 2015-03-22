# By: Laksh Bhasin
# Description: A set of functions that are commonly used in various
# modules.

import csv
import numpy as np


# Constants

# VALUES
from afghan_constants import VOTING_FRACTION

# DIRECTORIES
RAW_DATA_DIR = "../raw_data/"
CLEAN_DATA_DIR = "../clean_data/"

# INPUT FILES

# CSV file for runoff votes and turnout data (by district). This is what
# we'll use to get population data.
RUNOFF_TURNOUT_FILE = CLEAN_DATA_DIR + "runoff_votes_and_turnout.csv"


# Global variables

# Dicts to track province data (cached to avoid regeneration).
provinceNumToName = None
provinceNameToPop = None
provinceDistrictToPop = None


# This function populates a dictionary that maps province numbers to
# province names. This dictionary is stored in the global variable
# provinceNumToName.
#
# The number for each province is assigned by finding its index in a list
# of sorted province names.
#
def populateProvinceNumToName():
    global provinceNumToName

    # If it's already populated, there's nothing to do.
    if provinceNumToName != None:
        return provinceNumToName

    provinceNumToName = getProvinceNumToName()

    return provinceNumToName


# This function populates a dictionary that maps province names to their
# populations. This uses the data in RUNOFF_TURNOUT_FILE. The dictionary is
# then stored in the global variable provinceNameToPop.
#
def populateProvinceNameToPop():
    global provinceNameToPop

    # If it's already populated, there's nothing to do.
    if provinceNameToPop != None:
        return provinceNameToPop

    provinceNameToPop = getProvinceNameToPop()

    return provinceNameToPop


# This function populates a dictionary that maps (Province, District)
# tuples to their populations.
#
def populateProvinceDistrictToPop():
    global provinceDistrictToPop

    # If it's already populated, just return.
    if provinceDistrictToPop != None:
        return provinceDistrictToPop

    provinceDistrictToPop = getProvinceDistrictToPop()

    return provinceDistrictToPop


# This function returns a dictionary that maps province numbers to province
# names. The number for each province is assigned by finding its index in a
# list of sorted province names. This requires using the data in
# RUNOFF_TURNOUT_FILE.
#
def getProvinceNumToName():
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


# This function returns a dictionary that maps (Province, District) tuples
# to their populations. This is used to look up the population of a given
# district (where the "Province" field is used for disambiguation
# purposes).
#
def getProvinceDistrictToPop():
    provinceDistrictToPop = dict()

    # Populate provinceDistrictToPop by parsing RUNOFF_TURNOUT_FILE
    with open(RUNOFF_TURNOUT_FILE, 'rU') as csvFile:
        csvReader = csv.DictReader(csvFile)

        for row in csvReader:
            provinceName = row['Province']
            districtName = row['District']
            districtPop = int(row['TotalPopulation'])

            if (provinceName, districtName) in provinceDistrictToPop:
                # (Province, District) tuples shouldn't repeat in this
                # dictionary.
                raise Exception("Repeated (province, district)" +\
                        "tuple (" + provinceName + ", " +\
                        districtName + ") in " +\
                        RUNOFF_TURNOUT_FILE + "!")
            else:
                provinceDistrictToPop[(provinceName, districtName)] = \
                        districtPop

    return provinceDistrictToPop


# This function returns a dictionary that maps province numbers to the
# turnout in that province (for the runoff election).
#
def getProvinceNumToTurnoutRunoff():
    # Make sure provinceNumToName and provinceNameToPop are populated.
    global provinceNumToName, provinceNameToPop
    populateProvinceNumToName()
    populateProvinceNameToPop()

    # Get the number of people who voted in each province.
    provinceNameToNumVotes = dict()

    with open(RUNOFF_TURNOUT_FILE, 'rU') as csvFile:
        csvReader = csv.DictReader(csvFile)

        for row in csvReader:
            provinceName = row['Province']
            numVoted = int(row['PopulationVoted'])

            if provinceName in provinceNameToNumVotes:
                provinceNameToNumVotes[provinceName] += numVoted
            else:
                provinceNameToNumVotes[provinceName] = numVoted

    # Get the turnout in each province by dividing the number of votes in
    # that province by (its population times VOTING_FRACTION) and
    # multiplying by 100 to get a percentage. Note that the following
    # dictionary actually maps province *numbers* to their turnout
    # percentages.
    provinceNumToTurnout = dict()

    for provinceNum in provinceNumToName:
        provinceName = provinceNumToName[provinceNum]
        numVotes = provinceNameToNumVotes[provinceName]
        provincePop = provinceNameToPop[provinceName]

        provinceNumToTurnout[provinceNum] = 100.0 * \
                numVotes / (provincePop * VOTING_FRACTION)

    return provinceNumToTurnout


# This function returns a dictionary that maps (Province, District) tuples
# to the turnout in that province (for the runoff election).
#
def getProvinceDistrictToTurnoutRunoff():
    # Make sure provinceDistrictToPop is populated.
    global provinceDistrictToPop
    populateProvinceDistrictToPop()

    # Get the number of people who voted in each district. This dictionary
    # maps (Province, District) tuples to the number of votes in that
    # district.
    provinceDistrictToNumVotes = dict()

    with open(RUNOFF_TURNOUT_FILE, 'rU') as csvFile:
        csvReader = csv.DictReader(csvFile)

        for row in csvReader:
            provinceName = row['Province']
            districtName = row['District']
            numVoted = int(row['PopulationVoted'])

            if (provinceName, districtName) in provinceDistrictToNumVotes:
                provinceDistrictToNumVotes[\
                        (provinceName, districtName)] += numVoted
            else:
                provinceDistrictToNumVotes[\
                        (provinceName, districtName)] = numVoted

    # Get the turnout in each district by dividing the number of votes in
    # that distrit by (its population times VOTING_FRACTION) and
    # multiplying by 100 to get a percentage.
    provinceDistrictToTurnout = dict()

    for provinceDistrict in provinceDistrictToNumVotes:
        numVotes = provinceDistrictToNumVotes[provinceDistrict]
        districtPop = provinceDistrictToPop[provinceDistrict]

        provinceDistrictToTurnout[provinceDistrict] = 100.0 * \
                numVotes / (districtPop * VOTING_FRACTION)

    return provinceDistrictToTurnout


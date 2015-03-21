# By: Laksh Bhasin
# Description: A set of functions that are commonly used in various
# modules.

import csv
import numpy as np


# Constants

# DIRECTORIES
RAW_DATA_DIR = "../raw_data/"
CLEAN_DATA_DIR = "../clean_data/"

# INPUT FILES

# CSV file for runoff votes and turnout data (by district). This is what
# we'll use to get population data.
RUNOFF_TURNOUT_FILE = CLEAN_DATA_DIR + "runoff_votes_and_turnout.csv"


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


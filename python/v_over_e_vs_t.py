# By: Laksh Bhasin
# Description: As the name of this script suggests, this program outputs
# V/E vs T plots using all district-level data. These plots are generated
# for Ghani and Abdullah, using the data from the runoff election.
#
# Input files:
#       * ../clean_data/runoff_votes_and_turnout.csv
#
# Output files:
#       * ../figures/v_over_e_vs_t/runoff_abdullah_v_over_e_vs_t.png - The
#         V/E vs T plot for Abdullah. This includes all districts' data.
#       * ../figures/v_over_e_vs_t/runoff_abdullah_v_over_e_vs_t_resid.png
#         - The residual plot for a linear fit on the above data.
#       * ../figures/v_over_e_vs_t/runoff_ghani_v_over_e_vs_t.png - The V/E
#         vs T plot for Ghani. This includes all districts' data.
#       * ../figures/v_over_e_vs_t/runoff_ghani_v_over_e_vs_t_resid.png -
#         The residual plot for a linear fit on the above data.
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
FIGURE_DIR = "../figures/v_over_e_vs_t/"

# INPUT FILES

# CSV file for runoff votes (by district).
RUNOFF_VOTES_FILE = CLEAN_DATA_DIR + "runoff_votes_and_turnout.csv"

# OUTPUT FILES

# The V/E vs T plot for Abdullah, over all districts' data.
ABDULLAH_V_OVER_E_VS_T = FIGURE_DIR + "runoff_abdullah_v_over_e_vs_t.png"

# The residual plot for the above plot's linear fit.
ABDULLAH_V_OVER_E_VS_T_RESID = FIGURE_DIR +\
        "runoff_abdullah_v_over_e_vs_t_resid.png"

# The V/E vs T plot for Ghani, over all districts' data.
GHANI_V_OVER_E_VS_T = FIGURE_DIR + "runoff_ghani_v_over_e_vs_t.png"

# The residual plot for the above plot's linear fit.
GHANI_V_OVER_E_VS_T_RESID = FIGURE_DIR +\
        "runoff_ghani_v_over_e_vs_t_resid.png"


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


# This function takes a candidate (either "Abdullah" or "Ghani") and
# returns a mapping from (Province, District) tuples to the V/E for that
# candidate in that district. Note that the V/E is expressed as a
# percentage in the returned dictionary.
#
def getProvinceDistrictToVOverE(candidate):
    if candidate is not "Abdullah" and candidate is not "Ghani":
        raise ValueError("The input candidate " + candidate + " was " +\
                "neither Abdullah nor Ghani!")

    global provinceDistrictToPop
    populateProvinceDistrictToPop()

    # Set the column to look at in the CSV.
    voteColumn = "GhaniVotes"

    if candidate is "Abdullah":
        voteColumn = "AbdullahVotes"

    # Go through RUNOFF_VOTES_FILE, add up all of the votes for the
    # specified candidate, and divide by the voting-eligible population E
    # (which is the district population times VOTING_FRACTION).
    provinceDistrictToCandidateVOverE = dict()

    with open(RUNOFF_VOTES_FILE, 'rU') as csvFile:
        csvReader = csv.DictReader(csvFile)

        for row in csvReader:
            provinceName = row['Province']
            districtName = row['District']
            candidateVotes = float(row[voteColumn])

            districtPop = provinceDistrictToPop[(provinceName,
                                                 districtName)]

            if (provinceName, districtName) in \
                    provinceDistrictToCandidateVOverE:

                provinceDistrictToCandidateVOverE[\
                        (provinceName, districtName)] += 100.0 *\
                        candidateVotes / (VOTING_FRACTION * districtPop)

            else:
                provinceDistrictToCandidateVOverE[\
                        (provinceName, districtName)] = 100.0 *\
                        candidateVotes / (VOTING_FRACTION * districtPop)

    return provinceDistrictToCandidateVOverE


# This function plots V/E vs T for a given candidate, as well as a residual
# plot. It takes a dictionary that maps (Province, District) tuples to that
# candidate's V/E, as well as another dictionary that maps (Province,
# District) tuples to turnout. The output plots are saved to plotSaveFile
# (just the V/E vs T plot with the linear fit) and residPlotSaveFile (for
# the residual plot).
#
def plotVOverEVsT(candidate,
                  provinceDistrictToCandidateVOverE,
                  provinceDistrictToTurnout,
                  plotTitle,
                  residPlotTitle,
                  plotColor,
                  plotSaveFile,
                  residPlotSaveFile):

    if candidate is not "Abdullah" and candidate is not "Ghani":
        raise ValueError("The input candidate " + candidate + " was " +\
                "neither Abdullah nor Ghani!")

    # Make sure that both the V/E and turnout dictionaries have the same
    # keys!
    assert sorted(provinceDistrictToCandidateVOverE.keys()) == \
            sorted(provinceDistrictToTurnout.keys())

    # Get the x and y values for this plot by unpacking the dictionaries.
    xValues = list()
    yValues = list()

    for provinceDistrict in provinceDistrictToCandidateVOverE:
        xValues.append(provinceDistrictToTurnout[provinceDistrict])
        yValues.append(provinceDistrictToCandidateVOverE[provinceDistrict])

    xValues = np.array(xValues)
    yValues = np.array(yValues)

    # Perform linear regression on the data.
    slope, intercept, rValue, pValue, stdErr = linregress(xValues, yValues)
    xValuesFitLine = np.arange(0.0, 210.0, 10.0)
    yValuesFitLine = slope * xValuesFitLine + intercept

    # Get the residuals
    residValues = yValues - (slope * xValues + intercept)

    # Plot V/E vs T with the linear fit, as well as y = x for reference.
    fig = plt.figure()
    fig.set_facecolor('white')
    plt.scatter(xValues, yValues, color = plotColor, s = 20)
    plt.plot(xValuesFitLine, yValuesFitLine, 'k', lw=1.5)
    plt.plot([0.0, 300.0], [0.0, 300.0], 'k--')
    plt.xlim([0.0, 200.0])
    plt.ylim([0.0, 200.0])
    plt.xlabel("Turnout Percentage")
    plt.ylabel("V/E for " + candidate)
    plt.title(plotTitle)

    # Include the fitted line's equation and r^2. Format the equation
    # correctly depending on the intercept's sign.
    if intercept >= 0:
        plt.text(30.0, 150.0, r"$V/E \,= \," + str(slope)[0:6] + "T \,+\, " +\
                 str(intercept)[0:6] + r"$")
    else:
        plt.text(30.0, 150.0, r"$V/E \,= \," + str(slope)[0:6] + "T \,-\, " +\
                 str(abs(intercept))[0:6] + r"$")

    plt.text(30.0, 137.0, r"$r^2 = \," + str(rValue**2.0)[0:6] + r"$")

    # Save to file and inform the user.
    plt.savefig(plotSaveFile, bbox_inches = "tight")
    plt.close()
    print "Saved V/E vs T plot for", candidate, "to\n", plotSaveFile

    # Plot the residual plot, with a flat line at y = 0 for reference.
    fig = plt.figure()
    fig.set_facecolor('white')
    plt.scatter(xValues, residValues, color = plotColor, s = 20)
    plt.plot([0.0, 250.0], [0.0, 0.0], 'k--')
    plt.xlim([0.0, 200.0])
    plt.ylim([-100.0, 100.0])
    plt.xlabel("Turnout Percentage")
    plt.ylabel("Residual V/E")
    plt.title(residPlotTitle)

    # Save to file and inform the user.
    plt.savefig(residPlotSaveFile, bbox_inches = "tight")
    plt.close()
    print "Saved V/E vs T residual plot for", candidate, "to\n",\
            residPlotSaveFile, "\n"


# Main code
if __name__ == "__main__":
    # Get the necessary dictionaries for the runoff election data.
    provinceDistrictToTurnout = getProvinceDistrictToRunoffTurnout()
    provinceDistrictToAbdullahVOverE = \
            getProvinceDistrictToVOverE("Abdullah")
    provinceDistrictToGhaniVOverE = getProvinceDistrictToVOverE("Ghani")

    # Plot V/E vs T (including linear fits and residuals) for both
    # candidates, using all district-level data. The following function
    # calls will also save the plots to file.
    plotVOverEVsT("Abdullah",
                  provinceDistrictToAbdullahVOverE,
                  provinceDistrictToTurnout,
                  "V/E vs T for Abdullah",
                  "V/E vs T Residuals for Abdullah",
                  ABDULLAH_COLOR,
                  ABDULLAH_V_OVER_E_VS_T,
                  ABDULLAH_V_OVER_E_VS_T_RESID)

    plotVOverEVsT("Ghani",
                  provinceDistrictToGhaniVOverE,
                  provinceDistrictToTurnout,
                  "V/E vs T for Ghani",
                  "V/E vs T Residuals for Ghani",
                  GHANI_COLOR,
                  GHANI_V_OVER_E_VS_T,
                  GHANI_V_OVER_E_VS_T_RESID)


# Run this plot in base directory (afghan_election_analysis)
# Do: Rscript R/first_digit.R
# Output will be in figures/digit_analysis/<winner>_first_digit.png
# Get ggplot2 library on Linux by
# sudo apt-get install r-cran-ggplot2

# Read data.
results <- read.csv("clean_data/runoff_votes_and_turnout.csv", header=TRUE)

# Set plot output destination.
require(ggplot2)

# Get districts where Abdullah/Ghani won.
Abdullah_Won <- results[results[, 3] > results[, 4], ]
Ghani_Won <- results[results[, 3] < results[, 4], ]

# Start plotting Abdullah's data.
Abdullah_vote_counts <- c(Abdullah_Won$PopulationVoted)

# Take last digit
Abdullah_Won_First_Digit <- sapply(Abdullah_vote_counts,
    function(x) substr(x, 1, 1))
Abdullah_Won_first <- as.data.frame(as.numeric(Abdullah_Won_First_Digit))

votes <- ggplot(Abdullah_Won_first, aes(x=Abdullah_Won_First_Digit))

# Match color according to python/afghan_constants.py
savefile <- paste("figures/digit_analysis/Abdullah_first_digit.png", sep="")
png(file=savefile, width=600)
print(votes + geom_histogram(bins=100, fill="#FFAE19"))
length(Abdullah_Won_First_Digit)

# Start plotting Ghani's data.
Ghani_vote_counts <- c(Ghani_Won$PopulationVoted)

# Take last digit
Ghani_Won_First_Digit <- sapply(Ghani_vote_counts,
    function(x) substr(x, 1, 1))
Ghani_Won_first <- as.data.frame(as.numeric(Ghani_Won_First_Digit))
length(Ghani_Won_First_Digit)
votes <- ggplot(Ghani_Won_first, aes(x=Ghani_Won_First_Digit))

# Match color according to python/afghan_constants.py
savefile <- paste("figures/digit_analysis/Ghani_first_digit.png", sep="")
png(file=savefile, width=600)
print(votes + geom_histogram(bins=100, fill="#72AFE4"))

# Run this plot in base directory (afghan_election_analysis)
# Do: Rscript R/last_digit.R
# Output will be in figures/digit_analysis/<winner>_last_digit.pdf
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
Abdullah_Won_Last_Digit <- sapply(Abdullah_vote_counts,
    function(x) substr(x, nchar(x), nchar(x)))
Abdullah_Won_last_1 <- as.data.frame(as.numeric(Abdullah_Won_Last_Digit))

votes <- ggplot(Abdullah_Won_last_1, aes(x=Abdullah_Won_Last_Digit))

# Match color according to python/afghan_constants.py
savefile <- paste("figures/digit_analysis/Abdullah_last_digit.png", sep="")
png(file=savefile, width = 600)
print(votes + geom_histogram(bins=100, fill="#FFAE19"))

# Start plotting Ghani's data.
Ghani_vote_counts <- c(Ghani_Won$PopulationVoted)

# Take last digit
Ghani_Won_Last_Digit <- sapply(Ghani_vote_counts,
    function(x) substr(x, nchar(x), nchar(x)))
Ghani_Won_last_1 <- as.data.frame(as.numeric(Ghani_Won_Last_Digit))

votes <- ggplot(Ghani_Won_last_1, aes(x=Ghani_Won_Last_Digit))

# Match color according to python/afghan_constants.py
savefile <- paste("figures/digit_analysis/Ghani_last_digit.png", sep="")
png(file=savefile, width=600)
print(votes + geom_histogram(bins=100, fill="#72AFE4"))

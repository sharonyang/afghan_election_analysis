# Run this plot in base directory (afghan_election_analysis)
# Do: Rscript R/first_digit.R
# Output will be in figures/digit_analysis/first_digit_analysis.pdf
# Get ggplot2 library on Linux by
# sudo apt-get install r-cran-ggplot2

# Read data.
results <- read.csv("clean_data/runoff_votes_and_turnout.csv", header=TRUE)

# Set plot output destination.
require(ggplot2)
pdf(file="figures/digit_analysis/first_digit_analysis.pdf")

# Get districts where Abdullah/Ghani won.
Abdullah_Won <- results[results[, 3] > results[, 4], ]
Ghani_Won <- results[results[, 3] < results[, 4], ]

# Start plotting Abdullah's data.
Abdullah_vote_counts <- c(Abdullah_Won$PopulationVoted)

# Take last digit
Abdullah_Won_First_Digit <- sapply(Abdullah_vote_counts,
    function(x) substr(x, 1, 1))
Abdullah_Won_last_1 <- as.data.frame(as.numeric(Abdullah_Won_First_Digit))

votes <- ggplot(Abdullah_Won_last_1, aes(x=Abdullah_Won_First_Digit))

# Match color according to python/afghan_constants.py
votes + geom_histogram(bins=100, fill="#FFAE19")

# Start plotting Ghani's data.
Ghani_vote_counts <- c(Ghani_Won$PopulationVoted)

# Take last digit
Ghani_Won_First_Digit <- sapply(Ghani_vote_counts,
    function(x) substr(x, 1, 1))
Ghani_Won_last_1 <- as.data.frame(as.numeric(Ghani_Won_First_Digit))

votes <- ggplot(Ghani_Won_last_1, aes(x=Ghani_Won_First_Digit))

# Match color according to python/afghan_constants.py
votes + geom_histogram(bins=100, fill="#72AFE4")

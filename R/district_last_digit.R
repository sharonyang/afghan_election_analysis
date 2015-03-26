# Run this plot in base directory (afghan_election_analysis)
# Do: Rscript R/last_digit.R
# Output will be in figures/digit_analysis/<winner>_last_digit.pdf
# Get ggplot2 library on Linux by
# sudo apt-get install r-cran-ggplot2

#     Pearson's Chi-squared test

# data:  abdullah
# X-squared = 7.2676, df = 9, p-value = 0.6093


#     Pearson's Chi-squared test

# data:  ghani
# X-squared = 5.9023, df = 9, p-value = 0.7497



# Read data.
results <- read.csv("clean_data/runoff_votes_and_turnout.csv", header=TRUE)

# Set plot output destination.
require(ggplot2)
require(MASS)

Abdullah_Won <- results[results[, 3] > results[, 4], ]
Ghani_Won <- results[results[, 3] < results[, 4], ]

# Start plotting Abdullah's data.
Abdullah_vote_counts <- c(Abdullah_Won$AbdullahVotes)

# Take last digit
Abdullah_Won_Last_Digit <- sapply(Abdullah_vote_counts,
    function(x) substr(x, nchar(x), nchar(x)))
Abdullah_Won_last_1 <- as.data.frame(as.numeric(Abdullah_Won_Last_Digit))

votes <- ggplot(Abdullah_Won_last_1, aes(x=Abdullah_Won_Last_Digit))

# Match color according to python/afghan_constants.py
savefile <- paste("figures/digit_analysis/Abdullah_last_digit_district.png", sep="")
png(file=savefile, width = 600)
print(votes + geom_histogram(bins=100, fill="#FFAE19") +
    ggtitle("Last-Digit Analysis for Abdullah's Votes in Abdullah-Won Districts") +
    labs(x="Least Significant Digit", y="Count"))

# Start plotting Ghani's data.
Ghani_vote_counts <- c(Ghani_Won$GhaniVotes)

# Take last digit
Ghani_Won_Last_Digit <- sapply(Ghani_vote_counts,
    function(x) substr(x, nchar(x), nchar(x)))
Ghani_Won_last_1 <- as.data.frame(as.numeric(Ghani_Won_Last_Digit))

votes <- ggplot(Ghani_Won_last_1, aes(x=Ghani_Won_Last_Digit))

# Match color according to python/afghan_constants.py
savefile <- paste("figures/digit_analysis/Ghani_last_digit_district.png", sep="")
png(file=savefile, width=600)
print(votes + geom_histogram(bins=100, fill="#72AFE4") + 
    ggtitle("Last-Digit Analysis for Ghani's Votes in Ghani-Won Districts") +
    labs(x="Least Significant Digit", y="Count"))

# Abdullah's data for chi-squared analysis
abdullah_p <- as.data.frame(table(Abdullah_Won_last_1))$Freq
total <- length(Abdullah_vote_counts) / 10
abdullah_t <- c(total, total, total, total, total, total, total,
    total, total, total)

abdullah = as.data.frame(rbind(abdullah_p, abdullah_t))
chisq.test(abdullah)

# Ghani's data for chi-squared analysis
ghani_p <- as.data.frame(table(Ghani_Won_last_1))$Freq
total <- length(Ghani_vote_counts) / 10
ghani_t <- c(total, total, total, total, total, total, total,
    total, total, total)

ghani = as.data.frame(rbind(ghani_p, ghani_t))
chisq.test(ghani)

# Run this plot in base directory (afghan_election_analysis)
# Do: Rscript R/station_last_digit.R
# Output will be in figures/digit_analysis/<winner>_last_digit_polling_station.pdf
# Get ggplot2 library on Linux by
# sudo apt-get install r-cran-ggplot2

# 	Pearson's Chi-squared test

# data:  ghani
# X-squared = 90.1215, df = 9, p-value = 1.539e-15

#  [1] 2875 2151 2181 2195 2158 2217 2124 2209 2238 2121
#  [1] 2246.9 2246.9 2246.9 2246.9 2246.9 2246.9 2246.9 2246.9 2246.9 2246.9

# 	Pearson's Chi-squared test

# data:  abdullah
# X-squared = 160.0029, df = 9, p-value < 2.2e-16


require(MASS)
require(ggplot2)

## read data
results <- read.csv("raw_data/raw_votes_runoff.csv", header=TRUE)
## combine counts for both candidates
vote_counts <- c(results$"Ghani")
## remove counts under 100
vote_counts_filter <- vote_counts[vote_counts > 9 && vote_counts < 600]

## take last two digits; no need to add leading zero because all numbers are three digits
last_one <- sapply(vote_counts_filter, function(x) substr(x, nchar(x)  , nchar(x)))
last_1 <- as.data.frame(as.numeric(last_one))

## plot, actually done with d3.js in browser
votes <- ggplot(last_1, aes(x=last_one))

savefile <- paste("figures/digit_analysis/Ghani_last_digit_polling_stations.png", sep="")
png(file=savefile, width = 600)
print(votes + geom_histogram(bins=100, fill="#72AFE4") +
    ggtitle("Last-Digit Analysis for Ghani's Votes in All Polling Stations") +
    labs(x="Least Significant Digit", y="Count"))

total <- length(last_one) / 10
curr_t <- c(total, total, total, total, total, total, total,
    total, total, total)
last_1 <- as.data.frame(table(last_1))$Freq
ghani = as.data.frame(rbind(last_1, curr_t))
chisq.test(ghani)
last_1
curr_t

## combine counts for both candidates
vote_counts <- c(results$"Abdullah")
## remove counts under 100
vote_counts_filter <- vote_counts[vote_counts > 9 && vote_counts < 600]

## take last two digits; no need to add leading zero because all numbers are three digits
last_one <- sapply(vote_counts_filter, function(x) substr(x, nchar(x)  , nchar(x)))
last_1 <- as.data.frame(as.numeric(last_one))
## plot, actually done with d3.js in browser
votes <- ggplot(last_1, aes(x=last_one))

# Match color according to python/afghan_constants.py
savefile <- paste("figures/digit_analysis/Abdullah_last_digit_polling_stations.png", sep="")
png(file=savefile, width = 600)
print(votes + geom_histogram(bins=100, fill="#FFAE19") +
    ggtitle("Last-Digit Analysis for Abdullah's Votes in All Polling Stations") +
    labs(x="Least Significant Digit", y="Count"))

total <- length(last_one) / 10
curr_t <- c(total, total, total, total, total, total, total,
    total, total, total)
last_1 <- as.data.frame(table(last_1))$Freq
abdullah = as.data.frame(rbind(last_1, curr_t))
chisq.test(abdullah)
last_1
curr_t

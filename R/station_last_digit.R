# Run this plot in base directory (afghan_election_analysis)
# Do: Rscript R/station_last_digit.R
# Output will be in figures/digit_analysis/<winner>_last_digit_polling_station.pdf
# Get ggplot2 library on Linux by
# sudo apt-get install r-cran-ggplot2

# 	Pearson's Chi-squared test

# data:  ghani
# X-squared = 87.8034, df = 9, p-value = 4.487e-15

#  [1] 1619 1050 1119 1140 1073 1178 1106 1182 1198 1121
#  [1] 1178.6 1178.6 1178.6 1178.6 1178.6 1178.6 1178.6 1178.6 1178.6 1178.6

# 	Pearson's Chi-squared test

# data:  abdullah
# X-squared = 6.0607, df = 9, p-value = 0.7338

#  [1] 1155 1023 1048 1071 1042 1046 1061 1051 1073 1018
#  [1] 1058.8 1058.8 1058.8 1058.8 1058.8 1058.8 1058.8 1058.8 1058.8 1058.8


require(MASS)
require(ggplot2)

## read data
results <- read.csv("raw_data/raw_votes_runoff.csv", header=TRUE)

# Get districts won by each candidates.
Abdullah_Won <- results[results[, 5] > results[, 6], ]
Ghani_Won <- results[results[, 5] < results[, 6], ]

Abdullah_Won <- Abdullah_Won$"Abdullah"
Ghani_Won <- Ghani_Won$"Ghani"

## remove counts under 10 and above 600
vote_counts_filter <- Ghani_Won[Ghani_Won > 9 && Ghani_Won < 600]

## take last digit; no need to add leading zero because all numbers are three digits
last_one <- sapply(vote_counts_filter, function(x) substr(x, nchar(x)  , nchar(x)))
last_1 <- as.data.frame(as.numeric(last_one))

votes <- ggplot(last_1, aes(x=last_one))

savefile <- paste("figures/digit_analysis/Ghani_last_digit_polling_stations.png", sep="")
png(file=savefile, width = 600)
print(votes + geom_histogram(bins=100, fill="#72AFE4") +
    ggtitle("Last-Digit Analysis for Ghani's Votes in in Ghani-Won Polling Stations") +
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
## remove counts under 10 and above 600
vote_counts_filter <- Abdullah_Won[Abdullah_Won > 9 && Abdullah_Won < 600]

## take last digit; no need to add leading zero because all numbers are three digits
last_one <- sapply(vote_counts_filter, function(x) substr(x, nchar(x)  , nchar(x)))
last_1 <- as.data.frame(as.numeric(last_one))
votes <- ggplot(last_1, aes(x=last_one))

# Match color according to python/afghan_constants.py
savefile <- paste("figures/digit_analysis/Abdullah_last_digit_polling_stations.png", sep="")
png(file=savefile, width = 600)
print(votes + geom_histogram(bins=100, fill="#FFAE19") +
    ggtitle("Last-Digit Analysis for Abdullah's Votes in Abdullah-Won Polling Stations") +
    labs(x="Least Significant Digit", y="Count"))

total <- length(last_one) / 10
curr_t <- c(total, total, total, total, total, total, total,
    total, total, total)
last_1 <- as.data.frame(table(last_1))$Freq
abdullah = as.data.frame(rbind(last_1, curr_t))
chisq.test(abdullah)
last_1
curr_t

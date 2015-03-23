# Run this plot in base directory (afghan_election_analysis)
# Do: Rscript R/benford_pval.R
# Output will be shown in terminal.

#     Pearson's Chi-squared test

# data:  abdullah
# X-squared = 8.6113, df = 8, p-value = 0.3761


#     Pearson's Chi-squared test

# data:  ghani
# X-squared = 5.2783, df = 8, p-value = 0.7275


require(MASS)

# Read data.
results <- read.csv("clean_data/first_digit_abdullah.csv", header=TRUE)
obs <- results[results[, 3] == "Observed", ]$Count
pred <- results[results[, 3] == "Predicted", ]$Count

# Abdullah data output.
abdullah = as.data.frame(rbind(obs, pred))
chisq.test(abdullah)

# Read data.
results <- read.csv("clean_data/first_digit_ghani.csv", header=TRUE)
obs <- results[results[, 3] == "Observed", ]$Count
pred <- results[results[, 3] == "Predicted", ]$Count

# Ghani data output.
ghani = as.data.frame(rbind(obs, pred))
chisq.test(ghani)

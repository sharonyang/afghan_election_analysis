# Run this plot in base directory (afghan_election_analysis)
# Do: Rscript R/benford_pval.R
# Output will be shown in terminal.

#     Pearson's Chi-squared test
# 
# data:  abdullah
# X-squared = 18.8415, df = 8, p-value = 0.01573

# Warning message:
# In chisq.test(abdullah) : Chi-squared approximation may be incorrect

#     Pearson's Chi-squared test

# data:  ghani
# X-squared = 31.4226, df = 8, p-value = 0.0001181

# Warning message:
# In chisq.test(ghani) : Chi-squared approximation may be incorrect

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

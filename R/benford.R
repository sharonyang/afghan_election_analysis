# Run this plot in base directory (afghan_election_analysis)
# Do: Rscript R/benford.R
# Output will be in figures/digit_analysis/<winner>_benford.png
# Get ggplot2 library on Linux by
# sudo apt-get install r-cran-ggplot2

require(ggplot2)

# Read data.
dat1 <- read.csv("clean_data/first_digit_abdullah.csv", header=TRUE)

plot_abdullah <- ggplot(data=dat1, aes(x=Digit, y=Count, fill=Type)) +
    geom_bar(bins=100, stat="identity",
        position=position_dodge(), colour="black")

# Match color according to python/afghan_constants.py
savefile <- paste("figures/digit_analysis/Abdullah_benford.png", sep="")
png(file=savefile, width=600)
print(plot_abdullah + scale_x_continuous(breaks=c(1,2,3,4,5,6,7,8,9)) +
    ggtitle("Benford Analysis for Abdullah's Votes in All Districts") +
    scale_fill_manual("Count Type", values = c("#FFAE19", "gray")) +
    labs(x="Most Significant Digit"))

# Read data.
dat2 <- read.csv("clean_data/first_digit_ghani.csv", header=TRUE)

plot_ghani <- ggplot(data=dat2, aes(x=Digit, y=Count, fill=Type)) +
    geom_bar(bins=100, stat="identity",
        position=position_dodge(), colour="black")

# Match color according to python/afghan_constants.py
savefile <- paste("figures/digit_analysis/Ghani_benford.png", sep="")
png(file=savefile, width=600)
print(plot_ghani + scale_x_continuous(breaks=c(1,2,3,4,5,6,7,8,9)) +
    ggtitle("Benford Analysis for Ghani's Votes in All Districts") +
    scale_fill_manual("Count Type", values = c("#72AFE4", "gray")) +
    labs(x="Most Significant Digit"))

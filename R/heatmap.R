# Run this plot in base directory (afghan_election_analysis)
# Do: Rscript R/heatmap.R
# Output will be in figures/heatmap/heatmap_turnout.pdf
# Get ggplot2 library on Linux by
# sudo apt-get install r-cran-ggplot2

library(ggplot2)
pdf(file="figures/heatmap/heatmap_turnout.pdf")
full_data <- read.csv("clean_data/runoff_votes_and_turnout.csv", header = TRUE)

Voter_Turnout <- sapply(full_data$TurnoutPercent,
    function(x) min(x, 100)) # TODO: Where do we cap the turnout?
Winner_Voter_Turnout <-
    full_data$GhaniVotes * 100 / (full_data$PopulationVoted)

d1 <- ggplot(as.data.frame(cbind(Voter_Turnout, Winner_Voter_Turnout)),
	aes(Voter_Turnout, Winner_Voter_Turnout))
d1 + geom_bin2d(bins=40) + scale_fill_gradientn(colours= c('blue',
	'green', 'yellow', 'yellow', 'orange', 'orange', 'red', 'red',
	'red', 'red', 'red', 'red')) + theme(panel.background =
    element_rect(fill = 'darkblue'), panel.grid.major =
    element_line(colour = 'darkblue'), panel.grid.minor =
    element_line(colour= 'darkblue'))


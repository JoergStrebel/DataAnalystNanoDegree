
library(ggplot2)
library(tidyr)
library(dplyr)
library(RColorBrewer)

# Load the Data
setwd("/home/jstrebel/devel/udacity/Ch6_Project/")
stroop_df = read.csv("stroopdata.csv", fill = FALSE,
                      stringsAsFactors = FALSE,
                      na.strings=c("", "NA"))

stroop_df$participant <- seq(1,length(stroop_df$Congruent))
stroop_df$TimeDiff <- stroop_df$Congruent - stroop_df$Incongruent

# create long form
stroop_df_long <- gather(stroop_df, 'Congruent', 'Incongruent', 
                         key = 'Condition', value = 'Time')

# plots - boxplot
ggplot(aes(x = Condition, y = Time), data = stroop_df_long) + 
  geom_boxplot() +
  stat_summary(fun.y = mean, geom ='point', shape = 4) +
  xlab('Condition') +
  ylab('Time (seconds)')

by(stroop_df_long$Time, stroop_df_long$Condition , summary)
by(stroop_df_long$Time, stroop_df_long$Condition , sd)

# plots - histogram of the mean difference
ggplot(aes(x = TimeDiff),
       data = stroop_df) +
  geom_histogram(binwidth = 1) + 
  ylab('Frequency') +
  xlab('Time difference (seconds)')

summary(stroop_df$TimeDiff)
sd(stroop_df$TimeDiff)

# execute t-test automatically
t.test(stroop_df$Congruent, stroop_df$Incongruent, alternative = 'less', 
       paired = TRUE, conf.level = 0.95)


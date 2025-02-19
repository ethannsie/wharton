library(dplyr)

# Assuming 'whartondata' contains columns 'team' and 'win' (1 for win, 0 for loss)

# Calculate win-loss record for each team
team_records <- whartondata %>%
  group_by(V3) %>%
  summarize(
    wins = sum(V35, na.rm = TRUE), # Count the number of wins (1s)
    losses = n() - sum(V35, na.rm = TRUE) # Total games - wins = losses
  ) %>%
  arrange(desc(wins), losses)

# Save the win-loss record to a new CSV file
write.csv(team_records, file = "team_win_loss_records.csv", row.names = FALSE)

# Print the results
print(team_records)
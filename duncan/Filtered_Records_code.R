library(dplyr)

# Assuming 'whartondata' contains columns 'team' and 'win' (1 for win, 0 for loss)

#Assuming win is coded for each team game result as 1 or 0
team_records <- whartondata %>%
  group_by(V3) %>%
  summarize(
    wins = sum(V35, na.rm = TRUE), # Count the number of wins (1s)
    losses = n() - sum(V35, na.rm = TRUE),  # Total games - wins = losses
    num_games = n() #Count of the total amount of games
  ) %>%
  arrange(desc(wins), losses)

# Filter team_records to keep only teams with at least 5 games played
team_records_filtered <- team_records %>%
  filter(num_games >= 5)

# Print the filtered team records
print(team_records_filtered)

# Optional: Save the filtered team records to a CSV file
write.csv(team_records_filtered, "filtered_team_win_loss_records.csv", row.names = FALSE)
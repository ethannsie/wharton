library(dplyr)

# Assuming win is coded for each team game result as 1 or 0
team_records <- whartondata %>%
  group_by(V3) %>%
  summarize(
    wins = sum(V35, na.rm = TRUE), # Count the number of wins (1s)
    losses = n() - sum(V35, na.rm = TRUE),  # Total games - wins = losses
    num_games = n() #Count of the total amount of games
  ) %>%
  arrange(desc(wins), losses)

# 1. Calculate team-level averages of offensive and defensive rating in whartondata
# Assuming your offensive rating is in column 'offensive_rating' and
# defensive rating is in column 'defensive_rating'.  If they are in different
# Columns, please change accordingly

team_avg_ratings <- whartondata %>%
  group_by(V3) %>%
  summarize(
    avg_offensive_rating = mean(V32, na.rm = TRUE),
    avg_defensive_rating = mean(V33, na.rm = TRUE)
  )

# 2. Join offensive and defensive ratings into team_records
team_records_filtered <- team_records_filtered %>%
  left_join(team_avg_ratings, by = "V3") # Join by team name (V3)

# 3. Rearrange columns to position offensive and defensive rating after num_games

# Get a vector of existing column names in team_records
col_order <- names(team_records_filtered)

# Insert "avg_offensive_rating" and "avg_defensive_rating" to a vector containing
# the original column names
insert_index <- which(col_order == "num_games") + 1 # find the index of where we want to insert

#Using append to insert the offensive and defensive ratings after index
col_order <- append(col_order, c("avg_offensive_rating", "avg_defensive_rating"), after = insert_index)

#Select only unique columns for the ordering since the merge might have added duplicates
col_order <- unique(col_order)

# Reorder team_records based on the newly built vector
team_records_filtered <- team_records_filtered %>%
  select(all_of(col_order)) #Reorder all columns

# Display the first few rows of the modified team_records
print(team_records_filtered)

# Optional: Save the modified team_records to a CSV file
write.csv(team_records_filtered, "records_with_ratings.csv", row.names = FALSE)

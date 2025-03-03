# Load the data
team_data <- read.csv("normagg2.csv")
game_data <- read.csv("EastGames.csv")

# Inspect the data (optional)
head(team_data)
head(game_data)

# Prepare team skill parameters from the 'Normalized Aggregate Rating 2'
teams <- unique(c(as.character(team_data$Team))) #Ensure team names are characters

# Initialize skill parameters using Normalized Aggregate Rating
skill_parameters <- setNames(team_data$Normalized.Aggregate.Rating.2, as.character(team_data$Team)) #Ensures all the names are in characters

# If there are teams in the game data that are not in the team_data set, assign them a default initial skill
all_teams_in_games <- unique(c(as.character(game_data$team_home), as.character(game_data$team_away))) #Ensure team names are characters
missing_teams <- setdiff(all_teams_in_games, names(skill_parameters))

if(length(missing_teams) > 0) {
  default_skill <- mean(skill_parameters, na.rm = TRUE)  # or some other reasonable default, use na.rm = TRUE
  new_skills <- setNames(rep(default_skill, length(missing_teams)), missing_teams)
  skill_parameters <- c(skill_parameters, new_skills)
}

# Normalize the initial skill parameters
skill_parameters <- skill_parameters[all_teams_in_games] #Ensure same order as team vector.
total_skill <- sum(skill_parameters, na.rm = TRUE) #use na.rm = TRUE to not produce NA value
skill_parameters <- skill_parameters / total_skill

# Function to calculate the probability of team_home winning
predict_winning_probability <- function(team_home, team_away, skill_parameters) {
  skill_home <- skill_parameters[team_home]
  skill_away <- skill_parameters[team_away]
  
  if (is.na(skill_home) || is.na(skill_away)) {
    return(NA)  # Handle cases where skill is missing with NA or a default value
  }
  
  probability_home_wins <- skill_home / (skill_home + skill_away)
  return(probability_home_wins)
}


# Apply the prediction function to each game and add it as a new column
game_data$predicted_prob_home_win <- mapply(predict_winning_probability,
                                            as.character(game_data$team_home), #Ensure team names are characters
                                            as.character(game_data$team_away), #Ensure team names are characters
                                            MoreArgs = list(skill_parameters = skill_parameters))

# Print the game data with predicted winning probabilities
print(game_data)

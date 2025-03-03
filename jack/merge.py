import pandas as pd

# Assuming the first dataset is in a file named 'teams.csv'
# and the second dataset is in a file named 'ratings.csv'

# Load the datasets
teams_df = pd.read_csv('../data/updateRegionGroups.csv')
ratings_df = pd.read_csv('../data/ratings.csv')

# Rename columns for clarity
teams_df.columns = ['Team', 'Region', 'Conference']
ratings_df.columns = ['Team', 'agg_rating_1', 'agg_rating_2']

# Merge the datasets on the 'Team' column
merged_df = pd.merge(teams_df, ratings_df, on='Team')

# Save the merged dataset to a new CSV file
merged_df.to_csv('merged_teams.csv', index=False)

print("Data successfully merged and saved to merged_teams.csv")
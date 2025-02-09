import pandas as pd

# Load the CSV file into a DataFrame
dataDictionary = pd.read_csv('data/dataDictionary.csv')
games = pd.read_csv('data/games_2022.csv')
regionGroups = pd.read_csv('data/regionGroups.csv')

# so we can associate each variable to what it is
dictData = {}
for count, item in enumerate(dataDictionary['variable']):
    dictData[item] = dataDictionary['description'][count]

# so we know what team is in each region
regionData = {}
for count, item in enumerate(regionGroups['team']):
    regionData[item] = regionGroups['region'][count]

# CONDITION BASED FILTERING
# filtered_df = df[df['col_2'] > 15]

print(dictData)
print("--------")
print(regionData)
print("--------")

print(games[games['game_date'] == '2021-12-30'])

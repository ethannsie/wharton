import pandas as pd

# Load the CSV file into a DataFrame
dataDictionary = pd.read_csv('data/dataDictionary.csv')
games = pd.read_csv('data/games_2022.csv')
teams = pd.read_csv('data/regionGroups.csv')
teamList = []

# # so we can associate each variable to what it is
# dictData = {}
# for count, item in enumerate(dataDictionary['variable']):
#     dictData[item] = dataDictionary['description'][count]


# so we know what team is in each region
regionData = {}
for count, item in enumerate(teams['team']):
    regionData[item] = teams['region'][count]
    teamList.append(item)

# CONDITION BASED FILTERING
# filtered_df = df[df['col_2'] > 15]

# print(dictData)
# print("--------")
# print(regionData)
# print("--------")
#
# print(games[games['game_date'] == '2021-12-30'])
# print("--------")

# possessions
# Possession = 0.96 * [FGA_2 + FGA_3 + TOV + TOV_team + 0.44*(FTA) - OREB]
# Offensive and defensive ratings (# points scored/allowed per 100 possessions)
posessionList = []
for index, row in games.iterrows():
    posessionList.append(0.96 * (row['FGA_2'] + row['FGA_3'] + row['TOV'] + row['TOV_team'] + 0.44 *(row['FTA']) - row['OREB']))

games['posessions'] = posessionList

# offensive rating total points scored / total posessions * 100
offense = []
print(teamList)
for team in teamList:
    teamIsolate = games[games['team'] == team]
    totalPoses = 0
    for posess in teamIsolate['posessions']:
        totalPoses += posess
    totalScore = 0
    for score in teamIsolate['team_score']:
        totalScore += score
    offense.append(totalScore/totalPoses * 100)
teams['offensive rating'] = offense

print(teams.nsmallest(100, 'offensive rating'))

# win and loss
wins = []
loss = []
winRatio = []
for team in teamList:
    teamIsolate = games[games['team'] == team]
    totalWins = 0
    totalLoss = 0
    for index, row in teamIsolate.iterrows():
        if row['team_score'] > row['opponent_team_score']:
            totalWins += 1
        else:
            totalLoss += 1
    wins.append(totalWins)
    loss.append(totalLoss)
    winRatio.append(totalWins/(totalWins + totalLoss))
teams['wins'] = wins
teams['loss'] = loss
teams['winRatio'] = winRatio

print(teams.nsmallest(10, 'winRatio'))
# # print(games[games['possessions'] < 10])
# print(games.nsmallest(100, 'possessions'))
# print("--------")
# print(games.nlargest(100, 'possessions'))

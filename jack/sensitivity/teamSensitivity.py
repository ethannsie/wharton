import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import datasets
import pandas as pd
import numpy as np
import math
from collections import defaultdict
from datetime import datetime


dataDictionary = pd.read_csv('../../data/dataDictionary.csv')
games = pd.read_csv('../../data/games_2022.csv', parse_dates=['game_date'])

start_date = '2021-11-01'
end_date = '2022-03-31'

games = games[(games['game_date'] >= start_date) & (games['game_date'] <= end_date)]

teams = pd.read_csv('../../data/updateRegionGroups.csv')

totalTeamList = games['team'].unique()
teamData = {'team': totalTeamList}
allTeams = pd.DataFrame(teamData)

duncanData = pd.read_csv('../../data/duncan.csv')

efffectiveFieldGoal = []
posessionList = []
threeFieldGoal = []
for index, row in games.iterrows():
    posessionList.append(0.96 * (row['FGA_2'] + row['FGA_3'] + row['TOV'] + row['TOV_team'] + 0.44 *(row['FTA']) - row['OREB']))
    FG = row['FGM_2'] + row['FGM_3']
    PtM = row['FGM_3']
    FGA = row['FGA_2'] + row['FGA_3']
    try:
        efffectiveFieldGoal.append((FG + 0.5 * PtM)/FGA)
    except:
        efffectiveFieldGoal.append(0)
    threeFieldGoal.append(row['FGM_3']/row['FGA_3'])
games['posessions'] = posessionList
games['effectiveFieldGoals'] = efffectiveFieldGoal
games['threeFieldGoal'] = threeFieldGoal

# offensive rating total points scored / total posessions * 100
offense = []
scoreTotal = []
effectiveList = []
threeFieldGoals = []

# win and loss
wins = []
loss = []
listPose = []
winRatio = []

# averages for each of these FGA_2,FGM_2,FGA_3,FGM_3,FTA,FTM,AST,BLK,STL,TOV,TOV_team,DREB,OREB
FGA_2 = []
FGM_2 = []
FGA_3 = []
FGM_3 = []
FTA = []
FTM = []
AST = []
BLK = []
STL = []
TOV = []
DREB = []
OREB = []

for team in teams['team'].tolist():
    teamIsolate = games[games['team'] == team]

    totalPoses = 0
    totalWins = 0
    totalLoss = 0
    totalPosessions = 0
    totalGames = 0
    totalScore = 0
    gameCount = 0
    effectiveTotal = 0
    goalTotal = 0

    totalFGA_2 = 0
    totalFGM_2 = 0
    totalFGA_3 = 0
    totalFGM_3 = 0
    totalFTA = 0
    totalFTM = 0
    totalAST = 0
    totalBLK = 0
    totalSTL = 0
    totalTOV = 0
    totalDREB = 0
    totalOREB = 0

    if teamIsolate.empty:
        offense.append(0)
        scoreTotal.append(0)
        effectiveList.append(0)
        threeFieldGoals.append(0)
        wins.append(0)
        loss.append(0)
        winRatio.append(0)
        listPose.append(0)
        continue

    for posess in teamIsolate['posessions']:
        totalPoses += posess

    for score in teamIsolate['team_score']:
        gameCount += 1
        totalScore += score

    for effective in teamIsolate['effectiveFieldGoals']:
        effectiveTotal += effective

    for goal in teamIsolate['threeFieldGoal']:
        goalTotal += goal

    for index, row in teamIsolate.iterrows():
        if row['team_score'] > row['opponent_team_score']:
            totalWins += 1
        else:
            totalLoss += 1
        totalGames += 1
        totalPosessions += row['posessions']
    wins.append(totalWins)
    loss.append(totalLoss)
    try:
        listPose.append(totalPosessions/totalGames)
    except:
        listPose.append(0)
    try:
        winRatio.append(totalWins/(totalWins + totalLoss))
    except:
        winRatio.append(0)

    offense.append(totalScore/totalPoses * 100)
    scoreTotal.append(totalScore/gameCount)
    effectiveList.append(effectiveTotal/gameCount)
    threeFieldGoals.append(goalTotal/gameCount)

teams['offensive rating'] = offense
teams['totalScore'] = scoreTotal
teams['effectiveTotal'] = effectiveList
teams['threeFieldGoal'] = threeFieldGoals
teams['wins'] = wins
teams['loss'] = loss
teams['winRatio'] = winRatio
teams['posessions'] = listPose


# offensive rating total points scored / total posessions * 100
offense = []
scoreTotal = []
effectiveList = []
threeFieldGoals = []

# win and loss
wins = []
loss = []
listPose = []
winRatio = []

FGA_2 = []
FGM_2 = []
FGA_3 = []
FGM_3 = []
FTA = []
FTM = []
AST = []
BLK = []
STL = []
TOV = []
DREB = []
OREB = []

# print(teamList)
for team in allTeams['team'].tolist():
    teamIsolate = games[games['team'] == team]
    totalPoses = 0
    totalWins = 0
    totalLoss = 0
    totalPosessions = 0
    totalGames = 0
    totalFGA_2 = 0
    totalFGM_2 = 0
    totalFGA_3 = 0
    totalFGM_3 = 0
    totalFTA = 0
    totalFTM = 0
    totalAST = 0
    totalBLK = 0
    totalSTL = 0
    totalTOV = 0
    totalDREB = 0
    totalOREB = 0

    if teamIsolate.empty:
        offense.append(0)
        scoreTotal.append(0)
        effectiveList.append(0)
        threeFieldGoals.append(0)
        wins.append(0)
        loss.append(0)
        winRatio.append(0)
        listPose.append(0)
        FGA_2.append(0)
        FGM_2.append(0)
        FGA_3.append(0)
        FGM_3.append(0)
        FTA.append(0)
        FTM.append(0)
        AST.append(0)
        BLK.append(0)
        STL.append(0)
        TOV.append(0)
        DREB.append(0)
        OREB.append(0)
        continue

    for item in teamIsolate['FGA_2']:
        totalFGA_2 += item
    for item in teamIsolate['FGM_2']:
        totalFGM_2 += item
    for item in teamIsolate['FGA_2']:
        totalFGA_3 += item
    for item in teamIsolate['FGM_3']:
        totalFGM_3 += item
    for item in teamIsolate['FTA']:
        totalFTA += item
    for item in teamIsolate['FTM']:
        totalFTM += item
    for item in teamIsolate['AST']:
        totalAST += item
    for item in teamIsolate['BLK']:
        totalBLK += item
    for item in teamIsolate['STL']:
        totalSTL += item
    for item in teamIsolate['TOV']:
        totalTOV += item
    for item in teamIsolate['TOV_team']:
        totalTOV += item
    for item in teamIsolate['DREB']:
        totalDREB += item
    for item in teamIsolate['OREB']:
        totalOREB += item

    for posess in teamIsolate['posessions']:
        totalPoses += posess
    totalScore = 0
    gameCount = 0
    for score in teamIsolate['team_score']:
        gameCount += 1
        totalScore += score
    effectiveTotal = 0
    for effective in teamIsolate['effectiveFieldGoals']:
        effectiveTotal += effective
    goalTotal = 0
    for goal in teamIsolate['threeFieldGoal']:
        goalTotal += goal

    for index, row in teamIsolate.iterrows():
        if row['team_score'] > row['opponent_team_score']:
            totalWins += 1
        else:
            totalLoss += 1
        totalGames += 1
        totalPosessions += row['posessions']
    wins.append(totalWins)
    loss.append(totalLoss)
    try:
        listPose.append(totalPosessions/totalGames)
    except:
        listPose.append(0)
    try:
        winRatio.append(totalWins/(totalWins + totalLoss))
    except:
        winRatio.append(0)

    offense.append(totalScore/totalPoses * 100)
    scoreTotal.append(totalScore/gameCount)
    effectiveList.append(effectiveTotal/gameCount)
    threeFieldGoals.append(goalTotal/gameCount)
    FGA_2.append(totalFGA_2/gameCount)
    FGM_2.append(totalFGM_2/gameCount)
    FGA_3.append(totalFGA_3/gameCount)
    FGM_3.append(totalFGM_3/gameCount)
    FTA.append(totalFTA/gameCount)
    FTM.append(totalFTM/gameCount)
    AST.append(totalAST/gameCount)
    BLK.append(totalBLK/gameCount)
    STL.append(totalSTL/gameCount)
    TOV.append(totalTOV/gameCount)
    DREB.append(totalDREB/gameCount)
    OREB.append(totalOREB/gameCount)

allTeams['offensive rating'] = offense
allTeams['totalScore'] = scoreTotal
allTeams['effectiveTotal'] = effectiveList
allTeams['threeFieldGoal'] = threeFieldGoals
allTeams['wins'] = wins
allTeams['loss'] = loss
allTeams['winRatio'] = winRatio
allTeams['posessions'] = listPose
allTeams['FGA_2'] = FGA_2
allTeams['FGM_2'] = FGM_2
allTeams['FGA_3'] = FGA_3
allTeams['FGM_3'] = FGM_3
allTeams['FTA'] = FTA
allTeams['FTM'] = FTM
allTeams['AST'] = AST
allTeams['BLK'] = BLK
allTeams['STL'] = STL
allTeams['TOV'] = TOV
allTeams['DREB'] = DREB
allTeams['OREB'] = OREB


# print(games[games['team'] == 'georgia_lady_bulldogs'])
winners = []
losers = []
game_ids = []
dates = []
for index, row in games.iterrows():
    if index + 1 < 10438:
        # filters teams
        if row['team'] in teams['team'].tolist() and games.loc[index+1][2] in teams['team'].tolist():
            if games.loc[index+1][0] == row['game_id']:
                if row['team_score'] > row['opponent_team_score']:
                    winners.append(row['team'])
                    losers.append(games.loc[index+1][2])
                else:
                    winners.append(games.loc[index+1][2])
                    losers.append(row['team'])
                game_ids.append(row['game_id'])
                dates.append(row['game_date'])

colleyData = {
    'game_id': game_ids,
    'date': dates,
    'winner': winners,
    'loser': losers
            }
colleyData = pd.DataFrame(colleyData)

colleyData = colleyData.sort_values(by='date')
split_index = int(len(colleyData) * 0.8)
split_date = colleyData.iloc[split_index]['date']

train_data = colleyData[colleyData['date'] <= split_date]
test_data = colleyData[colleyData['date'] > split_date]

# print(colleyData)
# print(len(totalTeamList))

total_games = defaultdict(int)
pairwise_results = defaultdict(lambda: {'wins': 0, 'losses': 0})

for _, row in train_data.iterrows():
    winner = row['winner']
    loser = row['loser']

    start_date_obj = datetime.strptime("2021-11-09 00:00:00", "%Y-%m-%d %H:%M:%S")
    end_date_obj = datetime.strptime(str(row['date']), "%Y-%m-%d %H:%M:%S")
    days_difference = (end_date_obj - start_date_obj).days

    weighting = math.floor(days_difference/7 + 1)
    total_games[winner] += weighting
    total_games[loser] += weighting

    pairwise_results[(winner, loser)]['wins'] += weighting
    pairwise_results[(loser, winner)]['losses'] += weighting

# print("Total Games:", total_games)
# print("Pairwise Results:", pairwise_results)
# print(len(pairwise_results))

matrixList = []
for team1 in teams['team'].tolist():
    row = []
    for team2 in teams['team'].tolist():
        if team1 == team2:
            # Diagonal element: total games + 2
            row.append(total_games[team1] + 2)
        else:
            # Off Diagonal elements = -1 * num of games between team i and team j
            row.append(-1 * (pairwise_results[(team1, team2)]['wins'] + pairwise_results[(team1, team2)]['losses']))
    matrixList.append(row)

bVector = []

for team1 in teams['team'].tolist():
    wins = sum(pairwise_results[(team1, team2)]['wins'] for team2 in teams['team'].tolist())
    losses = sum(pairwise_results[(team1, team2)]['losses'] for team2 in teams['team'].tolist())

    bVector.append(1 + 0.5 * (wins - losses))

bVector = np.array(bVector).reshape(-1, 1)
colleyMatrix = np.matrix(matrixList)
# print(colleyMatrix)


inverseColley = np.linalg.inv(colleyMatrix)

rankings = inverseColley @ bVector
raw_values = [float(item[0, 0]) for item in rankings]

min_value = np.min(raw_values)
max_value = np.max(raw_values)
epsilon = 0.01

if max_value - min_value == 0:
    normalized_values = [1 for _ in raw_values]
else:
    normalized_values = [
        epsilon + (1 - epsilon) * (x - min_value) / (max_value - min_value)
        for x in raw_values
    ]

rankList = []
for index, norm_value in enumerate(normalized_values):
    rankList.append([teams['team'].tolist()[index], float(norm_value)])

sortedRankList = sorted(rankList, key=lambda x: x[1], reverse=True)
for item in sortedRankList:
    print(item)

def returnTeamRank():
    return sortedRankList

def returnTeamData():
    return test_data

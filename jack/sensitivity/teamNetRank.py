import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import datasets
import pandas as pd
import numpy as np

# Load the CSV file into a DataFrame
dataDictionary = pd.read_csv('../../data/dataDictionary.csv')
games = pd.read_csv('../../data/games_2022.csv', parse_dates=['game_date'])

start_date = '2021-11-01'
end_date = '2022-03-31'

games = games[(games['game_date'] >= start_date) & (games['game_date'] <= end_date)]

teams = pd.read_csv('../../data/updateRegionGroups.csv')
# teamList = []
totalTeamList = games['team'].unique()
teamData = {'team': totalTeamList}
allTeams = pd.DataFrame(teamData)

duncanData = pd.read_csv('../../data/duncan.csv')

# # so we can associate each variable to what it is
# dictData = {}
# for count, item in enumerate(dataDictionary['variable']):
#     dictData[item] = dataDictionary['description'][count]

# so we know what team is in each region
# regionData = {}
# for count, item in enumerate(teams['team']):
#     regionData[item] = teams['region'][count]
#     teamList.append(item)

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
# FG —> (FGM_2 + FGM_3)
# 3PtM —> FGM_3
# FGA —> FGA_2 + FGA_3
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
defense = []
scoreTotal = []
effectiveList = []
threeFieldGoals = []
netRanking = []

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

# print(teamList)
for team in teams['team'].tolist():
    teamIsolate = games[games['team'] == team]
    gameCount = 0
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
    totalScore = 0
    oppScore = 0
    effectiveTotal = 0
    goalTotal = 0
    totalAST = 0
    totalBLK = 0
    totalSTL = 0
    totalTOV = 0
    totalDREB = 0
    totalOREB = 0

    if teamIsolate.empty:
        offense.append(0)
        defense.append(0)
        netRanking.append(0)
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

    for score in teamIsolate['team_score']:
        gameCount += 1
        totalScore += score

    for score in teamIsolate['opponent_team_score']:
        oppScore += score

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
    defense.append(oppScore/totalPosessions * 100)
    offense.append(totalScore/totalPoses * 100)
    netRanking.append(totalScore/totalPoses * 100 - oppScore/totalPosessions * 100)
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

teams['net ranking'] = netRanking
teams['defensive rating'] = defense
teams['offensive rating'] = offense
teams['totalScore'] = scoreTotal
teams['effectiveTotal'] = effectiveList
teams['threeFieldGoal'] = threeFieldGoals
teams['wins'] = wins
teams['loss'] = loss
teams['winRatio'] = winRatio
teams['posessions'] = listPose
teams['FGA_2'] = FGA_2
teams['FGM_2'] = FGM_2
teams['FGA_3'] = FGA_3
teams['FGM_3'] = FGM_3
teams['FTA'] = FTA
teams['FTM'] = FTM
teams['AST'] = AST
teams['BLK'] = BLK
teams['STL'] = STL
teams['TOV'] = TOV
teams['DREB'] = DREB
teams['OREB'] = OREB

# offensive rating total points scored / total posessions * 100
offense = []
defense = []
scoreTotal = []
effectiveList = []
threeFieldGoals = []
netRanking = []

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

# print(teamList)
for team in allTeams['team'].tolist():
    teamIsolate = games[games['team'] == team]
    gameCount = 0
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
    totalScore = 0
    oppScore = 0
    effectiveTotal = 0
    goalTotal = 0
    totalAST = 0
    totalBLK = 0
    totalSTL = 0
    totalTOV = 0
    totalDREB = 0
    totalOREB = 0

    if teamIsolate.empty:
        offense.append(0)
        defense.append(0)
        netRanking.append(0)
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
    for score in teamIsolate['opponent_team_score']:
        oppScore += score
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
    defense.append(oppScore/totalPosessions * 100)
    offense.append(totalScore/totalPoses * 100)
    scoreTotal.append(totalScore/gameCount)
    effectiveList.append(effectiveTotal/gameCount)
    netRanking.append(totalScore/totalPoses * 100 - oppScore/totalPosessions * 100)
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
allTeams['defensive rating'] = defense
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
allTeams['net ranking'] = netRanking
# standardized_ratios = [(x - min(winRatio)) / (max(winRatio) - min(winRatio)) for x in winRatio]


# teams['standardWinRatio'] = standardized_ratios

# print(teams.nsmallest(10, 'winRatio'))
#
# someTeams = [
#     "alabama_crimson_tide",
#     "alabama_state_lady_hornets",
#     "arkansas_razorbacks",
#     "belmont_bruins",
#     "charleston_cougars",
#     "charlotte_49ers",
#     "davidson_wildcats",
#     "elon_phoenix",
#     "florida_gators",
#     "florida_gulf_coast_eagles",
#     "florida_state_seminoles",
#     "freed_hardeman_lions",
#     "furman_paladins",
#     "gardner_webb_runnin_bulldogs",
#     "georgia_lady_bulldogs",
#     "georgia_southern_eagles",
#     "georgia_tech_yellow_jackets",
#     "high_point_panthers",
#     "houston_christian_huskies",
#     "houston_cougars",
#     "jackson_state_lady_tigers",
#     "jacksonville_dolphins",
#     "jacksonville_state_gamecocks",
#     "little_rock_trojans",
#     "louisiana_ragin_cajuns",
#     "louisiana_tech_lady_techsters",
#     "lsu_tigers",
#     "memphis_tigers",
#     "mercer_bears",
#     "miami_hurricanes",
#     "middle_tennessee_blue_raiders",
#     "ole_miss_rebels",
#     "oral_roberts_golden_eagles",
#     "rice_owls",
#     "se_louisiana_lady_lions",
#     "south_carolina_gamecocks",
#     "south_carolina_upstate_spartans",
#     "south_florida_bulls",
#     "southern_miss_lady_eagles",
#     "stephen_f_austin_ladyjacks",
#     "stetson_hatters",
#     "tennessee_lady_volunteers",
#     "tennessee_tech_golden_eagles",
#     "troy_trojans",
#     "tulane_green_wave",
#     "tulsa_golden_hurricane",
#     "ucf_knights",
#     "wofford_terriers",
#     "akron_zips",
#     "app_state_mountaineers",
#     "austin_peay_governors",
#     "ball_state_cardinals",
#     "cleveland_state_vikings",
#     "coker_cobras",
#     "dayton_flyers",
#     "depaul_blue_demons",
#     "drake_bulldogs",
#     "eastern_illinois_panthers",
#     "green_bay_phoenix",
#     "illinois_state_redbirds",
#     "indiana_hoosiers",
#     "iowa_hawkeyes",
#     "iowa_state_cyclones",
#     "iu_indianapolis_jaguars",
#     "kansas_city_roos",
#     "kansas_jayhawks",
#     "kent_state_golden_flashes",
#     "kentucky_wildcats",
#     "louisville_cardinals",
#     "loyola_chicago_ramblers",
#     "marquette_golden_eagles",
#     "marshall_thundering_herd"
# ]

# winRatios = []
# for team, winRatio in zip(teams['team'], teams['winRatio']):
#     try:
#         if team in someTeams:  # Check if the current team is in 'someTeams'
#             winRatios.append(winRatio)  # Append the corresponding win ratio
#     except:
#         winRatios.append(winRatio)
#
# posessions = []
# for team, posession in zip(teams['team'], teams['posessions']):
#     try:
#         if team in someTeams:
#             posessions.append(posession)
#     except:
#         posessions.append(posession)
#
# offensiveRate = []
# for team, offense in zip(teams['team'], teams['offensive rating']):
#     try:
#         if team in someTeams:
#             offensiveRate.append(offense)
#     except:
#         offensiveRate.append(offense)
#
# score = []
# for team, total in zip(teams['team'], teams['totalScore']):
#     try:
#         if team in someTeams:
#             score.append(total)
#     except:
#         score.append(total)
#
# effec = []
# for team, effective in zip(teams['team'], teams['effectiveTotal']):
#     try:
#         if team in someTeams:
#             effec.append(effective)
#     except:
#         effec.append(effective)
#
# three = []
# for team, threeField in zip(teams['team'], teams['threeFieldGoal']):
#     try:
#         if team in someTeams:
#             three.append(threeField)
#     except:
#         three.append(threeField)

# standardized = []
# for team, standards in zip(teams['team'], teams['standardWinRatio']):
#     if team in someTeams:
#         standardized.append(standards)

# data = {
#     "winRatio": winRatios,
#     # "stdWinRatio": standardized,
#     "effective": effec,
#     "possessions": posessions,
#     "offensive rating": offensiveRate,
#     "three field goals": three,
#     "total score": score
# }

data = {
    "offensive rating": duncanData['avg_offensive_rating'].tolist(),
    "defensive rating": duncanData['avg_defensive_rating'].tolist(),
    "win percentage": duncanData['win_percentage'].tolist()
}
print(teams)

data = {
    "winRatio": teams['winRatio'].tolist(),
    # "stdWinRatio": standardized,
    "effective": teams['effectiveTotal'].tolist(),
    "possessions": teams['posessions'].tolist(),
    "offensive rating": teams['offensive rating'].tolist(),
    "three field goals": teams['threeFieldGoal'].tolist(),
    "total score": teams['totalScore'].tolist()
}

data = {
    "winRatio": teams['winRatio'].tolist(),
    # "stdWinRatio": standardized,
    "effec": teams['effectiveTotal'].tolist(),
    "posess": teams['posessions'].tolist(),
    "offense": teams['offensive rating'].tolist(),
    "3Goal": teams['threeFieldGoal'].tolist(),
    "score": teams['totalScore'].tolist(),
    "FGA_2": teams['FGA_2'].tolist(),
    "FGM_2": teams['FGM_2'].tolist(),
    "FGA_3": teams['FGA_3'].tolist(),
    "FGM_3": teams['FGM_3'].tolist(),
    "FTA": teams['FTA'].tolist(),
    "FTM": teams['FTM'].tolist(),
    "AST": teams['AST'].tolist(),
    "BLK": teams['BLK'].tolist(),
    "STL": teams['STL'].tolist(),
    "TOV": teams['TOV'].tolist(),
    "DREB": teams['DREB'].tolist(),
    "OREB": teams['OREB'].tolist(),
    "defensive": teams['defensive rating'].tolist(),
    "net off/def": teams['net ranking'].tolist()

}

data = {
    "winRatio": allTeams['winRatio'].tolist(),
    # "stdWinRatio": standardized,
    "effec": allTeams['effectiveTotal'].tolist(),
    "posess": allTeams['posessions'].tolist(),
    "offense": allTeams['offensive rating'].tolist(),
    "3Goal": allTeams['threeFieldGoal'].tolist(),
    "score": allTeams['totalScore'].tolist(),
    "FGA_2": allTeams['FGA_2'].tolist(),
    "FGM_2": allTeams['FGM_2'].tolist(),
    "FGA_3": allTeams['FGA_3'].tolist(),
    "FGM_3": allTeams['FGM_3'].tolist(),
    "FTA": allTeams['FTA'].tolist(),
    "FTM": allTeams['FTM'].tolist(),
    "AST": allTeams['AST'].tolist(),
    "BLK": allTeams['BLK'].tolist(),
    "STL": allTeams['STL'].tolist(),
    "TOV": allTeams['TOV'].tolist(),
    "DREB": allTeams['DREB'].tolist(),
    "OREB": allTeams['OREB'].tolist(),
    "defensive": allTeams['defensive rating'].tolist(),
    "net off/def": allTeams['net ranking'].tolist()

}

print(teams['team'].unique().tolist())
teamList = []
raw_values = []

for team in teams['team'].unique().tolist():
    teamList.append(team)
    raw_values.append(teams[teams['team'] == team]['offensive rating'] - teams[teams['team'] == team]['defensive rating'])
    print(teams[teams['team'] == team]['offensive rating'])
    print(teams[teams['team'] == team]['defensive rating'])


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

def returnNetRating():
    return sortedRankList

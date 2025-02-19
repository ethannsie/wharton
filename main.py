import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import datasets
import pandas as pd
import numpy as np

# Load the CSV file into a DataFrame
dataDictionary = pd.read_csv('data/dataDictionary.csv')
games = pd.read_csv('data/games_2022.csv', parse_dates=['game_date'])

start_date = '2022-01-10'
end_date = '2022-01-31'

games = games[(games['game_date'] >= start_date) & (games['game_date'] <= end_date)]

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
scoreTotal = []
effectiveList = []
threeFieldGoals = []
# print(teamList)
for team in teamList:
    teamIsolate = games[games['team'] == team]
    totalPoses = 0
    if teamIsolate.empty:
        offense.append(0)
        scoreTotal.append(0)
        effectiveList.append(0)
        threeFieldGoals.append(0)
        continue
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
    offense.append(totalScore/totalPoses * 100)
    scoreTotal.append(totalScore/gameCount)
    effectiveList.append(effectiveTotal/gameCount)
    threeFieldGoals.append(goalTotal/gameCount)
teams['offensive rating'] = offense
teams['totalScore'] = scoreTotal
teams['effectiveTotal'] = effectiveList
teams['threeFieldGoal'] = threeFieldGoals
print(teams['totalScore'])
# print(teams.nsmallest(100, 'offensive rating'))


# win and loss
wins = []
loss = []
listPose = []
winRatio = []
for team in teamList:
    teamIsolate = games[games['team'] == team]
    totalWins = 0
    totalLoss = 0
    totalPosessions = 0
    totalGames = 0
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

teams['wins'] = wins
teams['loss'] = loss
teams['winRatio'] = winRatio
teams['posessions'] = listPose
print(winRatio)
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

winRatios = []
for team, winRatio in zip(teams['team'], teams['winRatio']):
    try:
        if team in someTeams:  # Check if the current team is in 'someTeams'
            winRatios.append(winRatio)  # Append the corresponding win ratio
    except:
        winRatios.append(winRatio)

posessions = []
for team, posession in zip(teams['team'], teams['posessions']):
    try:
        if team in someTeams:
            posessions.append(posession)
    except:
        posessions.append(posession)

offensiveRate = []
for team, offense in zip(teams['team'], teams['offensive rating']):
    try:
        if team in someTeams:
            offensiveRate.append(offense)
    except:
        offensiveRate.append(offense)

score = []
for team, total in zip(teams['team'], teams['totalScore']):
    try:
        if team in someTeams:
            score.append(total)
    except:
        score.append(total)

effec = []
for team, effective in zip(teams['team'], teams['effectiveTotal']):
    try:
        if team in someTeams:
            effec.append(effective)
    except:
        effec.append(effective)

three = []
for team, threeField in zip(teams['team'], teams['threeFieldGoal']):
    try:
        if team in someTeams:
            three.append(threeField)
    except:
        three.append(threeField)

# standardized = []
# for team, standards in zip(teams['team'], teams['standardWinRatio']):
#     if team in someTeams:
#         standardized.append(standards)

data = {
    "winRatio": winRatios,
    # "stdWinRatio": standardized,
    "effective": effec,
    "possessions": posessions,
    "offensive rating": offensiveRate,
    "three field goals": three,
    "total score": score
}

teams = pd.DataFrame(data)

# Compute the correlation matrix
correlation_matrix = teams.corr()

# Display the correlation matrix
print("Correlation Matrix:")
print(correlation_matrix)

# Plot the correlation matrix as a heatmap
plt.figure(figsize=(6, 4))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Matrix: Win Ratio vs Possessions")
plt.show()

# # print(games[games['possessions'] < 10])
# print(games.nsmallest(100, 'possessions'))
# print("--------")
# print(games.nlargest(100, 'possessions'))

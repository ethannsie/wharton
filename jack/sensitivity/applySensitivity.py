import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import datasets
import pandas as pd
import numpy as np
import math
from collections import defaultdict
from datetime import datetime
import divisionSensitivity
import teamSensitivity
import teamNetRank

teams = pd.read_csv('../../data/updateRegionGroups.csv')

teamRankings = teamSensitivity.returnTeamRank()
divisionRankings = divisionSensitivity.returnDivisionRank()
netRating = teamNetRank.returnNetRating()

rankLOL = {}

teamConference = {}
usefulTeams = teams['team'].tolist()
associatedConference = teams['Conference'].tolist()

for count, team in enumerate(usefulTeams):
    teamConference[team] = associatedConference[count]

for r in netRating:
    rankLOL[r[0]] = r[1]
print(rankLOL)

print("-----PRE CONFERENCE RANKINGS------")
for rank in teamRankings:
    print(rank)

newRanking = []

for ranking in teamRankings:
    conference = teamConference[ranking[0]]
    ranking[1] = float(ranking[1] * divisionRankings[conference])
    newRanking.append(ranking[1])

def min_max_normalize(data):
    min_val = min(data)
    max_val = max(data)
    return [(x - min_val) / (max_val - min_val) for x in data]

normalized_ranking = min_max_normalize(newRanking)

for count, ranking in enumerate(teamRankings):
    ranking[1] = normalized_ranking[count]
    ranking[1] *= rankLOL.get(ranking[0])

print("-----------------------------------")
print("-----POST CONFERENCE and net rating RANKINGS------")
teamRanking = {}
sort = sorted(teamRankings, key=lambda x: x[1], reverse=True)
for rank in sort:
    teamRanking[rank[0]] = rank[1]



test_data = teamSensitivity.returnTeamData()
# print(test_data)
#
print(teamRanking)

accurateGames = 0
closeGames = 0
total = 0
for _, row in test_data.iterrows():
    if float(teamRanking[row['winner']]) * divisionRankings[teamConference[row['winner']]] > float(teamRanking[row['loser']]) * divisionRankings[teamConference[row['loser']]]:
        accurateGames += 1
    #use a STD or smth
    elif abs(float(teamRanking[row['winner']]) * divisionRankings[teamConference[row['winner']]] - float(teamRanking[row['loser']]) * divisionRankings[teamConference[row['loser']]]) < 0.01:
        # take something into consideration in this case
        closeGames += 1
    # print(f"winner: {row['winner']} | loser: {row['loser']}")
    # print(f"winner: {teamRanking[row['winner']]} | loser: {teamRanking[row['loser']]}")
    total += 1

print(f"Accurate Games: {accurateGames}")
print(f"Close Games: {closeGames}")
print(f"Total Games: {total}")
print(accurateGames/total)
print((accurateGames + closeGames)/total)

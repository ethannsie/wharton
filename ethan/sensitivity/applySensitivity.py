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

teams = pd.read_csv('../../data/updateRegionGroups.csv')

teamRankings = teamSensitivity.returnTeamRank()
divisionRankings = divisionSensitivity.returnDivisionRank()

teamConference = {}
usefulTeams = teams['team'].tolist()
associatedConference = teams['Conference'].tolist()
for count, team in enumerate(usefulTeams):
    teamConference[team] = associatedConference[count]

print("-----PRE CONFERENCE RANKINGS------")
for rank in teamRankings:
    print(rank)
for ranking in teamRankings:
    conference = teamConference[ranking[0]]
    ranking[1] = float(ranking[1] * divisionRankings[conference])

print("-----------------------------------")
print("-----POST CONFERENCE RANKINGS------")
teamRanking = {}
sort = sorted(teamRankings, key=lambda x: x[1], reverse=True)
for rank in sort:
    teamRanking[rank[0]] = rank[1]

test_data = teamSensitivity.returnTeamData()
# print(test_data)
#
# print(teamRanking)

accurateGames = 0
closeGames = 0
total = 0
for _, row in test_data.iterrows():
    if teamRanking[row['winner']] > teamRanking[row['loser']]:
        accurateGames += 1
    #use a STD or smth
    elif abs(teamRanking[row['winner']] - teamRanking[row['loser']]) < 0.01:
        # take something into consideration in this case
        closeGames += 1
    print(f"winner: {row['winner']} | loser: {row['loser']}")
    print(f"winner: {teamRanking[row['winner']]} | loser: {teamRanking[row['loser']]}")
    total += 1

print(f"Accurate Games: {accurateGames}")
print(f"Close Games: {closeGames}")
print(f"Total Games: {total}")
print(accurateGames/total)
print((accurateGames + closeGames)/total)

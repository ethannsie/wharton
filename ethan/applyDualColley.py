import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import datasets
import pandas as pd
import numpy as np
import math
from collections import defaultdict
from datetime import datetime
import colleyDivisions
import colleyTeams

dataDictionary = pd.read_csv('../data/dataDictionary.csv')
games = pd.read_csv('../data/games_2022.csv', parse_dates=['game_date'])

start_date = '2021-11-01'
end_date = '2022-03-31'

games = games[(games['game_date'] >= start_date) & (games['game_date'] <= end_date)]

teams = pd.read_csv('../data/updateRegionGroups.csv')

totalTeamList = games['team'].unique()
teamData = {'team': totalTeamList}
allTeams = pd.DataFrame(teamData)

duncanData = pd.read_csv('../data/duncan.csv')

teamRankings = colleyTeams.returnTeamRank()
divisionRankings = colleyDivisions.returnDivisionRank()

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
sort = sorted(teamRankings, key=lambda x: x[1], reverse=True)
for rank in sort:
    print(rank)

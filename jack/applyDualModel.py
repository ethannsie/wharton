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

teams = pd.read_csv('../data/updateRegionGroups.csv')
teamr = pd.read_csv('three_rankings.csv')
#print(teamr)

teamRankings1 = teamr[['team', 'agg_rating_1']].values.tolist()
teamRankings2 = teamr[['team', 'agg_rating_2']].values.tolist()
teamRankingsColley = teamr[['team', 'colley_rating']].values.tolist()

divisionRankings = colleyDivisions.returnDivisionRank()

teamConference = {}
usefulTeams = teams['team'].tolist()
associatedConference = teams['Conference'].tolist()
for count, team in enumerate(usefulTeams):
    teamConference[team] = associatedConference[count]

print("-----PRE CONFERENCE RANKINGS------")
for rank in teamRankings2:
    print(rank)
for ranking in teamRankings2:
    conference = teamConference[ranking[0]]
    ranking[1] = float(ranking[1] * divisionRankings[conference])

print("-----------------------------------")
print("-----POST CONFERENCE RANKINGS------")
sort = sorted(teamRankings2, key=lambda x: x[1], reverse=True)
for rank in sort:
    print(rank)

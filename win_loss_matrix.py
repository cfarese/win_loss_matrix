import json
import polars as pl

# I've never worked with polars before but I've heard that it's faster than pandas
# so I'm going to try and work it out here

with open('example.json', 'r') as f:
    data = json.load(f)

teams = list(data.keys()) # array #1

matchups = [] # array #2
for team in teams:
    team_matchups = []
    for opponent, record in data[team].items():
        team_matchups.append([opponent, record['W']])
    matchups.append(team_matchups)


rows = []
for team in teams:
    row = [team]
    for other_team in teams:
        if team == other_team:
            row.append("-")
        else:
            wins = data[team].get(other_team, {'W': 0})
            row.append(str(wins['W']))
    rows.append(row)

df = pl.DataFrame(rows, schema=['Team'] + teams, orient="row") # orient = "row" gets rid of some warning

pl.Config.set_tbl_cols(-1) # It wasn't showing all of the columns before this
pl.Config.set_tbl_rows(-1)

print(df)
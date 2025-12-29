# Win Loss Matrix

Win Loss Matrix for Sports Reference internship

The code itself is relatively simple, it took me about 15 minutes to make. It would've taken me less, but I decided to try using Polars for the first time instead of Pandas. I had to figure out some flags to give it so that it would stop sending me warnings and show all of the rows/columns, but it works great now.

I used the same JSON that was provided. The first thing I did in my code was just to import the JSON.

```python
with open('example.json', 'r') as f:
    data = json.load(f)
```

I decided that the easiest way to do this was going to be to create two arrays. The first array, ```teams```, would just have a list of all the teams: ```['BRO', 'BSN', 'CHC', 'CIN', 'NYG', 'PHI', 'PIT', 'STL']```. This would make it easier to iterate and go team by team, row by row building a dataframe. The second array, ```matchups```, was a 3D array. It would hold every team's win amount against other teams:

```python
[
    [
        ['BSN', 10], ['CHC', 15], ['CIN', 15], ['NYG', 14], 
        ['PHI', 14], ['PIT', 15], ['STL', 11]
    ],
    [
        ['BRO', 12], ['CHC', 13], ['CIN', 13], ['NYG', 13], 
        ['PHI', 14], ['PIT', 12], ['STL', 9]
    ],
    # ... and so on
]
```

I used a simple for loop to create this:

```python
matchups = [] # array #2
for team in teams:
    team_matchups = []
    for opponent, record in data[team].items():
        team_matchups.append([opponent, record['W']])
    matchups.append(team_matchups)
```

The next step is just putting the two steps together in a dataframe. I'm familiar with Pandas but this project gave me a good chance to learn some Polar. Luckily, both use pretty similar syntax and pretty similar ways of building a dataframe. I created a larger 2D array that would hold all of the individual rows. Then, for every team, I created a row. I looped through all the other teams and found their win amount and recorded it. I just put in a dash for their own team.

For example: for the Cubs, I would check how many wins they have against the Dodgers. Mark it down, then onto the Braves (Only team of the 8 where I didn't recognized the acronym!). Mark it down, and continnue on. If it's ever the Cubs, put a "-". Continue onto the next row.

```python
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
```

All that's left is putting all the rows into one dataframe and a few flags to make sure that the code would show all the columns and now throw useless warnings.

```python
df = pl.DataFrame(rows, schema=['Team'] + teams, orient="row") # orient = "row" gets rid of some warning

pl.Config.set_tbl_cols(-1) # It wasn't showing all of the columns before this
pl.Config.set_tbl_rows(-1)

print(df)
```

The result looks quite nice!

```
┌──────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
│ Team ┆ BRO ┆ BSN ┆ CHC ┆ CIN ┆ NYG ┆ PHI ┆ PIT ┆ STL │
│ ---  ┆ --- ┆ --- ┆ --- ┆ --- ┆ --- ┆ --- ┆ --- ┆ --- │
│ str  ┆ str ┆ str ┆ str ┆ str ┆ str ┆ str ┆ str ┆ str │
╞══════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╪═════╡
│ BRO  ┆ -   ┆ 10  ┆ 15  ┆ 15  ┆ 14  ┆ 14  ┆ 15  ┆ 11  │
│ BSN  ┆ 12  ┆ -   ┆ 13  ┆ 13  ┆ 13  ┆ 14  ┆ 12  ┆ 9   │
│ CHC  ┆ 7   ┆ 9   ┆ -   ┆ 12  ┆ 7   ┆ 16  ┆ 8   ┆ 10  │
│ CIN  ┆ 7   ┆ 9   ┆ 10  ┆ -   ┆ 13  ┆ 13  ┆ 13  ┆ 8   │
│ NYG  ┆ 8   ┆ 9   ┆ 15  ┆ 9   ┆ -   ┆ 12  ┆ 15  ┆ 13  │
│ PHI  ┆ 8   ┆ 8   ┆ 6   ┆ 9   ┆ 10  ┆ -   ┆ 13  ┆ 8   │
│ PIT  ┆ 7   ┆ 10  ┆ 14  ┆ 9   ┆ 7   ┆ 9   ┆ -   ┆ 6   │
│ STL  ┆ 11  ┆ 13  ┆ 12  ┆ 14  ┆ 9   ┆ 14  ┆ 16  ┆ -   │
└──────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘
```

Please hire me. I like sports. A lot. Baseball, Football, Soccer, Tennis, Motorsport, Basketball, you name it, I probably spend too much time reading useless rumors and arguing with people on the internet using stats from Sports Reference. I do the Immaculate Footy every day (I got all 9 of them once in 9 tries). I promise if you hire me I will never use FanGraphs again. I'll even use bWAR for modern-day catchers.













import numpy as np
import pandas as pd
# Use nba_api package to get data from the NBA.com API
# Get a list of all players and their matching Player IDs
from nba_api.stats.static import players
all_players = players.get_players()
active_players = []
player_ids = []
def name_grab(x):
    for name in list(x):
        if name['is_active'] == True:
            active_players.append(name['full_name'])
            player_ids.append(name['id'])
        else:
            pass
name_grab(all_players)

# Get a list of all teams and their matching abbreviations
from nba_api.stats.static import teams
nba_teams = teams.get_teams()
active_teams = []
team_abbreviations = []
def team_grab(x):
    for team in list(x):
        active_teams.append(team['full_name'])
        team_abbreviations.append(team['abbreviation'])
team_grab(nba_teams)

# Create updated team dictionary of names and abbreviations
active_teams.append('Seattle SuperSonics')
active_teams.append('Charlotte Bobcats')
active_teams.append('New Orleans/Oklahoma City Hornets')
active_teams.append('New Orleans Hornets')
active_teams.append('New Jersey Nets')
active_teams.append('Washington Bullets')
team_abbreviations.append('SEA')
team_abbreviations.append('CHA')
team_abbreviations.append('NOK')
team_abbreviations.append('NOH')
team_abbreviations.append('NJN')
team_abbreviations.append('WAS')
team_dictionary = dict(zip(active_teams,team_abbreviations))

# Import all regular season and playoff shotcharts from 2018-19 season into dataframes
from nba_api.stats.endpoints import shotchartdetail
# V1: pointdiffs 1-5 and match to shotchart data
# V2: run game_id and game_event_id to find assisted or not, who assisted and scoring margin in playbyplayv2
rs_shots_1819 = shotchartdetail.ShotChartDetail(0,0,season_nullable='2018-19',context_measure_simple='FGA')
rs_shotchart_1819 = rs_shots_1819.get_data_frames()[0]
playoff_shots_1819 = shotchartdetail.ShotChartDetail(0,0,season_nullable='2018-19',season_type_all_star='Playoffs',context_measure_simple='FGA')
playoff_shotchart_1819 = playoff_shots_1819.get_data_frames()[0]
regular = pd.concat([rs_shotchart_1819,playoff_shotchart_1819],sort=True)

# All shots attempted where point difference is 5 or less
rs_shots_1819_5 = shotchartdetail.ShotChartDetail(0,0,season_nullable='2018-19',context_measure_simple='FGA',point_diff_nullable=5)
rs_shotchart_1819_5 = rs_shots_1819_5.get_data_frames()[0]
playoff_shots_1819_5 = shotchartdetail.ShotChartDetail(0,0,season_nullable='2018-19',season_type_all_star='Playoffs',context_measure_simple='FGA',point_diff_nullable=5)
playoff_shotchart_1819_5 = playoff_shots_1819_5.get_data_frames()[0]
pointdiff_5 = pd.concat([rs_shotchart_1819_5,playoff_shotchart_1819_5],sort=True)

# All shots attempted where point difference is 3 or less
rs_shots_1819_3 = shotchartdetail.ShotChartDetail(0,0,season_nullable='2018-19',context_measure_simple='FGA',point_diff_nullable=3)
rs_shotchart_1819_3 = rs_shots_1819_3.get_data_frames()[0]
playoff_shots_1819_3 = shotchartdetail.ShotChartDetail(0,0,season_nullable='2018-19',season_type_all_star='Playoffs',context_measure_simple='FGA',point_diff_nullable=3)
playoff_shotchart_1819_3 = playoff_shots_1819_3.get_data_frames()[0]
pointdiff_3 = pd.concat([rs_shotchart_1819_3,playoff_shotchart_1819_3],sort=True)

# All shots attempted where point difference is 1 or 0
rs_shots_1819_1 = shotchartdetail.ShotChartDetail(0,0,season_nullable='2018-19',context_measure_simple='FGA',point_diff_nullable=1)
rs_shotchart_1819_1 = rs_shots_1819_1.get_data_frames()[0]
playoff_shots_1819_1 = shotchartdetail.ShotChartDetail(0,0,season_nullable='2018-19',season_type_all_star='Playoffs',context_measure_simple='FGA',point_diff_nullable=1)
playoff_shotchart_1819_1 = playoff_shots_1819_1.get_data_frames()[0]
pointdiff_1 = pd.concat([rs_shotchart_1819_1,playoff_shotchart_1819_1],sort=True)

# Concatenate full shotchart and "less than five" shotchart and find non-matching values.
# The values which aren't common between the shotcharts are those "greater than five"
get_diff = pd.concat([regular,pointdiff_5],sort=True)
get_diff = get_diff.reset_index(drop=True)
get_diff_grby = get_diff.groupby(list(get_diff.columns.str.strip()))
idx = [x[0] for x in get_diff_grby.groups.values() if len(x) == 1]
greater_than_five = get_diff.reindex(idx)

# Repeat above process for comparing the other filtered shotcharts
get_diff45 = pd.concat([pointdiff_5,pointdiff_3],sort=True)
get_diff45 = get_diff45.reset_index(drop=True)
get_diff_grby45 = get_diff45.groupby(list(get_diff45.columns.str.strip()))
idx = [x[0] for x in get_diff_grby45.groups.values() if len(x) == 1]
four_to_five = get_diff45.reindex(idx)

get_diff23 = pd.concat([pointdiff_3,pointdiff_1],sort=True)
get_diff23 = get_diff23.reset_index(drop=True)
get_diff_grby23 = get_diff23.groupby(list(get_diff23.columns.str.strip()))
idx = [x[0] for x in get_diff_grby23.groups.values() if len(x) == 1]
two_to_three = get_diff23.reindex(idx)

# Create a new column 'POINTS_DIFFERENCE' to label each shotchart before concatenating them
greater_than_five['POINTS_DIFFERENCE'] = 'More than 5 Points'
four_to_five['POINTS_DIFFERENCE'] = '4 - 5 Points'
two_to_three['POINTS_DIFFERENCE'] = '2 - 3 Points'
semi_shotchart = pd.concat([greater_than_five,four_to_five,two_to_three],sort=True)

regular['POINTS_DIFFERENCE'] = '0 - 1 Points'
get_diff01 = pd.concat([semi_shotchart,regular],sort=True)
get_diff01 = get_diff01.reset_index(drop=True)
get_diff_grby01 = get_diff01.groupby(list(get_diff01.columns.str.strip()))
idx = [x[0] for x in get_diff_grby01.groups.values() if len(x) == 1]
zero_to_one = get_diff01.reindex(idx)

shotchart = pd.concat([zero_to_one,semi_shotchart],sort=True)

# Set mins, secs remaining and period as string for text display
shotchart['MINUTES_REMAINING'] = shotchart['MINUTES_REMAINING'].astype('str')
shotchart['SECONDS_REMAINING'] = shotchart['SECONDS_REMAINING'].astype('str')
shotchart['PERIOD'] = shotchart['PERIOD'].astype('str')

# Assign whether shots are from regular season or playoffs
def season_type(x):
    if int(x['GAME_DATE']) > 20190410:
        return 'Playoffs'
    else:
        return 'Regular Season'
shotchart['SEASON_TYPE'] = shotchart.apply(lambda x: season_type(x), axis=1)

# Assign team abbreviation for shooting player
def team_checker(x):
    if x['TEAM_NAME'] == 'Charlotte Hornets' and int(x['GAME_DATE']) < 20021029:
        return 'CHH'
    else:
        if x['TEAM_NAME'] in team_dictionary.keys():
            return team_dictionary[x['TEAM_NAME']]
shotchart['TEAM_ABBREVIATION'] = shotchart.apply(lambda x: team_checker(x), axis=1)

# Assign the opponent based on whether the home team or away team matches the player's team abbreviation
def check_opponent(x):
    if x['HTM'] == x['TEAM_ABBREVIATION']:
        return x['VTM']
    else:
        return x['HTM']
shotchart['OPPONENT'] = shotchart.apply(lambda x: check_opponent(x), axis=1)

# Change the format of the game date from YYYYMMDD to MM/DD/YY
from datetime import datetime
shotchart['GAME_DATE'] = shotchart['GAME_DATE'].apply(lambda x: datetime.strptime(str(x), '%Y%m%d').strftime('%m/%d/%Y'))

# Categorize the shots based on how many minutes remain in the game
def minutes_group(x):
    if int(x['MINUTES_REMAINING']) >= 5:
        return '> 5 Minutes'
    elif int(x['MINUTES_REMAINING']) >= 1 and int(x['MINUTES_REMAINING']) <= 4:
        return '1-4 Minutes'
    elif int(x['MINUTES_REMAINING']) < 1 and int(x['SECONDS_REMAINING']) >= 30:
        return '30-59 Seconds'
    elif int(x['MINUTES_REMAINING']) < 1 and int(x['SECONDS_REMAINING']) >= 10 and int(x['SECONDS_REMAINING']) < 30:
        return '10-30 Seconds'
    else:
        return '< 10 Seconds'
shotchart['TIME_GROUP'] = shotchart.apply(lambda x: minutes_group(x), axis=1)

# Drop any remaining duplicates by keeping only the first value that appears from the combined shotcharts
shotchart = shotchart.sort_values(['GAME_ID', 'GAME_EVENT_ID', 'POINTS_DIFFERENCE']).drop_duplicates(['GAME_ID', 'GAME_EVENT_ID'], keep='last')
# Save the final dataframe as a CSV so to decrease intensive API calls
shotchart.to_csv('shotchart.csv')

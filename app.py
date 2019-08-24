import dash
import dash_core_components as dcc
import dash_html_components as html
import io
from io import StringIO
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objs as go
import requests

# Set the Dash App
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Import CSV into pandas
url = 'https://raw.githubusercontent.com/enova47/shotchart/master/shotchart.csv'
s=requests.get(url).content
shotchart=pd.read_csv(io.StringIO(s.decode('utf-8')),dtype={'GAME_ID': str,'GAME_EVENT_ID':str,'PLAYER_ID': str,'TEAM_NAME': str,'TEAM_ID':str,'PERIOD': str,'MINUTES_REMAINING':str,'SECONDS_REMAINING': str,'SHOT_DISTANCE':str})

# Create the court dimensions in plotly from: http://savvastjortjoglou.com/nba-shot-sharts.html
# and from: https://moderndata.plot.ly/nba-shots-analysis-using-plotly-shapes/
court_shapes = []
# Outer lines of the court
outer_lines_shape = dict(
    type='rect',
    xref='x',
    yref='y',
    # Bottom left edge of outer lines rectangle (x0,y0)
    x0='-250',
    y0='-47.5',
    # Bottom right edge of outer lines rectangle (x1,y1)
    x1='250',
    y1='422.5',
    line=dict(
        color='rgba(10, 10, 10, 1)',
        width=1
    )
)

court_shapes.append(outer_lines_shape)

# Basketball hoop - use Circle shape with the center of the hoop at 0,0. Radius of 7.5.
hoop_shape = dict(
    type='circle',
    # All coordinate (x and y) references are in relation to the plot axis
    xref='x',
    yref='y',
    x0='7.5',
    y0='7.5',
    x1='-7.5',
    y1='-7.5',
    # Set the color and style of circle
    line=dict(
        color='rgba(10,10,10,1)',
        width=1
    )
)

court_shapes.append(hoop_shape)

# Backboard
backboard_shape = dict(
    type='rect',
    xref='x',
    yref='y',
    x0='-30',
    y0='-7.5',
    x1='30',
    y1='-6.5',
    line=dict(
        color='rgba(10, 10, 10, 1)',
        width=1
    ),
    fillcolor='rgba(10, 10, 10, 1)'
)

court_shapes.append(backboard_shape)

# The paint (outer and inner boxes as rectangles)
outer_three_sec_shape = dict(
    type='rect',
    xref='x',
    yref='y',
    x0='-80',
    y0='-47.5',
    x1='80',
    y1='143.5',
    line=dict(
        color='rgba(10, 10, 10, 1)',
        width=1
    )
)

court_shapes.append(outer_three_sec_shape)

inner_three_sec_shape = dict(
    type='rect',
    xref='x',
    yref='y',
    x0='-60',
    y0='-47.5',
    x1='60',
    y1='143.5',
    line=dict(
        color='rgba(10, 10, 10, 1)',
        width=1
    )
)

court_shapes.append(inner_three_sec_shape)

# Three point line areas
left_line_shape = dict(
    type='line',
    xref='x',
    yref='y',
    x0='-220',
    y0='-47.5',
    x1='-220',
    y1='92.5',
    line=dict(
        color='rgba(10, 10, 10, 1)',
        width=1
    )
)

court_shapes.append(left_line_shape)

right_line_shape = dict(
    type='line',
    xref='x',
    yref='y',
    x0='220',
    y0='-47.5',
    x1='220',
    y1='92.5',
    line=dict(
        color='rgba(10, 10, 10, 1)',
        width=1
    )
)

court_shapes.append(right_line_shape)

# Using the path type to draw the arc using a Curve (C) command
three_point_arc_shape = dict(
    type='path',
    xref='x',
    yref='y',
    path='M -220 92.5 C -70 300, 70 300, 220 92.5',
    line=dict(
        color='rgba(10, 10, 10, 1)',
        width=1
    )
)

court_shapes.append(three_point_arc_shape)

# Center circle (area surrounding halfcourt - logo lines)
center_circle_shape = dict(
    type='circle',
    xref='x',
    yref='y',
    x0='60',
    y0='482.5',
    x1='-60',
    y1='362.5',
    line=dict(
        color='rgba(10, 10, 10, 1)',
        width=1
    )
)

court_shapes.append(center_circle_shape)

# Restraining circle (halfcourt small circle)
res_circle_shape = dict(
    type='circle',
    xref='x',
    yref='y',
    x0='20',
    y0='442.5',
    x1='-20',
    y1='402.5',
    line=dict(
        color='rgba(10, 10, 10, 1)',
        width=1
    )
)

court_shapes.append(res_circle_shape)

# Free throw circle
free_throw_circle_shape = dict(
    type='circle',
    xref='x',
    yref='y',
    x0='60',
    y0='200',
    x1='-60',
    y1='80',
    line=dict(
        color='rgba(10, 10, 10, 1)',
        width=1
    )
)

court_shapes.append(free_throw_circle_shape)

# Restricted area, using dash property to style the circle
res_area_shape = dict(
    type='circle',
    xref='x',
    yref='y',
    x0='40',
    y0='40',
    x1='-40',
    y1='-40',
    line=dict(
        color='rgba(10, 10, 10, 1)',
        width=1,
        dash='dot'
    )
)

court_shapes.append(res_area_shape)

# Initialize shotchart
name = 'Kawhi Leonard'
player = shotchart[shotchart.PLAYER_NAME == name]
missed_shot_trace = go.Scattergl(
    # Missed shots are 0, Made shots are 1
    x=player[player.SHOT_MADE_FLAG == 0]['LOC_X'],
    y=player[player.SHOT_MADE_FLAG == 0]['LOC_Y'],
    mode='markers',
    name='Miss',
    marker={'color': 'blue', 'size': 5},
    text=[str(htm) + str(vtm) + str(at) + str(st) + str(sz) + str(pr) + str(mr) + str(sr) + str(gd) for
            htm, vtm, at, st, sz, pr, mr, sr, gd in zip(player[player.SHOT_MADE_FLAG == 0]['HTM'] + ' vs ',
                                                          player[player.SHOT_MADE_FLAG == 0]['VTM'] + '<br>',
                                                          player[player.SHOT_MADE_FLAG == 0]['ACTION_TYPE'] + '<br>',
                                                          player[player.SHOT_MADE_FLAG == 0]['SHOT_TYPE'] + ', ',
                                                          player[player.SHOT_MADE_FLAG == 0]['SHOT_ZONE_RANGE'] + '<br>',
                                                          'Q' + player[player.SHOT_MADE_FLAG == 0]['PERIOD'] + ', ',
                                                          player[player.SHOT_MADE_FLAG == 0]['MINUTES_REMAINING'] + ':',
                                                          player[player.SHOT_MADE_FLAG == 0]['SECONDS_REMAINING'] + ' remaining' + '<br>',
                                                          player[player.SHOT_MADE_FLAG == 0]['GAME_DATE'])],
    hoverinfo='text',
)
made_shot_trace = go.Scattergl(
    x=player[player.SHOT_MADE_FLAG == 1]['LOC_X'],
    y=player[player.SHOT_MADE_FLAG == 1]['LOC_Y'],
    mode='markers',
    name='Make',
    marker={'color': 'red', 'size': 5},
    text=[str(htm) + str(vtm) + str(at) + str(st) + str(sz) + str(pr) + str(mr) + str(sr) + str(gd) for
          htm, vtm, at, st, sz, pr, mr, sr, gd in zip(player[player.SHOT_MADE_FLAG == 1]['HTM'] + ' vs ',
                                                          player[player.SHOT_MADE_FLAG == 1]['VTM'] + '<br>',
                                                          player[player.SHOT_MADE_FLAG == 1]['ACTION_TYPE'] + '<br>',
                                                          player[player.SHOT_MADE_FLAG == 1]['SHOT_TYPE'] + ', ',
                                                          player[player.SHOT_MADE_FLAG == 1]['SHOT_ZONE_RANGE'] + '<br>',
                                                          'Q' + player[player.SHOT_MADE_FLAG == 1]['PERIOD'] + ', ',
                                                          player[player.SHOT_MADE_FLAG == 1]['MINUTES_REMAINING'] + ':',
                                                          player[player.SHOT_MADE_FLAG == 1]['SECONDS_REMAINING'] + ' remaining' + '<br>',
                                                          player[player.SHOT_MADE_FLAG == 1]['GAME_DATE'])],
    hoverinfo='text',
)

# Set the dropdown menus for shotchart
app.layout = html.Div([
    html.Div([
        html.Label('Player'),
        dcc.Dropdown(
            id='PLAYER_NAME',
            options=[{'label': i, 'value': i} for i in shotchart['PLAYER_NAME'].unique()],
            value = 'Kawhi Leonard',
        )
    ],
    style={'width': '49%', 'display': 'inline-block'}),
    html.Div([
        html.Label('Season Type'),
        dcc.Dropdown(
            id='SEASON_TYPE',
            options=[{'label': i, 'value': i} for i in shotchart['SEASON_TYPE'].unique()],
            value = 'Regular Season',
        )
    ],
    style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
    html.Div([
        html.Label('Shot Type'),
        dcc.Dropdown(
            id='ACTION_TYPE',
            options=[{'label': i, 'value': i} for i in shotchart['ACTION_TYPE'].unique()],
        )
    ],
    style={'width': '49%', 'display': 'inline-block'}),
    html.Div([
        html.Label('Shot Distance'),
        dcc.Dropdown(
            id='SHOT_ZONE_RANGE',
            options=[{'label': i, 'value': i} for i in shotchart['SHOT_ZONE_RANGE'].unique()],
        )
    ],
    style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
    html.Div([
        html.Label('Shot Zone'),
        dcc.Dropdown(
            id='SHOT_ZONE_AREA',
            options=[{'label': i, 'value': i} for i in shotchart['SHOT_ZONE_AREA'].unique()],
        )
    ],
    style={'width': '49%', 'display': 'inline-block'}),
    html.Div([
        html.Label('Game Date'),
        dcc.Dropdown(
            id='GAME_DATE',
            options=[{'label': i, 'value': i} for i in shotchart['GAME_DATE'].unique()],
        )
    ],
    style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
    html.Div([
        html.Label('Quarter'),
        dcc.Dropdown(
            id='PERIOD',
            options=[{'label': i, 'value': i} for i in shotchart['PERIOD'].unique()],
        )
    ],
    style={'width': '49%', 'display': 'inline-block'}),
    html.Div([
        html.Label('Opponent'),
        dcc.Dropdown(
            id='OPPONENT',
            options=[{'label': i, 'value': i} for i in shotchart['OPPONENT'].unique()],
        )
    ],
    style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
    html.Div([
        html.Label('Time Remaining'),
        dcc.Dropdown(
            id='TIME_GROUP',
            options=[{'label': i, 'value': i} for i in shotchart['TIME_GROUP'].unique()],
        )
    ],
    style={'width': '49%', 'display': 'inline-block'}),
    html.Div([
        html.Label('Score Margin'),
        dcc.Dropdown(
            id='POINTS_DIFFERENCE',
            options=[{'label': i, 'value': i} for i in shotchart['POINTS_DIFFERENCE'].unique()],
        )
    ],
    style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
    html.Div([
        html.Label("Player's Team"),
        dcc.Dropdown(
            id='TEAM_NAME',
            options=[{'label': i, 'value': i} for i in shotchart['TEAM_NAME'].unique()],
            value = 'Toronto Raptors',
        )
    ],
    style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(
        id='shot_chart',
        figure={
            'data': [missed_shot_trace,made_shot_trace],
            'layout': go.Layout(
                title = name + ' - All Shots, 2018-19 ' + 'Regular Season',
                showlegend = True,
                xaxis = {'showgrid':False, 'range':[-300,300]},
                yaxis = {'showgrid':False, 'range':[500,-100]},
                height = 600,
                width= 650,
                shapes = court_shapes
            )
        }
        )
    ])
])

# Need to add:
# V2: Filter by season (set season for shotchartdetail, check if can import from CSV)
# V2: Filter by assisted or not (merge play by play v2 into shotchart to get assisted data)
# V2: Return game score in hovertext (Play by Play)
# V2: Player picture (see Sam Liebman's documentation)
# V2: Graph or table showing shooting percentages, etc.
# V2: Video link (get from NBA.com - 2016 season+) - Example: https://stats.nba.com/events/?flag=1&GameID=0021800001&GameEventID=7&Season=2018-19&title=MISS%20Covington%2027%27%203PT%20Jump%20Shot&sct=plot
# V2: Reset button - See David Comfort Dash
# V2: Print to PDF button - See David Comfort Dash
@app.callback(
    dash.dependencies.Output('shot_chart', 'figure'),
    [dash.dependencies.Input('PLAYER_NAME','value'),
     dash.dependencies.Input('SEASON_TYPE','value'),
     dash.dependencies.Input('ACTION_TYPE','value'),
     dash.dependencies.Input('SHOT_ZONE_RANGE','value'),
     dash.dependencies.Input('SHOT_ZONE_AREA','value'),
     dash.dependencies.Input('GAME_DATE','value'),
     dash.dependencies.Input('PERIOD','value'),
     dash.dependencies.Input('OPPONENT','value'),
     dash.dependencies.Input('TIME_GROUP','value'),
     dash.dependencies.Input('POINTS_DIFFERENCE','value'),
     dash.dependencies.Input('TEAM_NAME','value')])
def update_graph(player_name, season_type, action_type, shot_zone_range, shot_zone_area, game_date, period, opponent, time_group, points_difference, team_name):
    # Function if update value exists, then update player dataframe. If not, ignore it.
    player = shotchart
    if player_name in list(player.PLAYER_NAME):
        player = player[player.PLAYER_NAME == player_name]
    # Season Type
    if season_type in list(player.SEASON_TYPE):
        player = player[player.SEASON_TYPE == season_type]
    # Shot Type
    if action_type in list(player.ACTION_TYPE):
        player = player[player.ACTION_TYPE == action_type]
    # Shot Distance
    if shot_zone_range in list(player.SHOT_ZONE_RANGE):
        player = player[player.SHOT_ZONE_RANGE == shot_zone_range]
    # Shot Zone
    if shot_zone_area in list(player.SHOT_ZONE_AREA):
        player = player[player.SHOT_ZONE_AREA == shot_zone_area]
    # Game Date
    if game_date in list(player.GAME_DATE):
        player = player[player.GAME_DATE == game_date]
    # Quarter
    if period in list(player.PERIOD):
        player = player[player.PERIOD == period]
    # Opponent
    if opponent in list(player.OPPONENT):
        player = player[player.OPPONENT == opponent]
    # Time Remaining
    if time_group in list(player.TIME_GROUP):
        player = player[player.TIME_GROUP == time_group]
    # Scoring Margin
    if points_difference in list(player.POINTS_DIFFERENCE):
        player = player[player.POINTS_DIFFERENCE == points_difference]
    # Player's Team
    if team_name in list(player.TEAM_NAME):
        player = player[player.TEAM_NAME == team_name]
    missed_shot_trace = go.Scattergl(
        # Missed shots are 0, Made shots are 1
        x=player[player.SHOT_MADE_FLAG == 0]['LOC_X'],
        y=player[player.SHOT_MADE_FLAG == 0]['LOC_Y'],
        mode='markers',
        name='Miss',
        marker={'color': 'blue', 'size': 5},
        text=[str(htm) + str(vtm) + str(at) + str(st) + str(sz) + str(pr) + str(mr) + str(sr) + str(gd) for
              htm, vtm, at, st, sz, pr, mr, sr, gd in zip(player[player.SHOT_MADE_FLAG == 0]['HTM'] + ' vs ',
                                                          player[player.SHOT_MADE_FLAG == 0]['VTM'] + '<br>',
                                                          player[player.SHOT_MADE_FLAG == 0]['ACTION_TYPE'] + '<br>',
                                                          player[player.SHOT_MADE_FLAG == 0]['SHOT_TYPE'] + ', ',
                                                          player[player.SHOT_MADE_FLAG == 0]['SHOT_ZONE_RANGE'] + '<br>',
                                                          'Q' + player[player.SHOT_MADE_FLAG == 0]['PERIOD'] + ', ',
                                                          player[player.SHOT_MADE_FLAG == 0]['MINUTES_REMAINING'] + ':',
                                                          player[player.SHOT_MADE_FLAG == 0]['SECONDS_REMAINING'] + ' remaining' + '<br>',
                                                          player[player.SHOT_MADE_FLAG == 0]['GAME_DATE'])],
        hoverinfo='text',
    )
    made_shot_trace = go.Scattergl(
        x=player[player.SHOT_MADE_FLAG == 1]['LOC_X'],
        y=player[player.SHOT_MADE_FLAG == 1]['LOC_Y'],
        mode='markers',
        name='Make',
        marker={'color': 'red', 'size': 5},
        text=[str(htm) + str(vtm) + str(at) + str(st) + str(sz) + str(pr) + str(mr) + str(sr) + str(gd) for
              htm, vtm, at, st, sz, pr, mr, sr, gd in zip(player[player.SHOT_MADE_FLAG == 1]['HTM'] + ' vs ',
                                                          player[player.SHOT_MADE_FLAG == 1]['VTM'] + '<br>',
                                                          player[player.SHOT_MADE_FLAG == 1]['ACTION_TYPE'] + '<br>',
                                                          player[player.SHOT_MADE_FLAG == 1]['SHOT_TYPE'] + ', ',
                                                          player[player.SHOT_MADE_FLAG == 1]['SHOT_ZONE_RANGE'] + '<br>',
                                                          'Q' + player[player.SHOT_MADE_FLAG == 1]['PERIOD'] + ', ',
                                                          player[player.SHOT_MADE_FLAG == 1]['MINUTES_REMAINING'] + ':',
                                                          player[player.SHOT_MADE_FLAG == 1]['SECONDS_REMAINING'] + ' remaining' + '<br>',
                                                          player[player.SHOT_MADE_FLAG == 1]['GAME_DATE'])],
        hoverinfo='text',
    )

    return{
            'data': [missed_shot_trace,made_shot_trace],
            'layout': go.Layout(
                title = player_name + ' - All Shots, 2018-19 ' + season_type,
                showlegend = True,
                xaxis = {'showgrid':False, 'range':[-300,300]},
                yaxis = {'showgrid':False, 'range':[500,-100]},
                height = 600,
                width= 650,
                shapes = court_shapes
            )
    }

if __name__ == '__main__':
    app.run_server(debug=True)
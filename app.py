'''
Script to create a Dash web app for our soccer analytics dash
'''

import pandas as pd
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from soccer_data_api import SoccerDataAPI
from dash.dependencies import Input, Output

# Dash setup
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Getting serie A data
# soccer_data = SoccerDataAPI()
# serie_a = soccer_data.serie_a()
# ligue_1 = soccer_data.ligue_1()
# premier_league = soccer_data.english_premier()
# bundesliga = soccer_data.bundesliga()
# la_liga = soccer_data.la_liga()
# Converting to a df


# Laying out the application
app.layout = html.Div(children=[

    # League Selection DropDown
    html.Div([
        # Maybe do this as buttons instead of dropdown
        dcc.Dropdown(id='league-dropdown',
                     options=[
                    {'label': 'Premier League', 'value': 'Premier League'},
                    {'label': 'La Liga', 'value': 'La Liga'},
                    {'label': 'Bundesliga', 'value': 'Bundesliga'},
                    {'label': 'Serie A', 'value': 'Serie A'},
                    {'label': 'Ligue 1', 'value': 'Ligue 1'}],
                    value='SA'
                    )
            ]),

    html.Div([
        # Title
        # html.H1(children='Serie A stats'),

        dcc.Graph(id='points-goal-diff-graph')
    ]),
    # Goal bar graphs
    html.Div([
        html.Div([
        dcc.Graph(id='offense-graph')
        ], className = 'four columns'),

        # Defense
        html.Div([
        dcc.Graph(id='defense-graph')
        ], className = 'four columns'),
        
        # Goal differential bar chart
        html.Div([
        dcc.Graph(id='goal-diff-graph')
        ], className = 'four columns')
    
    ], className='row')
    
])


# Change graphs based on league selection
@app.callback(
    [Output('points-goal-diff-graph', 'figure'),
    Output('offense-graph', 'figure'),
    Output('defense-graph','figure'),
    Output('goal-diff-graph', 'figure')],
    Input('league-dropdown', 'value')
    )
def update_league(league):
    # Getting data
    # soccer_data = SoccerDataAPI()
    print(f'League Selected by user {league}')
    soccer_data = SoccerDataAPI()
    data = pd.DataFrame()
    # Checking for each type of league dfata call
    if league == "Premier League":
        data = soccer_data.english_premier()
        # df = pd.DataFrame(data)

    elif league == "La Liga":
        data = soccer_data.la_liga()
        # df = pd.DataFrame(data)

    elif league == "Serie A":
        data = soccer_data.serie_a()
        # df = pd.DataFrame(data)

    elif league == "Ligue 1":
        data = soccer_data.ligue_1()
        # df = pd.DataFrame(data)

    elif league == "Bundesliga":
        data = soccer_data.bundesliga()
        # df = pd.DataFrame(data)
    
    # Setting up and converting df
    df = pd.DataFrame(data)

    cols2int = ['pos','wins', 'losses',  'draws', 'losses',
       'goals_for', 'goals_against', 'goal_diff',]
    for col in cols2int:
        df[col] = df[col].astype(int)
        print(df[col])

    # Seeting up scatter
    f = px.scatter(df, x="goal_diff", y="points", 
                 text='team', title=league,
                 hover_data=['team', 'top_scorer'])
    f.update_traces(textposition='middle right')
    f.update_yaxes(autorange="reversed")

    # Attack bar graph
    a_bar = px.bar(df, x='team', y='goals_for', title=f'{league} Attack',
                   labels={'team':'','goals_for':'Goals For'})

    # Defense Bar graph
    d_bar = px.bar(df, x='team', y='goals_against', title=f'{league} Defense',
                   labels={'team':'','goals_against':'Goals Against'})

    # Goal differential bar graph
    diff_bar = px.bar(df, x='team', y='goal_diff', title=f'{league} Goal Differential',
                      labels={'team':'','goal_diff':'Goal Differential'})

    # Goal Diff Bar Graph
    return f, a_bar, d_bar, diff_bar


# run the app
if __name__ == '__main__':
    app.run_server(debug=True)








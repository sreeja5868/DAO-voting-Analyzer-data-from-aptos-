
import dash
from dash import dcc, html, dash_table, Input, Output, State
import pandas as pd
import plotly.express as px
import base64
import io
import os
import requests

# Fetch Aptos data and convert to DataFrame (Mock structure used as example)
def fetch_aptos_data():
    url = "https://fullnode.mainnet.aptoslabs.com/v1/accounts/0x1/resources"
    headers = {"Accept": "application/json"}
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        # Mock transformation (you'll replace this based on your actual DAO logic)
        df = pd.DataFrame([
            {"year": 2023, "category": "Governance", "gender": "Male", "votes": 1200, "proposals": 4, "participation_rate": 68.5, "dao_name": "Aptos DAO", "male_votes": 800, "female_votes": 400},
            {"year": 2024, "category": "Finance", "gender": "Female", "votes": 900, "proposals": 3, "participation_rate": 72.3, "dao_name": "Econ DAO", "male_votes": 300, "female_votes": 600},
        ])
        return df
    except Exception as e:
        print(f"Error fetching Aptos data: {e}")
        return pd.DataFrame()

# Initialize Dash app
app = dash.Dash(_name_)
app.title = "DAO Voting Pattern Analyzer"
df = pd.DataFrame()

# App layout
app.layout = html.Div([
    html.H1("DAO Voting Pattern Analyzer", style={'textAlign': 'center', 'padding': '10px'}),

    html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Button('Upload CSV', style={'marginRight': '10px'}),
            multiple=False
        ),
        html.Button('Fetch Aptos Data', id='fetch-data-btn', n_clicks=0)
    ], style={'textAlign': 'center', 'padding': '20px'}),

    html.Div([
        html.Div([
            html.Label("Filter by Year"),
            dcc.Dropdown(id='year-filter', multi=True),
        ], style={'width': '30%', 'display': 'inline-block'}),

        html.Div([
            html.Label("Filter by Category"),
            dcc.Dropdown(id='category-filter', multi=True),
        ], style={'width': '30%', 'display': 'inline-block'}),

        html.Div([
            html.Label("Filter by Gender"),
            dcc.Dropdown(id='gender-filter', value="All", clearable=False),
        ], style={'width': '30%', 'display': 'inline-block'}),
    ], style={'padding': '20px'}),

    html.Div(id='kpi-cards', style={'display': 'flex', 'justifyContent': 'space-around', 'flexWrap': 'wrap', 'padding': '20px'}),

    html.Div([
        html.Div([dcc.Graph(id='donut-participation')], style={'width': '33%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='bar-votes')], style={'width': '33%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='line-trend')], style={'width': '33%', 'display': 'inline-block'}),
    ], style={'padding': '20px'}),

    html.Div([dcc.Graph(id='key-metrics-trend')], style={'padding': '20px'}),

    html.Div([
        html.H3("Detailed DAO Proposal Data"),
        dash_table.DataTable(
            id='proposal-table',
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'center', 'padding': '5px'},
            style_header={'fontWeight': 'bold', 'backgroundColor': '#f2f2f2'},
            page_size=10
        )
    ], style={'padding': '20px'})
])

# CSV Upload Parser
def parse_contents(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        return pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return pd.DataFrame()

# Dropdowns update
@app.callback(
    [Output('year-filter', 'options'),
     Output('category-filter', 'options'),
     Output('gender-filter', 'options')],
    [Input('upload-data', 'contents'),
     Input('fetch-data-btn', 'n_clicks')],
    [State('upload-data', 'filename')]
)
def update_filter_options(uploaded_content, fetch_clicks, filename):
    global df
    ctx = dash.callback_context

    if not ctx.triggered:
        return [], [], []

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'upload-data' and uploaded_content:
        df = parse_contents(uploaded_content)
    elif trigger_id == 'fetch-data-btn' and fetch_clicks > 0:
        df = fetch_aptos_data()

    if df.empty:
        return [], [], []

    year_options = [{"label": str(y), "value": y} for y in sorted(df['year'].unique())]
    category_options = [{"label": c, "value": c} for c in sorted(df['category'].unique())]
    gender_options = [{"label": "All", "value": "All"}, {"label": "Male", "value": "Male"}, {"label": "Female", "value": "Female"}]

    return year_options, category_options, gender_options

# Dashboard update
@app.callback(
    [Output('kpi-cards', 'children'),
     Output('donut-participation', 'figure'),
     Output('bar-votes', 'figure'),
     Output('line-trend', 'figure'),
     Output('key-metrics-trend', 'figure'),
     Output('proposal-table', 'data')],
    [Input('year-filter', 'value'),
     Input('category-filter', 'value'),
     Input('gender-filter', 'value')]
)
def update_dashboard(years, categories, gender):
    if df.empty:
        return [html.Div("No data uploaded yet.")]*6

    filtered_df = df.copy()
    if years: filtered_df = filtered_df[filtered_df['year'].isin(years)]
    if categories: filtered_df = filtered_df[filtered_df['category'].isin(categories)]
    if gender and gender != "All":
        if gender == "Male":
            filtered_df = filtered_df[filtered_df['male_votes'] > 0]
        elif gender == "Female":
            filtered_df = filtered_df[filtered_df['female_votes'] > 0]

    total_votes = filtered_df['votes'].sum()
    total_proposals = filtered_df['proposals'].sum()
    avg_participation = round(filtered_df['participation_rate'].mean(), 2) if not filtered_df.empty else 0
    male_ratio = round((filtered_df['male_votes'].sum() / (filtered_df[['male_votes', 'female_votes']].sum().sum())) * 100, 2) if filtered_df[['male_votes', 'female_votes']].sum().sum() > 0 else 0
    female_ratio = 100 - male_ratio

    kpi_cards = [
        html.Div([html.H4("Total Votes"), html.H2(f"{total_votes}")], className="kpi"),
        html.Div([html.H4("Total Proposals"), html.H2(f"{total_proposals}")], className="kpi"),
        html.Div([html.H4("Avg Participation Rate"), html.H2(f"{avg_participation}%")], className="kpi"),
        html.Div([html.H4("Male vs Female"), html.H2(f"{male_ratio}% / {female_ratio}%")], className="kpi"),
    ]

    donut = px.pie(names=["Male", "Female"], values=[filtered_df['male_votes'].sum(), filtered_df['female_votes'].sum()], hole=0.5, title="Participation by Gender")
    bar = px.bar(filtered_df, x='dao_name', y='votes', color='category', barmode='group', title="Votes per DAO")
    line = px.line(filtered_df, x='year', y='votes', color='dao_name', markers=True, title="Voting Trend Over Years")

    trend_df = filtered_df.groupby('year', as_index=False).agg({
        'participation_rate': 'mean',
        'proposals': 'sum'
    })
    trend = px.line(trend_df, x='year', y=['participation_rate', 'proposals'], markers=True, title="Trend by Key Metrics")

    return kpi_cards, donut, bar, line, trend, filtered_df.to_dict('records')

# Run app
if _name_ == "_main_":
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port)
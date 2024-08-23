import dash
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import requests
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import base64
from io import BytesIO

# Initialize the Flask server for CORS
from flask import Flask
from flask_cors import CORS

# Initialize the Flask server and enable CORS
server = Flask(__name__)
CORS(server)

# Initialize the Dash app
app = Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout of the dashboard
app.layout = dbc.Container([
    html.H1("COVID-19 Data Dashboard", className='mb-4', style={'textAlign': 'center'}),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='data-dropdown',
                options=[
                    {'label': 'Deaths and vaccinations', 'value': 'JHU_COVID_19'},
                    {'label': 'Cases by Date', 'value': 'CDC_TESTING'},
                    {'label': 'Deaths and population', 'value': 'DATABANK_DEMOGRAPHICS'},
                    {'label': 'Population and Deaths rate', 'value': 'MOBILITY_COMPARISON'},
                    {'label': 'Positive tests by date', 'value': 'CASES_TESTING'},
                    {'label': 'Patterns of Increasing Cases', 'value': 'PATTERNS'}
                ],
                value='JHU_COVID_19',  # Default value
                clearable=False
            )
        ], width=4),

        dbc.Col([
            dcc.DatePickerRange(
                id='date-picker',
                start_date='2020-01-01',
                end_date='2022-12-31',
                display_format='YYYY-MM-DD'  # Date format
            )
        ], width=8)
    ]),

    dbc.Row([
        dbc.Col([
            html.Img(id='bar-graph-matplotlib')
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='data-graph')
        ], width=12, md=6),
        dbc.Col([
            dag.AgGrid(
                id='data-table',
                columnDefs=[],
                rowData=[],
                columnSize="sizeToFit",
            )
        ], width=12, md=6)
    ], className='mt-4'),

    dbc.Row([
        dbc.Col([
            html.Div(id='error-message', style={'padding': '20px', 'color': 'red'})
        ], width=12)
    ])
])

# Callback to update graph and data table based on dropdown selection
@app.callback(
    [Output('data-graph', 'figure'),
     Output('bar-graph-matplotlib', 'src'),
     Output('data-table', 'columnDefs'),
     Output('data-table', 'rowData'),
     Output('error-message', 'children')],
    [Input('data-dropdown', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_graph(data_point, start_date, end_date):
    query = ""
    if data_point == 'JHU_COVID_19':
        query = f"""
        SELECT DISTINCT o.people_vaccinated, deaths
        FROM owid_vaccinations AS o
        JOIN scs_be_detailed_mortality AS s
        ON o.date = s.date
        LIMIT 100;
        """
    elif data_point == 'CDC_TESTING':
        query = f"SELECT cases, date FROM jhu_covid_19 LIMIT 100;"
    elif data_point == 'DATABANK_DEMOGRAPHICS':
        query = f"""
        SELECT cases, date
        FROM ecdc_global
        WHERE population > 10000000 AND date BETWEEN '{start_date}' AND '{end_date}'
        LIMIT 30;
        """
    elif data_point == 'MOBILITY_COMPARISON':
        query = f"""
        SELECT DISTINCT state, population, death_rate
        FROM rki_ger_covid19_dashboard
        LIMIT 100;
        """
    elif data_point == 'CASES_TESTING':
        query = f"""
        SELECT positive, date
        FROM cdc_testing
        LIMIT 100;
        """
    elif data_point == 'PATTERNS':
        query = f'http://127.0.0.1:5000/patterns?start_date={start_date}&end_date={end_date}'
    else:
        return {}, "", [], [], "Invalid data point selected."

    try:
        if data_point == 'PATTERNS':
            response = requests.get(query)
        else:
            response = requests.get(f'http://127.0.0.1:5000/data?query={query}')
        response.raise_for_status()
        data = response.json()

        if not data:
            raise ValueError("No data returned from the API.")

        df = pd.DataFrame(data)

        # Build the Plotly bar chart
        if len(df.columns) >= 2:
            fig = px.bar(df, x=df.columns[0], y=df.columns[1], title=f'{data_point} Bar Chart')
        else:
            fig = px.bar(title=f"Data structure of {data_point} is not supported for plotting")

        # Build the Matplotlib bar chart
        fig_matplotlib = plt.figure(figsize=(14, 5))
        if len(df.columns) >= 2:
            plt.bar(df[df.columns[0]], df[df.columns[1]])
            plt.xlabel(df.columns[0])
            plt.ylabel(df.columns[1])
            plt.title(f'{data_point} Matplotlib Bar Chart')

        buf = BytesIO()
        fig_matplotlib.savefig(buf, format="png")
        fig_data = base64.b64encode(buf.getbuffer()).decode("ascii")
        fig_bar_matplotlib = f'data:image/png;base64,{fig_data}'

        # Build the data table
        column_defs = [{'field': col} for col in df.columns]
        row_data = df.to_dict("records")

        return fig, fig_bar_matplotlib, column_defs, row_data, ""

    except requests.exceptions.RequestException as e:
        return {}, "", [], [], f"Request error: {str(e)}"
    except ValueError as e:
        return {}, "", [], [], str(e)
    except Exception as e:
        return {}, "", [], [], f"Unexpected error: {str(e)}"

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)

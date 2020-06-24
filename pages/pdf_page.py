from index import app, APP_PATH
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from styles import styles
import pandas as pd
from plots import pdf

sample_range = [1, 2, 3, 4] + list(range(5, 105, 5))

col_level_one = ['vehicle_CO2', 'vehicle_CO', 'vehicle_HC', 'vehicle_NOx', 'vehicle_PMx', 'vehicle_electricity']
col_level_two = ['total', 'average_per_step', 'per_100km']
col_tuple = [(level_one, level_two) for level_one in ['distance', 'norm_time'] for level_two in ['total']] + \
            [(level_one, level_two) for level_one in ['vehicle_fuel'] for level_two in col_level_two + ['mpg']] + \
            [(level_one, level_two) for level_one in col_level_one for level_two in col_level_two]
col_df = pd.DataFrame(col_tuple)

html_base = html.Div([
    html.H2("Sample PDF Analysis",
            style={
                "text-align": "center",
                "font-family": styles.font['family'],
                'padding': 5,
            }),

    html.Div([
        html.H4("Sample Percentage 1",
                style={
                    "text-align": "center",
                    "font-family": styles.font['family'],
                    'padding': 10,
                }),
        dcc.Dropdown(
            id='percent-1',
            options=[{'label': str(x), 'value': str(x)} for x in sample_range],
            value=str(sample_range[0])
        ),
    ], style={'width': '24%', 'display': 'inline-block', 'font-size': 'medium', 'font-family': styles.font['family']}),

    html.Div([
        html.H4("Sample Percentage 2",
                style={
                    "text-align": "center",
                    "font-family": styles.font['family'],
                    'padding': 10,
                }),
        dcc.Dropdown(
            id='percent-2',
            options=[{'label': str(x), 'value': str(x)} for x in sample_range],
            value=str(sample_range[-1])
        ),

    ],  style={'width': '24%', 'padding': '2rem', 'display': 'inline-block', 'font-size': 'medium', 'font-family': styles.font['family']}),

    html.Div([
        html.H4("Emission Output Type",
                style={
                    "text-align": "center",
                    "font-family": styles.font['family'],
                    'padding': 10,
                }),
        dcc.Dropdown(
            id='emissions-type',
            options=[{'label': x, 'value': x} for x in col_df.loc[:, 0].unique()],
            value='vehicle_fuel'
        ),
    ],  style={'width': '24%', 'padding': '2rem', 'display': 'inline-block', 'font-size': 'medium', 'font-family': styles.font['family']}),

    html.Div([
        html.H4("Emissions Value Metric",
                style={
                    "text-align": "center",
                    "font-family": styles.font['family'],
                    'padding': 10,
                }),
        dcc.Dropdown(
            id='emissions-metric',
            options=[{'label': x, 'value': x} for x in col_df.loc[:, 1].unique()],
            value='mpg'
        ),
    ],  style={'width': '24%', 'padding': '2rem', 'display': 'inline-block', 'font-size': 'medium', 'font-family': styles.font['family']}),

    html.Div([dcc.Graph(id='pdf-figure',
                        style={
                            'height': 600,
                            "border-radius": 5,
                            'background-color': "#f9f9f9",
                            'margin': 5,
                            # 'padding': 10,
                            'position': "relative",
                            'box-shadow': "2px 2px 2px lightgrey",
                        },
                        )]),
], style=styles.DISPLAY_CONTENT)


@app.callback(dash.dependencies.Output('emissions-metric', 'options'),
              [dash.dependencies.Input('emissions-type', 'value')])
def update_detector_dropdown(emissions_type):
    return [{'label': x, 'value': x} for x in col_df[1].loc[col_df[0] == emissions_type].unique()]


@app.callback(
    dash.dependencies.Output('pdf-figure', 'figure'),
    [dash.dependencies.Input('percent-1', 'value'),
     dash.dependencies.Input('percent-2', 'value'),
     dash.dependencies.Input('emissions-type', 'value'),
     dash.dependencies.Input('emissions-metric', 'value')])
def update_graph(sample_percent1, sample_percent2, plot_var, plot_var2):
    return pdf.plot_pdf(sample_percent1=sample_percent1, sample_percent2=sample_percent2,
                        plot_var=plot_var, plot_var2=plot_var2)

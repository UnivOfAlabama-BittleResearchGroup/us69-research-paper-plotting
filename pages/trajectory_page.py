from index import app, APP_PATH
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from styles import styles
import pandas as pd
import plots.trace_visualisation as trace_visualisation
import os

summary_df = pd.read_csv(os.path.join(APP_PATH, 'data', 'data_summary.csv'), header=[0, 1],
                         skipinitialspace=True,
                         )

summary_df.set_index(summary_df.iloc[:, 0], inplace=True)
trace_visualisation.sampled_emissions_df = pd.read_csv(os.path.join(APP_PATH, 'data', 'data.csv'))

sampled_vehicle_ids=trace_visualisation.sampled_emissions_df['vehicle_id'].unique()
best_fit_vehicle='480_8.2'
trace_visual=trace_visualisation.trace_visual
summary_df=summary_df
drop_down_options = ['Best Fit'] + list(sampled_vehicle_ids)

display_data_table = pd.DataFrame(index=[0, 1], columns=['Vehicle ID', 'Distance (miles)', 'Time in Network',
                                                         'Fuel Economy (mpg)'])

html_base = html.Div([
    html.H2("Trajectory Plot",
            style={
                "text-align": "center",
                "font-family": styles.font['family'],
                'padding': 5,
            }),
    html.Div([
        html.H4("Vehicle_ID",
                style={
                    "text-align": "center",
                    "font-family": styles.font['family'],
                    'padding': 5,
                }),
        dcc.Dropdown(
            id='vehicle_id',
            options=[{'label': id, 'value': id} for id in drop_down_options],
            value=drop_down_options[0]
        ),
    ],
        style={"margin-left": "2rem", 'width': '33%', 'display': 'inline-block', 'font-size': 'medium',
               'font-family': styles.font['family']}),
    html.Div([html.Div(id='summary-table', style=styles.DISPLAY_CONTENT)]),
    html.Div([dcc.Graph(id='trace-figure',
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


@app.callback(
    dash.dependencies.Output('trace-figure', 'figure'),
    [dash.dependencies.Input('vehicle_id', 'value'), ])
def update_graph(vehicle_id):
    if vehicle_id == 'Best Fit':
        vehicle_id = best_fit_vehicle

    return trace_visual(vehicle_id)


@app.callback(
    dash.dependencies.Output('summary-table', 'children'),
    [dash.dependencies.Input('vehicle_id', 'value')])
def update_table(vehicle_id):
    # ['Distance (miles)', 'Time in Network', 'Fuel Economy (mpg)']

    if vehicle_id == 'Best Fit':
        vehicle_id = best_fit_vehicle

    display_data_table.loc[0, 'Vehicle ID'] = 'Simulation Average'
    display_data_table.loc[1, 'Vehicle ID'] = vehicle_id

    display_data_table.loc[0, 'Distance (miles)'] = summary_df.loc['Total_average', ('distance', 'total')]
    display_data_table.loc[1, 'Distance (miles)'] = summary_df.loc[vehicle_id, ('distance', 'total')]

    display_data_table.loc[0, 'Time in Network'] = summary_df.loc['Total_average', ('norm_time', 'total')]
    display_data_table.loc[1, 'Time in Network'] = summary_df.loc[vehicle_id, ('norm_time', 'total')]

    display_data_table.loc[0, 'Fuel Economy (mpg)'] = summary_df.loc['Total_average', ('vehicle_fuel', 'mpg')]
    display_data_table.loc[1, 'Fuel Economy (mpg)'] = summary_df.loc[vehicle_id, ('vehicle_fuel', 'mpg')]

    # return dash_table.DataTable(
    #     id='dash-table',
    #     columns=[{"name": i, "id": i} for i in display_data_table.columns],
    #     data=display_data_table.to_dict('records'),
    # )
    return dbc.Table.from_dataframe(display_data_table, striped=True, bordered=True, hover=True)

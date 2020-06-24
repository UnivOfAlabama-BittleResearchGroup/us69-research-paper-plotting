import os
import pandas as pd
import plotly.graph_objects as go
import plotly.figure_factory as ff
from index import APP_PATH
import numpy as np
import math

data_dir = os.path.join(APP_PATH, 'data', 'multiple_sample_test')
one_hundo_dir = os.path.join(APP_PATH, 'data', 'sample_analysis')

shortest_trip_coords = [[-287.69, -175.55], [97.73, -227.72]]

shortest_trip_length = math.sqrt((shortest_trip_coords[0][0] - shortest_trip_coords[1][0]) ** 2
                                 + (shortest_trip_coords[0][1] - shortest_trip_coords[1][1]) ** 2) * \
                       0.000621371  # Meters to Miles conversion

col_level_one = ['vehicle_CO2', 'vehicle_CO', 'vehicle_HC', 'vehicle_NOx', 'vehicle_PMx', 'vehicle_electricity']
col_level_two = ['total', 'average_per_step', 'per_100km']
col_tuple = [(level_one, level_two) for level_one in ['distance', 'norm_time'] for level_two in ['total']] + \
            [(level_one, level_two) for level_one in ['vehicle_fuel'] for level_two in col_level_two + ['mpg']] + \
            [(level_one, level_two) for level_one in col_level_one for level_two in col_level_two]


def get_all_data(sample_percent):
    sample_percent_int = int(sample_percent) - 1

    list_of_ind = [20 * sample_percent_int + x for x in list(range(0, 20))]

    concise_df = pd.DataFrame(index=list_of_ind, columns=pd.MultiIndex.from_tuples(col_tuple))

    for ind in list_of_ind:
        folder = f"{str(ind)}_{sample_percent}"
        local_df = pd.read_csv(os.path.join(data_dir, folder, 'data_summary.csv'), header=[0, 1], index_col=0)
        concise_df.loc[ind, :] = local_df.loc['Total_average', :].copy()

    return concise_df


def plot_pdf(sample_percent1, plot_var, plot_var2):
    df1 = get_all_data(sample_percent1)
    df2 = pd.read_csv(os.path.join(one_hundo_dir, '100', 'data_summary.csv'), header=[0, 1], index_col=0)

    label1 = sample_percent1 + ' Percent'
    label2 = '100 Percent'

    group_labels = [label1, label2]

    colors = ['magenta', 'slategray']

    x1 = df1[(plot_var, plot_var2)]
    x2 = df2.loc[df2[('distance', 'total')] > shortest_trip_length][(plot_var, plot_var2)].iloc[2:].replace([np.inf, -np.inf], np.nan)

    x1 = x1.dropna()
    x2 = x2.dropna()

    bin_size = round((max(x1) - min(x1))/25, 3)
    # try:
    fig = ff.create_distplot([list(x1.values), ], [group_labels[0]], bin_size=bin_size,
                             curve_type='normal',
                             histnorm='probability density',  # override default 'kde'
                             colors=[colors[0]])

    fig.add_annotation(
        x=df1[(plot_var, plot_var2)].mean(),
        y=max(fig._data[1]['y']),
        text=f"Mean Value of {sample_percent1}% is {round(df1[(plot_var, plot_var2)].mean(), 3)}",
        showarrow=True,
        arrowhead=7,
        ax=-40,
        ay=-40,
    )
    # fig.add_annotation(
    #     x=df2[(plot_var, plot_var2)].iloc[1],
    #     y=fig._data[3]['y'].max(),
    #     text=f"Mean Value of {sample_percent2}% is {round(df2[(plot_var, plot_var2)].iloc[1], 3)}",
    #     showarrow=True,
    #     arrowhead=7,
    #     ax=40,
    #     ay=-60
    # )

    fig.add_shape(
        x0=x2.mean(),
        x1=x2.mean(),
        y0=0,
        y1=max(fig._data[1]['y']) + 0.2,
    )

    fig.update_layout(yaxis=dict(title="Probability Density", exponentformat='E'))

    return fig

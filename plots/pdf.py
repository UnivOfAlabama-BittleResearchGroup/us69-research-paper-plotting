import os
import pandas as pd
import plotly.graph_objects as go
import plotly.figure_factory as ff
from index import APP_PATH
import numpy as np
import math
import plotly_template as pt
from plotly.subplots import make_subplots

data_dir = os.path.join(APP_PATH, 'data', 'sample_analysis')

shortest_trip_coords = [[-287.69, -175.55], [97.73, -227.72]]

shortest_trip_length = math.sqrt((shortest_trip_coords[0][0] - shortest_trip_coords[1][0]) ** 2
                                 + (shortest_trip_coords[0][1] - shortest_trip_coords[1][1]) ** 2) * \
                                 0.000621371 # Meters to Miles conversion


def plot_pdf(sample_percent1, sample_percent2, plot_var, plot_var2):

    df1 = pd.read_csv(os.path.join(data_dir, sample_percent1, 'data_summary.csv'), header=[0, 1], index_col=0)
    df2 = pd.read_csv(os.path.join(data_dir, sample_percent2, 'data_summary.csv'), header=[0, 1], index_col=0)

    label1 = sample_percent1 + ' Percent'
    label2 = sample_percent2 + ' Percent'

    group_labels = [label1, label2]

    colors = ['magenta', 'slategray']

    x1 = df1.loc[df1[('distance', 'total')] > shortest_trip_length][(plot_var, plot_var2)].iloc[2:]. \
        replace([np.inf, -np.inf], np.nan)
    x2 = df2.loc[df2[('distance', 'total')] > shortest_trip_length][(plot_var, plot_var2)].iloc[2:]. \
        replace([np.inf, -np.inf], np.nan)

    x1 = x1.dropna()
    x2 = x2.dropna()

    bin_size = round((max(x1 + x2) - min(x1 + x2)) / 100, 2)
    # try:
    fig = ff.create_distplot([x1, x2], group_labels, bin_size=bin_size,
                             curve_type='normal',
                             histnorm='probability density',  # override default 'kde'
                             colors=colors)

    # except RuntimeError:
    #     print('help')
    #     x = 1


    fig.add_annotation(
        x=df1[(plot_var, plot_var2)].iloc[1],
        y=fig._data[2]['y'].max(),
        text=f"Mean Value of {sample_percent1}% is {round(df1[(plot_var, plot_var2)].iloc[1], 3)}",
        showarrow=True,
        arrowhead=7,
        ax=-40,
        ay=-40,
    )
    fig.add_annotation(
        x=df2[(plot_var, plot_var2)].iloc[1],
        y=fig._data[3]['y'].max(),
        text=f"Mean Value of {sample_percent2}% is {round(df2[(plot_var, plot_var2)].iloc[1], 3)}",
        showarrow=True,
        arrowhead=7,
        ax=40,
        ay=-60
    )

    fig.update_layout(yaxis=dict(title="Probability Density", exponentformat='E'))

    return fig


def simple_pdf(pd_series, labels=None, xaxis_label=None, histnorm=True, bin_count=50, opacity=0.75):

    if not isinstance(pd_series, list):
        plot_vals = [list(pd_series.values)]
        bin_size = round((max(plot_vals[0]) - min(plot_vals[0])) / bin_count, 3)
    else:
        plot_vals = [list(vals) for vals in pd_series]
        bin_size = round((max(plot_vals[0]) - min(plot_vals[0])) / bin_count, 3)

    if not (isinstance(labels, list)):
        labels = [labels]

    if histnorm:
        fig = ff.create_distplot(plot_vals, labels, bin_size=bin_size,
                                 curve_type='normal',
                                 # histnorm='probability density',  # override default 'kde'
                                 histnorm=None,
				 show_rug=False,
				 show_hist=False, 
				 colors=pt.pdf_colors[:len(labels)])

        fig.update_layout(yaxis=dict(title="Probability Density", exponentformat='E'),
                          xaxis=dict(title=xaxis_label),
                          template=pt.template)

    else:
        fig = make_subplots()
        for i, series in enumerate(plot_vals):
            fig.add_trace(go.Histogram(
                x=series,
                name=labels[i],
                opacity=opacity,
                marker_color=pt.pdf_colors[i],
                xbins=dict(size=bin_size)
                )
            )

        fig.update_layout(yaxis=dict(title="Count"),
                          xaxis=dict(title=xaxis_label),
                          template=pt.template,
                          barmode='overlay')

    return fig

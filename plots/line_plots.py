import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly_template as pt
import pandas as pd

DF = pd.DataFrame()


def line_plot(time_column, plot_columns, time_range):

    fig = go.Figure()

    if time_column == 'index':
        time = DF.index.values
    else:
        time = DF[time_column]

    if time_range is None:
        local_df = DF
    else:
        indexer = (time >= time_range[0]) & (time <= time_range[1])
        local_df = DF.loc[indexer]

    if not isinstance(plot_columns, list):
        plot_columns = [plot_columns]

    for column in plot_columns:

        fig.add_trace(
            go.Scatter(x=time,
                       y=local_df[column].values,
                       name=column,
                       mode='lines'),
            # secondary_y=False,
        )

    fig.update_layout(template=pt.template)

    return fig
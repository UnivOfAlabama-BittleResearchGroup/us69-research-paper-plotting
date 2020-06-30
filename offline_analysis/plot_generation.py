from plots import trace_visualisation, pdf, line_plots
import pandas as pd
import definitions
import os
import datetime
from functions import mp_funcs
from functions import func
import pickle

DATA_FOLDER = '2020-06-24_09_03_03-Full-Analysis'
DATA_DIR_FULL_PATH = os.path.join(definitions.DATA_DIR, DATA_FOLDER)

RAW_DATA_FILE = 'data.csv'
RAW_DATA_SUMMARY = 'data_summary.csv'
# %% Import the Data
raw_data_df = pd.read_csv(os.path.join(DATA_DIR_FULL_PATH, RAW_DATA_FILE), low_memory=False, index_col=0)
summary_df = pd.read_csv(os.path.join(DATA_DIR_FULL_PATH, RAW_DATA_SUMMARY), header=[0, 1], index_col=0)
raw_data_df.loc[:, 'timestep_time'] = pd.to_datetime(raw_data_df.loc[:, 'timestep_time'])
# %% Convert the Raw Seconds to Pandas Datetime. This takes a long time. Run once than save the .csv

if raw_data_df['timestep_time'].dtype.name == 'float64':
    """ These don't work on Windows """
    # print("Calling mp apply")
    # raw_data_df.loc[:, 'timestep_time'] = mp_funcs.apply_by_multiprocessing(raw_data_df['timestep_time'], func)
    # raw_data_df.loc[:, 'timestep_time'] = pd.to_datetime(raw_data_df.loc[:, 'timestep_time'])
    raw_data_df['timestep_time'] = raw_data_df['timestep_time'].apply(func=func)
    raw_data_df.loc[:, 'timestep_time'] = pd.to_datetime(raw_data_df.loc[:, 'timestep_time'])
    print("Saving to .csv")
    raw_data_df.to_csv(os.path.join(DATA_DIR_FULL_PATH, RAW_DATA_FILE))

# %% Calculate the Best Fit Vehicle (Choose the columns below)
columns = [('distance', 'total'),
           ('norm_time', 'total'),
           ('vehicle_fuel', 'total'),
           # ('vehicle_fuel', 'average_per_step'),
           ('vehicle_fuel', 'per_100km'),
           # ('vehicle_fuel', 'mpg'),
           ('vehicle_CO2', 'total'),
           # ('vehicle_CO2', 'average_per_step'),
           ('vehicle_CO2', 'per_100km'),
           ('vehicle_CO', 'total'),
           # ('vehicle_CO', 'average_per_step'),
           ('vehicle_CO', 'per_100km'),
           ('vehicle_HC', 'total'),
           # ('vehicle_HC', 'average_per_step'),
           ('vehicle_HC', 'per_100km'),
           ('vehicle_NOx', 'total'),
           # ('vehicle_NOx', 'average_per_step'),
           ('vehicle_NOx', 'per_100km'),
           ('vehicle_PMx', 'total'),
           # ('vehicle_PMx', 'average_per_step'),
           ('vehicle_PMx', 'per_100km'),
           # ('vehicle_electricity', 'total'),
           # ('vehicle_electricity', 'average_per_step'),
           # ('vehicle_electricity', 'per_100km')
           ]

diff_df = pd.DataFrame(index=summary_df.index, columns=summary_df.columns)

for col in columns:
    diff_df[col].iloc[2:] = abs(summary_df[col].iloc[2:].subtract(summary_df.loc['Total_average', col]))
    diff_df[col].iloc[2:] = diff_df[col].iloc[2:] / \
                            summary_df[col].iloc[2:].add(summary_df.loc['Total_average', col])

diff_df['diff_sum'] = diff_df.sum(axis=1)
best_fit_vehicle = diff_df['diff_sum'].iloc[2:].idxmin()
print('The best fit vehicle is: {0}'.format(best_fit_vehicle))

# %% Trace Visualisation Plot
# plot_vehicle = # best_fit_vehicle
plot_vehicle = '60240_189'

trace_visualisation.sampled_emissions_df = raw_data_df
trace_visualisation.trace_visual(plot_vehicle).show()
trace_visualisation.trace_no_map(plot_vehicle, plot_columns=['vehicle_fuel', 'vehicle_CO2', 'vehicle_NOx']).show()
# %% Plot Function
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly_template as pt


def trace_no_map(vehicle_id, plot_columns):
    OFFSET = 0.075
    POSITION_START = 1 - len(plot_columns) * OFFSET

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig = go.Figure()

    local_df = raw_data_df.loc[raw_data_df['vehicle_id'] == vehicle_id]

    fig.add_trace(
        go.Scatter(x=local_df['timestep_time'],
                   y=local_df['vehicle_speed'],
                   name='Speed',
                   mode='lines'),
    )

    yaxis_dict = dict(yaxis=dict(
        title="Vehicle Speed [mph]",
        # titlefont=dict(
        #     color=pt.colors[0]
        # ),
        # tickfont=dict(
        #     color=pt.colors[0]
        # )
    )
    )

    for i, column in enumerate(plot_columns):

        fig.add_trace(
            go.Scatter(x=local_df['timestep_time'],
                       y=local_df[column],
                       name=column,
                       mode='lines',
                       line=dict(color=pt.colors[i]),
                       yaxis='y' + str(i + 2)),
        )

        yaxis_dict['yaxis' + str(i + 2)] = dict(title=column,
                                                titlefont=dict(
                                                    color=pt.colors[i]
                                                ),
                                                tickfont=dict(
                                                    color=pt.colors[i]
                                                ),
                                                anchor="free" if i > 0 else 'x',
                                                overlaying="y",
                                                side="right",
                                                position=POSITION_START + OFFSET * i)

    fig.update_layout(yaxis_dict)

    fig.update_layout(xaxis=dict(domain=[0, POSITION_START]),
                      template=pt.template,
                      #margin=dict(l=20, r=20, t=20, b=20),
                      )

    # fig.update_yaxes(automargin=True)

    # fig.update_layout(
    #     yaxis=dict(
    #         title="yaxis title",
    #         titlefont=dict(
    #             color="#1f77b4"
    #         ),
    #         tickfont=dict(
    #             color="#1f77b4"
    #         )
    #     ),
    #     yaxis2=dict(
    #         title="yaxis2 title",
    #         titlefont=dict(
    #             color="#ff7f0e"
    #         ),
    #         tickfont=dict(
    #             color="#ff7f0e"
    #         ),
    #         anchor="free",
    #         overlaying="y",
    #         side="left",
    #         position=0.15
    #     ),
    #     yaxis4=dict(
    #         title="yaxis4 title",
    #         titlefont=dict(
    #             color="#9467bd"
    #         ),
    #         tickfont=dict(
    #             color="#9467bd"
    #         ),
    #         anchor="free",
    #         overlaying="y",
    #         side="right",
    #         position=0.85
    #     )
    # )

    return fig


# %% Diff PDF
# pdf.simple_pdf(diff_df['diff_sum'].iloc[2:], labels="Percent Difference").show()

# %%
pdf.simple_pdf(summary_df[('vehicle_fuel', 'per_100km')].iloc[2:], labels="l/100km", xaxis_label="l/100km").show()

# %% Trying out pandas groubby. Groupby time
# Add a column to count the number of vehicles
raw_data_df['vehicle_count'] = int(1)

groupyby_obj = raw_data_df.groupby(['timestep_time'])
index = groupyby_obj.sum().index

sum_data_df = pd.DataFrame(index=index)
sum_data_df['timestep_time'] = index
# %%
sum_columns = ['vehicle_CO', 'vehicle_CO2', 'vehicle_HC', 'vehicle_NOx', 'vehicle_PMx',
               'vehicle_electricity', 'vehicle_fuel', 'vehicle_pos', 'vehicle_count', 'vehicle_waiting']

mean_columns = ['vehicle_speed']

sum_data_df[sum_columns] = groupyby_obj.sum().loc[:, sum_columns]
sum_data_df[mean_columns] = groupyby_obj.mean().loc[:, mean_columns]
# %% Plot the sum_data_df
line_plots.DF = sum_data_df
line_plots.line_plot(time_column='timestep_time', plot_columns='vehicle_count', time_range=None).show()
line_plots.line_plot(time_column='timestep_time', plot_columns='vehicle_speed', time_range=None).show()
# %%
binned_emissions_dict = pickle.load(open(os.path.join(definitions.DATA_DIR, 'emissions_dict.pkl'), 'rb'))
# %%
from plots import emissions_heatmap
from functions import emissions

time_range = pd.to_datetime('2020-02-13T10:00:00')

fig = emissions_heatmap.single_time_interval(binned_emissions_dict, time_range=time_range, )
fig.show()

# fig.write_image("fig1.svg")
# %% Load the MPG Distributions
from functions.emissions import get_time_based_emissions_distribution

time_interval = [['2020-02-13 06:00:00', '2020-02-13 09:00:00'], ['2020-02-13 11:00:00', '2020-02-13 14:00:00'],
                 ['2020-02-13 16:00:00', '2020-02-13 19:00:00']]

plot_column = ('norm_time', 'total')

interval_distribution = get_time_based_emissions_distribution(emissions_df=raw_data_df, summary_df=summary_df,
                                                              interval=time_interval, bin_column=plot_column,
                                                              return_data=True)

# interval_distribution = pickle.load(open(os.path.join(definitions.DATA_DIR, 'interval_distribution.pkl'), 'rb'))
# %%
dist_list = [list(item[1]) for item in interval_distribution]
label_list = [str(item[0][0]) + ' - ' + str(item[0][1]) for item in interval_distribution]

pdf_fig = pdf.simple_pdf(pd_series=dist_list, labels=label_list, xaxis_label="Vehicle Total Time [s]")
pdf_fig.show()

# with open(os.path.join("images", "-".join(plot_column)), 'wb') as img:
#     img.write(pdf_fig.to_image(format='png', height=1080, width=1920))

# %%

# px.histogram(df, x="total_bill", histnorm='probability density')

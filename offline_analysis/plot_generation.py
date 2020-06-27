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
#%% Import the Data
raw_data_df = pd.read_csv(os.path.join(DATA_DIR_FULL_PATH, RAW_DATA_FILE), low_memory=False, index_col=0)
summary_df = pd.read_csv(os.path.join(DATA_DIR_FULL_PATH, RAW_DATA_SUMMARY), header=[0, 1], index_col=0)
raw_data_df.loc[:, 'timestep_time'] = pd.to_datetime(raw_data_df.loc[:, 'timestep_time'])
#%% Convert the Raw Seconds to Pandas Datetime. This takes a long time. Run once than save the .csv

if raw_data_df['timestep_time'].dtype.name == 'float64':

    """ These don't work on Windows """
    #print("Calling mp apply")
    # raw_data_df.loc[:, 'timestep_time'] = mp_funcs.apply_by_multiprocessing(raw_data_df['timestep_time'], func)
    # raw_data_df.loc[:, 'timestep_time'] = pd.to_datetime(raw_data_df.loc[:, 'timestep_time'])
    raw_data_df['timestep_time'] = raw_data_df['timestep_time'].apply(func=func)
    raw_data_df.loc[:, 'timestep_time'] = pd.to_datetime(raw_data_df.loc[:, 'timestep_time'])
    print("Saving to .csv")
    raw_data_df.to_csv(os.path.join(DATA_DIR_FULL_PATH, RAW_DATA_FILE))


#%% Calculate the Best Fit Vehicle (Choose the columns below)
columns = [('distance', 'total'),
           ('norm_time', 'total'),
           ('vehicle_fuel', 'total'),
           #('vehicle_fuel', 'average_per_step'),
           ('vehicle_fuel', 'per_100km'),
           #('vehicle_fuel', 'mpg'),
           ('vehicle_CO2', 'total'),
           #('vehicle_CO2', 'average_per_step'),
           ('vehicle_CO2', 'per_100km'),
           ('vehicle_CO', 'total'),
           #('vehicle_CO', 'average_per_step'),
           ('vehicle_CO', 'per_100km'),
           ('vehicle_HC', 'total'),
           #('vehicle_HC', 'average_per_step'),
           ('vehicle_HC', 'per_100km'),
           ('vehicle_NOx', 'total'),
           #('vehicle_NOx', 'average_per_step'),
           ('vehicle_NOx', 'per_100km'),
           ('vehicle_PMx', 'total'),
           #('vehicle_PMx', 'average_per_step'),
           ('vehicle_PMx', 'per_100km'),
           #('vehicle_electricity', 'total'),
           #('vehicle_electricity', 'average_per_step'),
           #('vehicle_electricity', 'per_100km')
           ]

diff_df = pd.DataFrame(index=summary_df.index, columns=summary_df.columns)

for col in columns:
    diff_df[col].iloc[2:] = abs(summary_df[col].iloc[2:].subtract(summary_df.loc['Total_average', col]))
    diff_df[col].iloc[2:] = diff_df[col].iloc[2:] / \
    summary_df[col].iloc[2:].add(summary_df.loc['Total_average', col])

diff_df['diff_sum'] = diff_df.sum(axis=1)
best_fit_vehicle = diff_df['diff_sum'].iloc[2:].idxmin()
print('The best fit vehicle is: {0}'.format(best_fit_vehicle))

#%% Trace Visualisation Plot
# plot_vehicle = # best_fit_vehicle
plot_vehicle = '60240_189'

trace_visualisation.sampled_emissions_df = raw_data_df
trace_visualisation.trace_visual(plot_vehicle).show()

#%% Diff PDF
pdf.simple_pdf(diff_df['diff_sum'].iloc[2:], labels="Percent Difference").show()

#%%
pdf.simple_pdf(summary_df[('vehicle_fuel', 'per_100km')].iloc[2:], labels="l/100km", xaxis_label="l/100km").show()

#%% Trying out pandas groubby. Groupby time
# Add a column to count the number of vehicles
raw_data_df['vehicle_count'] = int(1)

groupyby_obj = raw_data_df.groupby(['timestep_time'])
index = groupyby_obj.sum().index

sum_data_df = pd.DataFrame(index=index)
sum_data_df['timestep_time'] = index
#%%
sum_columns = ['vehicle_CO', 'vehicle_CO2', 'vehicle_HC', 'vehicle_NOx', 'vehicle_PMx',
               'vehicle_electricity', 'vehicle_fuel', 'vehicle_pos', 'vehicle_count', 'vehicle_waiting']

mean_columns = ['vehicle_speed']

sum_data_df[sum_columns] = groupyby_obj.sum().loc[:, sum_columns]
sum_data_df[mean_columns] = groupyby_obj.mean().loc[:, mean_columns]
#%% Plot the sum_data_df
line_plots.DF = sum_data_df
line_plots.line_plot(time_column='timestep_time', plot_columns='vehicle_count', time_range=None).show()
line_plots.line_plot(time_column='timestep_time', plot_columns='vehicle_speed', time_range=None).show()
#%%
binned_emissions_dict = pickle.load(open(os.path.join(definitions.DATA_DIR, 'emissions_dict.pkl'), 'rb'))
#%%
from plots import emissions_heatmap
from functions import emissions

time_range = pd.to_datetime('2020-02-13T10:00:00')

x_bins_lon, y_bins_lat = emissions.convert_bins_2_lat_lon(5)

fig = emissions_heatmap.single_time_interval(binned_emissions_dict, time_range=time_range,)
fig.show()
fig.write_image("fig1.svg")

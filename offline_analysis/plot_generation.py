from plots import trace_visualisation, pdf
import pandas as pd
import definitions
import os
import datetime
from functions import mp_funcs
from functions import func

DATA_FOLDER = '2020-06-24_09_03_03-Full-Analysis'
DATA_DIR_FULL_PATH = os.path.join(definitions.DATA_DIR, DATA_FOLDER)

RAW_DATA_FILE = 'data.csv'
RAW_DATA_SUMMARY = 'data_summary.csv'
#%% Import the Data
raw_data_df = pd.read_csv(os.path.join(DATA_DIR_FULL_PATH, RAW_DATA_FILE), low_memory=False)
summary_df = pd.read_csv(os.path.join(DATA_DIR_FULL_PATH, RAW_DATA_SUMMARY), header=[0, 1], index_col=0)

#%% Convert the Raw Seconds to Pandas Datetime. This takes a long time. Run once than save the .csv

if raw_data_df['timestep_time'].dtype.name != 'datetime64[ns]':

    """ These don't work on Windows """
    #print("Calling mp apply")
    # raw_data_df.loc[:, 'timestep_time'] = mp_funcs.apply_by_multiprocessing(raw_data_df['timestep_time'], func)
    # raw_data_df.loc[:, 'timestep_time'] = pd.to_datetime(raw_data_df.loc[:, 'timestep_time'])
    raw_data_df['timestep_time'] = raw_data_df['timestep_time'].apply(func=func)

    print("Calling mp apply")
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
#plot_vehicle = # best_fit_vehicle
plot_vehicle = '60240_189'
trace_visualisation.sampled_emissions_df = raw_data_df
trace_visualisation.trace_visual(plot_vehicle).show()

#%% Diff PDF
pdf.simple_pdf(diff_df['diff_sum'].iloc[2:], labels="Percent Difference").show()
pdf.simple_pdf(diff_df[('vehicle_fuel', 'per_100km')], labels="l/100km").show()


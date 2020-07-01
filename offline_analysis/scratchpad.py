from plots import trace_visualisation, pdf, line_plots
from functions.emissions import get_time_based_emissions_distribution, get_time_based_emissions_points
from functions import mp_funcs
from functions import func

import pandas as pd
import definitions
import os
import datetime
import plotly.io as pio
import pickle
pio.renderers.default = "browser"

DATA_FOLDER = '2020-06-24_09_03_03-Full-Analysis'
DATA_DIR_FULL_PATH = os.path.join(definitions.DATA_DIR, DATA_FOLDER)

RAW_DATA_FILE = 'data.csv'
RAW_DATA_SUMMARY = 'data_summary.csv'

raw_data_df = pd.read_csv(os.path.join(DATA_DIR_FULL_PATH, RAW_DATA_FILE), low_memory=False, index_col=0)
summary_df = pd.read_csv(os.path.join(DATA_DIR_FULL_PATH, RAW_DATA_SUMMARY), header=[0, 1], index_col=0)
raw_data_df.loc[:, 'timestep_time'] = pd.to_datetime(raw_data_df.loc[:, 'timestep_time'])

plot_vehicle = '600_15'

trace_visualisation.pt.font_dict = None

trace_visualisation.sampled_emissions_df = raw_data_df
trace_visualisation.trace_visual(plot_vehicle).show()

trace_no_map = trace_visualisation.trace_no_map(plot_vehicle, plot_columns=['vehicle_fuel', 'vehicle_CO2', 'vehicle_NOx'],
                                 axis_names=["Vehicle Speed [mph]", 'Vehicle Fuel [gal/s]', 'Vehicle CO_2 [g/s]',
                                             'Vehicle NOx [g/s]'],
                                               offset=0.1)

trace_no_map.show()

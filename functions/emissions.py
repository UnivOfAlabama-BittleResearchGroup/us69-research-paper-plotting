import numpy as np
import definitions
import pandas as pd
import sumolib
import gc
from functions import mp_funcs, timing
import os
import pickle

#emissions_df = pd.DataFrame()
NET = sumolib.net.readNet(definitions.NET_FILE)


def get_net_bins(bin_size):
    net_bbox = NET.getBBoxXY()
    x_limits = [int(net_bbox[0][0]) - 20, int(net_bbox[1][0]) + 20]
    y_limits = [int(net_bbox[0][1]) - 20, int(net_bbox[1][1]) + 20]
    x_bins = np.arange(start=x_limits[0], stop=x_limits[1], step=bin_size)
    y_bins = np.arange(start=y_limits[0], stop=y_limits[1], step=bin_size)
    return x_bins, y_bins


def convert_bins_2_lat_lon(bin_size):
    x_bins, y_bins = get_net_bins(bin_size)
    x_bins_lon = [NET.convertXY2LonLat(x, 0)[0] for x in x_bins]
    y_bins_lat = [NET.convertXY2LonLat(0, y)[1] for y in y_bins]
    return x_bins_lon, y_bins_lat

@timing
def bin_2D_sum(emissions_df, bin_column, resample_period, bin_size, start_time=None, end_time=None,
               processor_num=mp_funcs.CPU_COUNT):

    x_bins, y_bins = get_net_bins(bin_size)

    # setup the time range
    start_time = emissions_df['timestep_time'].iloc[0] if start_time is None else start_time
    end_time = emissions_df['timestep_time'].iloc[-1] if end_time is None else end_time
    time_range = pd.date_range(start=start_time, end=end_time, freq=resample_period)

    # create the memmap object
    master_A_sum = np.memmap(definitions.MMAPPED_PATH, mode='w+', dtype=np.float32,
                             shape=(len(time_range), len(y_bins) - 1, len(x_bins) - 1))

    time_range = np.array_split(time_range, processor_num)

    computation_df = emissions_df[['timestep_time', 'vehicle_x', 'vehicle_y'] + bin_column].copy()

    master_A_sum = mp_funcs.shared_df_mp_func(time_range, _2d_bin, computation_df,
                                              bin_column=bin_column, x_bins=x_bins, y_bins=y_bins)

    x_bins_lon, y_bins_lat = convert_bins_2_lat_lon(bin_size)

    output_dict = {}
    for i, item in enumerate(master_A_sum):
        for j, inner_item in enumerate(item[1][0]):
            output_dict[time_range[i][j]] = {}
            # inner_item = np.transpose(np.nonzero(inner_item)) This is not used for this step
            output_dict[time_range[i][j]]["lat"] = [y_bins_lat[coord[0]] for coord in
                                                    np.transpose(np.nonzero(inner_item))]
            output_dict[time_range[i][j]]["lon"] = [x_bins_lon[coord[1]] for coord in
                                                    np.transpose(np.nonzero(inner_item))]
            inner_item = inner_item[inner_item != 0].flatten()
            output_dict[time_range[i][j]]["data"] = inner_item
            output_dict[time_range[i][j]]["max_value"] = item[1][1]
    del master_A_sum
    gc.collect()

    output = open(os.path.join(definitions.DATA_DIR, 'emissions_dict.pkl'), 'wb')
    pickle.dump(output_dict, output)
    output.close()


def _2d_bin(time_range, df, bin_column, x_bins, y_bins):
    result_dict = []
    max = 0
    bin_column = bin_column[0]

    for i, time in enumerate(time_range[:-1]):
        mask = (df['timestep_time'] >= time) & (df['timestep_time'] < time_range[i+1])
        local_df = df[mask]
        A, _, _ = np.histogram2d(local_df['vehicle_x'],
                                 local_df['vehicle_y'],
                                 bins=[x_bins, y_bins],
                                 weights=local_df[bin_column])
        A = A.transpose()
        result_dict.append(A)
        local_max = np.amax(A, axis=(0, 1))
        if local_max > max:
            max = local_max

    return result_dict, max


def get_time_based_emissions_distribution(emissions_df, summary_df, bin_column,
                                          interval, start_time=None, end_time=None, processor_num=1):
    if isinstance(interval, str):
        start_time = emissions_df['timestep_time'].iloc[0] if start_time is None else start_time
        end_time = emissions_df['timestep_time'].iloc[-1] if end_time is None else end_time
        time_range = pd.date_range(start=start_time, end=end_time, freq=interval)
        time_range = np.array_split(time_range, processor_num)
    else:
        time_range = [pd.to_datetime(time_list) for time_list in interval]

    computation_df = emissions_df[['timestep_time', 'vehicle_id']].copy()
    plot_data = _set_time_based_emissions_distribution(time_range, computation_df, bin_column, summary_df)
    pickle.dump(plot_data, open(os.path.join(definitions.DATA_DIR, 'interval_distribution.pkl'), 'wb'))


def _set_time_based_emissions_distribution(time_range, df, bin_column, summary_df):

    plot_list = []
    if isinstance(time_range, list):
        for i, time in enumerate(time_range):
            plot_list.append(["", ""])
            mask = (df['timestep_time'] >= time[0]) & (df['timestep_time'] < time[1])
            local_df = df[mask]
            unique_values = local_df['vehicle_id'].unique()
            plot_list[i][0] = time
            plot_list[i][1] = summary_df.loc[summary_df.index.isin(unique_values), bin_column]
        return plot_list
    else:
        x = 0  # need to do more advanced calculation in the case that pd.datetimeindex and smaller intervals


if __name__ == '__main__':

    heatmap_desired = False
    emission_distribution_desired = True

    DATA_FOLDER = '2020-06-24_09_03_03-Full-Analysis'
    DATA_DIR_FULL_PATH = os.path.join(definitions.DATA_DIR, DATA_FOLDER)
    RAW_DATA_FILE = 'data.csv'
    SUMMARY_DATA_FILE = 'data_summary.csv'

    time_interval = [['2020-02-13 06:00:00', '2020-02-13 09:00:00'], ['2020-02-13 11:00:00', '2020-02-13 14:00:00'],
                     ['2020-02-13 16:00:00', '2020-02-13 19:00:00']]

    df = pd.read_csv(os.path.join(DATA_DIR_FULL_PATH, RAW_DATA_FILE), low_memory=False, index_col=0)
    df['timestep_time'] = pd.to_datetime(df['timestep_time'])
    if heatmap_desired:
        # Increase the processor number the smaller the resample period is
        bin_2D_sum(emissions_df=df, bin_column=['vehicle_fuel'], resample_period='5T', bin_size=5, )

    if emission_distribution_desired:
        summary_df = pd.read_csv(os.path.join(DATA_DIR_FULL_PATH, SUMMARY_DATA_FILE), header=[0, 1], index_col=0)
        get_time_based_emissions_distribution(emissions_df=df, summary_df=summary_df, interval=time_interval,
                                              bin_column=('vehicle_fuel', 'mpg'))

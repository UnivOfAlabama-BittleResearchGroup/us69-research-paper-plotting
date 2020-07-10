import numpy as np
import definitions
import pandas as pd
import sumolib
import gc
from functions import mp_funcs, timing
import os
import pickle

# emissions_df = pd.DataFrame()
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
def bin_2D_average(emissions_df, bin_column, resample_period, bin_size, start_time=None, end_time=None,
               processor_num=mp_funcs.CPU_COUNT, output_path=None):

    x_bins, y_bins = get_net_bins(bin_size)
    start_time = emissions_df['timestep_time'].iloc[0] if start_time is None else start_time
    end_time = emissions_df['timestep_time'].iloc[-1] if end_time is None else end_time
    time_range = pd.date_range(start=start_time, end=end_time, freq=resample_period)
    time_range = np.array_split(time_range, processor_num)
    computation_df = emissions_df[['timestep_time', 'vehicle_x', 'vehicle_y'] + bin_column].copy()
    master_A_sum = mp_funcs.shared_df_mp_func(time_range, _2d_bin_simple, computation_df,
                                              bin_column=bin_column, x_bins=x_bins, y_bins=y_bins)
    x_bins_lon, y_bins_lat = convert_bins_2_lat_lon(bin_size)
    output_dict = {}
    for i, item in enumerate(master_A_sum):
        for j, inner_item in enumerate(item[1][0]):
            output_dict[time_range[i][j]] = {}
            # inner_item = np.transpose(np.nonzero(inner_item)) This is not used for this step
            output_dict[time_range[i][j]]["lat"] = [y_bins_lat[coord[0]] for coord in
                                                    np.transpose(np.nonzero(inner_item > 1))]
            output_dict[time_range[i][j]]["lon"] = [x_bins_lon[coord[1]] for coord in
                                                    np.transpose(np.nonzero(inner_item > 1))]
            inner_item = inner_item[inner_item > 1].flatten()
            output_dict[time_range[i][j]]["data"] = inner_item
            output_dict[time_range[i][j]]["max_value"] = item[1][1]
    del master_A_sum
    gc.collect()
    if output_path is None:
        return output_dict
    output = open(output_path, 'wb')
    pickle.dump(output_dict, output)
    output.close()


def _2d_bin_simple(time_range, df, bin_column, x_bins, y_bins):
    result_dict = []
    max = 0
    bin_column = bin_column[0]

    for i, time in enumerate(time_range[:-1]):
        mask = (df['timestep_time'] >= time) & (df['timestep_time'] < time_range[i + 1])
        local_df = df[mask]
        A, _, _ = np.histogram2d(local_df['vehicle_x'],
                                 local_df['vehicle_y'],
                                 bins=[x_bins, y_bins],
                                 weights=local_df[bin_column])
        B, _, _ = np.histogram2d(local_df['vehicle_x'],
                                 local_df['vehicle_y'],
                                 bins=[x_bins, y_bins])
        A = np.divide(A, B).transpose()
        result_dict.append(A)
        local_max = np.amax(A, axis=(0, 1))
        if local_max > max:
            max = local_max

    return result_dict, max

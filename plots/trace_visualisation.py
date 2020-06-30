import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly_template as pt
import math

mapbox_key = "pk.eyJ1IjoibWF4LXNjaHJhZGVyIiwiYSI6ImNrOHQxZ2s3bDAwdXQzbG81NjZpZm96bDEifQ.etUi4OK4ozzaP_P8foZn_A"

sampled_emissions_df = None


def trace_visual(vehicle_id):

    font_dict = pt.font_dict

    animation_step_duration = 500  # ms
    animation_step_size = 4  # animate two simulation steps in every animation

    local_df = sampled_emissions_df.loc[sampled_emissions_df['vehicle_id'] == vehicle_id]

    fig = make_subplots(rows=1, cols=2,
                        specs=[[{"secondary_y": True}, {'type': 'mapbox', }]],
                        # subplot_titles=('Subplot (1,1)', 'Subplot(1,2)'),
                        column_widths=[0.7, 0.3],
                        horizontal_spacing=0.1, )

    # for i in range(10):
    #     vehicle_id = sampled_vehicle_ids[i]
    #     local_df = sampled_emissions_df.loc[sampled_emissions_df['vehicle_id'] == vehicle_id]
    #
    #     fig.add_trace(
    #         go.Scatter(
    #             x=local_df['timestep_time'],
    #             y=local_df['vehicle_speed'],
    #             name=vehicle_id,
    #             mode='markers+lines'),
    #         secondary_y=False,
    #         row=1,
    #         col=1,
    #     )

    fig.add_trace(
        go.Scatter(x=local_df['timestep_time'],
                   y=local_df['vehicle_speed'],
                   name='Speed',
                   mode='lines'),
        secondary_y=False,
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(x=local_df['timestep_time'],
                   y=local_df['distance'],
                   name='Distance',
                   mode='lines', ),
        secondary_y=True,
        row=1,
        col=1,
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Simulation Time [s]",
                     row=1,
                     col=1,
                     range=[local_df['timestep_time'].iloc[0], local_df['timestep_time'].iloc[-1]]
                     )

    # Set y-axes titles
    fig.update_yaxes(title_text="Speed [mph]",
                     range=[0, 65],
                     secondary_y=False,
                     row=1,
                     col=1
                     )

    fig.update_yaxes(title_text="Distance Travelled [miles]",
                     secondary_y=True,
                     range=[0, local_df['distance'].iloc[-1] + 0.2],
                     row=1,
                     col=1
                     )

    fig.add_trace(go.Scattermapbox(
        lon=local_df['vehicle_x_geo'],
        lat=local_df['vehicle_y_geo'],
        mode='markers+lines',
        line={
            'color': 'blue',
            'width': 4,
        }), row=1, col=2
    )

    frames = [dict(
        name=k,
        data=[go.Scatter(x=local_df['timestep_time'].iloc[:k],
                         y=local_df['vehicle_speed'].iloc[:k],
                         mode='markers+lines', ),
              go.Scatter(x=local_df['timestep_time'].iloc[:k],
                         y=local_df['distance'].iloc[:k],
                         mode='markers+lines', ),
              go.Scattermapbox(
                  lat=local_df['vehicle_y_geo'].iloc[:k],
                  lon=local_df['vehicle_x_geo'].iloc[:k],
                  mode='lines',
                  line={
                      'color': 'blue',
                      'width': 4,
                  }
              ),
              ],
        traces=[0, 1, 2]  # the elements of the list [0,1,2] give info on the traces in fig.data
        # that are updated by the above three go.Scatter instances
    ) for k in range(0, len(local_df['vehicle_x_geo']), animation_step_size)]

    updatemenus = [
        {
            "buttons": [
                {
                    "args": [[f'{k}' for k in range(0, len(local_df['vehicle_x_geo']), animation_step_size)],
                             {"frame": {"duration": animation_step_duration, "redraw": True},
                              "fromcurrent": True,
                              "transition": {"duration": animation_step_duration}
                              }
                             ],
                    "label": "&#9654;",  # play symbol
                    "method": "animate",
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                      "mode": "immediate",
                                      "transition": {"duration": 0}}],
                    "label": "&#9724;",  # pause symbol
                    "method": "animate",
                },
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 30},
            "type": "buttons",
            "x": 0.1,
            "y": 0,
            'showactive': True,
        }
    ]

    sliders = [
        {
            "currentvalue": {
                "font": font_dict,
                "prefix": "Time: ",
                "visible": True,
                "xanchor": "right"
            },
            "pad": {"b": 20, "t": 30},
            "len": 0.9,
            "x": 0.1,
            "y": 0,
            "visible": True,
            "steps": [
                {
                    "args": [[f['name']], {"frame": {"duration": animation_step_duration, "redraw": True},
                                           "mode": "immediate",
                                           "transition": {"duration": animation_step_duration}}
                             ],
                    "label": str(local_df['timestep_time'].iloc[int(f['name'])]),
                    "method": "animate",
                }
                for f in frames
            ],
        }
    ]

    fig.update(frames=frames),
    fig.update_layout(updatemenus=updatemenus,
                      sliders=sliders,
                      font=font_dict,
                      margin=dict(l=15, r=15, t=15, b=15),
                      mapbox=dict(
                          accesstoken=mapbox_key,
                          bearing=0,
                          style='mapbox://styles/max-schrader/ck8t1cmmc02wk1it9rv28iyte',
                          center=go.layout.mapbox.Center(
                              lat=33.12627,
                              lon=-87.54891
                          ),
                          pitch=0,
                          zoom=14.1,
                      ),
                      template=pt.template
                      )
    return fig


def trace_no_map(vehicle_id, plot_columns, axis_names):

    OFFSET = 0.075
    POSITION_START = 1 - len(plot_columns) * OFFSET
    TICK_NUM = 5

    fig = go.Figure()

    mask = sampled_emissions_df['vehicle_id'] == vehicle_id
    local_df = sampled_emissions_df[mask]


    fig.add_trace(
        go.Scatter(x=local_df['timestep_time'],
                   y=local_df['vehicle_speed'],
                   name='Speed',
                   mode='lines'),
    )

    axis_class_list = []
    max_tick_ratio = 0
    for i, column in enumerate(['vehicle_speed'] + plot_columns):
        tick_calculation = CalculateTicks(local_df[column], TICK_NUM)
        axis_class_list.append(tick_calculation)
        max_tick_ratio = tick_calculation.y_dtick_ratio if tick_calculation.y_dtick_ratio > max_tick_ratio \
            else max_tick_ratio

    any_negative = False
    for i, tick_calculation in enumerate(axis_class_list):
        if tick_calculation.y_min < 0:
            any_negative = True
            axis_class_list[i].negative = True
            axis_class_list[i].y_negative_ratio = abs(tick_calculation.y_min / tick_calculation.y_range) * max_tick_ratio
        else:
            axis_class_list[i].y_negative_ratio = 0
        axis_class_list[i].y_positive_ratio = (tick_calculation.y_max / tick_calculation.y_range) * max_tick_ratio

    global_negative_ratio = 0
    global_positive_ratio = 0
    for i, tick_calculation in enumerate(axis_class_list):
        global_negative_ratio = tick_calculation.y_negative_ratio if tick_calculation.y_negative_ratio \
                                                                     > global_negative_ratio else global_negative_ratio
        global_positive_ratio = tick_calculation.y_positive_ratio if tick_calculation.y_positive_ratio \
                                                                     > global_positive_ratio else global_positive_ratio

    global_negative_ratio = global_negative_ratio + 0.1
    for i, tick_calculation in enumerate(axis_class_list):
        if any_negative:
            axis_class_list[i].y_range_min = global_negative_ratio * tick_calculation.y_dtick * -1
        else:
            axis_class_list[i].y_range_min = 0
        axis_class_list[i].y_range_max = global_positive_ratio * tick_calculation.y_dtick

    yaxis_dict = dict(yaxis=dict(
        title=axis_names[0],
        range=[axis_class_list[0].y_range_min, axis_class_list[0].y_range_max],
        dtick=axis_class_list[0].y_dtick,
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

        yaxis_dict['yaxis' + str(i + 2)] = dict(title=axis_names[i+1],
                                                range=[axis_class_list[i+1].y_range_min,
                                                       axis_class_list[i+1].y_range_max],
                                                dtick=axis_class_list[i+1].y_dtick,
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
                      showlegend=False,
                      #margin=dict(l=20, r=20, t=20, b=20),
                      )

    return fig


class CalculateTicks:

    def __init__(self, data, tick_num):

        self.negative = False
        self.y_negative_ratio = None
        self.y_positive_ratio = None
        self.y_range_min = None
        self.y_range_max = None

        self.y_min = min(data)
        self.y_max = max(data)

        self.y_range = self.y_max - self.y_min if self.y_min <0 else self.y_max
        self.y_range = self.y_range * 1000
        self.y_length = len(str(math.floor(self.y_range)))

        self.y_pw10_div = 10 ** (self.y_length - 1)
        self.y_first_digit = math.floor(self.y_range / self.y_pw10_div)
        self.y_max_base = self.y_pw10_div * self.y_first_digit / 1000

        self.y_dtick = self.y_max_base / tick_num
        self.y_dtick_ratio = self.y_range / self.y_dtick



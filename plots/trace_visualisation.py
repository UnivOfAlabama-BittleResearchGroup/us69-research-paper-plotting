import plotly.graph_objects as go
from plotly.subplots import make_subplots

mapbox_key = "pk.eyJ1IjoibWF4LXNjaHJhZGVyIiwiYSI6ImNrOHQxZ2s3bDAwdXQzbG81NjZpZm96bDEifQ.etUi4OK4ozzaP_P8foZn_A"

sampled_emissions_df = None


def trace_visual(vehicle_id):
    font_dict = dict(color="black",
                     family="Courier New, monospace",
                     size=16)

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
                    "label": local_df['timestep_time'].iloc[int(f['name'])],
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
                      )
    return fig

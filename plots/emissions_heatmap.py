import plotly.graph_objects as go
import numpy as np
import plotly_template as pt

plot_radius = 10
mapbox_key = "pk.eyJ1IjoibWF4LXNjaHJhZGVyIiwiYSI6ImNrOHQxZ2s3bDAwdXQzbG81NjZpZm96bDEifQ.etUi4OK4ozzaP_P8foZn_A"

def single_time_interval(emissions_data_dict, time_range, lat_edges, lon_edges):

    z_data = emissions_data_dict[time_range]['data']

    fig = go.Figure(go.Densitymapbox(
        lat=lat_edges,
        lon=lon_edges,
        z=z_data,
        # customdata=summed_array[0][2],
        # hovertemplate='%{customdata}' if sum else None,
        radius=plot_radius,
        hoverinfo='z',
        coloraxis="coloraxis"))
        # frames=[go.Frame(data=go.Densitymapbox(
        #     lat=summed_array[i][0] if sum else inst_array[i][0],
        #     lon=summed_array[i][1] if sum else inst_array[i][1],
        #     z=np.log10(summed_array[i][2]) if sum else inst_array[i][2],
        #     customdata=summed_array[i][2],
        #     hovertemplate='%{customdata}' if sum else None,
        #     radius=plot_radius,
        #     hoverinfo='z' if not sum else None,
        #     showscale=False,
        # ),
        #    name=step_time_values[i],
        #) for i in step_num]

    fig.update_layout(
        template=pt.template,
        # title={"text": "Fuel Consumption", "font": colorbar_font, 'yanchor': 'middle', 'xanchor': 'center'} if sum
        # else {"text": "Instantaneous Fuel Consumption", "font": colorbar_font, 'yanchor': 'middle', 'xanchor': 'center'},
        # font=colorbar_font,
        # paper_bgcolor='rgb(249, 249, 249)',
        # hovermode='closest',
        # margin=go.layout.Margin(
        #     l=20,  # left margin
        #     r=0,  # right margin
        #     b=5,  # bottom margin
        #     t=0  # top margin
        # ),
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
        # coloraxis=log_color_axis if sum else color_axis
    )

    return fig
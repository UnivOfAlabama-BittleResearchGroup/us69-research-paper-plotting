import plotly.graph_objects as go
import numpy as np
import plotly_template as pt
# import scipy.

plot_radius = 20
mapbox_key = "pk.eyJ1IjoibWF4LXNjaHJhZGVyIiwiYSI6ImNrOHQxZ2s3bDAwdXQzbG81NjZpZm96bDEifQ.etUi4OK4ozzaP_P8foZn_A"

colorscale = [
                      [0.0, "rgba(0, 255, 204, 0)"],
                      [0.2, "rgb(0, 255, 51)"],
                      [0.4, "rgb(204, 255, 0)"],
                      [0.6, "rgb(255, 204, 51)"],
                      [0.8, "rgb(255, 102, 51)"],
                      [1.0, "rgb(204,0,0)"],
                 ]

tickvalues = np.around(np.linspace(0, np.round(0.5, 0), 7), 3)
ticktext = [str(val) for val in tickvalues]

color_axis = dict(
            cmin=0,
            cmax=0.5,
            showscale=True,
            colorscale=colorscale,
            colorbar=dict(
                outlinecolor="black",
                outlinewidth=2,
                ticks="outside",
                tickfont=pt.font_dict,
                tickvals=tickvalues,
                ticktext=ticktext,
                title="[gal/hr]<br /> <br />",
                titlefont=pt.font_dict,
            )
)

def single_time_interval(emissions_data_dict, time_range,):

    z_data = emissions_data_dict[time_range]['data']
    lat_edges = emissions_data_dict[time_range]['lat']
    lon_edges = emissions_data_dict[time_range]['lon']
    color_axis['cmax'] = emissions_data_dict[time_range]['max_value']

    fig = go.Figure(go.Densitymapbox(
        lat=lat_edges,
        lon=lon_edges,
        z=z_data,
        # customdata=summed_array[0][2],
        # hovertemplate='%{customdata}' if sum else None,
        radius=plot_radius,
        hoverinfo='z',
        coloraxis="coloraxis"
        ))

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
        title={"text": "Fuel Consumption", "font": pt.font_dict, 'yanchor': 'middle', 'xanchor': 'center'},
        font=pt.font_dict,
        paper_bgcolor='rgb(249, 249, 249)',
        hovermode='closest',
        margin=go.layout.Margin(
            l=20,  # left margin
            r=0,  # right margin
            b=5,  # bottom margin
            t=0  # top margin
        ),
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
        coloraxis=color_axis
    )

    return fig
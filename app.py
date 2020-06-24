import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from index import app, APP_PATH
from pages import trajectory_page, pdf_page, pdf_same_sample_page
import dash_bootstrap_components as dbc
from styles import styles

sidebar = html.Div(
        [
            html.H2("Emissions \n Sanity \n Check", style={'font-family': styles.font['family']}),
            html.Hr(),
            dbc.Nav(
                [
                    dbc.NavLink("Trajectory Plot", href="/page-1", id="page-1-link"),
                    dbc.NavLink("Sample PDF Analysis", href="/page-2", id="page-2-link"),
                    dbc.NavLink("Multi-Sample PDF Analysis", href="/page-3", id="page-3-link"),
                ],
                vertical=True,
                pills=True,
                style=styles.NAV_TEXT_STYLE,
            ),
        ],
        style=styles.SIDEBAR_STYLE,
    )

html_base = html.Div(id='base_page', style=styles.CONTENT_STYLE)

#app.layout = html.Div([trajectory_page.html_base])

# -------------------------------------------------------------------------------------------------------
#                                  Setting the app layout and server
# -------------------------------------------------------------------------------------------------------
app.layout = html.Div([dcc.Location(id="url"), sidebar, html_base])
server = app.server
# -------------------------------------------------------------------------------------------------------
#
# -------------------------------------------------------------------------------------------------------
@app.callback(
    [dash.dependencies.Output(f"page-{i}-link", "active") for i in range(1, 4)],
    [dash.dependencies.Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/page-{i}" for i in range(1, 4)]


@app.callback(dash.dependencies.Output('base_page', 'children'),
              [dash.dependencies.Input("url", "pathname")])
def render_content(pathname):
    if pathname in ["/", "/page-1"]:
        return trajectory_page.html_base
    elif pathname == "/page-2":
        return pdf_page.html_base
    elif pathname == "/page-3":
        return pdf_same_sample_page.html_base
    #
    # elif pathname == "/page-3":
    #     return geh_analysis_html


if __name__ == "__main__":

    app.layout = html.Div([dcc.Location(id="url"), sidebar, html_base])
    server = app.server

    app.run_server(debug=False)
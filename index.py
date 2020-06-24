import dash_bootstrap_components as dbc
import dash
import pathlib

APP_PATH = str(pathlib.Path(__file__).parent.resolve())

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

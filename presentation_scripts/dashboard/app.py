"""Code to instantiate the web app. Import the app from this file into other
files rather than making a new instance."""

import dash
import dash_bootstrap_components as dbc

# Initialize app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.LITERA],
)
server = app.server
app.config.suppress_callback_exceptions = True

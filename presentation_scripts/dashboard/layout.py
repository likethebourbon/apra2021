"""Code for the web app's layout."""

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import numpy as np

from .navbar import Navbar
from .churn_glossary import churn_glossary
from .app import app


navbar = Navbar(app)

about_glamtk = dbc.Modal(
    [
        dbc.ModalHeader("About GLAMtk"),
        dbc.ModalBody(
            [
                dcc.Markdown(
                    """Georgetown Law Advancement Modeling Toolkit (GLAMtk)""",
                ),
                dcc.Markdown("""Version 0.1.1"""),
                dcc.Markdown("""Created by Evan Williams, ew648@georgetown.edu"""),
            ],
            style={"padding": "1em"},
        ),
        dbc.ModalFooter(dbc.Button("Close", id="close_about_glamtk", className="ml-auto")),
    ],
    id="about_glamtk",
    scrollable=True,
)


title = html.H3(
    "Donor Churn Dashboard",
    style={"textAlign": "center", "margin-top": "25px", "margin-bottom": "10px"},
)

controls = (
    html.Div(
        [
            html.P(
                "Select Fiscal Year:",
                style={
                    "font-family": "Open Sans, HelveticaNeue, Helvetica Neue, Helvetica, Arial, sans-serif"
                },
            ),
            dcc.Dropdown(
                id="year_select",
                options=[
                    {"label": year, "value": year}
                    for year in list(reversed(list(range(2014, 2020))))
                ],
                value=2018,
                clearable=False,
            ),
            html.P(
                "Set the Decision Threshold:",
                style={
                    "margin-top": 20,
                    "font-family": "Open Sans, HelveticaNeue, Helvetica Neue, Helvetica, Arial, sans-serif",
                },
            ),
            dcc.Slider(
                id="threshold_slider",
                min=0,
                max=1,
                step=0.01,
                value=0.37,
                marks={num: f"{num:.2f}" for num in np.linspace(0, 1, 6)},
                tooltip={"always_visible": False},
                className="fullsize",
            ),
            html.P(
                "Filter by Giving Levels:",
                style={
                    "margin-top": 20,
                    "font-family": "Open Sans, HelveticaNeue, Helvetica Neue, Helvetica, Arial, sans-serif",
                },
            ),
            dcc.Input(
                id="min_gift",
                type="number",
                debounce=True,
                placeholder="Minimum Giving",
                style={"margin-bottom": 5, "width": "100%"},
            ),
            dcc.Input(
                id="max_gift",
                type="number",
                debounce=True,
                placeholder="Maximum Giving",
                style={"width": "100%"},
            ),
            html.P(
                "Show/Hide Model Error Graphs:",
                style={
                    "margin-top": 20,
                    "font-family": "Open Sans, HelveticaNeue, Helvetica Neue, Helvetica, Arial, sans-serif",
                },
            ),
            daq.ToggleSwitch(  # noqa pylint: disable=not-callable
                id="hide_graphs_switch",
                label=["Hide", "Show"],
                labelPosition=["left", "right"],
                style={"margin": "auto", "width": "70%"},
            ),
            html.P(
                "Export Filtered Results:",
                style={
                    "margin-top": 20,
                    "font-family": "Open Sans, HelveticaNeue, Helvetica Neue, Helvetica, Arial, sans-serif",
                },
            ),
            dcc.Input(
                id="export_filename",
                type="text",
                placeholder="Name for .csv file",
                style={"width": "100%"},
            ),
            html.A(
                dbc.Button(
                    "Export Results",
                    outline=True,
                    color="primary",
                    size="md",
                    id="export_button",
                    block=True,
                    style={"margin-top": 5},
                ),
                id="export_link",
                className="text-decoration-none",
            ),
        ],
    ),
)


below_card = dbc.Card(
    [
        dbc.CardHeader("Donors Below Threshold"),
        dbc.CardBody(
            [html.H4(id="donors_below", className="card-title", style={"textAlign": "center"})]
        ),
    ],
    style={"margin-right": 5, "border": "1px solid rgba(0,0,0,0.125)"},
)

above_card = dbc.Card(
    [
        dbc.CardHeader("Donors Above Threshold"),
        dbc.CardBody(
            [html.H4(id="donors_above", className="card-title", style={"textAlign": "center"})]
        ),
    ],
    style={"border": "1px solid rgba(0,0,0,0.125)"},
)

selected_count_card = dbc.Card(
    [
        dbc.CardHeader("Donors to be Exported"),
        dbc.CardBody(
            [
                html.H4(
                    id="selected_donors_count",
                    className="card-title",
                    style={"textAlign": "center"},
                )
            ]
        ),
    ],
    style={"border": "1px solid rgba(0,0,0,0.125)"},
)


hist_layout = dbc.Container(
    [dcc.Graph(id="hist_fig", config={"displayModeBar": False})],
    fluid=True,
    style={"padding": "0 0 0 0"},
)


row_1 = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [dbc.Card([dbc.CardHeader("Controls"), dbc.CardBody(controls)])],
                    width=3,
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col([below_card], width=3),
                                dbc.Col([above_card], width=3),
                                dbc.Col([selected_count_card], width=3),
                            ],
                            style={"margin-bottom": "15px"},
                        ),
                        hist_layout,
                    ],
                    width=9,
                ),
            ],
        ),
    ],
)


cm_fig_col = dbc.Col(
    [
        html.Div(
            [dcc.Graph(id="cm_fig", config={"displayModeBar": False})],
            id="cm_fig_container",
        )
    ],
    className="col-md-6",
)

cpe_fig_col = dbc.Col(
    [
        html.Div(
            [dcc.Graph(id="cpe_fig", config={"displayModeBar": False})],
            id="cpe_fig_container",
        )
    ],
    className="col-md-6",
)

row_2 = html.Div(
    [dbc.Row([cm_fig_col, cpe_fig_col], style={"margin-top": "30px"})],
    id="prediction_error_row",
)


row_3 = dbc.Row(
    [
        dbc.Col(
            [
                html.Div(
                    [
                        dbc.Col(
                            [
                                html.H6(
                                    "Scatter Map: Donors with Predicted Churn Probability Above Threshold",
                                    style={"textAlign": "center"},
                                )
                            ]
                        ),
                        dcc.Graph(
                            id="scatter_map_fig",
                            config={
                                "modeBarButtonsToRemove": ["toImage", "toggleHover"],
                                "displaylogo": False,
                            },
                        ),
                    ],
                    id="scatter_map_fig_container",
                ),
            ],
            width=12,
        )
    ],
    style={"margin-top": "30px"},
)

# Create app layout
layout = html.Div(
    [
        churn_glossary,
        about_glamtk,
        dcc.Store(id="results_data"),
        dcc.Store(id="selected_results_data"),
        dcc.Store(id="cm_data"),
        navbar,
        dbc.Col([title, row_1, row_2, row_3]),
    ]
)

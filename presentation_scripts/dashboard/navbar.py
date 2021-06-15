"""Code for the web app's navigation bar."""

import dash_bootstrap_components as dbc
import dash_html_components as html


def Navbar(app):
    return dbc.Navbar(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.Img(
                            src=app.get_asset_url("georgetown_law_logo.png"),
                            height=50,
                        )
                    ),
                    dbc.Col(
                        dbc.NavbarBrand(
                            "GLAMtk",
                            style={
                                "font-size": "40px",
                                "font-weight": "bold",
                                "margin-left": "10px",
                                "color": "#00B5E2",
                                "line-height": "1",
                            },
                        ),
                        className="ml-2",
                    ),
                ],
                no_gutters=True,
            ),
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("Donor Churn", active=True, href="#")),
                    dbc.DropdownMenu(
                        [
                            dbc.DropdownMenuItem("Documentation", header=True),
                            dbc.DropdownMenuItem("About GLAMtk", id="about_glamtk_link"),
                            dbc.DropdownMenuItem("Getting Started", href="#", disabled=True),
                            dbc.DropdownMenuItem("User Guide", href="#", disabled=True),
                            dbc.DropdownMenuItem(divider=True),
                            dbc.DropdownMenuItem("Glossaries", header=True),
                            dbc.DropdownMenuItem(
                                "Donor Churn Glossary",
                                id="glossary_churn_link",
                            ),
                            dbc.DropdownMenuItem(divider=True),
                            dbc.DropdownMenuItem("About Machine Learning Models", header=True),
                            dbc.DropdownMenuItem(
                                "Explore Model Performance Metrics",
                                href="#",
                                disabled=True,
                            ),
                        ],
                        nav=True,
                        in_navbar=True,
                        label="Help",
                        right=True,
                    ),
                ],
                className="ml-auto",
                pills=True,
            ),
        ],
        color="active",
    )

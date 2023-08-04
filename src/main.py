# External dependencies
from dash import Dash, html, dcc, dash_table, Output, Input, State, callback, html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import flask

# Internal dependencies
from static.StaticData import StaticData
from static.Constants import METALS, QUALITY
from external_input.MarketData import MarketData
from pricing.OrderBook import OrderBook

server = flask.Flask(__name__)
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], server=server)

sidebar = html.Div(
    [
        dbc.Row(
            [html.H5("Settings", style={"margin-top": "12px", "margin-left": "24px"})],
            style={"height": "5vh"},
            className="bg-primary text-white font-italic",
        ),
        dbc.Row(
            [
                html.Div(
                    [
                        html.B(
                            "Copper fraction",
                            className="font-weight-bold",
                        ),
                        dcc.Slider(
                            min=0,
                            max=1,
                            step=0.01,
                            value=0.66,
                            id="copper-fraction-slider",
                            tooltip={"placement": "bottom", "always_visible": True},
                            marks=None,
                        ),
                        html.B(
                            "Zinc fraction",
                            className="font-weight-bold",
                        ),
                        dcc.Slider(
                            min=0,
                            max=1,
                            step=0.01,
                            value=0.34,
                            id="zinc-fraction-slider",
                            tooltip={"placement": "bottom", "always_visible": True},
                            marks=None,
                        ),
                        html.Hr(),
                        html.B(
                            "Labour factors",
                            className="font-weight-bold",
                        ),
                        dash_table.DataTable(
                            id="labour-factor-table",
                            columns=[
                                {
                                    "name": "Rod length (cm)",
                                    "id": "rod-length",
                                    "type": "numeric",
                                    "format": {"specifier": ".1f"},
                                    "on_change": {
                                        "action": "coerce",
                                        "failure": "default",
                                    },
                                },
                                {
                                    "name": "Labour factor",
                                    "id": "labour-factor",
                                    "type": "numeric",
                                    "format": {"specifier": ".2f"},
                                    "on_change": {"failure": "default"},
                                    "validation": {"default": ""},
                                },
                            ],
                            data=[
                                {"rod-length": x, "labour-factor": y}
                                for x, y in zip(
                                    [0, 75.0, 100, 125], [1.05, 1.1, 1.15, 1.25]
                                )
                            ],
                            editable=True,
                            row_deletable=True,
                            fill_width=False,
                        ),
                        # Add row button
                        html.Button("+", id="labour-factor-rows-button", n_clicks=0),
                        html.Hr(),
                        html.B(
                            "Market prices (USD / kg)",
                            className="font-weight-bold",
                        ),
                        html.Hr(),
                        html.P(
                            "Copper price:",
                        ),
                        html.Div(
                            children=dcc.Input(
                                id="copper-price",
                                type="number",
                                value=8.22,
                                placeholder=8.22,
                            ),
                        ),
                        html.Br(),
                        html.Br(),
                        dash_table.DataTable(
                            id="zinc-price-table",
                            columns=[
                                {
                                    "name": "Zinc quality",
                                    "id": "zinc-quality",
                                    "type": "text",
                                    "editable": False,
                                },
                                {
                                    "name": "Price",
                                    "id": "zinc-prices",
                                    "type": "numeric",
                                    "format": {"specifier": ".2f"},
                                    "editable": True,
                                },
                            ],
                            data=[
                                {"zinc-quality": x, "zinc-prices": p}
                                for x, p in zip(
                                    QUALITY.get_all_qualities(), [7.5, 4.9, 3.5, 3.05]
                                )
                            ],
                            row_deletable=False,
                            fill_width=False,
                        ),
                    ]
                )
            ],
            style={"height": "110vh", "margin": "8px"},
        ),
    ]
)

# Relative price shock maximum
MAX_PRICE_SHOCK = 0.25


content = html.Div(
    [
        dbc.Row(
            [
                html.Div(
                    [
                        html.H2("Brass rod pricing"),
                        html.P(
                            "Brass is an alloy of copper and zinc, in proportions which can be varied to achieve different properties. Clients place orders specifying the overall weight, the length of the rods and the quality of the zinc to be used."
                        ),
                        html.P(
                            "All these parameters affect the price of the order. The base price of the rods is computed as the price of the raw materials multiplied by a labour factor, which increases with the rod length, as making longer rods is harder and more time consuming."
                        ),
                        html.P(
                            "The rods are sold at market prices that fluctuate throughout the day and can be set in the table. For any client order, this code can calculate the total order price as well as the sensitivity to price movements in copper and zinc through algorithmic differentiation."
                        ),
                        html.Hr(),
                    ]
                ),
                dbc.Col(
                    [
                        html.B(
                            "Order input",
                            className="font-weight-bold",
                        ),
                        dash_table.DataTable(
                            id="order-parameters-table",
                            columns=[
                                {
                                    "name": "Client",
                                    "id": "order-client",
                                    "type": "text",
                                    "editable": True,
                                },
                                {
                                    "name": "Weight (kg)",
                                    "id": "order-weight",
                                    "type": "numeric",
                                    "format": {"specifier": ".1f"},
                                    "editable": True,
                                },
                                {
                                    "name": "Rod length (cm)",
                                    "id": "rod-length",
                                    "type": "numeric",
                                    "format": {"specifier": ".1f"},
                                    "editable": True,
                                },
                                {
                                    "name": "Zinc quality",
                                    "id": "input-zinc-quality",
                                    "type": "text",
                                    "presentation": "dropdown",
                                    "editable": True,
                                },
                            ],
                            dropdown={
                                "input-zinc-quality": {
                                    "options": [
                                        {"label": i, "value": i}
                                        for i in QUALITY.get_all_qualities()
                                    ]
                                },
                            },
                            data=[
                                {
                                    "order-client": "Quincy",
                                    "order-weight": 2340,
                                    "rod-length": 108,
                                    "input-zinc-quality": "A",
                                },
                                {},
                            ],
                            editable=True,
                            row_deletable=True,
                            fill_width=False,
                        ),
                        # Add row button
                        html.Button("+", id="editing-clients-button", n_clicks=0),
                        html.Br(),
                        html.Br(),
                        # Run order price calculation
                        html.Button(
                            "Calculate prices",
                            id="run-price-calculation-button",
                            n_clicks=0,
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        html.B(
                            "Client order prices",
                            className="font-weight-bold",
                        ),
                        dash_table.DataTable(
                            id="client-order-prices",
                            columns=[
                                {
                                    "name": " ",
                                    "id": "output-row-idx",
                                    "type": "numeric",
                                },
                                {
                                    "name": "Client",
                                    "id": "output-client",
                                    "type": "text",
                                },
                                {
                                    "name": "Price (USD)",
                                    "id": "output-price",
                                    "type": "numeric",
                                    "format": {"specifier": ".2f"},
                                },
                            ],
                            data=[],
                            fill_width=False,
                        ),
                    ]
                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(width=1),
                dbc.Col(
                    [
                        html.Br(),
                        html.Br(),
                        dcc.RangeSlider(
                            id="copper-shock-slider",
                            min=-25,
                            max=25,
                            step=0.01,
                            value=[-10, 10],
                            allowCross=False,
                            tooltip={"placement": "left", "always_visible": True},
                            marks=None,
                            vertical=True,
                        ),
                    ],
                    width=1,
                    style={"display": "none"},
                    id="price-shock-slider-vertical",
                ),
                dbc.Col(
                    [
                        dcc.Graph(id="price-shock-figure"),
                        html.Div(
                            [
                                dcc.RangeSlider(
                                    id="zinc-shock-slider",
                                    min=-25,
                                    max=25,
                                    step=0.01,
                                    value=[-10, 10],
                                    allowCross=False,
                                    tooltip={
                                        "placement": "bottom",
                                        "always_visible": True,
                                    },
                                    marks=None,
                                ),
                            ]
                        ),
                    ],
                    width=8,
                    style={"display": "none"},
                    id="price-shock-fig-col",
                ),
            ],
        ),
    ]
)

app.layout = dbc.Container(
    [
        dbc.Row(
            [dbc.Col(sidebar, width=3, className="bg-light"), dbc.Col(content, width=9)]
        ),
    ],
    fluid=True,
)


def extract_order_parameters(data_table):
    return {
        k: [
            order["order-client"],
            order["order-weight"],
            order["rod-length"],
            order["input-zinc-quality"],
        ]
        for k, order in enumerate(data_table)
        if len(order) > 0
    }


def extract_market_and_static_data(
    copper_fraction: float, labour_factors, copper_price: float, zinc_prices
):
    static_data = StaticData()
    market_data = MarketData()

    static_data.set_copper_fraction(copper_fraction)
    rod_key, factor_key = "rod-length", "labour-factor"
    factors = [
        (row[rod_key], row[factor_key])
        for row in labour_factors
        if (rod_key in row and factor_key in row)
    ]
    static_data.set_labour_factors(factors)

    market_data.set_price(copper_price, METALS.COPPER, QUALITY.DEFAULT)

    for row in zinc_prices:
        quality = QUALITY(row["zinc-quality"])
        price = row["zinc-prices"]
        market_data.set_price(price, METALS.ZINC, quality)

    return static_data, market_data


# Display client prices
@callback(
    Output("client-order-prices", "data"),
    Input("run-price-calculation-button", "n_clicks"),
    State("order-parameters-table", "data"),
    State("copper-fraction-slider", "value"),
    State("labour-factor-table", "data"),
    State("copper-price", "value"),
    State("zinc-price-table", "data"),
)
def compute_client_prices(
    n_clicks,
    order_data,
    copper_fraction,
    labour_factors,
    copper_price,
    zinc_prices,
):
    if n_clicks == 0:
        return [
            {"output-row-idx": "", "output-client": " ", "output-price": "-"},
            {"output-row-idx": "", "output-client": "TOTAL", "output-price": "-"},
        ]

    static_data, market_data = extract_market_and_static_data(
        copper_fraction=copper_fraction,
        labour_factors=labour_factors,
        copper_price=copper_price,
        zinc_prices=zinc_prices,
    )
    orderbook = OrderBook(static_data=static_data)

    order_dict = extract_order_parameters(order_data)
    orderbook.add_orders(order_dict, market_data=market_data)
    indices, names, prices = orderbook.get_order_prices()

    data = [
        {"output-row-idx": idx, "output-client": name, "output-price": price}
        for idx, name, price in zip(indices, names, prices)
    ]

    return data


# Display price sensitivity
@callback(
    Output("price-shock-figure", "figure"),
    Output("price-shock-fig-col", "style"),
    Output("price-shock-slider-vertical", "style"),
    [
        Input("run-price-calculation-button", "n_clicks"),
        Input("zinc-shock-slider", "value"),
        Input("copper-shock-slider", "value"),
    ],
    [
        State("order-parameters-table", "data"),
        State("copper-fraction-slider", "value"),
        State("labour-factor-table", "data"),
        State("copper-price", "value"),
        State("zinc-price-table", "data"),
    ],
)
def compute_price_shock(
    n_clicks,
    zinc_shock,
    copper_shock,
    order_data,
    copper_fraction,
    labour_factors,
    copper_price,
    zinc_prices,
):
    static_data, market_data = extract_market_and_static_data(
        copper_fraction=copper_fraction,
        labour_factors=labour_factors,
        copper_price=copper_price,
        zinc_prices=zinc_prices,
    )

    orderbook = OrderBook(static_data=static_data)
    order_dict = extract_order_parameters(order_data)

    orderbook.add_orders(order_dict, market_data=market_data)

    # Plot price shock effects
    (
        zinc_shock_ladder,
        copper_shock_ladder,
        price_change,
    ) = orderbook.get_price_shock_effects(zinc_shock, copper_shock, 250)
    fig = go.Figure(
        data=go.Contour(
            x=copper_shock_ladder,
            y=zinc_shock_ladder,
            z=price_change,
            colorbar=dict(
                title="Price change (USD)",
            ),
            # layout=dict(title={"text": "test"}),
        ),
    )

    fig.update_yaxes(
        title_text="Zinc price change (%)", title_font={"size": 20}, title_standoff=15
    )
    fig.update_xaxes(
        title_text="Copper price change (%)", title_font={"size": 20}, title_standoff=15
    )

    fig.update_layout(
        title_text="Client order price sensitivity (USD)",
        title_font={"size": 20},
        title_x=0.45,
    )
    display_style = {"display": "block"} if n_clicks > 0 else {"display": "none"}

    return fig, display_style, display_style


for table, button in zip(
    ["labour-factor-table", "order-parameters-table"],
    [
        "labour-factor-rows-button",
        "editing-clients-button",
    ],
):
    # Add row to input table
    @callback(
        Output(table, "data"),
        Input(button, "n_clicks"),
        State(table, "data"),
        State(table, "columns"),
    )
    def add_row(n_clicks, rows, columns):
        if n_clicks > 0:
            rows.append({c["id"]: "" for c in columns})
        return rows


# Automatically normalise alloy composition
for first_slider, second_slider in zip(
    ["copper-fraction-slider", "zinc-fraction-slider"],
    ["zinc-fraction-slider", "copper-fraction-slider"],
):

    @callback(
        Output(first_slider, "value"),
        Input(second_slider, "value"),
    )
    def normalise_slider(fraction):
        return 1.0 - fraction


if __name__ == "__main__":
    app.run_server(debug=True)

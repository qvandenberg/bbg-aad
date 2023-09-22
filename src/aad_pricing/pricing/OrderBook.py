# External dependencies
import warnings
import itertools
import numpy as np

# Internal dependencies
from aad_pricing.external_input.ClientOrder import ClientOrder
from aad_pricing.static.StaticData import StaticData
from aad_pricing.external_input.MarketData import MarketData
from aad_pricing.static.Constants import METALS


class OrderBook(object):
    """
    Class OrderBook is a container class for client orders.

    Client order input data is collected here. This class provides the price calculations
    and price sensitivities with respect to raw material price shocks.
    """

    def __init__(self, static_data: StaticData) -> None:
        self._static_data = static_data
        self._client_orders = {}

    def add_orders(self, orders: dict, market_data: MarketData) -> None:
        if any(key in self._client_orders for key, val in orders.items()):
            warnings.warn("Overwriting client order with the same id")
        client_order_objs = {
            k: ClientOrder(
                order[0], order[1], order[2], order[3], self._static_data, market_data
            )
            for k, order in orders.items()
        }

        self._client_orders.update(client_order_objs)

    def get_order_prices(self) -> dict:
        total_price = 0.0

        indices, names, prices = [], [], []
        for idx, order in self._client_orders.items():
            indices.append(idx + 1)
            names.append(order.get_name())
            price = order.get_price()
            prices.append(price)
            total_price += price

        indices.append("")
        names.append("TOTAL")
        prices.append(total_price)

        return indices, names, prices

    # Pass shock list as [low, high] to specify the range of price shocks
    def get_price_shock_effects(
        self, zinc_shock_percentages: list, copper_shock_percentages: list, n_steps=100
    ) -> dict:
        zinc_shock_ladder = (
            np.linspace(
                zinc_shock_percentages[0] / 100.0,
                zinc_shock_percentages[1] / 100.0,
                n_steps,
            )
        ).tolist()
        copper_shock_ladder = (
            np.linspace(
                copper_shock_percentages[0] / 100.0,
                copper_shock_percentages[1] / 100.0,
                n_steps,
            )
        ).tolist()

        shock_pairs = list(itertools.product(zinc_shock_ladder, copper_shock_ladder))
        price_change = np.zeros_like(shock_pairs)

        for k, order in self._client_orders.items():
            sensitivities = (
                order.get_sensitivity(METALS.ZINC),
                order.get_sensitivity(METALS.COPPER),
            )
            sensitivity_vector = np.full_like(shock_pairs, sensitivities)
            price_change += np.multiply(sensitivity_vector, shock_pairs)

        # Convert price differences to percentages because Dash doesn't support percentage formatting on RangeSlider
        diff_zn_price, diff_cu_price = [pair[0] * 100.0 for pair in shock_pairs], [
            pair[1] * 100.0 for pair in shock_pairs
        ]
        # Sum up price difference in the zinc and copper
        total_price_change = np.add.reduce(price_change, 1)

        return diff_zn_price, diff_cu_price, total_price_change

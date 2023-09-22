# Internal dependencies
from aad_pricing.static.StaticData import StaticData
from aad_pricing.static.Constants import METALS, QUALITY
from aad_pricing.external_input.MarketData import MarketData
from aad_pricing.pricing.DirectedAcyclicGraph import DirectedAcyclicGraph


class ClientOrder(object):
    """
    Class ClientOrder is an object containing a single entry for a client order containing:
     * Client name (string)
     * Weight in kg (float)
     * Rod length in cm (float)
     * Zinc quality (enumeration of AA, A, B, C)

     Together with static data and market data, these properties are fed into the directed acyclic graph
     to compute the order price and sensitivities.

     Static data and market data are tied to each object instance, allowing different market prices per client order.
    """

    def __init__(
        self,
        client_name: str,
        weight: float,
        rod_length: float,
        zinc_quality: str,
        static_data: StaticData,
        market_data: MarketData,
    ) -> None:
        # Unique client id
        self._client_name = client_name
        #  Directed acyclic graph to compute order price and sensitivity
        self._graph = self._compose_graph(
            static_data, market_data, weight, zinc_quality, rod_length
        )

    def _compose_graph(
        self,
        static_data: StaticData,
        market_data: MarketData,
        weight: float,
        zinc_quality: str,
        rod_length: float,
    ) -> None:
        copper_fraction = static_data.get_alloy_mass_fraction(METALS.COPPER)
        copper_price = market_data.get_price(METALS.COPPER)
        quality = QUALITY(zinc_quality)
        zinc_price = market_data.get_price(METALS.ZINC, quality=quality)
        labour_factor = static_data.get_labour_factor(rod_length)

        return DirectedAcyclicGraph(
            weight,
            copper_fraction,
            copper_price,
            zinc_price,
            labour_factor,
        )

    def get_name(self) -> str:
        return self._client_name

    def get_price(self) -> float:
        return self._graph.get_price() if self._graph is not None else 0.0

    def get_sensitivity(self, metal: METALS) -> float:
        return (
            self._graph.get_price_sensitivity(metal) if self._graph is not None else 0.0
        )

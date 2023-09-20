# External dependencies
from collections import defaultdict

# Internal dependencies
from aad_pricing.pricing.ComputationalNode import ComputationalNode
from aad_pricing.static.Constants import METALS


class DirectedAcyclicGraph:
    """
    Class DirectedAcyclicGraph executes the price calculation done the nodes. Each node contains a single assignment code, this graph combines them.
    We calculate gradients for sensitivity analysis in the same pass as the price value.
    """

    def __init__(
        self,
        total_weight: float,
        copper_fraction: float,
        copper_price: float,
        zinc_price: float,
        labour_factor: float,
    ):
        self._total_weight = ComputationalNode(total_weight)
        self._copper_split = ComputationalNode(copper_fraction)
        self._zinc_split = ComputationalNode(1.0) - self._copper_split
        self._copper_price = ComputationalNode(copper_price)
        self._zinc_price = ComputationalNode(zinc_price)
        self._labour_factor = ComputationalNode(labour_factor)
        self._graph = None
        self._build_graph()

    def _build_graph(self) -> ComputationalNode:
        self._graph = (
            (
                self._copper_price * self._copper_split
                + self._zinc_price * self._zinc_split
            )
            * self._total_weight
            * self._labour_factor
        )
        self._graph.set_gradient(1.0)

    def get_price(self) -> float:
        return self._graph.get_value()

    def get_price_sensitivity(self, metal: METALS) -> float:
        if metal == METALS.COPPER:
            return self._copper_price.get_gradient() * self._copper_price.get_value()
        elif metal == METALS.ZINC:
            return self._zinc_price.get_gradient() * self._zinc_price.get_value()
        else:
            raise NotImplementedError("Unknown metal requested.")

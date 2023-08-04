# External dependencies
from collections import defaultdict

# Internal dependencies
from pricing.ComputationalNode import ComputationalNode
from static.Constants import METALS


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
        self._zinc_split = ComputationalNode(1.0 - copper_fraction)
        self._copper_price = ComputationalNode(copper_price)
        self._zinc_price = ComputationalNode(zinc_price)
        self._labour_factor = ComputationalNode(labour_factor)
        self._percentage_sensitivities = defaultdict(float)

    def build_graph(self) -> ComputationalNode:
        return (
            (
                self._copper_price * self._copper_split
                + self._zinc_price * self._zinc_split
            )
            * self._total_weight
            * self._labour_factor
        )

    def reset_gradients(self) -> None:
        for attr, value in self.__dict__.items():
            if isinstance(value, ComputationalNode):
                value.set_gradient(None)

    def set_gradients_to_zero(self) -> None:
        for attr, value in self.__dict__.items():
            if isinstance(value, ComputationalNode):
                value.set_gradient(0.0)

    def get_price(self) -> float:
        graph = self.build_graph()
        return graph.get_value()

    def compute_gradients(self):
        self._percentage_sensitivities.clear()
        graph = self.build_graph()
        graph.set_gradient(1.0)
        self._percentage_sensitivities[METALS.COPPER] = (
            self._copper_price.get_gradient() * self._copper_price.get_value()
        )
        self._percentage_sensitivities[METALS.ZINC] = (
            self._zinc_price.get_gradient() * self._zinc_price.get_value()
        )

    def get_price_sensitivity(self, metal: METALS) -> float:
        if metal not in self._percentage_sensitivities:
            self.compute_gradients()
        return self._percentage_sensitivities.get(metal, 0.0)

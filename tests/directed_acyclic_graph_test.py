import pytest
import rootpath

rootpath.append()

from src.pricing.DirectedAcyclicGraph import DirectedAcyclicGraph
from src.static.Constants import METALS
import numpy as np


@pytest.mark.parametrize(
    "weight,copper_fraction,copper_price, zinc_price, labour_factor",
    [
        (1.0, 1.0, 8.22, 5.0, 1.0),
        (2.0, 0.8, 10.54, 5.0, 1.2),
        (50.0, 0.7, 11.78, 5.0, 1.4),
        (100.0, 0.3, 12.025, 5.0, 1.1),
        (950.0, 0.66, 20.4, 5.0, 1.9),
    ],
)
def test_copper_price_sensitivity(
    weight, copper_fraction, copper_price, zinc_price, labour_factor
):
    graph = DirectedAcyclicGraph(
        weight, copper_fraction, copper_price, zinc_price, labour_factor
    )

    copper_price_sensitivity = graph.get_price_sensitivity(METALS.COPPER)
    theoretical_sensitivity = weight * labour_factor * copper_fraction * copper_price
    assert np.isclose(copper_price_sensitivity, theoretical_sensitivity)


@pytest.mark.parametrize(
    "weight,copper_fraction,copper_price, zinc_price, labour_factor",
    [
        (1.0, 0.0, 1.0, 51.5, 1.0),
        (2.0, 0.0, 1.0, 12.7, 1.2),
        (50.0, 0.0, 1.0, 5.3, 1.4),
        (100.0, 0.0, 1.0, 8.32, 1.1),
        (950.0, 0.0, 1.0, 15.0, 1.9),
    ],
)
def test_zinc_price_sensitivity(
    weight, copper_fraction, copper_price, zinc_price, labour_factor
):
    graph = DirectedAcyclicGraph(
        weight, copper_fraction, copper_price, zinc_price, labour_factor
    )

    zinc_price_sensitivity = graph.get_price_sensitivity(METALS.ZINC)
    theoretical_sensitivity = (
        weight * labour_factor * (1.0 - copper_fraction) * zinc_price
    )
    assert np.isclose(zinc_price_sensitivity, theoretical_sensitivity)

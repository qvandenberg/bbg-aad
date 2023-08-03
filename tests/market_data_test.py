import pytest
import rootpath

rootpath.append()
from src.external_input.MarketData import MarketData
from src.static.Constants import METALS, QUALITY
import numpy as np


@pytest.mark.parametrize(
    "price,metal,quality",
    [
        (1.5, METALS.COPPER, QUALITY.DEFAULT),
        (5.5, METALS.ZINC, QUALITY.AA),
        (2.5, METALS.ZINC, QUALITY.C),
    ],
)
def test_set_and_get_price_success(price, metal, quality):
    market_data = MarketData()
    market_data.set_price(price, metal, quality)
    retrieved_price = market_data.get_price(metal, quality)

    assert np.isclose(price, retrieved_price)


@pytest.mark.parametrize(
    "price,metal,quality",
    [
        (1.5, "Gold", QUALITY.DEFAULT),
    ],
)
def test_set_unknown_metal_failure(price, metal, quality):
    market_data = MarketData()

    with pytest.raises(
        NotImplementedError,
    ):
        market_data.set_price(price, metal, quality)


@pytest.mark.parametrize(
    "price,metal,quality",
    [
        (-2.5, METALS.COPPER, QUALITY.DEFAULT),
    ],
)
def test_negative_price_failure(price, metal, quality):
    market_data = MarketData()

    with pytest.raises(ValueError, match=r"Price must be a positive numeric value"):
        market_data.set_price(price, metal, quality)

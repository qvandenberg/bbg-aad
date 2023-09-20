# External dependencies
from typing import Any
import numbers

# Internal dependencies
from aad_pricing.static.Constants import METALS, QUALITY


class MarketData(object):
    def __init__(self) -> None:
        # Market prices: {METALS (enum): {QUALITY (enum): price (float)} }
        self._prices = {}

    def market_data_validator(setter_func):
        def function_wrapper(self, price: float, metal: str, quality: str):
            if not METALS.from_string(metal) in [x.value for x in METALS]:
                raise KeyError("Metal is not recognised")
            if not isinstance(price, numbers.Number) or price <= 0.0:
                raise ValueError("Price must be a positive numeric value")
            if QUALITY(quality) is None:
                raise ValueError("No metal quality indicated")

            return setter_func(self, price, metal, quality)

        return function_wrapper

    @market_data_validator
    def set_price(self, price: float, metal: METALS, quality: QUALITY) -> None:
        if metal not in self._prices:
            self._prices.setdefault(metal, dict())

        self._prices[metal][quality] = price

    def get_price(self, metal: METALS, quality: QUALITY = QUALITY.DEFAULT) -> float:
        return self._prices.get(metal, {}).get(quality, 0.0)

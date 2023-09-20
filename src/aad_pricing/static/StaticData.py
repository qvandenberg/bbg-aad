# External dependencies
from typing import Tuple, List
from functools import reduce
import numpy as np
import warnings
import bisect

# Internal dependencies
from aad_pricing.static.Constants import METALS


def is_sorted(iterable):
    # We can't simply use iterable == sorted(iterable) when iterable contains floats
    previous_or_nan = lambda previous, x: x if previous < x else np.NaN
    return not np.isnan(reduce(previous_or_nan, iterable))


class StaticData(object):
    # Alloy composition by weight fractions
    _alloy_composition = {}
    # Labour factor to account for production effort of rod length. Data structure: list( (max_length, labour_factor) ... )
    _labour_factors = []

    def alloy_validator(setter_func):
        def function_wrapper(self, copper_fraction: float):
            if not 0.0 <= copper_fraction <= 1.0:
                raise ValueError("Copper fraction must be between 0 and 1")

            return setter_func(self, copper_fraction)

        return function_wrapper

    @alloy_validator
    def set_copper_fraction(self, copper_fraction: float) -> None:
        self._alloy_composition[METALS.COPPER] = copper_fraction
        self._alloy_composition[METALS.ZINC] = 1.0 - copper_fraction

    def get_alloy_mass_fraction(self, metal: METALS) -> float:
        return self._alloy_composition[metal]

    def labour_factor_validator(setter_func):
        def function_wrapper(self, labour_factors: List[Tuple[float, float]]):
            lengths, factors = zip(*labour_factors)

            if not is_sorted(lengths):
                raise ValueError("Lengths must be supplied in ascending order")
            if not is_sorted(factors):
                warnings.warn(
                    "Labour factors are expected to be monotonically increasing"
                )
            return setter_func(self, labour_factors)

        return function_wrapper

    @labour_factor_validator
    def set_labour_factors(self, labour_factors: List[Tuple[float, float]]) -> None:
        self._labour_factors = labour_factors

    def get_labour_factor(self, rod_length: float) -> float:
        factor_idx = (
            bisect.bisect_left([x[0] for x in self._labour_factors], rod_length) - 1
        )
        return self._labour_factors[factor_idx][1]

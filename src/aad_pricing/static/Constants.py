from enum import Enum, EnumMeta, auto
from typing import Any, List


class EnumWithMetaValue(EnumMeta):
    def __getattribute__(cls, __name: str) -> Any:
        value = super().__getattribute__(__name)
        if isinstance(value, cls):
            value = value.value
        return value


class METALS(Enum, metaclass=EnumWithMetaValue):
    COPPER = "Copper"
    ZINC = "Zinc"

    @staticmethod
    def from_string(name: str) -> Any:
        if name.lower() == METALS.COPPER.lower():
            return METALS.COPPER
        elif name.lower() == METALS.ZINC.lower():
            return METALS.ZINC
        else:
            raise NotImplementedError


class QUALITY(Enum):
    DEFAULT = auto()
    C = "C"
    B = "B"
    A = "A"
    AA = "AA"

    @classmethod
    def _missing_(cls, value: object) -> Any:
        return cls.DEFAULT

    @classmethod
    def get_all_qualities(cls) -> List:
        return ["AA", "A", "B", "C"]

from typing import Any


class ComputationalNode:
    """
    Class Node represents each step of the pricing calculation as a piece of single assignment code.
    It holds both the value and Jacobian (gradients)calculated directly from the pricing calculation,
    so we can provide a sensitivity analysis without computing finite differences etc.
    """

    def __init__(self, value):
        self._gradient_value = None
        self._value = value
        self._children_nodes = []

    def __mul__(self, other) -> Any:
        z = ComputationalNode(self._value * other._value)
        # Apply product rule: dz = x*dy + y*dx
        # weight = dz/ dself = other.value
        self._children_nodes.append((other._value, z))
        # weight = dz/ dother = self.value
        other._children_nodes.append((self._value, z))

        return z

    def __add__(self, other) -> Any:
        z = ComputationalNode(self._value + other._value)
        # dz = dx + dy
        # weight = dz/ dself = 1
        self._children_nodes.append((1.0, z))
        # weight = dz/ dother = 1
        other._children_nodes.append((1.0, z))

        return z

    def get_gradient(self) -> float:
        if self._gradient_value is None:
            self._gradient_value = sum(
                weight * val.get_gradient() for weight, val in self._children_nodes
            )
        return self._gradient_value

    def set_gradient(self, gradient: float) -> None:
        self._gradient_value = gradient

    def get_value(self) -> float:
        return self._value

from abc import ABC, abstractmethod
from typing import List
from server.components.abc_components import BikeComponent

class PricingStrategy(ABC):
    @abstractmethod
    def calculate(self, components: List[BikeComponent]) -> float:
        pass

class StandardPricingStrategy(PricingStrategy):
    
    def calculate(self, components: List[BikeComponent]) -> float:
        return sum(c.price for c in components)

class ComboPricingStrategy(PricingStrategy):
    def calculate(self, components: List[BikeComponent]) -> float:
        base_price = super().calculate(components)

        return base_price * 0.90
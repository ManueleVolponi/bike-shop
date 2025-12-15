from typing import List
from server.bike.models import Bike
from .price_strategy import PricingStrategy
from server.components.abc_components import BikeComponent

class PriceCalculator:
    def __init__(self, bike_instance: Bike, strategy: PricingStrategy):
        self.bike = bike_instance
        self.strategy = strategy

    def get_selected_components(self) -> List[BikeComponent]:
        components = []
        
        component_keys = ["frame_type", "frame_finish", "wheels", "rim_color", "chain"]
        
        for key in component_keys:
            component = getattr(self.bike, key, None)
            
            if component and isinstance(component, BikeComponent):
                components.append(component)
        
        return components

    def process_calculation(self) -> float:
        return self.strategy.calculate(self.get_selected_components())
        
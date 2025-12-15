from .models import Wheel
from server.components.abc_components import BikeComponent

class WheelFactory:
    @classmethod
    def create_component(cls, data: dict) -> BikeComponent:
        component_category = data.get("category")
        
        if component_category != "wheels":
            raise ValueError(f"Category {component_category} not handled by WheelFactory.")
        
        filtered_data = {k:v for k,v in data.items()}
        
        try:
            return Wheel(
                id=filtered_data['id'],
                category='wheels',
                name=filtered_data['name'],
                price=filtered_data['base_price']
            )
        except KeyError as e:
            raise ValueError(f"Missing required field {e} for {Wheel.__name__}")

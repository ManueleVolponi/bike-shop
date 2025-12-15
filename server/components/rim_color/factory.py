from .models import Rim
from server.components.abc_components import BikeComponent

class RimFactory:
    
    @classmethod
    def create_component(cls, data: dict) -> BikeComponent:
        component_category = data.get("category")
        
        if component_category != "rim_color":
            raise ValueError(f"Category {component_category} not handled by RimFactory.")
        
        filtered_data = {k:v for k,v in data.items()}
        
        try:
            return Rim(
                id=filtered_data['id'],
                category="rim_color",
                name=filtered_data['name'],
                price=filtered_data['base_price']
            )
        except KeyError as e:
            raise ValueError(f"Missing required field {e} for {Rim.__name__}")

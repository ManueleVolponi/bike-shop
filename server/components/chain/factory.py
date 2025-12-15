from .models import Chain
from server.components.abc_components import BikeComponent

class ChainFactory:
    
    @classmethod
    def create_component(cls, data: dict) -> BikeComponent:
        component_category = data.get("category")
        
        if component_category != "chain":
            raise ValueError(f"Category {component_category} not handled by ChainFactory.")
        
        filtered_data = {k:v for k,v in data.items()}
        
        try:
            return Chain(
                id=filtered_data['id'],
                category="chain",
                name=filtered_data['name'],
                price=filtered_data['base_price']
            )
        except KeyError as e:
            raise ValueError(f"Missing required field {e} for {Chain.__name__}")
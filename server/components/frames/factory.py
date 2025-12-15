from .models import FrameType, FrameFinish
from server.components.abc_components import BikeComponent
from typing import Type

class FrameFactory:
    
    _component_map: dict[str, Type[BikeComponent]] = {
        "frame_type": FrameType,
        "frame_finish": FrameFinish,
    }

    @classmethod
    def create_component(cls, data: dict) -> BikeComponent:
        component_category = data.get("category")
        
        if component_category not in cls._component_map:
            raise ValueError(f"Category '{component_category}' not handled by FrameFactory.")

        ComponentClass = cls._component_map[component_category]
        
        filtered_data = {k: v for k, v in data.items()}

        try:
            return ComponentClass(
                id=filtered_data['id'],
                category=filtered_data['category'],
                name=filtered_data['name'],
                price=filtered_data['base_price']
            )
        except KeyError as e:
            raise ValueError(f"Missing required field {e} for {ComponentClass.__name__}")
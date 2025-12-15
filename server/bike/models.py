from typing import List
from server.components.abc_components import BikeComponent
from dataclasses import dataclass, field

@dataclass
class Bike:
    frame_type: BikeComponent
    frame_finish: BikeComponent
    wheels: BikeComponent
    chain: BikeComponent
    rim_color: BikeComponent

    is_valid: bool = True
    price: float = 0.00 
    compatibility_errors: List[str] = field(default_factory=list)
        
    
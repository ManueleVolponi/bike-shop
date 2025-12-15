from server.components.abc_components import BikeComponent
from dataclasses import dataclass

@dataclass
class Wheel(BikeComponent):
    id:str
    name: str
    
    price: float
    category: str = "wheels"
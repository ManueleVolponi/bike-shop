from server.components.abc_components import BikeComponent
from dataclasses import dataclass

@dataclass
class Rim(BikeComponent):
    id:str
    name: str
    
    price: float
    category: str = "rim_color"
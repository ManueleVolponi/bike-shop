from server.components.abc_components import BikeComponent
from dataclasses import dataclass

@dataclass
class Chain(BikeComponent):
    id: str
    name: str
    
    price: float
    category: str = "chain"
from server.components.abc_components import BikeComponent
from dataclasses import dataclass

@dataclass
class FrameFinish(BikeComponent):
    id: str
    name: str
    
    price: float
    category: str= "frame_finish"

@dataclass
class FrameType(BikeComponent):
    id: str
    name: str
    
    price: float
    category: str= "frame_type"
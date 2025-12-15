from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class BikeComponent(ABC):
    id: str
    name: str
    
    category: str
    price: float = 0.00
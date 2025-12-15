from typing import Dict, List
from .catalogue_gateway import CatalogueGateway
from .pricing.price_calculator import PriceCalculator
from server.bike.models import Bike
from server.components.abc_components import BikeComponent
from .pricing.pricing_rule_applicator import PricingRuleApplicator

class BikeConfiguratorService:
    
    def __init__(self, catalogue_gateway: CatalogueGateway, price_calculator: PriceCalculator, pricing_rules_app: PricingRuleApplicator):
        self.catalogue = catalogue_gateway 
        self.price_calculator = price_calculator
        self.rule_applicator = pricing_rules_app

    async def create_bike_from_selection(self, selection_ids: Dict[str, str]) -> Bike:
        frame_type = await self.catalogue.get_component_by_id(selection_ids.get('frame_type'))
        frame_finish = await self.catalogue.get_component_by_id(selection_ids.get('frame_finish'))
        wheels = await self.catalogue.get_component_by_id(selection_ids.get('wheels'))
        chain = await self.catalogue.get_component_by_id(selection_ids.get('chain'))
        rim_color = await self.catalogue.get_component_by_id(selection_ids.get('rim_color'))
        
        if not all([frame_type, frame_finish, wheels, chain, rim_color]):
            raise ValueError("Incomplete selection or components not in the catalogue.")

        assembled_bike = Bike(frame_type=frame_type, frame_finish=frame_finish, wheels=wheels, chain=chain, rim_color=rim_color)
        
        component_objects: Dict[str, BikeComponent] = {
            "frame_type": frame_type,
            "frame_finish": frame_finish,
            "wheels": wheels,
            "chain": chain,
            "rim_color": rim_color
        }

        errors = await self.catalogue.check_compatibility_of_selection(component_objects)
        
        if errors:
            assembled_bike.is_valid = False
            assembled_bike.compatibility_errors = errors
            assembled_bike.price = 0.0 
            return assembled_bike

        self.price_calculator.set_bike_instance(bike_instance=assembled_bike)

        assembled_bike.price = self.rule_applicator.apply_rules(self.price_calculator.get_selected_components())
        
        return assembled_bike
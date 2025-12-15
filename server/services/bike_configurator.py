from typing import Dict, List
from .catalogue_gateway import CatalogueGateway
from .pricing.price_calculator import PriceCalculator
from .pricing.price_strategy import PricingStrategy
from server.bike.models import Bike
from server.components.abc_components import BikeComponent
from .pricing.pricing_rule_applicator import PricingRuleApplicator

class BikeConfiguratorService:
    
    def __init__(self, catalogue_gateway: CatalogueGateway, pricing_strategy: PricingStrategy):
        self.catalogue = catalogue_gateway 
        self.pricing_strategy = pricing_strategy

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

        calculator = PriceCalculator(bike_instance=assembled_bike, strategy=self.pricing_strategy)
        base_price = calculator.process_calculation()

        pricing_rules = await self.catalogue.get_pricing_rules()

        rule_applicator = PricingRuleApplicator(pricing_rules=pricing_rules)
        assembled_bike.price = rule_applicator.apply_rules(calculator.get_selected_components(), base_price)
        
        return assembled_bike
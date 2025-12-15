from typing import List, Dict
from server.components.abc_components import BikeComponent

class PricingRuleApplicator:
    def __init__(self, pricing_rules: List[Dict]):
        self.rules = pricing_rules

    def apply_rules(self, components: List[BikeComponent], current_price: float) -> float:
        final_prices = {c.category: c.price for c in components}
        components_by_category = {c.category: c for c in components}

        for rule in self.rules:
            is_match = True
            
            for selector_condition in rule.get("selector", []):
                category = selector_condition['category']
                required_id = selector_condition['id']
                
                selected_component = components_by_category.get(category)
                
                if not selected_component or selected_component.id != required_id:
                    is_match = False
                    break
            
            if is_match:
                effect = rule['effect']
                target_cat = effect.get('target_category')
                target_id = effect.get('target_id')
                
                current_target_comp = components_by_category.get(target_cat)
                
                if current_target_comp:
                    if not target_id or current_target_comp.id == target_id:
                        if effect['type'] == 'FIXED_PRICE':
                            final_prices[target_cat] = effect['value']
                    
                    
                                
        return sum(final_prices.values())
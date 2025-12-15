import json
from pathlib import Path
from typing import Dict, List, Optional, Set
from server.components.abc_components import BikeComponent
from collections import defaultdict

CUR_PATH = Path(__file__).resolve().parent
DATA_PATH = CUR_PATH.parent / "static_data"

class CatalogueGateway:
    
    def __init__(self):
        self.components_raw = self._load_json("components.json")
        self.rules_raw = self._load_json("compatibility_rules.json")
        self.pricing_rules = self._load_json("pricing_rules.json")
        self.components_by_category: Dict[str, List[BikeComponent]] = {}
        self.components_by_id = self._process_components()
        
    def _load_json(self, filename: str) -> List[Dict]:
        file_path = DATA_PATH / filename
        if not file_path.exists():
            print(f"ERROR: file not found in {file_path}")
            return []
        with open(file_path, 'r') as f:
            return json.load(f)

    def _process_components(self) -> Dict[str, BikeComponent]:
        by_id = {}
        for item in self.components_raw:
            try:
                model = BikeComponent(
                    id=item["id"],
                    price=item["price"],
                    category=item["category"],
                    name=item["name"],
                    **{k: v for k, v in item.items() if k not in ["id", "price", "category", "name"]}
                )
                by_id[item["id"]] = model
                
                category = item["category"]
                
                if category not in self.components_by_category:
                    self.components_by_category[category] = []
                self.components_by_category[category].append(model)
                
            except Exception as e:
                print(f"Error converting {item.get('id', 'unknown')}: {e}")
        return by_id
    
    async def get_all_components(self) -> Dict[str, List[BikeComponent]]:
        return self.components_by_category

    async def get_component_by_id(self, component_id: str) -> Optional[BikeComponent]:
        return self.components_by_id.get(component_id)
    
    async def get_components_by_category(self, category: str) -> List[BikeComponent]:
        return self.components_by_category.get(category, [])
    
    async def get_pricing_rules(self) -> List[Dict]:
        return self.pricing_rules

    async def check_compatibility_of_selection(self, selection: Dict[str, BikeComponent]) -> List[str]:
        errors = []
        selection_by_category = {comp.category: comp for comp in selection.values() if comp}
        
        for rule in self.rules_raw:
            rule_id = rule.get("rule_id", "N/A")
            affects_category = rule.get("affects_category")
            
            component_to_validate = selection_by_category.get(affects_category)
            
            if not component_to_validate:
                continue

            for condition_set in rule.get("conditions", []):
                selector = condition_set.get("selector", {})
                result_set = condition_set.get("result_set", {})
                
                selector_category = selector.get("category")
                selector_component = selection_by_category.get(selector_category)

                if selector_component and selector_component.id == selector.get("id"):
                    
                    value_to_check = component_to_validate.id 
                    
                    if 'include' in result_set.get(affects_category, {}):
                        required_values = result_set[affects_category]['include']

                        if value_to_check not in required_values:
                            errors.append(
                                f"({rule_id}): The selection of {selector_component.id} requires "
                                f"{affects_category} to be one of {required_values}, but component ID is '{value_to_check}'."
                            )

                    if 'exclude' in result_set.get(affects_category, {}):
                        forbidden_values = result_set[affects_category]['exclude']
                        
                        if value_to_check in forbidden_values:
                            errors.append(
                                f"({rule_id}): The selection of {selector_component.id} does not allow "
                                f"{affects_category} to be '{value_to_check}'."
                            )

        return errors
    
    async def get_compatibility_constraints(self) -> Dict[str, Dict[str, Set[str]]]:
        constraints = defaultdict(lambda: defaultdict(set))

        all_component_ids_by_category = {
            cat: {comp.id for comp in components}
            for cat, components in self.components_by_category.items()
        }
        
        for rule in self.rules_raw:
            affects_category = rule.get("affects_category")
            
            for condition_set in rule.get("conditions", []):
                selector = condition_set.get("selector", {})
                result_set = condition_set.get("result_set", {})
                
                selector_id = selector.get("id")
                
                if affects_category in result_set:
                    rule_details = result_set[affects_category]
                    
                    if "exclude" in rule_details:
                        forbidden_ids = set(rule_details["exclude"])
                        
                        constraints[selector_id][affects_category].update(forbidden_ids)
                        
                    if "include" in rule_details:
                        allowed_ids = set(rule_details["include"])
                        
                        all_ids_in_category = all_component_ids_by_category.get(affects_category, set())
                        
                        exclude_ids = all_ids_in_category - allowed_ids
                        
                        constraints[selector_id][affects_category].update(exclude_ids)
                        
        final_constraints = {}
        for selector_id, affects_category in constraints.items():
            final_constraints[selector_id] = {
                cat: list(ids) for cat, ids in affects_category.items()
            }
            
        return final_constraints
    
    async def build_id_to_category_map(self):
        catalogue = await self.get_all_components()
        id_to_category_map = defaultdict(str)
        
        for category_name, component_list in catalogue.items():
            for component_object in component_list:
                if hasattr(component_object, 'id'):
                    component_id_str = component_object.id
                    id_to_category_map[component_id_str] = category_name
                    
        return id_to_category_map
from fastapi import APIRouter, Depends
from typing import Dict, Union, Annotated, List
from collections import defaultdict
from server.services.catalogue_gateway import CatalogueGateway
from server.services.pricing.price_strategy import StandardPricingStrategy
from server.services.bike_configurator import BikeConfiguratorService

router = APIRouter()

# --- Dependency Injectors ---

def get_catalogue_gateway() -> CatalogueGateway:
  return CatalogueGateway()

def get_bike_configurator_service(
  gateway: CatalogueGateway = Depends(get_catalogue_gateway)
) -> BikeConfiguratorService:
  return BikeConfiguratorService(
    catalogue_gateway=gateway,
    pricing_strategy=StandardPricingStrategy()
  )

ConfigService = Annotated[BikeConfiguratorService, Depends(get_bike_configurator_service)]

# --- API Endpoints ---

@router.get("/catalogue/full")
async def get_full_catalogue(gateway: CatalogueGateway = Depends(get_catalogue_gateway)):
  return await gateway.get_all_components()

@router.get("/catalogue/category/{category}")
async def get_catalogue_category(category: str, gateway: CatalogueGateway = Depends(get_catalogue_gateway)):
  return await gateway.get_components_by_category(category)

@router.get("/catalogue/constraints")
async def get_cataloue_constraints(gateway: CatalogueGateway = Depends(get_catalogue_gateway)):
  return await gateway.get_compatibility_constraints()

@router.get("/catalogue/pricing_rules")
async def get_pricing_rules(gateway: CatalogueGateway = Depends(get_catalogue_gateway)):
  return await gateway.get_pricing_rules()

@router.post("/price/check")
async def price_check(payload: Dict[str, Union[List[str], float, int]], gateway: CatalogueGateway = Depends(get_catalogue_gateway), bike_conf: BikeConfiguratorService = Depends(get_bike_configurator_service)):

  id_to_category_map = await gateway.build_id_to_category_map()
  
  selection_ids = defaultdict(str)
  
  for id in payload.get("component_ids", []):
    category_name = id_to_category_map.get(id)
    if category_name:
      selection_ids[category_name] = id
  
  if not selection_ids:
    return {
      "valid": False,
      "final_price": None,
      "message": "Error: Selected IDs could not be mapped to existing categories."
    }
    
  bike = await bike_conf.create_bike_from_selection(selection_ids)
  
  bike_price = bike.price
  
  is_valid = abs(bike_price - payload.get("client_total", 0)) < 0.01
  
  return {
    "valid": is_valid,
    "final_price": bike_price,
    "message": "Order verified successfully" if is_valid else "Price mismatch"
  }

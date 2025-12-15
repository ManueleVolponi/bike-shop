import unittest
from server.services.bike_configurator import BikeConfiguratorService
from server.services.catalogue_gateway import CatalogueGateway
from server.services.pricing.price_strategy import StandardPricingStrategy
from server.services.pricing.price_calculator import PriceCalculator
from server.services.pricing.pricing_rule_applicator import PricingRuleApplicator

T_DIA = "T-DIAMOND"
T_FS = "T-FS"
T_STEP = "T-STEP"

F_SHINY = "F-SHINY"
F_MAT = "F-MATTE"

W_FAT = "W-FAT"
W_R = "W-ROAD"
W_MTN = "W-MTN"

C_BLACK = "C-BLACK"
C_RED = "C-RED"

CH_SS = "CH-SS"
CH_8S = "CH-8S"


class TestBikeConfigurationIntegration(unittest.IsolatedAsyncioTestCase): 

    async def asyncSetUp(self):
        self.catalogue_gateway = CatalogueGateway()
        self.standard_strategy = StandardPricingStrategy()
        pricing_rules = await self.catalogue_gateway.get_pricing_rules()
        self.price_calculator = PriceCalculator(strategy=self.standard_strategy)
        self.pricing_rules_applicator = PricingRuleApplicator(pricing_rules=pricing_rules)
        
        self.config_service = BikeConfiguratorService(
            catalogue_gateway=self.catalogue_gateway,
            price_calculator=self.price_calculator,
            pricing_rules_app=self.pricing_rules_applicator
        )

        self.selection_ok = {
            "frame_type": T_DIA, 
            "frame_finish": F_SHINY,
            "wheels": W_R, 
            "rim_color": C_BLACK,
            "chain": CH_SS
        }
        
        self.selection_ok_1 = {
            "frame_type": T_FS, 
            "frame_finish": F_MAT,
            "wheels": W_MTN, 
            "rim_color": C_BLACK,
            "chain": CH_8S
        }
        
        self.selection_nok_r1 = {
            "frame_type": T_DIA, 
            "frame_finish": F_MAT,
            "wheels": W_MTN, 
            "rim_color": C_BLACK,
            "chain": CH_8S
        }

        self.selection_nok_r2 = {
            "frame_type": T_STEP, 
            "frame_finish": F_SHINY,
            "wheels": W_FAT, 
            "rim_color": C_RED,
            "chain": CH_SS
        }

    async def test_configuration_is_valid_and_priced_correctly(self):
        bike_ok = await self.config_service.create_bike_from_selection(self.selection_ok)
        
        self.assertTrue(bike_ok.is_valid)
        self.assertEqual(len(bike_ok.compatibility_errors), 0)
        
        # Expected Price (100 + 30 + 80 + 25 + 43) = 278.00
        self.assertEqual(bike_ok.price, 278.00)

    async def test_configuration_is_valid_and_priced_correctly_2(self):
        bike_ok = await self.config_service.create_bike_from_selection(self.selection_ok_1)
        
        self.assertTrue(bike_ok.is_valid)
        self.assertEqual(len(bike_ok.compatibility_errors), 0)
        
        # Expected price (130 + 50 + 90 + 25 + 67) = 362.00
        self.assertEqual(bike_ok.price, 362.00)
    
    async def test_rule_r001_violation_in_frame_type(self):
        bike_nok = await self.config_service.create_bike_from_selection(self.selection_nok_r1)
        
        self.assertFalse(bike_nok.is_valid)
        self.assertEqual(bike_nok.price, 0.0)
        self.assertGreater(len(bike_nok.compatibility_errors), 0)
        
        expected_error_substring = "(R001):" 
        self.assertTrue(any(expected_error_substring in err for err in bike_nok.compatibility_errors))

    async def test_rule_r002_violation_in_rim_color(self):
        bike_nok = await self.config_service.create_bike_from_selection(self.selection_nok_r2)
        
        self.assertFalse(bike_nok.is_valid)
        self.assertEqual(bike_nok.price, 0.0)
        self.assertGreater(len(bike_nok.compatibility_errors), 0)
        
        expected_error_substring = "(R002):" 
        self.assertTrue(any(expected_error_substring in err for err in bike_nok.compatibility_errors))

    async def test_incomplete_selection_raises_value_error(self):
        selection_incomplete = {
            "frame_type": T_DIA, 
            "frame_finish": F_SHINY,
            "wheels": W_R
        }
        
        with self.assertRaises(ValueError):
            await self.config_service.create_bike_from_selection(selection_incomplete)
            
    async def asyncTearDown(self):
        self.catalogue_gateway = None
        self.standard_strategy = None
        self.price_calculator = None
        self.pricing_rules_applicator = None
        self.config_service = None
        
        self.selection_ok = {}
        self.selection_ok_1 = {}
        self.selection_nok_r1 = {}
        self.selection_nok_r2 = {}
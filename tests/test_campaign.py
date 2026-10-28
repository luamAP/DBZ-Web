import unittest
from models import Campaign, Character
from data_loader import load_campaign_data, load_characters_data, load_items_data


class TestCampaign(unittest.TestCase):

    def setUp(self):
        self.raw_campaign = {
            "id": "test_saga",
            "name": "Saga de Teste",
            "description": "Uma jornada simulada.",
            "stages": [
                {
                    "stage": 1,
                    "name": "Fase 1",
                    "enemy": "Vegeta",
                    "recovery": {"hp_pct": 0.20, "ki_bonus": 15},
                    "drop_table": [
                        {"item_id": "senzu_bean", "item_type": "consumable", "chance": 0.50, "quantity": 1},
                        {"item_id": "capsule_scouter", "item_type": "equipment", "chance": 0.25}
                    ]
                },
                {
                    "stage": 2,
                    "name": "Fase 2",
                    "enemy": "Frieza",
                    "recovery": {"hp_pct": 0.0, "ki_bonus": 0},
                    "drop_table": [
                        {"item_id": "ki_capsule", "item_type": "consumable", "chance": 1.0, "quantity": 2}
                    ]
                }
            ]
        }
        self.campaign = Campaign(self.raw_campaign)
        self.goku_data = {
            'name': 'Goku',
            'hp': 100,
            'attack': 20,
            'defense': 30,
            'ki_max': 100,
            'speed': 80,
            'moves': [{'name': 'Soco', 'ki_cost': 0, 'multiplier': 1.0, 'type': 'basic'}]
        }

    def test_campaign_initialization(self):
        self.assertEqual(self.campaign.id, "test_saga")
        self.assertEqual(self.campaign.name, "Saga de Teste")
        self.assertFalse(self.campaign.is_completed())
        stage1 = self.campaign.get_current_stage()
        self.assertIsNotNone(stage1)
        self.assertEqual(stage1["stage"], 1)

    def test_campaign_stage_progression(self):
        success, meta = self.campaign.advance_stage()
        self.assertTrue(success)
        self.assertEqual(meta["current_stage_index"], 1)
        self.assertFalse(meta["is_completed"])

        stage2 = self.campaign.get_current_stage()
        self.assertEqual(stage2["stage"], 2)

        success2, meta2 = self.campaign.advance_stage()
        self.assertTrue(success2)
        self.assertTrue(meta2["is_completed"])
        self.assertTrue(self.campaign.is_completed())
        self.assertIsNone(self.campaign.get_current_stage())

        # Tentativa de avançar após concluída
        success3, meta3 = self.campaign.advance_stage()
        self.assertFalse(success3)
        self.assertEqual(meta3["reason"], "already_completed")

    def test_resolve_drops_with_guaranteed_roll(self):
        stage1 = self.campaign.stages[0]
        # Força RNG a retornar 0.10 (menor que 0.50 e 0.25)
        drops = Campaign.resolve_drops(stage1, rng=lambda: 0.10)
        self.assertEqual(len(drops), 2)
        self.assertEqual(drops[0]["item_id"], "senzu_bean")
        self.assertEqual(drops[0]["quantity"], 1)
        self.assertEqual(drops[1]["item_id"], "capsule_scouter")

    def test_resolve_drops_with_unlucky_roll(self):
        stage1 = self.campaign.stages[0]
        # Força RNG a retornar 0.99 (maior que 0.50 e 0.25)
        drops = Campaign.resolve_drops(stage1, rng=lambda: 0.99)
        self.assertEqual(len(drops), 0)

    def test_calculate_stage_recovery(self):
        player = Character(self.goku_data)
        stage1 = self.campaign.stages[0]
        hp_amount, ki_bonus = Campaign.calculate_stage_recovery(player, stage1)
        self.assertEqual(hp_amount, 20)  # 20% de 100
        self.assertEqual(ki_bonus, 15)

    def test_player_recover_mechanic(self):
        player = Character(self.goku_data)
        player.hp = 50
        player.ki = 10
        success, meta = player.recover(hp_amount=30, ki_amount=40)
        self.assertTrue(success)
        self.assertEqual(player.hp, 80)
        self.assertEqual(player.ki, 50)
        self.assertEqual(meta["hp_gain"], 30)
        self.assertEqual(meta["ki_gain"], 40)

        # Não ultrapassa o máximo
        player.recover(hp_amount=50, ki_amount=100)
        self.assertEqual(player.hp, player.max_hp)
        self.assertEqual(player.ki, player.max_ki)

    def test_character_add_to_inventory(self):
        player = Character(self.goku_data, initial_inventory={"senzu_bean": 1})
        success, meta = player.add_to_inventory("senzu_bean", quantity=2)
        self.assertTrue(success)
        self.assertEqual(player.inventory["senzu_bean"], 3)
        self.assertEqual(meta["total"], 3)

        # Item novo no inventário
        success2, meta2 = player.add_to_inventory("ki_capsule", quantity=1)
        self.assertTrue(success2)
        self.assertEqual(player.inventory["ki_capsule"], 1)

        # Quantidade inválida
        success3, meta3 = player.add_to_inventory("senzu_bean", quantity=0)
        self.assertFalse(success3)
        self.assertEqual(meta3["reason"], "invalid_quantity")

    def test_load_campaign_yaml_structure(self):
        campaign_data = load_campaign_data()
        self.assertIn("campaigns", campaign_data)
        self.assertIn("saiyan_invasion", campaign_data["campaigns"])

        invasion = campaign_data["campaigns"]["saiyan_invasion"]
        self.assertIn("stages", invasion)
        self.assertGreaterEqual(len(invasion["stages"]), 2)

        # Valida se os oponentes existem em characters.yml
        characters_db = load_characters_data()
        for stage in invasion["stages"]:
            self.assertIn(stage["enemy"], characters_db)


if __name__ == '__main__':
    unittest.main()

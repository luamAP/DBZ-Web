import os
import json
import tempfile
import unittest

from models import Character, Campaign
from data_loader import save_game_state, load_game_state


class TestSaveState(unittest.TestCase):

    def setUp(self):
        self.goku_data = {
            'name': 'Goku',
            'hp': 100,
            'attack': 20,
            'defense': 30,
            'ki_max': 100,
            'speed': 80,
            'moves': [{'name': 'Soco', 'ki_cost': 0, 'multiplier': 1.0, 'type': 'basic'}],
            'transformations': [
                {
                    'name': 'Super Saiyan',
                    'required_ki': 50,
                    'hp_threshold_pct': 1.0,
                    'stat_multipliers': {'attack': 1.5, 'defense': 1.3, 'speed': 1.2}
                }
            ]
        }
        self.equipment_db = {
            'weighted_clothing': {
                'id': 'weighted_clothing',
                'name': 'Roupas Pesadas de Treino',
                'stat_multipliers': {'defense': 1.15, 'speed': 0.90},
                'stat_bonuses': {'hp': 15, 'ki_max': 0}
            },
            'capsule_scouter': {
                'id': 'capsule_scouter',
                'name': 'Rastreador Capsule Corp',
                'stat_multipliers': {'speed': 1.25},
                'stat_bonuses': {'hp': 0, 'ki_max': 0}
            }
        }
        self.campaign_data = {
            'id': 'test_campaign',
            'name': 'Campanha de Teste',
            'stages': [
                {'stage': 1, 'name': 'Fase 1', 'enemy': 'Vegeta'},
                {'stage': 2, 'name': 'Fase 2', 'enemy': 'Frieza'}
            ]
        }

    def test_character_serialization_and_restoration(self):
        player = Character(self.goku_data, initial_inventory={'senzu_bean': 2})
        player.equip_item(self.equipment_db['weighted_clothing'])
        player.hp = 75
        player.ki = 40

        serialized = player.to_dict()
        self.assertEqual(serialized['raw_name'], 'Goku')
        self.assertEqual(serialized['hp'], 75)
        self.assertEqual(serialized['ki'], 40)
        self.assertEqual(serialized['inventory'], {'senzu_bean': 2})
        self.assertIn('weighted_clothing', serialized['equipped_items'])

        # Cria um novo personagem e restaura
        restored_player = Character(self.goku_data)
        success, meta = restored_player.load_state(serialized, available_equipment=self.equipment_db)
        self.assertTrue(success)
        self.assertEqual(restored_player.hp, 75)
        self.assertEqual(restored_player.ki, 40)
        self.assertEqual(restored_player.inventory['senzu_bean'], 2)
        self.assertEqual(len(restored_player.equipped_items), 1)
        self.assertEqual(restored_player.equipped_items[0]['id'], 'weighted_clothing')

    def test_campaign_serialization_and_restoration(self):
        campaign = Campaign(self.campaign_data)
        campaign.advance_stage()

        serialized = campaign.to_dict()
        self.assertEqual(serialized['campaign_id'], 'test_campaign')
        self.assertEqual(serialized['current_stage_index'], 1)
        self.assertFalse(serialized['is_completed'])

        # Restaura em nova instância
        restored_campaign = Campaign(self.campaign_data)
        success, meta = restored_campaign.load_state(serialized)
        self.assertTrue(success)
        self.assertEqual(restored_campaign.current_stage_index, 1)

    def test_save_and_load_file_io(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_save_file = os.path.join(tmp_dir, "temp_save.json")
            save_payload = {
                "player": {"hp": 90, "ki": 30, "inventory": {"ki_capsule": 1}},
                "campaign": {"current_stage_index": 1}
            }

            # Salva no arquivo temporário
            with open(temp_save_file, 'w', encoding='utf-8') as f:
                json.dump(save_payload, f)

            self.assertTrue(os.path.isfile(temp_save_file))

            # Carrega e valida
            with open(temp_save_file, 'r', encoding='utf-8') as f:
                loaded = json.load(f)

            self.assertEqual(loaded['player']['hp'], 90)
            self.assertEqual(loaded['campaign']['current_stage_index'], 1)

    def test_load_non_existent_file(self):
        data, meta = load_game_state(filename="arquivo_inexistente_123.json")
        self.assertIsNone(data)
        self.assertEqual(meta.get("reason"), "file_not_found")


if __name__ == '__main__':
    unittest.main()

import unittest
import yaml
import os
from models import Character


class TestCombatMechanics(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        base_dir = os.path.dirname(os.path.abspath(__file__))

        char_path = os.path.join(base_dir, 'characters.yml')
        with open(char_path, 'r', encoding='utf-8') as f:
            cls.characters_db = yaml.safe_load(f)

        items_path = os.path.join(base_dir, 'items.yml')
        with open(items_path, 'r', encoding='utf-8') as f:
            cls.items_db = yaml.safe_load(f)

        cls.defense_cfg = cls.characters_db.get('defense_mechanics', {})
        cls.equipment_items = cls.items_db.get('equipment', {})
        cls.consumables = cls.items_db.get('consumables', {})

    def setUp(self):
        initial_inv = {
            item_id: item_data.get('default_quantity', 1)
            for item_id, item_data in self.consumables.items()
        }
        self.goku = Character(self.characters_db['Goku'], initial_inv)
        self.vegeta = Character(self.characters_db['Vegeta'])

    def test_special_move_ki_validation(self):
        kamehameha = next(m for m in self.goku.moves if m['name'] == 'Kamehameha')
        self.goku.ki = 0

        success = self.goku.execute_move(kamehameha, self.vegeta, self.defense_cfg)
        self.assertFalse(success)
        self.assertEqual(self.goku.ki, 0)
        self.assertEqual(self.vegeta.hp, self.vegeta.max_hp)

        self.goku.ki = kamehameha['ki_cost']
        success = self.goku.execute_move(kamehameha, self.vegeta, self.defense_cfg)
        self.assertTrue(success)
        self.assertEqual(self.goku.ki, 0)
        self.assertLess(self.vegeta.hp, self.vegeta.max_hp)

    def test_combo_execution(self):
        combo = next(m for m in self.goku.moves if m['type'] == 'combo')
        self.goku.ki = combo['ki_cost']

        initial_hp = self.vegeta.hp
        success = self.goku.execute_move(combo, self.vegeta, self.defense_cfg)

        self.assertTrue(success)
        self.assertEqual(self.goku.ki, 0)
        self.assertLessEqual(self.vegeta.hp, initial_hp)

    def test_vanish_defense(self):
        self.vegeta.defend('vanish')
        initial_hp = self.vegeta.hp

        basic_move = next(m for m in self.goku.moves if m['type'] == 'basic')
        self.goku.execute_move(basic_move, self.vegeta, self.defense_cfg)

        self.assertEqual(self.vegeta.hp, initial_hp)

    def test_counter_defense(self):
        self.vegeta.defend('counter')
        initial_goku_hp = self.goku.hp
        initial_vegeta_hp = self.vegeta.hp

        basic_move = next(m for m in self.goku.moves if m['type'] == 'basic')
        self.goku.execute_move(basic_move, self.vegeta, self.defense_cfg)

        self.assertLess(self.vegeta.hp, initial_vegeta_hp)
        self.assertLess(self.goku.hp, initial_goku_hp)

    def test_end_turn_resets_stance(self):
        self.vegeta.defend('block')
        self.assertEqual(self.vegeta.defensive_stance, 'block')

        self.vegeta.end_turn()
        self.assertIsNone(self.vegeta.defensive_stance)

    def test_transformation_attributes_and_ki_cost(self):
        trans = self.goku.transformations[0]
        self.goku.ki = trans['required_ki']
        old_atk = self.goku.base_attack

        success = self.goku.transform(trans)
        self.assertTrue(success)
        self.assertEqual(self.goku.ki, 0)
        self.assertEqual(self.goku.name, trans['name'])
        self.assertGreater(self.goku.base_attack, old_atk)

        self.goku.ki = 100
        can_again, _ = self.goku.can_transform(trans)
        self.assertFalse(can_again)

    def test_equip_and_unequip_item_stats(self):
        item = self.equipment_items['weighted_clothing']
        initial_def = self.goku.defense
        initial_spd = self.goku.speed
        initial_max_hp = self.goku.max_hp

        success, _ = self.goku.equip_item(item)
        self.assertTrue(success)
        self.assertGreater(self.goku.defense, initial_def)
        self.assertLess(self.goku.speed, initial_spd)
        self.assertGreater(self.goku.max_hp, initial_max_hp)

        dup_success, _ = self.goku.equip_item(item)
        self.assertFalse(dup_success)

        unequip_success, _ = self.goku.unequip_item(item['id'])
        self.assertTrue(unequip_success)
        self.assertEqual(self.goku.defense, initial_def)
        self.assertEqual(self.goku.speed, initial_spd)
        self.assertEqual(self.goku.max_hp, initial_max_hp)

    def test_equipment_granted_moves(self):
        item = self.equipment_items['potara_earring']
        move_name = "Potara Spirit Lance"

        self.assertFalse(any(m['name'] == move_name for m in self.goku.moves))

        self.goku.equip_item(item)
        self.assertTrue(any(m['name'] == move_name for m in self.goku.moves))

        self.goku.unequip_item(item['id'])
        self.assertFalse(any(m['name'] == move_name for m in self.goku.moves))

    def test_equipment_and_transformation_stacking(self):
        item = self.equipment_items['potara_earring']
        self.goku.equip_item(item)

        trans = self.goku.transformations[0]
        self.goku.ki = trans['required_ki']
        self.goku.transform(trans)

        expected_atk = int(self.goku.raw_attack * item['stat_multipliers']['attack'] * trans['stat_multipliers']['attack'])
        self.assertEqual(self.goku.base_attack, expected_atk)

    def test_use_consumable_restores_hp_and_ki(self):
        """Valida restauracao de HP e Ki respeitando os limites maximos."""
        item = self.consumables['senzu_bean']
        self.goku.hp = 20
        self.goku.ki = 10

        success, _ = self.goku.use_consumable(item['id'], item)
        self.assertTrue(success)
        self.assertEqual(self.goku.hp, self.goku.max_hp)
        self.assertEqual(self.goku.ki, 10 + item['ki_restore_amount'])

    def test_use_consumable_decrements_inventory(self):
        """Valida que o inventario e decrementado a cada uso."""
        item = self.consumables['ki_capsule']
        initial_qty = self.goku.inventory[item['id']]

        success, _ = self.goku.use_consumable(item['id'], item)
        self.assertTrue(success)
        self.assertEqual(self.goku.inventory[item['id']], initial_qty - 1)

    def test_use_consumable_without_quantity_fails(self):
        """Valida que o uso falha quando a quantidade no inventario e zero."""
        item = self.consumables['senzu_bean']
        self.goku.inventory[item['id']] = 0

        success, msg = self.goku.use_consumable(item['id'], item)
        self.assertFalse(success)
        self.assertIn("nao possui mais unidades", msg)


if __name__ == '__main__':
    unittest.main()

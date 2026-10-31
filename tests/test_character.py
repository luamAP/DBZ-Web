import unittest
from models import Character
from engine.data_loader import load_characters_data, load_items_data, create_initial_inventory


class TestCharacter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.characters_db = load_characters_data()
        cls.items_db = load_items_data()
        cls.equipment_items = cls.items_db.get('equipment', {})
        cls.consumables = cls.items_db.get('consumables', {})

    def setUp(self):
        initial_inv = create_initial_inventory(self.consumables)
        self.goku = Character(self.characters_db['Goku'], initial_inv)
        self.vegeta = Character(self.characters_db['Vegeta'])

    def test_transformation_attributes_and_ki_cost(self):
        trans = self.goku.transformations[0]
        self.goku.ki = trans['required_ki']
        old_atk = self.goku.base_attack

        success, _ = self.goku.transform(trans)
        self.assertTrue(success)
        self.assertEqual(self.goku.ki, 0)
        self.assertEqual(self.goku.name, trans['name'])
        self.assertGreater(self.goku.base_attack, old_atk)

        self.goku.ki = 100
        can_again, reason_payload = self.goku.can_transform(trans)
        self.assertFalse(can_again)
        self.assertEqual(reason_payload['reason'], 'already_transformed')

    def test_transformation_insufficient_ki(self):
        trans = self.goku.transformations[0]
        self.goku.ki = 0
        can, payload = self.goku.can_transform(trans)
        self.assertFalse(can)
        self.assertEqual(payload['reason'], 'insufficient_ki')

    def test_equip_and_unequip_item_stats(self):
        item = self.equipment_items['weighted_clothing']
        initial_def = self.goku.defense
        initial_spd = self.goku.speed
        initial_max_hp = self.goku.max_hp

        success, equip_payload = self.goku.equip_item(item)
        self.assertTrue(success)
        self.assertEqual(equip_payload['item_id'], item['id'])
        self.assertGreater(self.goku.defense, initial_def)
        self.assertLess(self.goku.speed, initial_spd)
        self.assertGreater(self.goku.max_hp, initial_max_hp)

        dup_success, dup_payload = self.goku.equip_item(item)
        self.assertFalse(dup_success)
        self.assertEqual(dup_payload['reason'], 'already_equipped')

        unequip_success, unequip_payload = self.goku.unequip_item(item['id'])
        self.assertTrue(unequip_success)
        self.assertEqual(unequip_payload['item_id'], item['id'])
        self.assertEqual(self.goku.defense, initial_def)
        self.assertEqual(self.goku.speed, initial_spd)
        self.assertEqual(self.goku.max_hp, initial_max_hp)

        not_found_success, not_found_payload = self.goku.unequip_item('fake_item')
        self.assertFalse(not_found_success)
        self.assertEqual(not_found_payload['reason'], 'not_found')

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
        item = self.consumables['senzu_bean']
        self.goku.hp = 20
        self.goku.ki = 10

        success, _ = self.goku.use_consumable(item['id'], item)
        self.assertTrue(success)
        self.assertEqual(self.goku.hp, self.goku.max_hp)
        self.assertEqual(self.goku.ki, 10 + item['ki_restore_amount'])

    def test_use_consumable_decrements_inventory(self):
        item = self.consumables['ki_capsule']
        initial_qty = self.goku.inventory[item['id']]

        success, _ = self.goku.use_consumable(item['id'], item)
        self.assertTrue(success)
        self.assertEqual(self.goku.inventory[item['id']], initial_qty - 1)

    def test_use_consumable_without_quantity_fails(self):
        item = self.consumables['senzu_bean']
        self.goku.inventory[item['id']] = 0

        success, payload = self.goku.use_consumable(item['id'], item)
        self.assertFalse(success)
        self.assertIn("Voce nao possui mais unidades", payload['msg'])


if __name__ == '__main__':
    unittest.main()

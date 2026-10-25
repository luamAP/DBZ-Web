import unittest
from models import Character, Team
from data_loader import load_characters_data, load_items_data, create_initial_inventory


class TestCombatMechanics(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.characters_db = load_characters_data()
        cls.items_db = load_items_data()

        cls.defense_cfg = cls.characters_db.get('defense_mechanics', {})
        cls.equipment_items = cls.items_db.get('equipment', {})
        cls.consumables = cls.items_db.get('consumables', {})

    def setUp(self):
        initial_inv = create_initial_inventory(self.consumables)
        self.goku = Character(self.characters_db['Goku'], initial_inv)
        self.vegeta = Character(self.characters_db['Vegeta'])
        self.frieza = Character(self.characters_db['Frieza'])

    def test_special_move_ki_validation(self):
        kamehameha = next(m for m in self.goku.moves if m['name'] == 'Kamehameha')
        self.goku.ki = 0

        success, _ = self.goku.execute_move(kamehameha, self.vegeta, self.defense_cfg)
        self.assertFalse(success)
        self.assertEqual(self.goku.ki, 0)
        self.assertEqual(self.vegeta.hp, self.vegeta.max_hp)

        self.goku.ki = kamehameha['ki_cost']
        success, _ = self.goku.execute_move(kamehameha, self.vegeta, self.defense_cfg)
        self.assertTrue(success)
        self.assertEqual(self.goku.ki, 0)
        self.assertLess(self.vegeta.hp, self.vegeta.max_hp)

    def test_combo_execution(self):
        combo = next(m for m in self.goku.moves if m['type'] == 'combo')
        self.goku.ki = combo['ki_cost']

        initial_hp = self.vegeta.hp
        success, _ = self.goku.execute_move(combo, self.vegeta, self.defense_cfg)

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

    # --- Testes de Batalhas em Equipe (Tag Team) ---

    def test_team_initialization_and_active_member(self):
        team = Team("Guerreiros Z", [self.goku, self.vegeta])
        self.assertEqual(team.active_member, self.goku)
        self.assertTrue(team.has_alive_members())
        self.assertEqual(len(team.get_bench_members()), 1)

    def test_team_voluntary_switch(self):
        team = Team("Guerreiros Z", [self.goku, self.vegeta])
        success, event_data = team.switch_member(1)
        self.assertTrue(success)
        self.assertEqual(team.active_member, self.vegeta)
        self.assertEqual(event_data['new_name'], self.vegeta.name)

        same_success, same_payload = team.switch_member(1)
        self.assertFalse(same_success)
        self.assertEqual(same_payload['reason'], 'already_active')

    def test_team_cannot_switch_to_dead_member(self):
        self.vegeta.hp = 0
        team = Team("Guerreiros Z", [self.goku, self.vegeta])
        success, payload = team.switch_member(1)
        self.assertFalse(success)
        self.assertEqual(payload['reason'], 'is_dead')
        self.assertEqual(team.active_member, self.goku)

    def test_team_auto_switch_on_ko(self):
        team = Team("Guerreiros Z", [self.goku, self.vegeta])
        self.goku.hp = 0
        switched, event_data = team.auto_switch_next_alive()
        self.assertTrue(switched)
        self.assertEqual(team.active_member, self.vegeta)
        self.assertEqual(event_data['new_name'], self.vegeta.name)

    def test_team_all_dead_condition(self):
        team = Team("Guerreiros Z", [self.goku, self.vegeta])
        self.goku.hp = 0
        self.vegeta.hp = 0
        self.assertFalse(team.has_alive_members())
        switched, payload = team.auto_switch_next_alive()
        self.assertFalse(switched)
        self.assertEqual(payload['reason'], 'no_alive_members')


if __name__ == '__main__':
    unittest.main()

import unittest
from models import Character
from engine.data_loader import load_characters_data


class TestCombatFlow(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.characters_db = load_characters_data()
        cls.defense_cfg = cls.characters_db.get('defense_mechanics', {})

    def setUp(self):
        self.goku = Character(self.characters_db['Goku'])
        self.vegeta = Character(self.characters_db['Vegeta'])

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


if __name__ == '__main__':
    unittest.main()

import unittest
from models import Character
from engine.data_loader import load_characters_data


class TestCombatFlow(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.characters_db = load_characters_data()
        cls.defense_cfg = cls.characters_db.get('defense_mechanics', {})
        cls.combat_cfg = cls.characters_db.get('combat_mechanics', {})

    def setUp(self):
        self.goku = Character(self.characters_db['Goku'], combat_cfg=self.combat_cfg)
        self.vegeta = Character(self.characters_db['Vegeta'], combat_cfg=self.combat_cfg)

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

    def test_charge_ki_with_injected_rng_and_custom_combat_cfg(self):
        custom_cfg = {"charge_ki": {"min": 20, "max": 40}}
        called_args = []

        def mock_randint(low, high):
            called_args.append((low, high))
            return 28

        ev = self.goku.charge_ki(combat_cfg=custom_cfg, rng=mock_randint)
        self.assertEqual(called_args, [(20, 40)])
        self.assertEqual(ev["amount"], 28)
        self.assertEqual(self.goku.ki, 28)

    def test_basic_attack_with_injected_rng_and_variance(self):
        basic_move = next(m for m in self.goku.moves if m['type'] == 'basic')
        called_ranges = []

        def mock_randint(low, high):
            called_ranges.append((low, high))
            return high  # valor maximo da variacao (+4)

        success, ev = self.goku.execute_move(basic_move, self.vegeta, self.defense_cfg, rng=mock_randint)
        self.assertTrue(success)
        self.assertEqual(called_ranges, [(-4, 4)])

    def test_combo_attack_with_deterministic_rng_class(self):
        combo_move = next(m for m in self.goku.moves if m['type'] == 'combo')
        self.goku.ki = combo_move['ki_cost']

        class DeterministicRNG:
            def random(self):
                return 0.1  # sempre acerta o golpe

            def randint(self, low, high):
                return 0    # variacao zero

        success, ev = self.goku.execute_move(combo_move, self.vegeta, self.defense_cfg, rng=DeterministicRNG())
        self.assertTrue(success)
        self.assertEqual(ev["successful_hits"], ev["hits_total"])
        self.assertTrue(all(ev["hit_results"]))

    def test_special_attack_damage_variance_rng(self):
        special_move = next(m for m in self.goku.moves if m['type'] == 'special')
        self.goku.ki = special_move['ki_cost']

        called_ranges = []

        def mock_randint(low, high):
            called_ranges.append((low, high))
            return low  # valor minimo da variacao (+0)

        success, ev = self.goku.execute_move(special_move, self.vegeta, self.defense_cfg, rng=mock_randint)
        self.assertTrue(success)
        self.assertEqual(called_ranges, [(0, 8)])

    def test_dodge_defense_with_injected_rng(self):
        basic_move = next(m for m in self.goku.moves if m['type'] == 'basic')

        # Caso 1: esquiva bem sucedida (roll <= 0.60)
        self.vegeta.defend('dodge')
        initial_hp = self.vegeta.hp
        self.goku.execute_move(basic_move, self.vegeta, self.defense_cfg, rng=lambda: 0.1)
        self.assertEqual(self.vegeta.hp, initial_hp)

        # Caso 2: esquiva falha (roll > 0.60)
        self.vegeta.defend('dodge')
        self.goku.execute_move(basic_move, self.vegeta, self.defense_cfg, rng=lambda: 0.9)
        self.assertLess(self.vegeta.hp, initial_hp)


if __name__ == '__main__':
    unittest.main()

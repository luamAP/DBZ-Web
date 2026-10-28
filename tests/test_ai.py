import unittest
from unittest.mock import patch

from models import Character
from data_loader import load_characters_data
from ai_controller import execute_ai_turn


class TestAIController(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.characters_db = load_characters_data()
        cls.defense_cfg = cls.characters_db.get('defense_mechanics', {})
        cls.ai_profiles_cfg = cls.characters_db.get('ai_profiles', {})

    def setUp(self):
        self.goku = Character(self.characters_db['Goku'])
        self.vegeta = Character(self.characters_db['Vegeta'])
        self.frieza = Character(self.characters_db['Frieza'])

    def test_character_profile_assignment(self):
        self.assertEqual(self.goku.ai_profile, 'tatico')
        self.assertEqual(self.vegeta.ai_profile, 'agressivo')
        self.assertEqual(self.frieza.ai_profile, 'defensivo')

    def test_fallback_to_default_profile(self):
        custom_char = Character({
            'name': 'Piccolo',
            'hp': 100,
            'attack': 20,
            'defense': 20,
            'ki_max': 100,
            'speed': 80,
            'moves': [{'name': 'Punch', 'ki_cost': 0, 'multiplier': 1.0, 'type': 'basic'}]
        })
        self.assertEqual(custom_char.ai_profile, 'tatico')

    def test_aggressive_profile_prioritizes_specials_when_ki_available(self):
        # Garante Ki maximo para poder executar special
        self.vegeta.ki = 100
        # Simula random para favorecer ramo de special
        with patch('random.random', return_value=0.1):
            action_type, ev_data = execute_ai_turn(
                self.vegeta, self.goku, self.defense_cfg, self.ai_profiles_cfg
            )
        self.assertEqual(action_type, 'move')
        self.assertEqual(ev_data['move_name'], 'Final Flash')

    def test_defensive_profile_defends_at_higher_hp(self):
        # Frieza defensivo com 45% de vida (limiar eh 50%) e Goku com Ki alto
        self.frieza.hp = int(self.frieza.max_hp * 0.45)
        self.frieza.ki = 30
        self.goku.ki = 50

        with patch('random.random', return_value=0.1):
            action_type, ev_data = execute_ai_turn(
                self.frieza, self.goku, self.defense_cfg, self.ai_profiles_cfg
            )
        self.assertEqual(action_type, 'defend')
        self.assertIn(ev_data['stance'], ['vanish', 'counter', 'dodge', 'block'])

    def test_low_ki_triggers_charge(self):
        # Sem Ki para especiais/combos e abaixo do threshold
        self.vegeta.ki = 10
        self.goku.ki = 0

        action_type, ev_data = execute_ai_turn(
            self.vegeta, self.goku, self.defense_cfg, self.ai_profiles_cfg
        )
        self.assertEqual(action_type, 'charge')
        self.assertGreater(ev_data['amount'], 0)

    def test_transformation_trigger(self):
        self.goku.ki = 100
        self.goku.hp = self.goku.max_hp

        action_type, ev_data = execute_ai_turn(
            self.goku, self.vegeta, self.defense_cfg, self.ai_profiles_cfg
        )
        self.assertEqual(action_type, 'transform')
        self.assertEqual(ev_data['new_name'], 'Super Saiyan Goku')


if __name__ == '__main__':
    unittest.main()

import unittest
from models import Character, Team
from data_loader import load_characters_data


class TestTeam(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.characters_db = load_characters_data()

    def setUp(self):
        self.goku = Character(self.characters_db['Goku'])
        self.vegeta = Character(self.characters_db['Vegeta'])
        self.frieza = Character(self.characters_db['Frieza'])

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

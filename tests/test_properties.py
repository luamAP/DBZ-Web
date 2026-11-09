import unittest
from hypothesis import HealthCheck, given, settings, strategies as st

from models.character import Character

settings.register_profile("default", suppress_health_check=[HealthCheck.too_slow], deadline=None)
settings.load_profile("default")


def _sample_character_data(name="Goku", hp=100, attack=20, defense=30, ki_max=100, speed=80):
    return {
        'name': name,
        'hp': hp,
        'attack': attack,
        'defense': defense,
        'ki_max': ki_max,
        'speed': speed,
        'moves': [
            {'name': 'Soco', 'ki_cost': 0, 'multiplier': 1.0, 'type': 'basic'},
            {'name': 'Kamehameha', 'ki_cost': 30, 'multiplier': 1.5, 'type': 'special'},
            {'name': 'Combo Rapido', 'ki_cost': 20, 'multiplier': 0.5, 'hits': 3, 'hit_chance': 0.8, 'type': 'combo'},
        ],
        'transformations': [
            {
                'name': 'Super Saiyan',
                'required_ki': 50,
                'hp_threshold_pct': 1.0,
                'stat_multipliers': {'attack': 1.5, 'defense': 1.3, 'speed': 1.2}
            }
        ]
    }


def _defense_cfg():
    return {
        'block': {'damage_reduction': 0.50},
        'dodge': {'success_rate': 0.60},
        'counter': {'damage_reduction': 0.30, 'counter_damage_ratio': 0.60}
    }


class TestCharacterProperties(unittest.TestCase):

    # ---------------------------------------------------------
    # Invariantes de HP e Ki dentro dos limites [0, max]
    # ---------------------------------------------------------
    @given(
        initial_hp=st.integers(min_value=1, max_value=500),
        raw_damage=st.integers(min_value=0, max_value=2000),
        stance=st.sampled_from([None, 'block', 'dodge', 'counter', 'vanish'])
    )
    def test_apply_incoming_damage_keeps_hp_bounds(self, initial_hp, raw_damage, stance):
        data = _sample_character_data(hp=max(initial_hp, 10))
        target = Character(data)
        target.hp = min(initial_hp, target.max_hp)
        target.defensive_stance = stance

        attacker = Character(_sample_character_data(name="Vegeta"))

        target.apply_incoming_damage(raw_damage, attacker, _defense_cfg())

        self.assertGreaterEqual(target.hp, 0)
        self.assertLessEqual(target.hp, target.max_hp)
        self.assertGreaterEqual(attacker.hp, 0)
        self.assertLessEqual(attacker.hp, attacker.max_hp)

    @given(
        hp_amount=st.integers(min_value=-500, max_value=500),
        ki_amount=st.integers(min_value=-500, max_value=500),
        start_hp=st.integers(min_value=0, max_value=200),
        start_ki=st.integers(min_value=0, max_value=200)
    )
    def test_recover_keeps_hp_and_ki_bounds(self, hp_amount, ki_amount, start_hp, start_ki):
        char = Character(_sample_character_data(hp=150, ki_max=120))
        char.hp = min(start_hp, char.max_hp)
        char.ki = min(start_ki, char.max_ki)

        char.recover(hp_amount=hp_amount, ki_amount=ki_amount)

        self.assertGreaterEqual(char.hp, 0)
        self.assertLessEqual(char.hp, char.max_hp)
        self.assertGreaterEqual(char.ki, 0)
        self.assertLessEqual(char.ki, char.max_ki)

    @given(
        start_ki=st.integers(min_value=0, max_value=100),
        charge_min=st.integers(min_value=5, max_value=25),
        charge_max=st.integers(min_value=25, max_value=60)
    )
    def test_charge_ki_never_exceeds_max_ki(self, start_ki, charge_min, charge_max):
        if charge_min > charge_max:
            charge_min, charge_max = charge_max, charge_min
        cfg = {'charge_ki': {'min': charge_min, 'max': charge_max}}
        char = Character(_sample_character_data(ki_max=100), combat_cfg=cfg)
        char.ki = min(start_ki, char.max_ki)

        char.charge_ki()

        self.assertGreaterEqual(char.ki, 0)
        self.assertLessEqual(char.ki, char.max_ki)

    @given(
        ki_cost=st.integers(min_value=0, max_value=80),
        current_ki=st.integers(min_value=0, max_value=100)
    )
    def test_execute_special_move_ki_spending(self, ki_cost, current_ki):
        char = Character(_sample_character_data(ki_max=100))
        char.ki = current_ki
        target = Character(_sample_character_data(name="Inimigo"))

        move = {'name': 'Super Ataque', 'ki_cost': ki_cost, 'multiplier': 1.5, 'type': 'special'}
        success, _ = char.execute_move(move, target, defense_cfg=_defense_cfg())

        if current_ki >= ki_cost:
            self.assertTrue(success)
            self.assertEqual(char.ki, current_ki - ki_cost)
        else:
            self.assertFalse(success)
            self.assertEqual(char.ki, current_ki)

        self.assertGreaterEqual(char.ki, 0)
        self.assertLessEqual(char.ki, char.max_ki)

    # ---------------------------------------------------------
    # Inventário nunca negativo
    # ---------------------------------------------------------
    @given(
        operations=st.lists(
            st.tuples(
                st.sampled_from(['add', 'use']),
                st.sampled_from(['senzu_bean', 'ki_capsule', 'unknown_item']),
                st.integers(min_value=-5, max_value=10)
            ),
            max_size=30
        )
    )
    def test_inventory_quantities_never_negative(self, operations):
        char = Character(_sample_character_data(), initial_inventory={'senzu_bean': 1})
        consumables_db = {
            'senzu_bean': {'name': 'Semente dos Deuses', 'hp_restore_pct': 1.0, 'ki_restore_amount': 30},
            'ki_capsule': {'name': 'Cápsula de Ki', 'hp_restore_pct': 0.0, 'ki_restore_amount': 50},
            'unknown_item': {'name': 'Item Misterioso', 'hp_restore_pct': 0.1, 'ki_restore_amount': 0}
        }

        for op, item_id, qty in operations:
            if op == 'add':
                char.add_to_inventory(item_id, qty)
            elif op == 'use':
                char.use_consumable(item_id, consumables_db[item_id])

            for item_qty in char.inventory.values():
                self.assertGreaterEqual(item_qty, 0)

    # ---------------------------------------------------------
    # Equip / Unequip reversível
    # ---------------------------------------------------------
    @given(
        hp_bonus=st.integers(min_value=0, max_value=50),
        ki_bonus=st.integers(min_value=0, max_value=50),
        atk_mult=st.floats(min_value=0.5, max_value=2.0),
        def_mult=st.floats(min_value=0.5, max_value=2.0),
        spd_mult=st.floats(min_value=0.5, max_value=2.0),
        has_granted_move=st.booleans()
    )
    def test_equip_unequip_reversibility(self, hp_bonus, ki_bonus, atk_mult, def_mult, spd_mult, has_granted_move):
        char = Character(_sample_character_data())
        initial_max_hp = char.max_hp
        initial_defense = char.defense
        initial_attack = char.base_attack
        initial_speed = char.speed
        initial_moves = [m['name'] for m in char.moves]
        initial_equipped_count = len(char.equipped_items)

        item = {
            'id': 'test_equipment',
            'name': 'Item de Teste',
            'stat_bonuses': {'hp': hp_bonus, 'ki_max': ki_bonus},
            'stat_multipliers': {'attack': atk_mult, 'defense': def_mult, 'speed': spd_mult},
            'granted_moves': [{'name': 'Golpe Extra', 'ki_cost': 10, 'multiplier': 1.2, 'type': 'special'}] if has_granted_move else []
        }

        equip_success, _ = char.equip_item(item)
        self.assertTrue(equip_success)

        unequip_success, _ = char.unequip_item(item['id'])
        self.assertTrue(unequip_success)

        self.assertEqual(char.max_hp, initial_max_hp)
        self.assertEqual(char.defense, initial_defense)
        self.assertEqual(char.base_attack, initial_attack)
        self.assertEqual(char.speed, initial_speed)
        self.assertEqual([m['name'] for m in char.moves], initial_moves)
        self.assertEqual(len(char.equipped_items), initial_equipped_count)
        self.assertGreaterEqual(char.hp, 0)
        self.assertLessEqual(char.hp, char.max_hp)

    # ---------------------------------------------------------
    # to_dict -> load_state idempotente
    # ---------------------------------------------------------
    @given(
        target_hp=st.integers(min_value=0, max_value=120),
        target_ki=st.integers(min_value=0, max_value=120),
        senzu_qty=st.integers(min_value=0, max_value=10),
        capsule_qty=st.integers(min_value=0, max_value=10),
        equip_weighted=st.booleans(),
        transformed=st.booleans()
    )
    def test_to_dict_load_state_idempotence(self, target_hp, target_ki, senzu_qty, capsule_qty, equip_weighted, transformed):
        equip_db = {
            'weighted_clothing': {
                'id': 'weighted_clothing',
                'name': 'Roupas Pesadas',
                'stat_bonuses': {'hp': 20, 'ki_max': 0},
                'stat_multipliers': {'defense': 1.15, 'speed': 0.9}
            }
        }
        data = _sample_character_data(hp=100, ki_max=100)
        char = Character(data, initial_inventory={'senzu_bean': senzu_qty, 'ki_capsule': capsule_qty})

        if equip_weighted:
            char.equip_item(equip_db['weighted_clothing'])

        if transformed:
            char.ki = 100
            char.transform(data['transformations'][0])

        char.hp = min(target_hp, char.max_hp)
        char.ki = min(target_ki, char.max_ki)

        # 1ª serialização
        state1 = char.to_dict()

        # Restaura em nova instância
        restored1 = Character(data)
        success1, _ = restored1.load_state(state1, available_equipment=equip_db)
        self.assertTrue(success1)
        state2 = restored1.to_dict()

        self.assertEqual(state1, state2)

        # Restaura em 2ª instância a partir de state2 (idempotência)
        restored2 = Character(data)
        success2, _ = restored2.load_state(state2, available_equipment=equip_db)
        self.assertTrue(success2)
        state3 = restored2.to_dict()

        self.assertEqual(state2, state3)


if __name__ == '__main__':
    unittest.main()


import random

class Character:
    def __init__(self, data, initial_inventory=None):
        self.raw_name = data['name']
        self.name = data['name']
        self.raw_max_hp = data['hp']
        self.raw_attack = data['attack']
        self.raw_defense = data['defense']
        self.raw_max_ki = data['ki_max']
        self.raw_speed = data['speed']
        self.max_hp = self.raw_max_hp
        self.hp = self.max_hp
        self.base_attack = self.raw_attack
        self.defense = self.raw_defense
        self.max_ki = self.raw_max_ki
        self.ki = 0
        self.speed = self.raw_speed
        self.base_moves = list(data.get('moves', []))
        self.moves = list(self.base_moves)
        self.transformations = list(data.get('transformations', []))
        self.current_transformation = None
        self.ai_profile = data.get('ai_profile', 'tatico')
        self.equipped_items = []
        self.inventory = dict(initial_inventory) if initial_inventory else {}
        self.defensive_stance = None
        self.is_charging = False

    def is_alive(self):
        return self.hp > 0

    def equip_item(self, item_data):
        item_id = item_data.get('id', item_data.get('name'))
        if any(item.get('id', item.get('name')) == item_id for item in self.equipped_items):
            return False, {"reason": "already_equipped", "item_id": item_id, "item_name": item_data.get('name')}
        self.equipped_items.append(item_data)
        for move in item_data.get('granted_moves', []):
            if not any(m['name'] == move['name'] for m in self.moves):
                self.moves.append(move)
        self._recalculate_stats()
        return True, {"item_id": item_id, "item_name": item_data.get('name'), "granted_moves": item_data.get('granted_moves', [])}

    def unequip_item(self, item_id):
        item_to_remove = next((item for item in self.equipped_items if item.get('id', item.get('name')) == item_id), None)
        if not item_to_remove:
            return False, {"reason": "not_found", "item_id": item_id}
        self.equipped_items.remove(item_to_remove)
        granted_names = {m['name'] for m in item_to_remove.get('granted_moves', [])}
        self.moves = [m for m in self.moves if m['name'] not in granted_names]
        self._recalculate_stats()
        return True, {"item_id": item_id, "item_name": item_to_remove.get('name')}

    def use_consumable(self, item_id, item_data):
        current_qty = self.inventory.get(item_id, 0)
        if current_qty <= 0:
            return False, {"msg": f"Voce nao possui mais unidades de {item_data.get('name')}."}

        hp_restore_pct = item_data.get('hp_restore_pct', 0.0)
        hp_restore_fixed = item_data.get('hp_restore_fixed', 0)
        ki_restore_amount = item_data.get('ki_restore_amount', 0)

        hp_gain = int(self.max_hp * hp_restore_pct) + hp_restore_fixed
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + hp_gain)
        actual_hp_gain = self.hp - old_hp

        old_ki = self.ki
        self.ki = min(self.max_ki, self.ki + ki_restore_amount)
        actual_ki_gain = self.ki - old_ki
        self.inventory[item_id] -= 1

        return True, {
            "item_name": item_data.get('name'),
            "hp_gain": actual_hp_gain,
            "hp_now": self.hp,
            "max_hp": self.max_hp,
            "ki_gain": actual_ki_gain,
            "ki_now": self.ki,
            "max_ki": self.max_ki
        }

    def add_to_inventory(self, item_id, quantity=1):
        if quantity <= 0:
            return False, {"reason": "invalid_quantity", "item_id": item_id}
        self.inventory[item_id] = self.inventory.get(item_id, 0) + quantity
        return True, {"item_id": item_id, "quantity": quantity, "total": self.inventory[item_id]}

    def recover(self, hp_amount=0, ki_amount=0):
        old_hp = self.hp
        self.hp = min(self.max_hp, max(0, self.hp + hp_amount))
        actual_hp_gain = self.hp - old_hp

        old_ki = self.ki
        self.ki = min(self.max_ki, max(0, self.ki + ki_amount))
        actual_ki_gain = self.ki - old_ki

        return True, {
            "hp_gain": actual_hp_gain,
            "hp_now": self.hp,
            "max_hp": self.max_hp,
            "ki_gain": actual_ki_gain,
            "ki_now": self.ki,
            "max_ki": self.max_ki
        }

    def _recalculate_stats(self):
        hp_bonus = sum(item.get('stat_bonuses', {}).get('hp', 0) for item in self.equipped_items)
        ki_bonus = sum(item.get('stat_bonuses', {}).get('ki_max', 0) for item in self.equipped_items)
        item_atk_mult = 1.0
        item_def_mult = 1.0
        item_spd_mult = 1.0
        for item in self.equipped_items:
            mults = item.get('stat_multipliers', {})
            item_atk_mult *= mults.get('attack', 1.0)
            item_def_mult *= mults.get('defense', 1.0)
            item_spd_mult *= mults.get('speed', 1.0)

        trans_atk_mult = 1.0
        trans_def_mult = 1.0
        trans_spd_mult = 1.0
        if self.current_transformation:
            trans_data = next((t for t in self.transformations if t['name'] == self.current_transformation), None)
            if trans_data:
                t_mults = trans_data.get('stat_multipliers', {})
                trans_atk_mult = t_mults.get('attack', 1.0)
                trans_def_mult = t_mults.get('defense', 1.0)
                trans_spd_mult = t_mults.get('speed', 1.0)

        old_max_hp = self.max_hp
        self.max_hp = self.raw_max_hp + hp_bonus
        hp_diff = self.max_hp - old_max_hp
        if hp_diff > 0:
            self.hp += hp_diff
        self.hp = min(self.hp, self.max_hp)
        self.max_ki = self.raw_max_ki + ki_bonus
        self.ki = min(self.ki, self.max_ki)
        self.base_attack = int(self.raw_attack * item_atk_mult * trans_atk_mult)
        self.defense = int(self.raw_defense * item_def_mult * trans_def_mult)
        self.speed = int(self.raw_speed * item_spd_mult * trans_spd_mult)

    def defend(self, stance_type='block'):
        self.defensive_stance = stance_type
        return {"stance": stance_type, "name": self.name}

    def charge_ki(self):
        self.is_charging = True
        amount = random.randint(15, 30)
        self.ki = min(self.ki + amount, self.max_ki)
        return {"amount": amount, "ki_now": self.ki, "max_ki": self.max_ki, "name": self.name}

    def apply_incoming_damage(self, raw_damage, attacker, defense_cfg):
        stance = self.defensive_stance
        event = {"target": self.name, "stance": stance, "evaded": False, "damage_taken": 0, "reflected_damage": 0, "attacker_name": attacker.name}

        if stance == 'vanish':
            event["evaded"] = True
            return event

        if stance == 'dodge':
            dodge_chance = defense_cfg.get('dodge', {}).get('success_rate', 0.60)
            if random.random() <= dodge_chance:
                event["evaded"] = True
                return event

        if stance == 'counter':
            reduction = defense_cfg.get('counter', {}).get('damage_reduction', 0.30)
            effective_damage = max(1, int(raw_damage * (1.0 - (self.defense / 100) * reduction)))
            self.hp = max(0, self.hp - effective_damage)
            event["damage_taken"] = effective_damage
            
            counter_ratio = defense_cfg.get('counter', {}).get('counter_damage_ratio', 0.60)
            reflected_damage = max(1, int(effective_damage * counter_ratio))
            attacker.hp = max(0, attacker.hp - reflected_damage)
            event["reflected_damage"] = reflected_damage
            return event

        if stance == 'block':
            reduction = defense_cfg.get('block', {}).get('damage_reduction', 0.50)
            effective_damage = max(1, int(raw_damage * (1.0 - (self.defense / 100) * (1.0 + reduction))))
            self.hp = max(0, self.hp - effective_damage)
            event["damage_taken"] = effective_damage
            event["blocked"] = True
            return event

        effective_damage = max(1, int(raw_damage * (1.0 - (self.defense / 200))))
        self.hp = max(0, self.hp - effective_damage)
        event["damage_taken"] = effective_damage
        return event

    def execute_move(self, move, target, defense_cfg=None):
        cfg = defense_cfg or {}
        if move['type'] == 'basic':
            return self._basic_attack(target, move['name'], cfg)
        elif move['type'] == 'combo':
            return self._combo_attack(target, move, cfg)
        elif move['type'] == 'special':
            return self._special_attack(target, move, cfg)
        return False, {"msg": "Tipo de movimento invalido."}

    def _basic_attack(self, target, move_name, defense_cfg):
        raw_damage = random.randint(self.base_attack - 4, self.base_attack + 4)
        target_event = target.apply_incoming_damage(raw_damage, self, defense_cfg)
        return True, {"type": "basic", "attacker": self.name, "move_name": move_name, "target_event": target_event}

    def _combo_attack(self, target, move, defense_cfg):
        ki_cost = move.get('ki_cost', 0)
        if self.ki < ki_cost:
            return False, {"msg": f"Ki insuficiente. Custo: {ki_cost}", "ki_cost": ki_cost}

        self.ki -= ki_cost
        hits_total = move.get('hits', 3)
        hit_chance = move.get('hit_chance', 0.8)
        multiplier = move.get('multiplier', 0.5)

        successful_hits = 0
        total_damage = 0
        hit_results = []

        for i in range(1, hits_total + 1):
            if random.random() <= hit_chance:
                successful_hits += 1
                hit_damage = int(random.randint(self.base_attack - 2, self.base_attack + 2) * multiplier)
                total_damage += hit_damage
                hit_results.append(True)
            else:
                hit_results.append(False)

        target_event = None
        if total_damage > 0:
            target_event = target.apply_incoming_damage(total_damage, self, defense_cfg)

        return True, {
            "type": "combo", "attacker": self.name, "move_name": move['name'], 
            "hits_total": hits_total, "successful_hits": successful_hits, 
            "hit_results": hit_results, "target_event": target_event
        }

    def _special_attack(self, target, move, defense_cfg):
        ki_cost = move['ki_cost']
        multiplier = move['multiplier']
        move_name = move['name']

        if self.ki >= ki_cost:
            self.ki -= ki_cost
            raw_damage = int(random.randint(self.base_attack, self.base_attack + 8) * multiplier)
            target_event = target.apply_incoming_damage(raw_damage, self, defense_cfg)
            return True, {"type": "special", "attacker": self.name, "move_name": move_name, "target_event": target_event}
        return False, {"msg": f"Ki insuficiente. Custo: {ki_cost}", "ki_cost": ki_cost}

    def end_turn(self):
        self.defensive_stance = None
        self.is_charging = False

    def can_transform(self, trans):
        if self.current_transformation == trans['name']:
            return False, {"reason": "already_transformed", "current": self.current_transformation}
        if self.ki < trans['required_ki']:
            return False, {"reason": "insufficient_ki", "required_ki": trans['required_ki'], "current_ki": self.ki}
        hp_limit = trans.get('hp_threshold_pct', 1.0) * self.max_hp
        if self.hp > hp_limit:
            return False, {"reason": "hp_above_threshold", "hp_limit": hp_limit, "current_hp": self.hp}
        return True, {"reason": "ready"}

    def transform(self, trans):
        can, payload = self.can_transform(trans)
        if not can:
            return False, payload

        self.ki -= trans['required_ki']
        self.current_transformation = trans['name']
        old_name = self.name
        self.name = trans['name']
        self._recalculate_stats()

        return True, {
            "old_name": old_name, "new_name": self.name,
            "attack": self.base_attack, "defense": self.defense, "speed": self.speed
        }

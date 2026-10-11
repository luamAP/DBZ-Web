import random
import time

class Character:
    def __init__(self, data, initial_inventory=None):
        self.raw_name = data['name']
        self.name = data['name']

        # Atributos base imutaveis
        self.raw_max_hp = data['hp']
        self.raw_attack = data['attack']
        self.raw_defense = data['defense']
        self.raw_max_ki = data['ki_max']
        self.raw_speed = data['speed']

        # Atributos computados em tempo de execucao
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

        self.equipped_items = []
        self.inventory = dict(initial_inventory) if initial_inventory else {}
        self.defensive_stance = None
        self.is_charging = False

    def is_alive(self):
        return self.hp > 0

    def equip_item(self, item_data):
        item_id = item_data.get('id', item_data.get('name'))
        if any(item.get('id', item.get('name')) == item_id for item in self.equipped_items):
            return False, "Item ja equipado."

        self.equipped_items.append(item_data)

        for move in item_data.get('granted_moves', []):
            if not any(m['name'] == move['name'] for m in self.moves):
                self.moves.append(move)

        self._recalculate_stats()
        return True, f"{item_data.get('name')} equipado com sucesso!"

    def unequip_item(self, item_id):
        item_to_remove = next(
            (item for item in self.equipped_items if item.get('id', item.get('name')) == item_id),
            None
        )
        if not item_to_remove:
            return False, "Item nao encontrado nos equipamentos."

        self.equipped_items.remove(item_to_remove)

        granted_names = {m['name'] for m in item_to_remove.get('granted_moves', [])}
        self.moves = [m for m in self.moves if m['name'] not in granted_names]

        self._recalculate_stats()
        return True, f"{item_to_remove.get('name')} desequipado!"

    def use_consumable(self, item_id, item_data):
        current_qty = self.inventory.get(item_id, 0)
        if current_qty <= 0:
            return False, f"Voce nao possui mais unidades de {item_data.get('name')}."

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

        print(f"\n[ITEM] {self.name} usou {item_data.get('name')}!")
        if actual_hp_gain > 0:
            print(f" -> Recuperou {actual_hp_gain} HP! (Atual: {self.hp}/{self.max_hp})")
        if actual_ki_gain > 0:
            print(f" -> Recuperou {actual_ki_gain} Ki! (Atual: {self.ki}/{self.max_ki})")
        time.sleep(1)

        return True, "Item consumido com sucesso."

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
        stances_desc = {
            'block': "assume uma guarda de Bloqueio rigido!",
            'counter': "prepara os sentidos para um Contra-Ataque!",
            'dodge': "fica leve nos pes pronto para Esquivar!",
            'vanish': "concentra Ki para Teleporte / Esquiva Perfeita!"
        }
        print(f"\n{self.name} {stances_desc.get(stance_type, 'assume postura defensiva!')}")
        time.sleep(1)

    def charge_ki(self):
        self.is_charging = True
        amount = random.randint(15, 30)
        self.ki = min(self.ki + amount, self.max_ki)
        print(f"\n{self.name} concentra sua energia! HAAAAAAAA!")
        print(f"{self.name} recuperou {amount} de Ki. Ki Atual: {self.ki}/{self.max_ki}")
        time.sleep(1)

    def apply_incoming_damage(self, raw_damage, attacker, defense_cfg):
        stance = self.defensive_stance

        if stance == 'vanish':
            print(f"[!] {self.name} usou o Teleporte Instantaneo! Dano completamente evitado!")
            return 0

        if stance == 'dodge':
            dodge_chance = defense_cfg.get('dodge', {}).get('success_rate', 0.60)
            if random.random() <= dodge_chance:
                print(f"[!] {self.name} esquivou com agilidade acrobatica! Ataque desviado!")
                return 0
            else:
                print(f"[!] {self.name} tentou esquivar, mas foi pego!")

        if stance == 'counter':
            reduction = defense_cfg.get('counter', {}).get('damage_reduction', 0.30)
            effective_damage = max(1, int(raw_damage * (1.0 - (self.defense / 100) * reduction)))
            self.hp = max(0, self.hp - effective_damage)
            print(f"{self.name} suportou parte do golpe ({effective_damage} sofrido) e contra-ataca!")

            counter_ratio = defense_cfg.get('counter', {}).get('counter_damage_ratio', 0.60)
            reflected_damage = max(1, int(effective_damage * counter_ratio))
            attacker.hp = max(0, attacker.hp - reflected_damage)
            print(f"[REVIDE] {self.name} devolveu {reflected_damage} de dano contra {attacker.name}!")
            return effective_damage

        if stance == 'block':
            reduction = defense_cfg.get('block', {}).get('damage_reduction', 0.50)
            effective_damage = max(1, int(raw_damage * (1.0 - (self.defense / 100) * (1.0 + reduction))))
            self.hp = max(0, self.hp - effective_damage)
            print(f"{self.name} bloqueou firmemente! Dano atenuado para {effective_damage}.")
            return effective_damage

        effective_damage = max(1, int(raw_damage * (1.0 - (self.defense / 200))))
        self.hp = max(0, self.hp - effective_damage)
        print(f"Acerto direto em {self.name}! Causou {effective_damage} de dano.")
        return effective_damage

    def execute_move(self, move, target, defense_cfg=None):
        cfg = defense_cfg or {}
        if move['type'] == 'basic':
            return self._basic_attack(target, move['name'], cfg)
        elif move['type'] == 'combo':
            return self._combo_attack(target, move, cfg)
        elif move['type'] == 'special':
            return self._special_attack(target, move, cfg)
        return False

    def _basic_attack(self, target, move_name, defense_cfg):
        print(f"\n{self.name} avanca com {move_name}!")
        time.sleep(0.8)
        raw_damage = random.randint(self.base_attack - 4, self.base_attack + 4)
        target.apply_incoming_damage(raw_damage, self, defense_cfg)
        time.sleep(1)
        return True

    def _combo_attack(self, target, move, defense_cfg):
        ki_cost = move.get('ki_cost', 0)
        if self.ki < ki_cost:
            print(f"\n{self.name} tenta um combo, mas nao tem Ki suficiente! (Custo: {ki_cost})")
            time.sleep(1)
            return False

        self.ki -= ki_cost
        hits_total = move.get('hits', 3)
        hit_chance = move.get('hit_chance', 0.8)
        multiplier = move.get('multiplier', 0.5)

        print(f"\n{self.name} inicia uma investida: {move['name']}!")
        time.sleep(1)

        successful_hits = 0
        total_damage = 0

        for i in range(1, hits_total + 1):
            if random.random() <= hit_chance:
                successful_hits += 1
                hit_damage = int(random.randint(self.base_attack - 2, self.base_attack + 2) * multiplier)
                total_damage += hit_damage
                print(f" Golpe {i}: CONECTOU!")
            else:
                print(f" Golpe {i}: ERROU!")
            time.sleep(0.3)

        if total_damage > 0:
            print(f"Sequencia conectada ({successful_hits}/{hits_total} acertos):")
            target.apply_incoming_damage(total_damage, self, defense_cfg)
        else:
            print(f"{target.name} esquivou de todos os golpes do combo!")
        time.sleep(1)
        return True

    def _special_attack(self, target, move, defense_cfg):
        ki_cost = move['ki_cost']
        multiplier = move['multiplier']
        move_name = move['name']

        if self.ki >= ki_cost:
            self.ki -= ki_cost
            raw_damage = int(random.randint(self.base_attack, self.base_attack + 8) * multiplier)
            print(f"\n{self.name} reune uma quantidade massiva de energia...")
            time.sleep(1)
            print(f"{self.name}: {move_name.upper()}!!!")
            time.sleep(1)
            target.apply_incoming_damage(raw_damage, self, defense_cfg)
            time.sleep(1)
            return True
        else:
            print(f"\n{self.name} tenta usar {move_name}, mas nao tem Ki suficiente! (Custo: {ki_cost})")
            time.sleep(1)
            return False

    def end_turn(self):
        self.defensive_stance = None
        self.is_charging = False

    def can_transform(self, trans):
        if self.current_transformation == trans['name']:
            return False, "Ja esta transformado nesta forma."
        if self.ki < trans['required_ki']:
            return False, f"Ki insuficiente (Requer {trans['required_ki']} Ki)."
        hp_limit = trans.get('hp_threshold_pct', 1.0) * self.max_hp
        if self.hp > hp_limit:
            return False, f"HP muito alto para liberar esta forma (Exige HP <= {int(hp_limit)})."
        return True, "Apto."

    def transform(self, trans):
        can, reason = self.can_transform(trans)
        if not can:
            print(f"\n[!] Nao foi possivel transformar: {reason}")
            time.sleep(1)
            return False

        self.ki -= trans['required_ki']
        self.current_transformation = trans['name']
        old_name = self.name
        self.name = trans['name']

        self._recalculate_stats()

        print(f"\n{'*'*50}")
        print(f"{old_name} ROMPE SEUS LIMITES E SE TRANSFORMA EM {self.name.upper()}!")
        print(f"Novos Atributos -> Ataque: {self.base_attack} | Defesa: {self.defense} | Vel: {self.speed}")
        print(f"{'*'*50}")
        time.sleep(1.5)
        return True

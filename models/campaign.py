import random


class Campaign:
    def __init__(self, data):
        self.id = data.get('id', 'default_campaign')
        self.name = data.get('name', 'Modo Campanha')
        self.description = data.get('description', '')
        self.stages = list(data.get('stages', []))
        self.current_stage_index = 0

    def get_current_stage(self):
        if 0 <= self.current_stage_index < len(self.stages):
            return self.stages[self.current_stage_index]
        return None

    def is_completed(self):
        return self.current_stage_index >= len(self.stages)

    def advance_stage(self):
        if self.is_completed():
            return False, {"reason": "already_completed", "current_stage_index": self.current_stage_index}
        self.current_stage_index += 1
        return True, {
            "current_stage_index": self.current_stage_index,
            "total_stages": len(self.stages),
            "is_completed": self.is_completed()
        }

    def to_dict(self):
        return {
            "campaign_id": self.id,
            "current_stage_index": self.current_stage_index,
            "is_completed": self.is_completed()
        }

    def load_state(self, state):
        if not isinstance(state, dict):
            return False, {"reason": "invalid_state_format"}
        if "current_stage_index" in state:
            idx = int(state["current_stage_index"])
            self.current_stage_index = max(0, min(idx, len(self.stages)))
            return True, {
                "current_stage_index": self.current_stage_index,
                "is_completed": self.is_completed()
            }
        return False, {"reason": "missing_stage_index"}

    @staticmethod
    def resolve_drops(stage_data, rng=random.random):
        dropped = []
        for drop_cfg in stage_data.get('drop_table', []):
            chance = drop_cfg.get('chance', 0.0)
            roll = rng()
            if roll <= chance:
                dropped.append({
                    "item_id": drop_cfg.get('item_id'),
                    "item_type": drop_cfg.get('item_type', 'consumable'),
                    "quantity": drop_cfg.get('quantity', 1)
                })
        return dropped

    @staticmethod
    def calculate_stage_recovery(player, stage_data):
        recovery_cfg = stage_data.get('recovery', {})
        hp_pct = recovery_cfg.get('hp_pct', 0.0)
        hp_fixed = recovery_cfg.get('hp_fixed', 0)
        ki_bonus = recovery_cfg.get('ki_bonus', 0)

        hp_amount = int(player.max_hp * hp_pct) + hp_fixed
        return hp_amount, ki_bonus

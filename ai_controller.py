import random
import time

def execute_ai_turn(ai_character, target, defense_cfg=None):
    """
    IA genérica que avalia os golpes disponíveis lidos do YAML
    e toma decisões baseadas no estado atual da luta.
    """
    cfg = defense_cfg or {}
    print(f"\n--- Turno de {ai_character.name} ---")
    time.sleep(1)
    
    # 1. Avalia necessidade defensiva crítica
    if ai_character.hp < (ai_character.max_hp * 0.25) and target.ki >= 30:
        if random.random() > 0.35:
            # Seleciona postura de acordo com o Ki disponível
            if ai_character.ki >= cfg.get('vanish', {}).get('ki_cost', 25):
                ai_character.ki -= cfg['vanish']['ki_cost']
                ai_character.defend('vanish')
            elif ai_character.ki >= cfg.get('counter', {}).get('ki_cost', 10):
                ai_character.ki -= cfg['counter']['ki_cost']
                ai_character.defend('counter')
            else:
                ai_character.defend('block')
            return

    # 2. Avalia golpes especiais disponíveis
    available_specials = [m for m in ai_character.moves if m['type'] == 'special' and ai_character.ki >= m['ki_cost']]
    if available_specials and random.random() > 0.4:
        best_special = sorted(available_specials, key=lambda x: x['ki_cost'])[-1]
        ai_character.execute_move(best_special, target, cfg)
        return

    # 3. Avalia combos disponíveis
    available_combos = [m for m in ai_character.moves if m['type'] == 'combo' and ai_character.ki >= m.get('ki_cost', 0)]
    if available_combos and random.random() > 0.4:
        best_combo = sorted(available_combos, key=lambda x: x.get('ki_cost', 0))[-1]
        ai_character.execute_move(best_combo, target, cfg)
        return

    # 4. Decisão entre ataque básico ou carregar Ki
    if ai_character.ki < 40 and random.random() > 0.3:
        ai_character.charge_ki()
    else:
        basic_move = next((m for m in ai_character.moves if m['type'] == 'basic'), ai_character.moves[0])
        ai_character.execute_move(basic_move, target, cfg)

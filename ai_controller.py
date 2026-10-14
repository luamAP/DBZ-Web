import random

def execute_ai_turn(ai_character, target, defense_cfg=None):
    """
    Decide a melhor acao para a IA e retorna uma tupla (action_type, event_data)
    para renderizacao na camada de apresentacao.
    """
    cfg = defense_cfg or {}

    # 1. Avalia necessidade defensiva critica
    if ai_character.hp < (ai_character.max_hp * 0.25) and target.ki >= 30:
        if random.random() > 0.35:
            vanish_cost = cfg.get('vanish', {}).get('ki_cost', 25)
            counter_cost = cfg.get('counter', {}).get('ki_cost', 10)

            if ai_character.ki >= vanish_cost:
                ai_character.ki -= vanish_cost
                event_data = ai_character.defend('vanish')
                return ('defend', event_data)
            elif ai_character.ki >= counter_cost:
                ai_character.ki -= counter_cost
                event_data = ai_character.defend('counter')
                return ('defend', event_data)
            else:
                event_data = ai_character.defend('block')
                return ('defend', event_data)

    # 2. Avalia golpes especiais disponiveis
    available_specials = [m for m in ai_character.moves if m['type'] == 'special' and ai_character.ki >= m.get('ki_cost', 0)]
    if available_specials and random.random() > 0.4:
        best_special = sorted(available_specials, key=lambda x: x.get('ki_cost', 0))[-1]
        success, event_data = ai_character.execute_move(best_special, target, cfg)
        if success:
            return ('move', event_data)

    # 3. Avalia combos disponiveis
    available_combos = [m for m in ai_character.moves if m['type'] == 'combo' and ai_character.ki >= m.get('ki_cost', 0)]
    if available_combos and random.random() > 0.4:
        best_combo = sorted(available_combos, key=lambda x: x.get('ki_cost', 0))[-1]
        success, event_data = ai_character.execute_move(best_combo, target, cfg)
        if success:
            return ('move', event_data)

    # 4. Decisao entre ataque basico ou carregar Ki
    if ai_character.ki < 40 and random.random() > 0.3:
        event_data = ai_character.charge_ki()
        return ('charge', event_data)

    basic_move = next((m for m in ai_character.moves if m['type'] == 'basic'), ai_character.moves[0])
    success, event_data = ai_character.execute_move(basic_move, target, cfg)
    return ('move', event_data)

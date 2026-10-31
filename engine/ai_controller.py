import random


def execute_ai_turn(ai_character, target, defense_cfg=None, ai_profiles_cfg=None):
    """
    Decide a melhor acao para a IA e retorna uma tupla (action_type, event_data)
    para renderizacao na camada de apresentacao, respeitando o perfil comportamental
    configurado nos dados (agressivo, defensivo, tatico).
    """
    cfg = defense_cfg or {}
    profiles = ai_profiles_cfg or {}

    profile_name = getattr(ai_character, 'ai_profile', 'tatico')
    profile = profiles.get(profile_name, profiles.get('tatico', {}))

    special_bias = profile.get('special_bias', 0.5)
    combo_bias = profile.get('combo_bias', 0.5)
    charge_ki_threshold = profile.get('charge_ki_threshold', 40)
    defend_hp_threshold = profile.get('defend_hp_threshold', 0.30)
    defense_bias = profile.get('defense_bias', 0.50)

    # 1. Se o perfil for tatico/defensivo, prioriza evolucao tatica (transformacao)
    if profile_name != 'agressivo' and hasattr(ai_character, 'transformations') and not ai_character.current_transformation:
        for trans in ai_character.transformations:
            can, _ = ai_character.can_transform(trans)
            if can:
                success, ev = ai_character.transform(trans)
                if success:
                    return ('transform', ev)

    # 2. Avalia necessidade defensiva de acordo com o perfil
    if ai_character.hp <= (ai_character.max_hp * defend_hp_threshold) and target.ki >= 20:
        if random.random() < defense_bias:
            vanish_cost = cfg.get('vanish', {}).get('ki_cost', 25)
            counter_cost = cfg.get('counter', {}).get('ki_cost', 10)
            dodge_cost = cfg.get('dodge', {}).get('ki_cost', 5)

            if ai_character.ki >= vanish_cost:
                ai_character.ki -= vanish_cost
                event_data = ai_character.defend('vanish')
                return ('defend', event_data)
            elif ai_character.ki >= counter_cost:
                ai_character.ki -= counter_cost
                event_data = ai_character.defend('counter')
                return ('defend', event_data)
            elif ai_character.ki >= dodge_cost:
                ai_character.ki -= dodge_cost
                event_data = ai_character.defend('dodge')
                return ('defend', event_data)
            else:
                event_data = ai_character.defend('block')
                return ('defend', event_data)

    # 3. Avalia golpes especiais disponiveis
    available_specials = [m for m in ai_character.moves if m.get('type') == 'special' and ai_character.ki >= m.get('ki_cost', 0)]
    if available_specials and random.random() < special_bias:
        best_special = sorted(available_specials, key=lambda x: x.get('ki_cost', 0))[-1]
        success, event_data = ai_character.execute_move(best_special, target, cfg)
        if success:
            return ('move', event_data)

    # 4. Transformacao para perfil agressivo se especiais nao foram priorizados
    if profile_name == 'agressivo' and hasattr(ai_character, 'transformations') and not ai_character.current_transformation:
        for trans in ai_character.transformations:
            can, _ = ai_character.can_transform(trans)
            if can:
                success, ev = ai_character.transform(trans)
                if success:
                    return ('transform', ev)

    # 5. Avalia necessidade de recarregar Ki antes de gastar recursos em combos
    if ai_character.ki < charge_ki_threshold:
        event_data = ai_character.charge_ki()
        return ('charge', event_data)

    # 6. Avalia combos disponiveis
    available_combos = [m for m in ai_character.moves if m.get('type') == 'combo' and ai_character.ki >= m.get('ki_cost', 0)]
    if available_combos and random.random() < combo_bias:
        best_combo = sorted(available_combos, key=lambda x: x.get('ki_cost', 0))[-1]
        success, event_data = ai_character.execute_move(best_combo, target, cfg)
        if success:
            return ('move', event_data)

    # 7. Golpe basico como acao padrao
    basic_move = next((m for m in ai_character.moves if m.get('type') == 'basic'), ai_character.moves[0])
    success, event_data = ai_character.execute_move(basic_move, target, cfg)
    return ('move', event_data)

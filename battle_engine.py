import time
from ai_controller import execute_ai_turn
from models import Team


def print_status(player, enemy):
    print("\n" + "=" * 45)
    print(f"{player.name}: HP [{player.hp}/{player.max_hp}] | KI [{player.ki}/{player.max_ki}]")
    print(f"{enemy.name}: HP [{enemy.hp}/{enemy.max_hp}] | KI [{enemy.ki}/{enemy.max_ki}]")
    print("=" * 45)


def manage_equipment_menu(character, available_items):
    item_list = list(available_items.values())

    while True:
        print(f"\n--- EQUIPAMENTOS: {character.name} ---")
        print(f"Atributos atuais: ATK {character.base_attack} | DEF {character.defense} | SPD {character.speed} | HP {character.hp}/{character.max_hp}")
        print("\nItens Atualmente Equipados:")
        if character.equipped_items:
            for eq in character.equipped_items:
                print(f" - [X] {eq['name']}")
        else:
            print(" (Nenhum item equipado)")

        print("\nCapsulas Disponiveis:")
        for idx, item in enumerate(item_list, 1):
            is_eq = any(eq.get('id', eq.get('name')) == item.get('id', item.get('name')) for eq in character.equipped_items)
            status = "[Equipado]" if is_eq else "[Livre]"
            print(f"{idx}. {item['name']} {status} - {item.get('description', '')}")

        back_opt = len(item_list) + 1
        print(f"{back_opt}. Concluir e Voltar")

        try:
            choice = int(input(f"Selecione uma opcao (1-{back_opt}): "))
            if 1 <= choice <= len(item_list):
                selected_item = item_list[choice - 1]
                item_id = selected_item.get('id', selected_item.get('name'))
                is_eq = any(eq.get('id', eq.get('name')) == item_id for eq in character.equipped_items)

                if is_eq:
                    success, ev = character.unequip_item(item_id)
                    if success:
                        print(f"\n[!] {ev['item_name']} desequipado!")
                    else:
                        print(f"\n[!] Falha ao desequipar: {ev.get('reason')}")
                else:
                    success, ev = character.equip_item(selected_item)
                    if success:
                        print(f"\n[!] {ev['item_name']} equipado com sucesso!")
                    else:
                        reasons = {
                            "already_equipped": "Item ja equipado."
                        }
                        print(f"\n[!] Falha ao equipar: {reasons.get(ev.get('reason'), ev.get('reason'))}")
            elif choice == back_opt:
                break
            else:
                print("Opcao invalida.")
        except ValueError:
            print("Digite um numero valido.")


def get_consumable_choice(player, consumables_cfg):
    usable_items = [
        (item_id, item_data)
        for item_id, item_data in consumables_cfg.items()
        if player.inventory.get(item_id, 0) > 0
    ]

    if not usable_items:
        print("\n[!] Nenhum consumivel disponivel no inventario!")
        return None

    print("\n--- Inventario de Consumiveis ---")
    for idx, (item_id, item_data) in enumerate(usable_items, 1):
        qty = player.inventory.get(item_id, 0)
        print(f"{idx}. {item_data['name']} (x{qty}) - {item_data.get('description', '')}")
    back_opt = len(usable_items) + 1
    print(f"{back_opt}. Voltar")

    while True:
        try:
            choice = int(input(f"Selecione o item (1-{back_opt}): "))
            if 1 <= choice <= len(usable_items):
                return usable_items[choice - 1]
            elif choice == back_opt:
                return None
            print("Opcao invalida.")
        except ValueError:
            print("Digite um numero valido.")


def get_defense_choice(player, defense_cfg):
    print("\n--- Opcoes de Defesa ---")
    print("1. Bloqueio Simples (0 Ki) - Reduz dano significativamente")
    print(f"2. Contra-Ataque ({defense_cfg['counter']['ki_cost']} Ki) - Reduz dano e devolve parte do impacto")
    print(f"3. Esquiva ({defense_cfg['dodge']['ki_cost']} Ki) - {int(defense_cfg['dodge']['success_rate'] * 100)}% de chance de evitar dano")
    print(f"4. Teleporte Perfeito ({defense_cfg['vanish']['ki_cost']} Ki) - Evita 100% do dano")
    print("5. Voltar")

    while True:
        try:
            choice = int(input("Selecione sua manobra (1-5): "))
            if choice == 1:
                return 'block'
            elif choice == 2:
                cost = defense_cfg['counter']['ki_cost']
                if player.ki < cost:
                    print(f"Ki insuficiente para Contra-Ataque! (Requer {cost} Ki)")
                    continue
                player.ki -= cost
                return 'counter'
            elif choice == 3:
                cost = defense_cfg['dodge']['ki_cost']
                if player.ki < cost:
                    print(f"Ki insuficiente para Esquiva! (Requer {cost} Ki)")
                    continue
                player.ki -= cost
                return 'dodge'
            elif choice == 4:
                cost = defense_cfg['vanish']['ki_cost']
                if player.ki < cost:
                    print(f"Ki insuficiente para Teleporte! (Requer {cost} Ki)")
                    continue
                player.ki -= cost
                return 'vanish'
            elif choice == 5:
                return None
            print("Opcao invalida.")
        except ValueError:
            print("Digite um numero valido.")


def get_transformation_choice(player):
    print("\n--- Formas Disponiveis ---")
    for idx, trans in enumerate(player.transformations, 1):
        status = " (ATIVA)" if player.current_transformation == trans['name'] else ""
        print(f"{idx}. {trans['name']} [Custo: {trans['required_ki']} Ki]{status}")
    back_opt = len(player.transformations) + 1
    print(f"{back_opt}. Voltar")

    while True:
        try:
            choice = int(input(f"Selecione a forma (1-{back_opt}): "))
            if 1 <= choice <= len(player.transformations):
                return player.transformations[choice - 1]
            elif choice == back_opt:
                return None
            print("Opcao invalida.")
        except ValueError:
            print("Digite um numero valido.")


def get_team_switch_choice(player_team):
    bench = player_team.get_bench_members()
    if not bench:
        print("\n[!] Nao ha outros guerreiros disponiveis na reserva!")
        return None

    print("\n--- Guerreiros na Reserva ---")
    for num, (orig_idx, member) in enumerate(bench, 1):
        print(f"{num}. {member.name} (HP: {member.hp}/{member.max_hp} | KI: {member.ki}/{member.max_ki})")
    back_opt = len(bench) + 1
    print(f"{back_opt}. Voltar")

    while True:
        try:
            choice = int(input(f"Selecione o substituto (1-{back_opt}): "))
            if 1 <= choice <= len(bench):
                return bench[choice - 1][0]
            elif choice == back_opt:
                return None
            print("Opcao invalida.")
        except ValueError:
            print("Digite um numero valido.")


def get_player_choice(player, has_team_bench=False):
    print("\nOpcoes de Acao:")
    for idx, move in enumerate(player.moves, 1):
        ki_req = f"({move['ki_cost']} Ki)"
        print(f"{idx}. {move['name']} {ki_req}")

    offset = len(player.moves)
    charge_opt = offset + 1
    defend_opt = offset + 2
    item_opt = offset + 3
    transform_opt = offset + 4 if player.transformations else None

    current_max = offset + 3
    if transform_opt:
        current_max = transform_opt

    switch_opt = current_max + 1 if has_team_bench else None
    if switch_opt:
        current_max = switch_opt

    print(f"{charge_opt}. Carregar Ki")
    print(f"{defend_opt}. Defender")
    print(f"{item_opt}. Usar Item")
    if transform_opt:
        print(f"{transform_opt}. Transformar")
    if switch_opt:
        print(f"{switch_opt}. Trocar Lutador (Tag Team)")

    while True:
        try:
            choice = int(input(f"Selecione (1-{current_max}): "))
            if 1 <= choice <= current_max:
                return choice, offset, charge_opt, defend_opt, item_opt, transform_opt, switch_opt
            print("Escolha invalida.")
        except ValueError:
            print("Digite um numero valido.")


def process_combat_event(event):
    if not event:
        return
    t_event = event.get("target_event")

    if event.get("type") == "basic":
        print(f"\n{event['attacker']} avanca com {event['move_name']}!")
        time.sleep(0.8)
    elif event.get("type") == "combo":
        print(f"\n{event['attacker']} inicia uma investida: {event['move_name']}!")
        time.sleep(1)
        for i, hit in enumerate(event.get('hit_results', []), 1):
            if hit:
                print(f" Golpe {i}: CONECTOU!")
            else:
                print(f" Golpe {i}: ERROU!")
            time.sleep(0.3)
        if event.get('successful_hits', 0) > 0:
            print(f"Sequencia conectada ({event['successful_hits']}/{event['hits_total']} acertos):")
        else:
            print("O alvo esquivou de todos os golpes do combo!")
    elif event.get("type") == "special":
        print(f"\n{event['attacker']} reune uma quantidade massiva de energia...")
        time.sleep(1)
        print(f"{event['attacker']}: {event['move_name'].upper()}!!!")
        time.sleep(1)

    if t_event:
        if t_event.get("evaded"):
            if t_event.get("stance") == "vanish":
                print(f"[!] {t_event['target']} usou o Teleporte Instantaneo! Dano completamente evitado!")
            elif t_event.get("stance") == "dodge":
                print(f"[!] {t_event['target']} esquivou com agilidade acrobatica! Ataque desviado!")
        else:
            if t_event.get("stance") == "dodge":
                print(f"[!] {t_event['target']} tentou esquivar, mas foi pego!")
            elif t_event.get("stance") == "counter":
                print(f"{t_event['target']} suportou parte do golpe ({t_event['damage_taken']} sofrido) e contra-ataca!")
                print(f"[REVIDE] {t_event['target']} devolveu {t_event['reflected_damage']} de dano contra {t_event['attacker_name']}!")
            elif t_event.get("blocked"):
                print(f"{t_event['target']} bloqueou firmemente! Dano atenuado para {t_event['damage_taken']}.")
            else:
                print(f"Acerto direto em {t_event['target']}! Causou {t_event['damage_taken']} de dano.")
    time.sleep(1)


def render_action_event(action_type, ev_data):
    """Renderiza eventos de ação genéricos para qualquer combatente."""
    if action_type == 'move':
        process_combat_event(ev_data)
    elif action_type == 'charge':
        print(f"\n{ev_data['name']} concentra sua energia! HAAAAAAAA!")
        print(f"{ev_data['name']} recuperou {ev_data['amount']} de Ki. Ki Atual: {ev_data['ki_now']}/{ev_data['max_ki']}")
        time.sleep(1)
    elif action_type == 'defend':
        stances_desc = {
            'block': "assume uma guarda de Bloqueio rigido!",
            'counter': "prepara os sentidos para um Contra-Ataque!",
            'dodge': "fica leve nos pes pronto para Esquivar!",
            'vanish': "concentra Ki para Teleporte / Esquiva Perfeita!"
        }
        print(f"\n{ev_data['name']} {stances_desc.get(ev_data['stance'], 'assume postura defensiva!')}")
        time.sleep(1)
    elif action_type == 'transform':
        print(f"\n{ev_data['old_name']} atinge um novo nivel de poder!")
        print(f"Transformacao: {ev_data['new_name']}! (ATK: {ev_data['attack']} | DEF: {ev_data['defense']} | SPD: {ev_data['speed']})")
        time.sleep(1)


def battle_team(player_team, enemy_team, defense_cfg=None, consumables_cfg=None, ai_profiles_cfg=None):
    cfg_def = defense_cfg or {}
    cfg_cons = consumables_cfg or {}
    print("\n" * 5)
    print(f"=== BATALHA: {player_team.name} vs {enemy_team.name}! ===")
    time.sleep(1.5)

    while player_team.has_alive_members() and enemy_team.has_alive_members():
        player = player_team.active_member
        enemy = enemy_team.active_member
        turn_order = [player, enemy] if player.speed >= enemy.speed else [enemy, player]

        for combatant in turn_order:
            if not player_team.has_alive_members() or not enemy_team.has_alive_members():
                break

            current_player = player_team.active_member
            current_enemy = enemy_team.active_member

            if combatant == current_player and current_player.is_alive():
                print_status(current_player, current_enemy)
                print(f"\n--- Seu Turno ({current_player.name}) ---")

                has_bench = len(player_team.get_bench_members()) > 0
                valid_turn = False
                while not valid_turn:
                    choice_data = get_player_choice(current_player, has_bench)
                    choice, total_moves, charge_opt, defend_opt, item_opt, transform_opt, switch_opt = choice_data

                    if choice <= total_moves:
                        move = current_player.moves[choice - 1]
                        success, ev_data = current_player.execute_move(move, current_enemy, cfg_def)
                        if success:
                            render_action_event('move', ev_data)
                            valid_turn = True
                        else:
                            print(f"\n[!] {ev_data.get('msg')}")
                    elif choice == charge_opt:
                        ev_data = current_player.charge_ki()
                        render_action_event('charge', ev_data)
                        valid_turn = True
                    elif choice == defend_opt:
                        stance = get_defense_choice(current_player, cfg_def)
                        if stance:
                            ev_data = current_player.defend(stance)
                            render_action_event('defend', ev_data)
                            valid_turn = True
                    elif choice == item_opt:
                        item_selection = get_consumable_choice(current_player, cfg_cons)
                        if item_selection:
                            item_id, item_data = item_selection
                            success, ev_data = current_player.use_consumable(item_id, item_data)
                            if success:
                                print(f"\n[ITEM] {current_player.name} usou {ev_data['item_name']}!")
                                if ev_data['hp_gain'] > 0:
                                    print(f" -> Recuperou {ev_data['hp_gain']} HP! (Atual: {ev_data['hp_now']}/{ev_data['max_hp']})")
                                if ev_data['ki_gain'] > 0:
                                    print(f" -> Recuperou {ev_data['ki_gain']} Ki! (Atual: {ev_data['ki_now']}/{ev_data['max_ki']})")
                                time.sleep(1)
                                valid_turn = True
                            else:
                                print(f"\n[!] {ev_data.get('msg')}")
                    elif transform_opt and choice == transform_opt:
                        trans = get_transformation_choice(current_player)
                        if trans:
                            success, ev_data = current_player.transform(trans)
                            if success:
                                print(f"\n{'*'*50}")
                                print(f"{ev_data['old_name']} ROMPE SEUS LIMITES E SE TRANSFORMA EM {ev_data['new_name'].upper()}!")
                                print(f"Novos Atributos -> Ataque: {ev_data['attack']} | Defesa: {ev_data['defense']} | Vel: {ev_data['speed']}")
                                print(f"{'*'*50}")
                                time.sleep(1.5)
                                valid_turn = True
                            else:
                                trans_errors = {
                                    "already_transformed": f"Ja esta transformado nesta forma ({ev_data.get('current')}).",
                                    "insufficient_ki": f"Ki insuficiente (Requer {ev_data.get('required_ki')} Ki, atual: {ev_data.get('current_ki')}).",
                                    "hp_above_threshold": f"HP muito alto para liberar esta forma (Exige HP <= {int(ev_data.get('hp_limit', 0))})."
                                }
                                err_msg = trans_errors.get(ev_data.get('reason'), ev_data.get('msg', 'Falha na transformacao.'))
                                print(f"\n[!] Nao foi possivel transformar: {err_msg}")
                                time.sleep(1)
                    elif switch_opt and choice == switch_opt:
                        sub_idx = get_team_switch_choice(player_team)
                        if sub_idx is not None:
                            success, ev_data = player_team.switch_member(sub_idx)
                            if success:
                                print(f"\n[TAG TEAM] Troca realizada! {ev_data['old_name']} recua e {ev_data['new_name']} assume a arena!")
                                valid_turn = True
                            else:
                                switch_errors = {
                                    "invalid_index": "Indice de lutador invalido.",
                                    "already_active": "Este lutador ja esta em combate!",
                                    "is_dead": "Nao e possivel selecionar um combatente derrotado!"
                                }
                                print(f"\n[TAG TEAM] Falha: {switch_errors.get(ev_data.get('reason'), ev_data.get('reason'))}")

            elif combatant == current_enemy and current_enemy.is_alive():
                print_status(current_player, current_enemy)
                print(f"\n--- Turno de {current_enemy.name} ---")
                time.sleep(1)
                ai_action = execute_ai_turn(current_enemy, current_player, cfg_def, ai_profiles_cfg)
                if ai_action:
                    action_type, ev_data = ai_action
                    render_action_event(action_type, ev_data)

            if not current_enemy.is_alive() and enemy_team.has_alive_members():
                print(f"\n[!] {current_enemy.name} foi derrotado!")
                switched, ev_data = enemy_team.auto_switch_next_alive()
                if switched:
                    print(f"[!] {ev_data['new_name']} assume a luta pelo adversario!")
                time.sleep(1)

            if not current_player.is_alive() and player_team.has_alive_members():
                print(f"\n[!] {current_player.name} caiu!")
                bench = player_team.get_bench_members()
                if len(bench) == 1:
                    _, ev_data = player_team.switch_member(bench[0][0])
                    print(f"[!] {ev_data['new_name']} entra imediatamente no combate!")
                else:
                    print("Selecione o proximo combatente para assumir o turno:")
                    chosen_idx = None
                    while chosen_idx is None:
                        chosen_idx = get_team_switch_choice(player_team)
                    _, ev_data = player_team.switch_member(chosen_idx)
                    print(f"[!] {ev_data['new_name']} entra no combate!")
                time.sleep(1)

            combatant.end_turn()
            time.sleep(1.2)

    print("\n" + "!" * 45)
    if player_team.has_alive_members():
        print(f"{player_team.name} VENCEU! A Terra esta salva por enquanto.")
    else:
        print(f"{enemy_team.name} VENCEU... O universo esta condenado.")
    print("!" * 45)
    return player_team.has_alive_members()


def battle(player, enemy, defense_cfg=None, consumables_cfg=None, ai_profiles_cfg=None):
    p_team = Team(player.name, [player])
    e_team = Team(enemy.name, [enemy])
    return battle_team(p_team, e_team, defense_cfg, consumables_cfg, ai_profiles_cfg)


def run_campaign(player, campaign_cfg, characters_db, items_db, defense_cfg=None, consumables_cfg=None, ai_profiles_cfg=None, campaign_instance=None):
    from models import Campaign, Character
    from data_loader import save_game_state

    campaign = campaign_instance if campaign_instance is not None else Campaign(campaign_cfg)
    print("\n" + "=" * 55)
    print(f"MODO CAMPANHA: {campaign.name.upper()}")
    if campaign.description:
        print(f"{campaign.description}")
    print("=" * 55)

    total_stages = len(campaign.stages)

    while not campaign.is_completed():
        stage_num = campaign.current_stage_index + 1
        stage = campaign.get_current_stage()
        enemy_name = stage.get('enemy')
        enemy_data = characters_db.get(enemy_name)
        if not enemy_data:
            print(f"\n[ERRO] Oponente '{enemy_name}' nao encontrado nos dados de personagens!")
            return False

        enemy = Character(enemy_data)

        print("\n" + "#" * 50)
        print(f"FASE {stage_num}/{total_stages}: {stage.get('name', enemy.name)}")
        print(f"Oponente: {enemy.name} (HP: {enemy.max_hp} | KI: {enemy.max_ki})")
        print("#" * 50)
        time.sleep(1)

        won = battle(player, enemy, defense_cfg, consumables_cfg, ai_profiles_cfg)
        if not won or not player.is_alive():
            print(f"\n[FIM DE JOGO] {player.name} foi superado na Fase {stage_num}. A campanha terminou.")
            return False

        print(f"\n[VITORIA] Fase {stage_num} concluida com exito!")

        # Processar drops
        dropped_items = campaign.resolve_drops(stage)
        if dropped_items:
            print("\n--- RECOMPENSAS DE COMBATE (DROPS) ---")
            for drop in dropped_items:
                item_id = drop['item_id']
                item_type = drop.get('item_type', 'consumable')
                qty = drop.get('quantity', 1)

                if item_type == 'consumable':
                    cons_info = consumables_cfg.get(item_id, {}) if consumables_cfg else {}
                    item_display = cons_info.get('name', item_id)
                    player.add_to_inventory(item_id, qty)
                    print(f" [DROP] +{qty}x {item_display} adicionado(s) ao inventario!")
                elif item_type == 'equipment':
                    eq_info = items_db.get('equipment', {}).get(item_id, {})
                    item_display = eq_info.get('name', item_id)
                    success, ev = player.equip_item(eq_info)
                    if success:
                        print(f" [DROP] Equipamento lendario obtido e equipado: {item_display}!")
                    else:
                        print(f" [DROP] Equipamento obtido: {item_display} (ja equipado anteriormente).")

        # Recuperação pós-fase
        hp_rec, ki_rec = campaign.calculate_stage_recovery(player, stage)
        if hp_rec > 0 or ki_rec > 0:
            player.recover(hp_amount=hp_rec, ki_amount=ki_rec)
            print(f"[RECUPERACAO] {player.name} descansa brevemente: +{hp_rec} HP | +{ki_rec} Ki")
            print(f"Status Atual -> HP: {player.hp}/{player.max_hp} | Ki: {player.ki}/{player.max_ki}")

        campaign.advance_stage()

        # Auto-save após avançar de fase
        save_payload = {
            "player": player.to_dict(),
            "campaign": campaign.to_dict(),
        }
        saved, _ = save_game_state(save_payload)
        if saved:
            print("[SAVE] Progresso salvo automaticamente em save.json!")

        if not campaign.is_completed():
            try:
                input("\nPressione ENTER para marchar rumo ao proximo desafio...")
            except (EOFError, KeyboardInterrupt):
                pass

    print("\n" + "*" * 55)
    print(f"PARABENS! VOCE COMPLETOU A CAMPANHA: {campaign.name}!")
    print(f"O universo reconhece {player.name} como o guerreiro supremo!")
    print("*" * 55 + "\n")
    return True

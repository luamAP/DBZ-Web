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
                    _, msg = character.unequip_item(item_id)
                else:
                    _, msg = character.equip_item(selected_item)
                print(f"\n[!] {msg}")
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
    """Submenu para selecao e troca de integrante da equipe."""
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


def battle_team(player_team, enemy_team, defense_cfg=None, consumables_cfg=None):
    """Executa a batalha suportando equipes completas ou combates individuais."""
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
                        if move.get('ki_cost', 0) > 0 and current_player.ki < move['ki_cost']:
                            print(f"\n[!] Ki insuficiente para {move['name']}! Requer {move['ki_cost']} de Ki.")
                        else:
                            current_player.execute_move(move, current_enemy, cfg_def)
                            valid_turn = True
                    elif choice == charge_opt:
                        current_player.charge_ki()
                        valid_turn = True
                    elif choice == defend_opt:
                        stance = get_defense_choice(current_player, cfg_def)
                        if stance:
                            current_player.defend(stance)
                            valid_turn = True
                    elif choice == item_opt:
                        item_selection = get_consumable_choice(current_player, cfg_cons)
                        if item_selection:
                            item_id, item_data = item_selection
                            success, _ = current_player.use_consumable(item_id, item_data)
                            if success:
                                valid_turn = True
                    elif transform_opt and choice == transform_opt:
                        trans = get_transformation_choice(current_player)
                        if trans and current_player.transform(trans):
                            valid_turn = True
                    elif switch_opt and choice == switch_opt:
                        sub_idx = get_team_switch_choice(player_team)
                        if sub_idx is not None:
                            _, msg = player_team.switch_member(sub_idx)
                            print(f"\n[TAG TEAM] {msg}")
                            valid_turn = True

            elif combatant == current_enemy and current_enemy.is_alive():
                execute_ai_turn(current_enemy, current_player, cfg_def)

            # Validacoes de KO e trocas compulsórias
            if not current_enemy.is_alive() and enemy_team.has_alive_members():
                print(f"\n[!] {current_enemy.name} foi derrotado!")
                enemy_team.auto_switch_next_alive()
                print(f"[!] {enemy_team.active_member.name} assume a luta pelo adversario!")
                time.sleep(1)

            if not current_player.is_alive() and player_team.has_alive_members():
                print(f"\n[!] {current_player.name} caiu!")
                bench = player_team.get_bench_members()
                if len(bench) == 1:
                    player_team.switch_member(bench[0][0])
                    print(f"[!] {player_team.active_member.name} entra imediatamente no combate!")
                else:
                    print("Selecione o proximo combatente para assumir o turno:")
                    chosen_idx = None
                    while chosen_idx is None:
                        chosen_idx = get_team_switch_choice(player_team)
                    player_team.switch_member(chosen_idx)
                time.sleep(1)

            combatant.end_turn()
            time.sleep(1.2)

    print("\n" + "!" * 45)
    if player_team.has_alive_members():
        print(f"{player_team.name} VENCEU! A Terra esta salva por enquanto.")
    else:
        print(f"{enemy_team.name} VENCEU... O universo esta condenado.")
    print("!" * 45)


def battle(player, enemy, defense_cfg=None, consumables_cfg=None):
    """Encapsulador legado mantido para compatibilidade total."""
    p_team = Team(player.name, [player])
    e_team = Team(enemy.name, [enemy])
    battle_team(p_team, e_team, defense_cfg, consumables_cfg)

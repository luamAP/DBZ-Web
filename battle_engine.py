import time
from ai_controller import execute_ai_turn


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
    """Submenu de selecao e uso de consumiveis em combate."""
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


def get_player_choice(player):
    print("\nOpcoes de Acao:")
    for idx, move in enumerate(player.moves, 1):
        ki_req = f"({move['ki_cost']} Ki)"
        print(f"{idx}. {move['name']} {ki_req}")

    offset = len(player.moves)
    charge_opt = offset + 1
    defend_opt = offset + 2
    item_opt = offset + 3
    transform_opt = offset + 4

    print(f"{charge_opt}. Carregar Ki")
    print(f"{defend_opt}. Defender")
    print(f"{item_opt}. Usar Item")
    if player.transformations:
        print(f"{transform_opt}. Transformar")

    max_choice = transform_opt if player.transformations else item_opt

    while True:
        try:
            choice = int(input(f"Selecione (1-{max_choice}): "))
            if 1 <= choice <= max_choice:
                return choice, offset, charge_opt, defend_opt, item_opt, transform_opt
            print("Escolha invalida.")
        except ValueError:
            print("Digite um numero valido.")


def battle(player, enemy, defense_cfg=None, consumables_cfg=None):
    if defense_cfg is None:
        defense_cfg = {}
    if consumables_cfg is None:
        consumables_cfg = {}

    print("\n" * 10)
    print(f"Batalha Iniciada! {player.name} vs {enemy.name}!")
    time.sleep(2)

    turn_order = [player, enemy] if player.speed >= enemy.speed else [enemy, player]

    while player.is_alive() and enemy.is_alive():
        for combatant in turn_order:
            if not player.is_alive() or not enemy.is_alive():
                break

            if combatant == player:
                print_status(player, enemy)
                print(f"\n--- Seu Turno ({player.name}) ---")

                valid_turn = False
                while not valid_turn:
                    choice_data = get_player_choice(player)
                    choice = choice_data[0]
                    total_moves = choice_data[1]
                    charge_opt = choice_data[2]
                    defend_opt = choice_data[3]
                    item_opt = choice_data[4]
                    transform_opt = choice_data[5] if len(choice_data) > 5 else None

                    if choice <= total_moves:
                        move = player.moves[choice - 1]
                        if move.get('ki_cost', 0) > 0 and player.ki < move['ki_cost']:
                            print(f"\n[!] Ki insuficiente para {move['name']}! Requer {move['ki_cost']} de Ki.")
                        else:
                            player.execute_move(move, enemy, defense_cfg)
                            valid_turn = True
                    elif choice == charge_opt:
                        player.charge_ki()
                        valid_turn = True
                    elif choice == defend_opt:
                        stance = get_defense_choice(player, defense_cfg)
                        if stance:
                            player.defend(stance)
                            valid_turn = True
                    elif choice == item_opt:
                        item_selection = get_consumable_choice(player, consumables_cfg)
                        if item_selection:
                            item_id, item_data = item_selection
                            success, _ = player.use_consumable(item_id, item_data)
                            if success:
                                valid_turn = True
                    elif choice == transform_opt and player.transformations:
                        trans = get_transformation_choice(player)
                        if trans:
                            if player.transform(trans):
                                valid_turn = True

                execute_ai_turn(enemy, player, defense_cfg)

            combatant.end_turn()
            time.sleep(1.5)

    print("\n" + "!" * 45)
    if player.is_alive():
        print(f"{player.name} VENCEU! A Terra esta salva por enquanto.")
    else:
        print(f"{enemy.name} VENCEU... O universo esta condenado.")
    print("!" * 45)


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

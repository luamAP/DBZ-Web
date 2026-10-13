import sys

from models import Character, Team
from battle_engine import battle, battle_team, manage_equipment_menu
from data_loader import load_characters_data, load_items_data, create_initial_inventory


def main():
    characters_db = load_characters_data()
    items_db = load_items_data()

    defense_cfg = characters_db.get("defense_mechanics", {})
    available_equipment = items_db.get("equipment", {})
    available_consumables = items_db.get("consumables", {})

    player = Character(characters_db["Goku"], create_initial_inventory(available_consumables))

    while True:
        print("\n=== DRAGON BALL Z TEXT BATTLE ===")
        print(f"Guerreiro Atual: {player.name} (Itens Equipados: {len(player.equipped_items)})")
        print("1. Batalha 1v1 contra Vegeta")
        print("2. Batalha 1v1 contra Frieza")
        print("3. Batalha Tag Team 2v2 (Goku & Vegeta vs Frieza Army)")
        print("4. Equipamentos e Capsulas (Customizar Goku)")
        print("5. Sair")

        choice = input("Selecione uma opcao: ")

        if choice == '1':
            enemy = Character(characters_db["Vegeta"])
            battle(player, enemy, defense_cfg, available_consumables)
            player = Character(characters_db["Goku"], create_initial_inventory(available_consumables))
        elif choice == '2':
            enemy = Character(characters_db["Frieza"])
            battle(player, enemy, defense_cfg, available_consumables)
            player = Character(characters_db["Goku"], create_initial_inventory(available_consumables))
        elif choice == '3':
            p1 = player
            p2 = Character(characters_db["Vegeta"], create_initial_inventory(available_consumables))
            e1 = Character(characters_db["Frieza"])
            e2 = Character(characters_db["Vegeta"])
            e2.name = "Clone Sombra de Vegeta"

            p_team = Team("Guerreiros Z", [p1, p2])
            e_team = Team("Exercito de Frieza", [e1, e2])

            battle_team(p_team, e_team, defense_cfg, available_consumables)
            player = Character(characters_db["Goku"], create_initial_inventory(available_consumables))
        elif choice == '4':
            manage_equipment_menu(player, available_equipment)
        elif choice == '5':
            print("Ate mais!")
            sys.exit()
        else:
            print("Opcao invalida.")


if __name__ == "__main__":
    main()

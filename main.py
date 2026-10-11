import sys
import yaml
import os

from models import Character, Team
from battle_engine import battle, battle_team, manage_equipment_menu


def load_characters_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'characters.yml')
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_items_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'items.yml')
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def create_initial_inventory(consumables_cfg):
    return {
        item_id: item_data.get('default_quantity', 1)
        for item_id, item_data in consumables_cfg.items()
    }


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

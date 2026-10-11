import sys
import yaml
import os

from models import Character
from battle_engine import battle, manage_equipment_menu


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
    """Monta o inventario inicial a partir dos valores padrao declarados no YAML."""
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
        print("1. Jogar contra Vegeta")
        print("2. Jogar contra Frieza")
        print("3. Equipamentos e Capsulas (Customizar)")
        print("4. Sair")

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
            manage_equipment_menu(player, available_equipment)
        elif choice == '4':
            print("Ate mais!")
            sys.exit()
        else:
            print("Opcao invalida.")


if __name__ == "__main__":
    main()

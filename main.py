import sys

from models import Character, Team, Campaign
from battle_engine import battle, battle_team, manage_equipment_menu, run_campaign
from data_loader import (
    load_characters_data,
    load_items_data,
    load_campaign_data,
    create_initial_inventory,
    save_game_state,
    load_game_state,
)


def main():
    characters_db = load_characters_data()
    items_db = load_items_data()
    campaigns_db = load_campaign_data()

    defense_cfg = characters_db.get("defense_mechanics", {})
    ai_profiles_cfg = characters_db.get("ai_profiles", {})
    available_equipment = items_db.get("equipment", {})
    available_consumables = items_db.get("consumables", {})
    campaign_cfg = campaigns_db.get("campaigns", {}).get("saiyan_invasion", {})

    player = Character(characters_db["Goku"], create_initial_inventory(available_consumables))
    campaign_progress = Campaign(campaign_cfg)

    while True:
        stage_info = f"Fase {campaign_progress.current_stage_index + 1}/{len(campaign_progress.stages)}" if not campaign_progress.is_completed() else "Campanha Concluida"
        print("\n=== DRAGON BALL Z TEXT BATTLE ===")
        print(f"Guerreiro Atual: {player.name} (HP: {player.hp}/{player.max_hp} | KI: {player.ki}/{player.max_ki})")
        print(f"Itens Equipados: {len(player.equipped_items)} | Progresso da Campanha: {stage_info}")
        print("1. Batalha 1v1 contra Vegeta")
        print("2. Batalha 1v1 contra Frieza")
        print("3. Batalha Tag Team 2v2 (Goku & Vegeta vs Frieza Army)")
        print("4. Equipamentos e Capsulas (Customizar Goku)")
        print("5. Modo Campanha (Saga dos Saiyajins e Ameaça Cósmica)")
        print("6. Salvar Progresso (save.json)")
        print("7. Carregar Progresso (save.json)")
        print("8. Sair")

        choice = input("Selecione uma opcao: ")

        if choice == '1':
            enemy = Character(characters_db["Vegeta"])
            battle(player, enemy, defense_cfg, available_consumables, ai_profiles_cfg)
            player = Character(characters_db["Goku"], create_initial_inventory(available_consumables))
        elif choice == '2':
            enemy = Character(characters_db["Frieza"])
            battle(player, enemy, defense_cfg, available_consumables, ai_profiles_cfg)
            player = Character(characters_db["Goku"], create_initial_inventory(available_consumables))
        elif choice == '3':
            p1 = player
            p2 = Character(characters_db["Vegeta"], create_initial_inventory(available_consumables))
            e1 = Character(characters_db["Frieza"])
            e2 = Character(characters_db["Vegeta"])
            e2.name = "Clone Sombra de Vegeta"

            p_team = Team("Guerreiros Z", [p1, p2])
            e_team = Team("Exercito de Frieza", [e1, e2])

            battle_team(p_team, e_team, defense_cfg, available_consumables, ai_profiles_cfg)
            player = Character(characters_db["Goku"], create_initial_inventory(available_consumables))
        elif choice == '4':
            manage_equipment_menu(player, available_equipment)
        elif choice == '5':
            run_campaign(
                player,
                campaign_cfg,
                characters_db,
                items_db,
                defense_cfg,
                available_consumables,
                ai_profiles_cfg,
                campaign_instance=campaign_progress,
            )
        elif choice == '6':
            save_payload = {
                "player": player.to_dict(),
                "campaign": campaign_progress.to_dict(),
            }
            saved, meta = save_game_state(save_payload)
            if saved:
                print(f"\n[SUCESSO] Jogo salvo com sucesso em {meta['filename']}!")
            else:
                print(f"\n[ERRO] Falha ao salvar o jogo: {meta.get('msg', meta.get('reason'))}")
        elif choice == '7':
            save_data, meta = load_game_state()
            if save_data:
                player_state = save_data.get("player", {})
                campaign_state = save_data.get("campaign", {})
                player.load_state(player_state, available_equipment)
                campaign_progress.load_state(campaign_state)
                print(f"\n[SUCESSO] Save state carregado com sucesso!")
                print(f" -> Guerreiro: {player.name} (HP: {player.hp}/{player.max_hp})")
                print(f" -> Campanha: Fase {campaign_progress.current_stage_index + 1}")
            else:
                print(f"\n[AVISO] Nao foi possivel carregar save state: {meta.get('reason')}")
        elif choice == '8':
            print("Ate mais!")
            sys.exit()
        else:
            print("Opcao invalida.")


if __name__ == "__main__":
    main()

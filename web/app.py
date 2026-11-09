"""Servidor Flask da interface Web estilo Game Boy do Dragon Ball Z.

Expõe endpoints REST integrando o domínio puro (models/), o carregamento
de dados (engine.data_loader) e o controle da IA (engine.ai_controller).
"""

from flask import Flask, jsonify, render_template, request
from engine.ai_controller import execute_ai_turn
from engine.data_loader import (
    create_initial_inventory,
    load_campaign_data,
    load_characters_data,
    load_game_state,
    load_items_data,
    save_game_state,
)
from models import Campaign, Character, Team

META_KEYS = {"defense_mechanics", "ai_profiles", "combat_mechanics"}


def get_characters_catalog(chars_data):
    """Extrai apenas os personagens do dicionário carregado de characters.yml."""
    return {k: v for k, v in chars_data.items() if k not in META_KEYS}


def find_character_data(catalog, char_id):
    """Localiza a definição do combatente por ID ou nome case-insensitive."""
    if char_id in catalog:
        return catalog[char_id]
    for k, v in catalog.items():
        if k.lower() == str(char_id).lower():
            return v
    return None


def serialize_character(character):
    """Formata o combatente para resposta da API / interface de apresentação."""
    if character is None:
        return None
    return {
        "name": character.name,
        "raw_name": getattr(character, "raw_name", character.name),
        "hp": character.hp,
        "max_hp": character.max_hp,
        "ki": character.ki,
        "max_ki": character.max_ki,
        "base_attack": character.base_attack,
        "defense": character.defense,
        "speed": character.speed,
        "moves": list(character.moves),
        "transformations": list(character.transformations),
        "current_transformation": character.current_transformation,
        "defensive_stance": character.defensive_stance,
        "is_alive": character.is_alive(),
        "inventory": dict(character.inventory),
        "equipped_items": [
            item.get("id", item.get("name")) for item in character.equipped_items
        ],
        "sprites": (
            character.get_current_sprites()
            if hasattr(character, "get_current_sprites")
            else getattr(character, "sprites", {})
        ),
    }


def serialize_team(team):
    """Serializa a equipe: índice ativo e resumo de cada integrante."""
    return {
        "name": team.name,
        "active_index": team.active_index,
        "members": [
            {
                "index": idx,
                "name": m.name,
                "hp": m.hp,
                "max_hp": m.max_hp,
                "ki": m.ki,
                "max_ki": m.max_ki,
                "is_alive": m.is_alive(),
                "sprites": (
                    m.get_current_sprites()
                    if hasattr(m, "get_current_sprites")
                    else getattr(m, "sprites", {})
                ),
            }
            for idx, m in enumerate(team.members)
        ],
    }


def serialize_battle(battle):
    """Serializa o estado completo da batalha para o cliente."""
    player_team = battle["player_team"]
    enemy_team = battle["enemy_team"]
    chars_data = load_characters_data()
    items_data = load_items_data()
    return {
        "session_id": battle["session_id"],
        "turn": battle["turn"],
        "status": battle["status"],
        "player": serialize_character(player_team.active_member),
        "enemy": serialize_character(enemy_team.active_member),
        "player_team": serialize_team(player_team),
        "enemy_team": serialize_team(enemy_team),
        "log": battle.get("log", []),
        "defense_mechanics": chars_data.get("defense_mechanics", {}),
        "consumables": items_data.get("consumables", {}),
        "campaign": battle.get("campaign"),
        "campaign_stage": battle.get("campaign_stage"),
        "last_drops": battle.get("last_drops", []),
    }


def get_or_create_default_battle(battles):
    """Retorna ou inicializa a batalha padrão (Goku vs Vegeta) alinhada ao main.py."""
    if "default" not in battles:
        chars_data = load_characters_data()
        catalog = get_characters_catalog(chars_data)
        items_data = load_items_data()
        consumables_cfg = items_data.get("consumables", {})
        combat_cfg = chars_data.get("combat_mechanics", {})

        player = Character(
            find_character_data(catalog, "Goku"),
            initial_inventory=create_initial_inventory(consumables_cfg),
            combat_cfg=combat_cfg,
        )
        enemy = Character(find_character_data(catalog, "Vegeta"), combat_cfg=combat_cfg)
        player_team = Team("Guerreiros Z", [player])
        enemy_team = Team("Exercito de Freeza", [enemy])

        battles["default"] = {
            "session_id": "default",
            "player_team": player_team,
            "enemy_team": enemy_team,
            "turn": 1,
            "status": "ongoing",
            "log": [f"Batalha iniciada: {player.name} vs {enemy.name}!"],
        }
    return battles["default"]


def create_app(test_config=None):
    """Cria e configura a instância da aplicação Flask."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dbz-gameboy-web-secret-key",
    )

    if test_config:
        app.config.from_mapping(test_config)

    # Armazenamento em memória das batalhas ativas por session_id
    battles = {}
    app.extensions["battles"] = battles

    @app.route("/", methods=["GET"])
    def index():
        if (
            request.headers.get("Accept") == "application/json"
            or request.args.get("format") == "json"
        ):
            return jsonify(
                {
                    "status": "ok",
                    "app": "Dragon Ball Z - Game Boy Web Interface",
                    "version": "2.0",
                }
            )
        default_battle = get_or_create_default_battle(battles)
        return render_template("index.html", initial_battle=serialize_battle(default_battle))

    # --- Catálogos de Dados ---

    @app.route("/api/characters", methods=["GET"])
    def get_characters():
        data = load_characters_data()
        catalog = get_characters_catalog(data)
        return jsonify(
            {
                "characters": catalog,
                "defense_mechanics": data.get("defense_mechanics", {}),
                "combat_mechanics": data.get("combat_mechanics", {}),
                "ai_profiles": data.get("ai_profiles", {})
            }
        )

    @app.route("/api/items", methods=["GET"])
    def get_items():
        data = load_items_data()
        return jsonify(data)

    @app.route("/api/campaign", methods=["GET"])
    def get_campaign():
        data = load_campaign_data()
        return jsonify(data)

    @app.route("/api/campaign/start", methods=["POST"])
    def start_campaign():
        payload = request.get_json(silent=True) or {}
        session_id = payload.get("session_id", "default")
        campaign_id = payload.get("campaign_id", "saiyan_invasion")
        player_id = payload.get("player_id", "Goku")

        camp_data_all = load_campaign_data()
        all_campaigns = camp_data_all.get("campaigns", {})
        if campaign_id not in all_campaigns:
            return jsonify({"error": f"Campanha '{campaign_id}' não encontrada."}), 404

        camp_instance = Campaign(all_campaigns[campaign_id])
        stage_data = camp_instance.get_current_stage()
        if not stage_data:
            return jsonify({"error": "Campanha sem estágios válidos."}), 400

        chars_data = load_characters_data()
        catalog = get_characters_catalog(chars_data)
        items_data = load_items_data()
        consumables_cfg = items_data.get("consumables", {})
        combat_cfg = chars_data.get("combat_mechanics", {})

        player_data = find_character_data(catalog, player_id)
        if not player_data:
            return jsonify({"error": f"Personagem '{player_id}' não encontrado."}), 404

        enemy_name = stage_data.get("enemy")
        enemy_data = find_character_data(catalog, enemy_name)
        if not enemy_data:
            return jsonify({"error": f"Inimigo da fase '{enemy_name}' não encontrado."}), 404

        player = Character(
            player_data,
            initial_inventory=create_initial_inventory(consumables_cfg),
            combat_cfg=combat_cfg,
        )
        enemy = Character(enemy_data, combat_cfg=combat_cfg)
        player_team = Team("Guerreiros Z", [player])
        enemy_team = Team(f"Fase {stage_data.get('stage')}: {stage_data.get('name')}", [enemy])

        battle = {
            "session_id": session_id,
            "player_team": player_team,
            "enemy_team": enemy_team,
            "turn": 1,
            "status": "ongoing",
            "log": [f"Campanha iniciada: Fase {stage_data.get('stage')} — {stage_data.get('name')}! {player.name} vs {enemy.name}!"],
            "campaign": camp_instance.to_dict(),
            "campaign_stage": stage_data,
            "campaign_instance": camp_instance,
            "last_drops": [],
        }
        battles[session_id] = battle

        return jsonify({
            "success": True,
            "campaign": camp_instance.to_dict(),
            "stage": stage_data,
            "battle": serialize_battle(battle),
        })

    @app.route("/api/campaign/next", methods=["POST"])
    def next_campaign_stage():
        payload = request.get_json(silent=True) or {}
        session_id = payload.get("session_id", "default")
        battle = battles.get(session_id)

        if not battle or "campaign_instance" not in battle:
            return jsonify({"error": "Nenhuma campanha ativa para avançar."}), 400

        camp_instance = battle["campaign_instance"]
        current_stage = camp_instance.get_current_stage()
        player = battle["player_team"].active_member

        # 1. Resolução de Drops da fase anterior
        drops = []
        if current_stage:
            drops = Campaign.resolve_drops(current_stage)
            for drop in drops:
                item_id = drop.get("item_id")
                qty = drop.get("quantity", 1)
                player.inventory[item_id] = player.inventory.get(item_id, 0) + qty

            # 2. Recuperação entre fases
            hp_rec, ki_rec = camp_instance.calculate_stage_recovery(player, current_stage)
            player.hp = min(player.max_hp, player.hp + hp_rec)
            player.ki = min(player.max_ki, player.ki + ki_rec)

        # 3. Avança o estágio
        advanced, adv_info = camp_instance.advance_stage()
        if camp_instance.is_completed():
            battle["status"] = "campaign_completed"
            battle["campaign"] = camp_instance.to_dict()
            battle["last_drops"] = drops
            battle["log"].append("Parabéns! Você concluiu todos os desafios da campanha!")
            return jsonify({
                "success": True,
                "completed": True,
                "drops": drops,
                "battle": serialize_battle(battle),
            })

        next_stage = camp_instance.get_current_stage()
        chars_data = load_characters_data()
        catalog = get_characters_catalog(chars_data)
        combat_cfg = chars_data.get("combat_mechanics", {})
        enemy_data = find_character_data(catalog, next_stage["enemy"])

        new_enemy = Character(enemy_data, combat_cfg=combat_cfg)
        enemy_team = Team(f"Fase {next_stage.get('stage')}: {next_stage.get('name')}", [new_enemy])

        battle["enemy_team"] = enemy_team
        battle["status"] = "ongoing"
        battle["campaign"] = camp_instance.to_dict()
        battle["campaign_stage"] = next_stage
        battle["last_drops"] = drops
        battle["turn"] = 1
        battle["log"].append(
            f"Fase {next_stage.get('stage')}: {next_stage.get('name')} iniciada! Oponente: {new_enemy.name}."
        )

        return jsonify({
            "success": True,
            "completed": False,
            "stage": next_stage,
            "drops": drops,
            "battle": serialize_battle(battle),
        })

    # --- Gerenciamento de Batalha ---

    @app.route("/api/battle/new", methods=["POST"])
    def new_battle():
        payload = request.get_json(silent=True) or {}
        # Aceita lista (Tag Team) ou ID único (1v1)
        player_ids = payload.get("player_ids") or [payload.get("player_id", "Goku")]
        enemy_ids = payload.get("enemy_ids") or [payload.get("enemy_id", "Vegeta")]
        session_id = payload.get("session_id", "default")

        chars_data = load_characters_data()
        catalog = get_characters_catalog(chars_data)

        for char_id in player_ids:
            if not find_character_data(catalog, char_id):
                return (
                    jsonify(
                        {"error": f"Personagem do jogador '{char_id}' não encontrado."}
                    ),
                    400,
                )
        for char_id in enemy_ids:
            if not find_character_data(catalog, char_id):
                return (
                    jsonify(
                        {"error": f"Personagem do oponente '{char_id}' não encontrado."}
                    ),
                    400,
                )

        items_data = load_items_data()
        consumables_cfg = items_data.get("consumables", {})
        combat_cfg = chars_data.get("combat_mechanics", {})

        player_members = [
            Character(
                find_character_data(catalog, char_id),
                initial_inventory=create_initial_inventory(consumables_cfg),
                combat_cfg=combat_cfg,
            )
            for char_id in player_ids
        ]
        enemy_members = [
            Character(find_character_data(catalog, char_id), combat_cfg=combat_cfg)
            for char_id in enemy_ids
        ]
        player_team = Team(payload.get("player_team_name", "Jogador"), player_members)
        enemy_team = Team(payload.get("enemy_team_name", "Oponente"), enemy_members)

        battles[session_id] = {
            "session_id": session_id,
            "player_team": player_team,
            "enemy_team": enemy_team,
            "turn": 1,
            "status": "ongoing",
            "log": [
                f"Batalha iniciada: {player_team.active_member.name} vs {enemy_team.active_member.name}!"
            ],
        }

        return (
            jsonify(
                {
                    "success": True,
                    "battle": serialize_battle(battles[session_id]),
                }
            ),
            201,
        )

    @app.route("/api/battle/state", methods=["GET"])
    def get_battle_state():
        session_id = request.args.get("session_id", "default")
        if session_id == "default":
            battle = get_or_create_default_battle(battles)
        else:
            battle = battles.get(session_id)

        if not battle:
            return (
                jsonify(
                    {"error": f"Batalha não encontrada para session_id '{session_id}'."}
                ),
                404,
            )
        return jsonify({"success": True, "battle": serialize_battle(battle)})

    @app.route("/api/battle/action", methods=["POST"])
    def battle_action():
        payload = request.get_json(silent=True) or {}
        session_id = payload.get("session_id", "default")
        battle = battles.get(session_id)

        if not battle:
            return (
                jsonify(
                    {"error": f"Batalha não encontrada para session_id '{session_id}'."}
                ),
                404,
            )

        if battle["status"] != "ongoing":
            return (
                jsonify(
                    {
                        "error": f"Batalha já finalizada com status '{battle['status']}'."
                    }
                ),
                400,
            )

        player_team = battle["player_team"]
        enemy_team = battle["enemy_team"]
        player = player_team.active_member
        enemy = enemy_team.active_member
        action = payload.get("action")

        chars_data = load_characters_data()
        defense_cfg = chars_data.get("defense_mechanics", {})
        combat_cfg = chars_data.get("combat_mechanics", {})
        ai_profiles_cfg = chars_data.get("ai_profiles", {})
        items_data = load_items_data()
        consumables_cfg = items_data.get("consumables", {})

        player_event = None

        # 1. Executa a ação do jogador
        if action == "move":
            move_name = payload.get("move_name")
            move_index = payload.get("move_index")
            selected_move = None

            if move_name:
                selected_move = next(
                    (m for m in player.moves if m.get("name").lower() == move_name.lower()),
                    None,
                )
            elif move_index is not None and 0 <= move_index < len(player.moves):
                selected_move = player.moves[move_index]

            if not selected_move:
                return jsonify({"error": "Movimento inválido ou não informado."}), 400

            # Limpa postura de defesa anterior ao atacar
            player.defensive_stance = None
            success, ev = player.execute_move(
                selected_move, enemy, defense_cfg, combat_cfg
            )
            if not success:
                return (
                    jsonify(
                        {
                            "error": ev.get("msg", "Falha ao executar movimento."),
                            "reason": ev,
                        }
                    ),
                    400,
                )
            player_event = {"action": "move", "data": ev}
            battle["log"].append(
                f"{player.name} usou {selected_move.get('name', 'ataque')}!"
            )

        elif action == "charge_ki" or action == "charge":
            player.defensive_stance = None
            ev = player.charge_ki(combat_cfg)
            player_event = {"action": "charge", "data": ev}
            battle["log"].append(
                f"{player.name} concentrou Ki (+{ev['amount']} Ki, total: {ev['ki_now']})!"
            )

        elif action == "defend":
            stance = payload.get("stance", "block")
            if stance not in ["block", "counter", "dodge", "vanish"]:
                return jsonify({"error": f"Postura defensiva '{stance}' inválida."}), 400

            # Valida custo de Ki da postura
            cost = defense_cfg.get(stance, {}).get("ki_cost", 0)
            if player.ki < cost:
                return (
                    jsonify(
                        {
                            "error": f"Ki insuficiente para {stance}. Requer {cost} Ki, atual {player.ki}."
                        }
                    ),
                    400,
                )

            player.ki -= cost
            ev = player.defend(stance)
            player_event = {"action": "defend", "data": ev}
            battle["log"].append(f"{player.name} assumiu postura defensiva: {stance}!")

        elif action == "transform":
            trans_name = payload.get("transformation") or payload.get(
                "transformation_name"
            )
            trans = next(
                (t for t in player.transformations if t.get("name") == trans_name),
                None,
            )
            if not trans:
                return (
                    jsonify({"error": f"Transformação '{trans_name}' não encontrada."}),
                    400,
                )
            success, ev = player.transform(trans)
            if not success:
                return (
                    jsonify(
                        {
                            "error": f"Não é possível transformar em {trans_name}.",
                            "reason": ev,
                        }
                    ),
                    400,
                )
            player_event = {"action": "transform", "data": ev}
            battle["log"].append(f"{ev['old_name']} transformou-se em {ev['new_name']}!")

        elif action == "switch":
            target_index = payload.get("target_index")
            if not isinstance(target_index, int):
                return jsonify({"error": "target_index inteiro obrigatório."}), 400
            success, ev = player_team.switch_member(target_index)
            if not success:
                return (
                    jsonify({"error": "Falha na troca de lutador.", "reason": ev}),
                    400,
                )
            player_event = {
                "action": "switch",
                "data": {"old_name": ev["old_name"], "new_name": ev["new_name"]},
            }
            battle["log"].append(
                f"Troca: {ev['old_name']} recua e {ev['new_name']} assume a arena!"
            )
            player = player_team.active_member

        elif action == "item":
            item_id = payload.get("item_id")
            if not item_id or item_id not in consumables_cfg:
                return jsonify({"error": f"Item '{item_id}' inválido."}), 400
            item_data = consumables_cfg[item_id]
            success, ev = player.use_consumable(item_id, item_data)
            if not success:
                return (
                    jsonify(
                        {
                            "error": ev.get("msg", "Falha ao usar item."),
                            "reason": ev,
                        }
                    ),
                    400,
                )
            player_event = {"action": "item", "data": ev}
            battle["log"].append(f"{player.name} usou {ev.get('item_name')}!")

        else:
            return jsonify({"error": f"Ação '{action}' desconhecida."}), 400

        # 2. Verifica se o oponente ativo foi derrotado (KO / troca automática)
        if not enemy.is_alive():
            battle["log"].append(f"{enemy.name} foi derrotado!")
            switched, sw_ev = enemy_team.auto_switch_next_alive()
            if not switched:
                battle["status"] = "won"
                battle["log"].append(f"Vitória de {player_team.name}!")
                return jsonify(
                    {
                        "success": True,
                        "player_event": player_event,
                        "ai_event": None,
                        "battle": serialize_battle(battle),
                    }
                )
            battle["log"].append(f"{sw_ev['new_name']} assume a luta pelo adversário!")
            enemy = enemy_team.active_member

        # Contra-ataque inimigo pode nocautear o jogador durante o próprio turno
        if not player.is_alive():
            battle["log"].append(f"{player.name} caiu!")
            switched, sw_ev = player_team.auto_switch_next_alive()
            if not switched:
                battle["status"] = "lost"
                battle["log"].append(f"{player_team.name} foi derrotado!")
                return jsonify(
                    {
                        "success": True,
                        "player_event": player_event,
                        "ai_event": None,
                        "battle": serialize_battle(battle),
                    }
                )
            battle["log"].append(f"{sw_ev['new_name']} entra no combate!")
            player = player_team.active_member

        # 3. Turno da IA
        # Reseta postura de defesa do oponente para a nova rodada
        enemy.defensive_stance = None
        ai_action_type, ai_ev = execute_ai_turn(
            enemy, player, defense_cfg, ai_profiles_cfg, combat_cfg
        )
        ai_event = {"action": ai_action_type, "data": ai_ev}

        if ai_action_type == "move":
            battle["log"].append(
                f"{enemy.name} executou {ai_ev.get('move_name', 'golpe')}!"
            )
        elif ai_action_type == "charge":
            battle["log"].append(
                f"{enemy.name} concentrou Ki (+{ai_ev.get('amount', 0)} Ki)!"
            )
        elif ai_action_type == "defend":
            battle["log"].append(
                f"{enemy.name} assumiu postura defensiva: {ai_ev.get('stance')}!"
            )
        elif ai_action_type == "transform":
            battle["log"].append(
                f"{enemy.name} atingiu a forma {ai_ev.get('new_name')}!"
            )

        # 4. Contra-ataque pode nocautear o oponente durante o próprio turno
        if not enemy.is_alive():
            battle["log"].append(f"{enemy.name} foi derrotado!")
            switched, sw_ev = enemy_team.auto_switch_next_alive()
            if switched:
                battle["log"].append(f"{sw_ev['new_name']} assume a luta pelo adversário!")
            else:
                battle["status"] = "won"
                battle["log"].append(f"Vitória de {player_team.name}!")

        # 5. Verifica se o jogador ativo foi derrotado (troca automática)
        if not player.is_alive():
            battle["log"].append(f"{player.name} caiu!")
            switched, sw_ev = player_team.auto_switch_next_alive()
            if switched:
                battle["log"].append(f"{sw_ev['new_name']} entra no combate!")
            elif battle["status"] == "ongoing":
                battle["status"] = "lost"
                battle["log"].append(f"{player_team.name} foi derrotado!")

        battle["turn"] += 1

        return jsonify(
            {
                "success": True,
                "player_event": player_event,
                "ai_event": ai_event,
                "battle": serialize_battle(battle),
            }
        )

    # --- Persistência de Save State ---

    @app.route("/api/save", methods=["POST"])
    def save_state():
        payload = request.get_json(silent=True) or {}
        filename = payload.get("filename", "save.json")
        save_data = payload.get("save_data")

        if not save_data:
            session_id = payload.get("session_id", "default")
            battle = battles.get(session_id)
            if not battle:
                return (
                    jsonify(
                        {
                            "error": "Nenhum save_data informado e nenhuma batalha ativa para salvar."
                        }
                    ),
                    400,
                )
            save_data = {
                "player": battle["player_team"].active_member.to_dict(),
                "player_team": [m.to_dict() for m in battle["player_team"].members],
                "turn": battle["turn"],
                "status": battle["status"],
                "campaign": battle.get("campaign"),
                "campaign_stage": battle.get("campaign_stage"),
            }

        success, info = save_game_state(save_data, filename=filename)
        status_code = 200 if success else 500
        return jsonify({"success": success, "result": info}), status_code

    @app.route("/api/load", methods=["POST"])
    def load_state():
        payload = request.get_json(silent=True) or {}
        filename = payload.get("filename", "save.json")
        session_id = payload.get("session_id", "default")
        data, info = load_game_state(filename=filename)
        if data is None:
            return jsonify({"success": False, "result": info}), 404

        chars_data = load_characters_data()
        catalog = get_characters_catalog(chars_data)
        items_data = load_items_data()
        available_equipment = items_data.get("equipment", {})
        combat_cfg = chars_data.get("combat_mechanics", {})

        player_dict = data.get("player")
        if player_dict and "raw_name" in player_dict:
            p_data = find_character_data(catalog, player_dict["raw_name"])
            if p_data:
                player = Character(p_data, combat_cfg=combat_cfg)
                player.load_state(player_dict, available_equipment=available_equipment)
                player_team = Team("Guerreiros Z", [player])

                camp_dict = data.get("campaign")
                camp_data_all = load_campaign_data()
                all_campaigns = camp_data_all.get("campaigns", {})

                if camp_dict and camp_dict.get("campaign_id") in all_campaigns:
                    c_id = camp_dict["campaign_id"]
                    camp_instance = Campaign(all_campaigns[c_id])
                    camp_instance.load_state(camp_dict)
                    stage_data = camp_instance.get_current_stage() or all_campaigns[c_id]["stages"][0]
                    enemy_data = find_character_data(catalog, stage_data["enemy"])
                    enemy = Character(enemy_data, combat_cfg=combat_cfg)
                    enemy_team = Team(f"Fase {stage_data.get('stage')}: {stage_data.get('name')}", [enemy])
                    battle = {
                        "session_id": session_id,
                        "player_team": player_team,
                        "enemy_team": enemy_team,
                        "turn": data.get("turn", 1),
                        "status": data.get("status", "ongoing"),
                        "log": [f"Jogo carregado com sucesso! Fase: {stage_data.get('name')}."],
                        "campaign": camp_instance.to_dict(),
                        "campaign_stage": stage_data,
                        "campaign_instance": camp_instance,
                        "last_drops": [],
                    }
                else:
                    enemy = Character(find_character_data(catalog, "Vegeta"), combat_cfg=combat_cfg)
                    enemy_team = Team("Exercito de Freeza", [enemy])
                    battle = {
                        "session_id": session_id,
                        "player_team": player_team,
                        "enemy_team": enemy_team,
                        "turn": data.get("turn", 1),
                        "status": data.get("status", "ongoing"),
                        "log": ["Jogo carregado com sucesso!"],
                    }
                battles[session_id] = battle
                return jsonify({
                    "success": True,
                    "data": data,
                    "result": info,
                    "battle": serialize_battle(battle),
                })

        return jsonify({"success": True, "data": data, "result": info})

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)

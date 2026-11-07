import os
import unittest
from web.app import create_app


class TestWebApi(unittest.TestCase):

    def setUp(self):
        self.app = create_app({"TESTING": True})
        self.client = self.app.test_client()

    def test_index_route(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "ok")
        self.assertIn("Dragon Ball Z", data["app"])

    def test_catalogs_endpoints(self):
        # Characters catalog
        res_chars = self.client.get("/api/characters")
        self.assertEqual(res_chars.status_code, 200)
        data_chars = res_chars.get_json()
        self.assertIn("characters", data_chars)
        self.assertIn("Goku", data_chars["characters"])

        # Items catalog
        res_items = self.client.get("/api/items")
        self.assertEqual(res_items.status_code, 200)
        data_items = res_items.get_json()
        self.assertIn("consumables", data_items)

        # Campaign catalog
        res_camp = self.client.get("/api/campaign")
        self.assertEqual(res_camp.status_code, 200)
        data_camp = res_camp.get_json()
        self.assertIn("campaigns", data_camp)

    def test_battle_new_and_state(self):
        # Criação de nova batalha válida (usando nomes case-insensitive)
        res = self.client.post(
            "/api/battle/new",
            json={"player_id": "goku", "enemy_id": "vegeta", "session_id": "sess_1"},
        )
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertTrue(data["success"])
        battle = data["battle"]
        self.assertEqual(battle["session_id"], "sess_1")
        self.assertEqual(battle["player"]["name"], "Goku")
        self.assertEqual(battle["enemy"]["name"], "Vegeta")
        self.assertEqual(battle["status"], "ongoing")

        # Consulta de estado da batalha
        res_state = self.client.get("/api/battle/state?session_id=sess_1")
        self.assertEqual(res_state.status_code, 200)
        state_data = res_state.get_json()
        self.assertTrue(state_data["success"])
        self.assertEqual(state_data["battle"]["player"]["name"], "Goku")

        # Batalha inexistente
        res_not_found = self.client.get("/api/battle/state?session_id=inexistente")
        self.assertEqual(res_not_found.status_code, 404)

    def test_battle_new_invalid_characters(self):
        res_invalid_player = self.client.post(
            "/api/battle/new",
            json={"player_id": "lutador_fantasma", "enemy_id": "vegeta"},
        )
        self.assertEqual(res_invalid_player.status_code, 400)

        res_invalid_enemy = self.client.post(
            "/api/battle/new",
            json={"player_id": "goku", "enemy_id": "lutador_fantasma"},
        )
        self.assertEqual(res_invalid_enemy.status_code, 400)

    def test_battle_action_charge_ki(self):
        self.client.post(
            "/api/battle/new",
            json={"player_id": "goku", "enemy_id": "vegeta", "session_id": "sess_charge"},
        )
        res = self.client.post(
            "/api/battle/action",
            json={"action": "charge_ki", "session_id": "sess_charge"},
        )
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["player_event"]["action"], "charge")
        self.assertIn("ai_event", data)
        self.assertGreater(data["battle"]["turn"], 1)

    def test_battle_action_defend(self):
        self.client.post(
            "/api/battle/new",
            json={"player_id": "goku", "enemy_id": "vegeta", "session_id": "sess_def"},
        )
        # Bloqueio custa 0 Ki
        res = self.client.post(
            "/api/battle/action",
            json={"action": "defend", "stance": "block", "session_id": "sess_def"},
        )
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["player_event"]["action"], "defend")
        self.assertEqual(data["player_event"]["data"]["stance"], "block")

        # Teleporte requer 25 Ki, com Ki 0 deve falhar
        res_fail = self.client.post(
            "/api/battle/action",
            json={"action": "defend", "stance": "vanish", "session_id": "sess_def"},
        )
        self.assertEqual(res_fail.status_code, 400)
        self.assertIn("Ki insuficiente", res_fail.get_json()["error"])

    def test_battle_action_move(self):
        self.client.post(
            "/api/battle/new",
            json={"player_id": "goku", "enemy_id": "vegeta", "session_id": "sess_move"},
        )
        # Movimento básico por nome
        res = self.client.post(
            "/api/battle/action",
            json={"action": "move", "move_name": "Melee Attack", "session_id": "sess_move"},
        )
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["player_event"]["action"], "move")
        self.assertEqual(data["player_event"]["data"]["type"], "basic")

        # Movimento por índice
        res_idx = self.client.post(
            "/api/battle/action",
            json={"action": "move", "move_index": 0, "session_id": "sess_move"},
        )
        self.assertEqual(res_idx.status_code, 200)

        # Movimento inválido
        res_inv = self.client.post(
            "/api/battle/action",
            json={"action": "move", "move_name": "Golpe Inexistente", "session_id": "sess_move"},
        )
        self.assertEqual(res_inv.status_code, 400)

    def test_battle_action_item(self):
        self.client.post(
            "/api/battle/new",
            json={"player_id": "goku", "enemy_id": "vegeta", "session_id": "sess_item"},
        )
        # Uso de Semente dos Deuses
        res = self.client.post(
            "/api/battle/action",
            json={"action": "item", "item_id": "senzu_bean", "session_id": "sess_item"},
        )
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["player_event"]["action"], "item")

        # Item inválido
        res_inv = self.client.post(
            "/api/battle/action",
            json={"action": "item", "item_id": "item_fantasma", "session_id": "sess_item"},
        )
        self.assertEqual(res_inv.status_code, 400)

    def _new_tag_battle(self, session_id):
        res = self.client.post(
            "/api/battle/new",
            json={
                "player_ids": ["Goku", "Vegeta"],
                "enemy_ids": ["Frieza", "Vegeta"],
                "session_id": session_id,
            },
        )
        self.assertEqual(res.status_code, 201)
        return res.get_json()["battle"]

    def _battle(self, session_id):
        return self.app.extensions["battles"][session_id]

    def test_battle_new_tag_team(self):
        battle = self._new_tag_battle("sess_tag")
        self.assertEqual(len(battle["player_team"]["members"]), 2)
        self.assertEqual(len(battle["enemy_team"]["members"]), 2)
        self.assertEqual(battle["player_team"]["active_index"], 0)
        self.assertEqual(battle["player"]["name"], "Goku")

    def test_battle_action_switch(self):
        self._new_tag_battle("sess_switch")
        res = self.client.post(
            "/api/battle/action",
            json={"action": "switch", "target_index": 1, "session_id": "sess_switch"},
        )
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["player_event"]["action"], "switch")
        self.assertEqual(data["player_event"]["data"]["new_name"], "Vegeta")
        self.assertEqual(data["battle"]["player_team"]["active_index"], 1)
        self.assertEqual(data["battle"]["player"]["name"], "Vegeta")

    def test_battle_action_switch_errors(self):
        self._new_tag_battle("sess_switch_err")
        for payload in (
            {"target_index": 0},   # já ativo
            {"target_index": 9},   # índice inválido
            {"target_index": "1"},  # tipo inválido
            {},                    # ausente
        ):
            res = self.client.post(
                "/api/battle/action",
                json={"action": "switch", "session_id": "sess_switch_err", **payload},
            )
            self.assertEqual(res.status_code, 400, payload)

        # Lutador nocauteado não pode entrar
        self._battle("sess_switch_err")["player_team"].members[1].hp = 0
        res = self.client.post(
            "/api/battle/action",
            json={"action": "switch", "target_index": 1, "session_id": "sess_switch_err"},
        )
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.get_json()["reason"]["reason"], "is_dead")

    def test_enemy_ko_triggers_auto_switch(self):
        self._new_tag_battle("sess_enemy_ko")
        self._battle("sess_enemy_ko")["enemy_team"].members[0].hp = 1
        res = self.client.post(
            "/api/battle/action",
            json={"action": "move", "move_index": 0, "session_id": "sess_enemy_ko"},
        )
        data = res.get_json()
        self.assertEqual(data["battle"]["status"], "ongoing")
        self.assertEqual(data["battle"]["enemy_team"]["active_index"], 1)
        self.assertEqual(data["battle"]["enemy"]["name"], "Vegeta")

    def test_player_ko_triggers_auto_switch_and_loss(self):
        self._new_tag_battle("sess_player_ko")
        battle = self._battle("sess_player_ko")
        battle["player_team"].members[0].hp = 0
        # Força KO do ativo e simula o turno via ação neutra
        res = self.client.post(
            "/api/battle/action",
            json={"action": "defend", "stance": "block", "session_id": "sess_player_ko"},
        )
        data = res.get_json()
        self.assertEqual(data["battle"]["player_team"]["active_index"], 1)
        self.assertEqual(data["battle"]["status"], "ongoing")

        # Sem reservas vivas: derrota
        battle["player_team"].members[1].hp = 0
        res = self.client.post(
            "/api/battle/action",
            json={"action": "defend", "stance": "block", "session_id": "sess_player_ko"},
        )
        self.assertEqual(res.get_json()["battle"]["status"], "lost")

    def test_battle_won_blocks_further_actions(self):
        self.client.post(
            "/api/battle/new",
            json={"player_id": "goku", "enemy_id": "vegeta", "session_id": "sess_win"},
        )
        self._battle("sess_win")["enemy_team"].members[0].hp = 1
        res = self.client.post(
            "/api/battle/action",
            json={"action": "move", "move_index": 0, "session_id": "sess_win"},
        )
        data = res.get_json()
        self.assertEqual(data["battle"]["status"], "won")
        self.assertIsNone(data["ai_event"])

        res_after = self.client.post(
            "/api/battle/action",
            json={"action": "charge", "session_id": "sess_win"},
        )
        self.assertEqual(res_after.status_code, 400)

    def test_battle_action_transform(self):
        self.client.post(
            "/api/battle/new",
            json={"player_id": "goku", "enemy_id": "vegeta", "session_id": "sess_trans"},
        )
        # Ki 0: requer 50
        res_fail = self.client.post(
            "/api/battle/action",
            json={"action": "transform", "transformation": "Super Saiyan Goku", "session_id": "sess_trans"},
        )
        self.assertEqual(res_fail.status_code, 400)
        self.assertEqual(res_fail.get_json()["reason"]["reason"], "insufficient_ki")

        # Transformação inexistente
        res_unknown = self.client.post(
            "/api/battle/action",
            json={"action": "transform", "transformation": "Forma Fantasma", "session_id": "sess_trans"},
        )
        self.assertEqual(res_unknown.status_code, 400)

        self._battle("sess_trans")["player_team"].members[0].ki = 100
        res = self.client.post(
            "/api/battle/action",
            json={"action": "transform", "transformation": "Super Saiyan Goku", "session_id": "sess_trans"},
        )
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["player_event"]["action"], "transform")
        self.assertEqual(data["battle"]["player"]["current_transformation"], "Super Saiyan Goku")

    def test_save_and_load_api(self):
        temp_save = "temp_test_save.json"
        try:
            # Inicia batalha
            self.client.post(
                "/api/battle/new",
                json={"player_id": "goku", "enemy_id": "vegeta", "session_id": "sess_save"},
            )
            # Salva estado da batalha ativa
            res_save = self.client.post(
                "/api/save",
                json={"filename": temp_save, "session_id": "sess_save"},
            )
            self.assertEqual(res_save.status_code, 200)
            self.assertTrue(res_save.get_json()["success"])

            # Carrega estado
            res_load = self.client.post(
                "/api/load",
                json={"filename": temp_save},
            )
            self.assertEqual(res_load.status_code, 200)
            data = res_load.get_json()
            self.assertTrue(data["success"])
            self.assertEqual(data["data"]["player"]["raw_name"], "Goku")
        finally:
            if os.path.exists(temp_save):
                os.remove(temp_save)


if __name__ == "__main__":
    unittest.main()

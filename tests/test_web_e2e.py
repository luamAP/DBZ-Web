import json
import os
import threading
import unittest
import urllib.error
import urllib.request
from werkzeug.serving import make_server
from web.app import create_app


class TestWebE2E(unittest.TestCase):
    server = None
    server_thread = None
    base_url = None

    @classmethod
    def setUpClass(cls):
        app = create_app({"TESTING": True})
        # make_server com porta 0 aloca uma porta livre pelo SO
        cls.server = make_server("127.0.0.1", 0, app)
        cls.port = cls.server.port
        cls.base_url = f"http://127.0.0.1:{cls.port}"

        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        if cls.server:
            cls.server.shutdown()

    def _http_request(self, method, path, data=None):
        url = f"{self.base_url}{path}"
        headers = {}
        payload = None
        if data is not None:
            headers["Content-Type"] = "application/json"
            payload = json.dumps(data).encode("utf-8")

        req = urllib.request.Request(url, data=payload, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req) as response:
                status = response.status
                body = json.loads(response.read().decode("utf-8"))
                return status, body
        except urllib.error.HTTPError as e:
            status = e.code
            body = json.loads(e.read().decode("utf-8"))
            return status, body

    def test_e2e_full_battle_lifecycle_over_network(self):
        # 1. Health check HTTP real
        status, body = self._http_request("GET", "/")
        self.assertEqual(status, 200)
        self.assertEqual(body.get("status"), "ok")

        # 2. Consulta de catálogo
        status, body = self._http_request("GET", "/api/characters")
        self.assertEqual(status, 200)
        self.assertIn("Goku", body.get("characters", {}))

        # 3. Inicialização de Batalha via rede
        status, body = self._http_request(
            "POST",
            "/api/battle/new",
            {"player_id": "Goku", "enemy_id": "Vegeta", "session_id": "e2e_sess"},
        )
        self.assertEqual(status, 201)
        self.assertTrue(body["success"])
        self.assertEqual(body["battle"]["status"], "ongoing")
        self.assertEqual(body["battle"]["player"]["name"], "Goku")

        # 4. Consulta de estado de batalha via GET com query params
        status, body = self._http_request("GET", "/api/battle/state?session_id=e2e_sess")
        self.assertEqual(status, 200)
        self.assertEqual(body["battle"]["session_id"], "e2e_sess")

        # 5. Ação de Turno 1: Carregar Ki
        status, body = self._http_request(
            "POST",
            "/api/battle/action",
            {"action": "charge_ki", "session_id": "e2e_sess"},
        )
        self.assertEqual(status, 200)
        self.assertTrue(body["success"])
        self.assertEqual(body["player_event"]["action"], "charge")
        self.assertIsNotNone(body["ai_event"])
        self.assertEqual(body["battle"]["turn"], 2)

        # 6. Ação de Turno 2: Movimento de Ataque
        status, body = self._http_request(
            "POST",
            "/api/battle/action",
            {"action": "move", "move_name": "Melee Attack", "session_id": "e2e_sess"},
        )
        self.assertEqual(status, 200)
        self.assertTrue(body["success"])
        self.assertEqual(body["player_event"]["action"], "move")
        self.assertEqual(body["battle"]["turn"], 3)

        # 7. Persistência E2E: Salvar e restaurar estado
        temp_save = "e2e_temp_save.json"
        try:
            status, body = self._http_request(
                "POST",
                "/api/save",
                {"filename": temp_save, "session_id": "e2e_sess"},
            )
            self.assertEqual(status, 200)
            self.assertTrue(body["success"])

            status, body = self._http_request(
                "POST",
                "/api/load",
                {"filename": temp_save},
            )
            self.assertEqual(status, 200)
            self.assertTrue(body["success"])
            self.assertEqual(body["data"]["player"]["raw_name"], "Goku")
            self.assertEqual(body["data"]["turn"], 3)
        finally:
            if os.path.exists(temp_save):
                os.remove(temp_save)


if __name__ == "__main__":
    unittest.main()

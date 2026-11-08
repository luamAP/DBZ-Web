import unittest
from web.app import create_app


class TestWebLayout(unittest.TestCase):

    def setUp(self):
        self.app = create_app({"TESTING": True})
        self.client = self.app.test_client()

    def test_root_renders_gameboy_html(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn("text/html", res.content_type)
        html = res.get_data(as_text=True)

        # Valida a presença da carcaça do portátil
        self.assertIn("gameboy-console", html)
        self.assertIn("gameboy-screen-wrapper", html)
        self.assertIn("gameboy-controls-wrapper", html)

        # Valida metade superior (Visor, Display LCD e Diálogo)
        self.assertIn("screen-display", html)
        self.assertIn("battle-arena", html)
        self.assertIn("hud-opponent", html)
        self.assertIn("hud-player", html)
        self.assertIn("dialogue-box", html)

        # Valida metade inferior (Controles: D-Pad, A/B, Select/Start)
        self.assertIn("dpad-cross", html)
        self.assertIn("btnUp", html)
        self.assertIn("btnDown", html)
        self.assertIn("btnLeft", html)
        self.assertIn("btnRight", html)
        self.assertIn("btnA", html)
        self.assertIn("btnB", html)
        self.assertIn("btnSelect", html)
        self.assertIn("btnStart", html)

    def test_static_css_is_served(self):
        res = self.client.get("/static/css/gameboy.css")
        self.assertEqual(res.status_code, 200)
        self.assertIn("text/css", res.content_type)
        css = res.get_data(as_text=True)
        self.assertIn("--gb-body", css)
        self.assertIn(".gameboy-console", css)
        self.assertIn(".screen-display", css)

    def test_root_returns_json_when_requested(self):
        res = self.client.get("/?format=json")
        self.assertEqual(res.status_code, 200)
        self.assertIn("application/json", res.content_type)
        data = res.get_json()
        self.assertEqual(data["status"], "ok")


if __name__ == "__main__":
    unittest.main()

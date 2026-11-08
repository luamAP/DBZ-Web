import unittest
from web.app import create_app


class TestWebController(unittest.TestCase):

    def setUp(self):
        self.app = create_app({"TESTING": True})
        self.client = self.app.test_client()

    def test_gamepad_static_script_is_served(self):
        res = self.client.get("/static/js/gamepad.js")
        self.assertEqual(res.status_code, 200)
        self.assertTrue(
            "javascript" in res.content_type or "text/plain" in res.content_type
        )
        content = res.get_data(as_text=True)
        res.close()

        # Mapeamentos e funções essenciais
        self.assertIn("GamepadController", content)
        self.assertIn("BUTTON_NAMES", content)
        self.assertIn("KEY_CODE_MAP", content)
        self.assertIn("gb-input", content)
        self.assertIn("pointerdown", content)
        self.assertIn("keydown", content)
        self.assertIn("navigator.vibrate", content)

    def test_index_includes_controller_script_and_attributes(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        html = res.get_data(as_text=True)

        # Inclusão do script
        self.assertIn("js/gamepad.js", html)

        # Todos os 8 botões devem possuir o atributo data-btn
        expected_buttons = ["UP", "DOWN", "LEFT", "RIGHT", "A", "B", "SELECT", "START"]
        for btn in expected_buttons:
            self.assertIn(f'data-btn="{btn}"', html)


if __name__ == "__main__":
    unittest.main()

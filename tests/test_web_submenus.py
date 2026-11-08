import unittest
from web.app import create_app


class TestWebSubmenus(unittest.TestCase):

    def setUp(self):
        self.app = create_app({"TESTING": True})
        self.client = self.app.test_client()

    def test_submenus_html_elements_present(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        html = res.get_data(as_text=True)

        # Estrutura do submenu retrô
        self.assertIn('id="battleSubmenu"', html)
        self.assertIn('class="battle-submenu hidden"', html)
        self.assertIn('id="submenuTitle"', html)
        self.assertIn('id="submenuBackBtn"', html)
        self.assertIn('id="submenuList"', html)
        self.assertIn('[B] VOLTAR', html)

    def test_menu_js_contains_submenu_logic(self):
        res = self.client.get("/static/js/menu.js")
        self.assertEqual(res.status_code, 200)
        js = res.get_data(as_text=True)

        # Máquina de estados e transição de telas
        self.assertIn("currentScreen", js)
        self.assertIn("openSubmenu", js)
        self.assertIn("closeSubmenu", js)
        self.assertIn("navigateSubmenu", js)
        self.assertIn("selectSubmenuItem", js)
        self.assertIn("getSubmenuItems", js)
        self.assertIn("setCombatantData", js)

        # Categorias de submenus
        self.assertIn("'fight'", js)
        self.assertIn("'defend'", js)
        self.assertIn("'ki_form'", js)
        self.assertIn("'items_team'", js)

        # Eventos disparados
        self.assertIn("battle:submenu-open", js)
        self.assertIn("battle:submenu-close", js)
        self.assertIn("battle:submenu-move", js)
        self.assertIn("battle:submenu-select", js)
        self.assertIn("battle:action-execute", js)

    def test_gameboy_css_submenu_styles(self):
        res = self.client.get("/static/css/gameboy.css")
        self.assertEqual(res.status_code, 200)
        css = res.get_data(as_text=True)

        self.assertIn(".battle-submenu", css)
        self.assertIn(".battle-submenu.hidden", css)
        self.assertIn(".submenu-header", css)
        self.assertIn(".submenu-title", css)
        self.assertIn(".submenu-back-btn", css)
        self.assertIn(".submenu-list", css)
        self.assertIn(".submenu-item", css)
        self.assertIn(".submenu-item-info", css)


if __name__ == "__main__":
    unittest.main()

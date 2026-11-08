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
        self.assertIn('id="initialBattleData"', html)

    def test_submenus_initial_battle_data_data_driven(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        html = res.get_data(as_text=True)

        # Metadados reais dos YAMLs injetados no payload inicial
        self.assertIn('"Melee Attack"', html)
        self.assertIn('"Kamehameha"', html)
        self.assertIn('"Spirit Bomb"', html)
        self.assertIn('"Super Saiyan Goku"', html)
        self.assertIn('"defense_mechanics"', html)
        self.assertIn('"vanish"', html)
        self.assertIn('"consumables"', html)
        self.assertIn('"senzu_bean"', html)
        self.assertIn('"ki_capsule"', html)

    def test_menu_js_does_not_contain_mocked_fake_moves(self):
        res = self.client.get("/static/js/menu.js")
        self.assertEqual(res.status_code, 200)
        js = res.get_data(as_text=True)

        # Garante a ausência de opções fictícias hardcoded
        self.assertNotIn("'punch'", js)
        self.assertNotIn("'kaioken_rush'", js)
        self.assertNotIn("'ki_blast'", js)
        self.assertNotIn("'capsule_ki'", js)

    def test_api_battle_state_includes_yamls_catalogs(self):
        res = self.client.get("/api/battle/state")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get("success"))
        battle = data.get("battle", {})

        # Confirma que defense_mechanics e consumables são expostos
        self.assertIn("defense_mechanics", battle)
        self.assertIn("vanish", battle["defense_mechanics"])
        self.assertEqual(battle["defense_mechanics"]["vanish"]["ki_cost"], 25)

        self.assertIn("consumables", battle)
        self.assertIn("senzu_bean", battle["consumables"])
        self.assertIn("ki_capsule", battle["consumables"])
        self.assertEqual(battle["consumables"]["senzu_bean"]["name"], "Semente dos Deuses")

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

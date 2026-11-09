import unittest
from web.app import create_app


class TestWebMenu2x2(unittest.TestCase):

    def setUp(self):
        self.app = create_app({"TESTING": True})
        self.client = self.app.test_client()

    def test_menu_html_structure_in_root(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        html = res.get_data(as_text=True)

        # Inclusão do script do menu retrô
        self.assertIn("static/js/menu.js", html)

        # Caixa de diálogo e container da grade
        self.assertIn('id="dialogueBox"', html)
        self.assertIn('id="dialogueContent"', html)
        self.assertIn('id="dialogueText"', html)
        self.assertIn('class="battle-menu-grid"', html)
        self.assertIn('id="battleMenuGrid"', html)

        # Botões de ação 2x2 com coordenadas e identificadores
        expected_buttons = [
            ('id="btnActionFight"', 'data-action="fight"', 'data-row="0"', 'data-col="0"', "LUTAR"),
            ('id="btnActionDefend"', 'data-action="defend"', 'data-row="0"', 'data-col="1"', "DEFENDER"),
            ('id="btnActionKiForm"', 'data-action="ki_form"', 'data-row="1"', 'data-col="0"', "KI / FORMA"),
            ('id="btnActionItemsTeam"', 'data-action="items_team"', 'data-row="1"', 'data-col="1"', "ITENS / EQUIPE"),
        ]

        for btn_id, action, row, col, label in expected_buttons:
            self.assertIn(btn_id, html)
            self.assertIn(action, html)
            self.assertIn(row, html)
            self.assertIn(col, html)
            self.assertIn(label, html)

        # Cursor retrô indicador
        self.assertIn("menu-cursor", html)
        self.assertIn("▶", html)

        # Modais de sistema (START/SELECT) e campanha
        self.assertIn('id="systemMenuModal"', html)
        self.assertIn('id="systemMenuList"', html)
        self.assertIn('data-action="campaign"', html)
        self.assertIn('data-action="save"', html)
        self.assertIn('data-action="load"', html)
        self.assertIn('id="campaignModal"', html)
        self.assertIn('id="campaignDropsList"', html)
        self.assertIn('id="campaignContinueBtn"', html)

    def test_menu_js_is_served(self):
        res = self.client.get("/static/js/menu.js")
        self.assertEqual(res.status_code, 200)
        self.assertTrue(
            res.content_type.startswith("application/javascript")
            or res.content_type.startswith("text/javascript")
        )
        js = res.get_data(as_text=True)

        # Classes, matrizes e métodos essenciais
        self.assertIn("class BattleMenu", js)
        self.assertIn("MENU_ACTIONS", js)
        self.assertIn("ACTION_LABELS", js)
        self.assertIn("navigate", js)
        self.assertIn("setSelection", js)
        self.assertIn("selectCurrent", js)
        self.assertIn("cancel", js)
        self.assertIn("updateSelectionVisuals", js)
        self.assertIn("getSelectedAction", js)
        self.assertIn("toggleSystemMenu", js)
        self.assertIn("openSystemMenu", js)
        self.assertIn("closeSystemMenu", js)
        self.assertIn("navigateSystemMenu", js)
        self.assertIn("selectSystemMenuItem", js)

        # Integração de eventos
        self.assertIn("gb-input", js)
        self.assertIn("battle:action-select", js)
        self.assertIn("battle:menu-move", js)
        self.assertIn("window.BattleMenu = BattleMenu", js)

    def test_gameboy_css_menu_styles(self):
        res = self.client.get("/static/css/gameboy.css")
        self.assertEqual(res.status_code, 200)
        css = res.get_data(as_text=True)

        self.assertIn(".battle-menu-grid", css)
        self.assertIn(".menu-action-btn", css)
        self.assertIn(".menu-cursor", css)
        self.assertIn(".menu-action-btn.selected", css)
        self.assertIn("@keyframes cursor-blink", css)

        # Estilos dos modais de sistema e campanha
        self.assertIn(".system-menu-modal", css)
        self.assertIn(".system-menu-item.selected", css)
        self.assertIn(".campaign-modal", css)
        self.assertIn(".campaign-drop-badge", css)


if __name__ == "__main__":
    unittest.main()

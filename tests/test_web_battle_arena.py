import unittest
from web.app import create_app


class TestWebBattleArena(unittest.TestCase):

    def setUp(self):
        self.app = create_app({"TESTING": True})
        self.client = self.app.test_client()

    def test_arena_elements_rendered_in_html(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        html = res.get_data(as_text=True)

        # Arena e containers principais
        self.assertIn('class="battle-arena"', html)
        self.assertIn('id="opponentHud"', html)
        self.assertIn('id="playerHud"', html)

        # Plataformas retrô de combate (chão estilo Pokémon)
        self.assertIn("battle-ground opponent-ground", html)
        self.assertIn("battle-ground player-ground", html)

        # Sprites e placeholders
        self.assertIn('id="enemySpriteArea"', html)
        self.assertIn('id="enemySprite"', html)
        self.assertIn('id="enemySpriteImg"', html)
        self.assertIn('id="enemySpriteFallback"', html)
        self.assertIn('id="enemyKiAura"', html)
        self.assertIn('id="enemyDamagePopup"', html)
        self.assertIn('id="playerSpriteArea"', html)
        self.assertIn('id="playerSprite"', html)
        self.assertIn('id="playerSpriteImg"', html)
        self.assertIn('id="playerSpriteFallback"', html)
        self.assertIn('id="playerKiAura"', html)
        self.assertIn('id="playerDamagePopup"', html)
        self.assertIn('class="character-sprite"', html)
        self.assertIn('id="battleEffectsLayer"', html)

        # Barras de HP e Ki com classes de status
        self.assertIn('id="enemyHpBar"', html)
        self.assertIn('id="enemyKiBar"', html)
        self.assertIn('id="playerHpBar"', html)
        self.assertIn('id="playerKiBar"', html)
        self.assertIn("hp-high", html)

        # Valores numéricos e badges
        self.assertIn('id="enemyHpValues"', html)
        self.assertIn('id="playerHpValues"', html)
        self.assertIn('id="playerKiValues"', html)
        self.assertIn('id="enemyForm"', html)
        self.assertIn('id="playerForm"', html)
        self.assertIn('id="enemyStance"', html)
        self.assertIn('id="playerStance"', html)

        # Scripts carregados
        self.assertIn("static/js/battle.js", html)
        self.assertIn("static/js/gamepad.js", html)

    def test_battle_js_is_served(self):
        res = self.client.get("/static/js/battle.js")
        self.assertEqual(res.status_code, 200)
        self.assertTrue(
            res.content_type.startswith("application/javascript")
            or res.content_type.startswith("text/javascript")
        )
        js = res.get_data(as_text=True)
        self.assertIn("class BattleUI", js)
        self.assertIn("calculatePercentage", js)
        self.assertIn("getHpStatusClass", js)
        self.assertIn("updateCombatant", js)
        self.assertIn("animateDamage", js)
        self.assertIn("showDamagePopup", js)
        self.assertIn("playKiAura", js)
        self.assertIn("playSpecialAttackAnimation", js)
        self.assertIn("updateFromState", js)
        self.assertIn("window.BattleUI = BattleUI", js)
        self.assertEqual(js.count("{"), js.count("}"), "Chaves desbalanceadas em battle.js")

    def test_gameboy_css_has_arena_and_animation_rules(self):
        res = self.client.get("/static/css/gameboy.css")
        self.assertEqual(res.status_code, 200)
        css = res.get_data(as_text=True)

        # Plataformas
        self.assertIn(".battle-ground", css)
        self.assertIn(".opponent-ground", css)
        self.assertIn(".player-ground", css)

        # Estados de HP e Ki
        self.assertIn(".hp-high", css)
        self.assertIn(".hp-mid", css)
        self.assertIn(".hp-low", css)
        self.assertIn(".hp-critical", css)
        self.assertIn(".charging", css)

        # Animações de dano e efeitos
        self.assertIn(".damaged", css)
        self.assertIn("@keyframes damage-shake", css)
        self.assertIn("@keyframes damage-flash", css)
        self.assertIn("@keyframes hp-critical-blink", css)

        # Regras de renderização de sprites retrô
        self.assertIn("image-rendering: pixelated", css)
        self.assertIn(".character-sprite", css)
        self.assertIn(".pixel-sprite-container.has-sprite", css)

        # Efeitos visuais de combate: aura de ki, dano numérico e ataques especiais
        self.assertIn(".ki-aura-effect", css)
        self.assertIn("@keyframes ki-aura-pulse", css)
        self.assertIn(".damage-popup", css)
        self.assertIn("@keyframes damage-float", css)
        self.assertIn(".special-attack-beam", css)
        self.assertIn("@keyframes beam-shoot-player", css)
        self.assertIn("@keyframes beam-shoot-enemy", css)
        self.assertIn(".impact-burst", css)
        self.assertIn("@keyframes impact-explode", css)

    def test_battle_api_exposes_sprites(self):
        res = self.client.get("/api/battle/state")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get("success"))
        battle = data.get("battle", {})
        self.assertIn("player", battle)
        self.assertIn("enemy", battle)
        self.assertIn("sprites", battle["player"])
        self.assertIn("sprites", battle["enemy"])

        # Valida estrutura dos sprites serializados
        for key in ("front", "back", "portrait"):
            self.assertIn(key, battle["player"]["sprites"])
            self.assertIn(key, battle["enemy"]["sprites"])
            self.assertTrue(battle["player"]["sprites"][key].startswith("/static/"))
            self.assertTrue(battle["enemy"]["sprites"][key].startswith("/static/"))

    def test_static_sprite_svgs_are_served(self):
        sprites_to_check = [
            "/static/img/sprites/goku_front.svg",
            "/static/img/sprites/goku_back.svg",
            "/static/img/sprites/goku_portrait.svg",
            "/static/img/sprites/goku_ssj_front.svg",
            "/static/img/sprites/vegeta_front.svg",
            "/static/img/sprites/vegeta_back.svg",
            "/static/img/sprites/frieza_front.svg",
            "/static/img/sprites/frieza_final_front.svg",
        ]
        for sprite_url in sprites_to_check:
            with self.subTest(sprite=sprite_url):
                res = self.client.get(sprite_url)
                self.assertEqual(res.status_code, 200)
                self.assertIn("image/svg+xml", res.content_type)
                content = res.get_data(as_text=True)
                self.assertIn("<svg", content)
                self.assertIn("shape-rendering", content)


if __name__ == "__main__":
    unittest.main()

import os
import unittest
import yaml
from engine.data_loader import (
    load_characters_data,
    load_items_data,
    load_campaign_data,
    _get_data_dir,
)

RESERVED_CHARACTER_KEYS = {"defense_mechanics", "ai_profiles"}
ALLOWED_STAT_MULTIPLIERS = {"attack", "defense", "speed"}
ALLOWED_STAT_BONUSES = {"hp", "ki_max"}
MANDATORY_COMBATANTS = {"Goku", "Vegeta", "Frieza"}
MANDATORY_AI_PROFILES = {"tatico"}
MANDATORY_CAMPAIGNS = {"saiyan_invasion"}


class UniqueKeyLoader(yaml.SafeLoader):
    """Loader YAML que detecta chaves duplicadas no mesmo nível de mapeamento."""
    pass


def _construct_mapping(loader, node, deep=False):
    loader.flatten_mapping(node)
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"Chave duplicada encontrada no YAML: '{key}'")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_mapping,
)


class TestDataIntegrity(unittest.TestCase):

    def setUp(self):
        self.characters_data = load_characters_data()
        self.items_data = load_items_data()
        self.campaign_data = load_campaign_data()

    def _get_fighters(self):
        return {
            k: v for k, v in self.characters_data.items()
            if k not in RESERVED_CHARACTER_KEYS
        }

    def _assert_non_empty_str(self, val, field_name):
        self.assertIsInstance(val, str, f"{field_name} deve ser uma string.")
        self.assertTrue(len(val.strip()) > 0, f"{field_name} não pode ser vazio.")

    def _assert_int(self, val, field_name, min_val=None, max_val=None):
        self.assertIsInstance(val, int, f"{field_name} deve ser int.")
        self.assertNotIsInstance(val, bool, f"{field_name} não pode ser bool.")
        if min_val is not None:
            self.assertGreaterEqual(val, min_val, f"{field_name} deve ser >= {min_val}.")
        if max_val is not None:
            self.assertLessEqual(val, max_val, f"{field_name} deve ser <= {max_val}.")

    def _assert_num(self, val, field_name, min_val=None, max_val=None):
        self.assertIsInstance(val, (int, float), f"{field_name} deve ser numérico.")
        self.assertNotIsInstance(val, bool, f"{field_name} não pode ser bool.")
        if min_val is not None:
            self.assertGreaterEqual(val, min_val, f"{field_name} deve ser >= {min_val}.")
        if max_val is not None:
            self.assertLessEqual(val, max_val, f"{field_name} deve ser <= {max_val}.")

    def _assert_move(self, move, context, max_ki=None):
        self._assert_non_empty_str(move.get("name"), f"Nome do golpe em {context}")
        self._assert_int(move.get("ki_cost"), f"ki_cost em {context}", min_val=0)
        if max_ki is not None:
            self.assertLessEqual(
                move["ki_cost"],
                max_ki,
                f"ki_cost de '{move['name']}' ({move['ki_cost']}) não pode exceder ki_max ({max_ki}) em {context}."
            )

        self._assert_num(move.get("multiplier"), f"multiplier em {context}", min_val=0.01)
        self.assertIn(move.get("type"), ("basic", "combo", "special"), f"Tipo de golpe inválido em {context}.")

        if move["type"] == "combo":
            self._assert_int(move.get("hits"), f"hits do combo '{move['name']}' em {context}", min_val=2)
            self._assert_num(move.get("hit_chance"), f"hit_chance de '{move['name']}' em {context}", min_val=0.01, max_val=1.0)

    # --- Testes de Integridade Estrutural e Arquivos ---

    def test_yaml_files_have_no_duplicate_keys(self):
        """Garante que nenhum arquivo YAML possua chaves duplicadas mascaradas."""
        data_dir = _get_data_dir()
        yaml_files = ["characters.yml", "items.yml", "campaign.yml"]
        for yml_name in yaml_files:
            with self.subTest(file=yml_name):
                fpath = os.path.join(data_dir, yml_name)
                self.assertTrue(os.path.isfile(fpath), f"Arquivo {yml_name} não encontrado.")
                with open(fpath, "r", encoding="utf-8") as f:
                    try:
                        yaml.load(f, Loader=UniqueKeyLoader)
                    except ValueError as e:
                        self.fail(f"Chave duplicada detectada em {yml_name}: {e}")

    def test_critical_entrypoint_entities_exist(self):
        """Valida a existência das entidades que o código base e main.py referenciam diretamente."""
        fighters = self._get_fighters()
        for name in MANDATORY_COMBATANTS:
            with self.subTest(combatant=name):
                self.assertIn(name, fighters, f"Lutador obrigatório '{name}' não está em characters.yml.")

        profiles = self.characters_data.get("ai_profiles", {})
        for prof in MANDATORY_AI_PROFILES:
            with self.subTest(ai_profile=prof):
                self.assertIn(prof, profiles, f"Perfil de IA padrão '{prof}' não está em characters.yml.")

        campaigns = self.campaign_data.get("campaigns", {})
        for camp_id in MANDATORY_CAMPAIGNS:
            with self.subTest(campaign=camp_id):
                self.assertIn(camp_id, campaigns, f"Campanha obrigatória '{camp_id}' não está em campaign.yml.")

    # --- Testes de Mecânicas de Defesa e IA ---

    def test_defense_mechanics_integrity(self):
        """Valida que characters.yml contém defense_mechanics válidos."""
        self.assertIn("defense_mechanics", self.characters_data)
        defense = self.characters_data["defense_mechanics"]
        expected_defenses = {"block", "counter", "dodge", "vanish"}
        self.assertTrue(expected_defenses.issubset(set(defense.keys())))

        # Block
        self._assert_num(defense["block"].get("damage_reduction"), "block.damage_reduction", min_val=0.0, max_val=1.0)
        self._assert_int(defense["block"].get("ki_cost"), "block.ki_cost", min_val=0)

        # Counter
        self._assert_num(defense["counter"].get("damage_reduction"), "counter.damage_reduction", min_val=0.0, max_val=1.0)
        self._assert_num(defense["counter"].get("counter_damage_ratio"), "counter.counter_damage_ratio", min_val=0.01)
        self._assert_int(defense["counter"].get("ki_cost"), "counter.ki_cost", min_val=0)

        # Dodge
        self._assert_num(defense["dodge"].get("success_rate"), "dodge.success_rate", min_val=0.01, max_val=1.0)
        self._assert_int(defense["dodge"].get("ki_cost"), "dodge.ki_cost", min_val=0)

        # Vanish
        self._assert_int(defense["vanish"].get("ki_cost"), "vanish.ki_cost", min_val=0)

    def test_ai_profiles_integrity(self):
        """Valida todos os perfis de IA em characters.yml."""
        self.assertIn("ai_profiles", self.characters_data)
        profiles = self.characters_data["ai_profiles"]
        self.assertGreater(len(profiles), 0)

        required_keys = {
            "name", "special_bias", "combo_bias",
            "charge_ki_threshold", "defend_hp_threshold", "defense_bias"
        }

        for profile_id, profile in profiles.items():
            with self.subTest(profile_id=profile_id):
                for key in required_keys:
                    self.assertIn(key, profile, f"Perfil '{profile_id}' deve conter '{key}'.")

                self._assert_non_empty_str(profile["name"], f"{profile_id}.name")
                self._assert_num(profile["special_bias"], f"{profile_id}.special_bias", min_val=0.0, max_val=1.0)
                self._assert_num(profile["combo_bias"], f"{profile_id}.combo_bias", min_val=0.0, max_val=1.0)
                self._assert_num(profile["defense_bias"], f"{profile_id}.defense_bias", min_val=0.0, max_val=1.0)
                self._assert_num(profile["defend_hp_threshold"], f"{profile_id}.defend_hp_threshold", min_val=0.0, max_val=1.0)
                self._assert_int(profile["charge_ki_threshold"], f"{profile_id}.charge_ki_threshold", min_val=0)

    # --- Testes de Combatentes, Golpes e Transformações ---

    def test_characters_attributes_and_references(self):
        """Valida combatentes: atributos base, unicidade de golpes/transformações e requisitos."""
        profiles = self.characters_data.get("ai_profiles", {})
        fighters = self._get_fighters()
        self.assertGreater(len(fighters), 0, "Deve haver ao menos um combatente em characters.yml.")

        required_fighter_keys = {"name", "hp", "attack", "defense", "ki_max", "speed", "moves"}

        for fighter_id, fighter in fighters.items():
            with self.subTest(fighter=fighter_id):
                for key in required_fighter_keys:
                    self.assertIn(key, fighter, f"Combatente '{fighter_id}' deve conter '{key}'.")

                self._assert_non_empty_str(fighter["name"], f"{fighter_id}.name")
                self._assert_int(fighter["hp"], f"{fighter_id}.hp", min_val=1)
                self._assert_int(fighter["attack"], f"{fighter_id}.attack", min_val=1)
                self._assert_int(fighter["defense"], f"{fighter_id}.defense", min_val=1)
                self._assert_int(fighter["ki_max"], f"{fighter_id}.ki_max", min_val=1)
                self._assert_int(fighter["speed"], f"{fighter_id}.speed", min_val=1)

                # ai_profile é opcional conforme documentação (padrão 'tatico' no código)
                if "ai_profile" in fighter:
                    self._assert_non_empty_str(fighter["ai_profile"], f"{fighter_id}.ai_profile")
                    self.assertIn(
                        fighter["ai_profile"],
                        profiles,
                        f"ai_profile '{fighter['ai_profile']}' de '{fighter_id}' não existe em ai_profiles."
                    )

                # Golpes (moves)
                self.assertIsInstance(fighter["moves"], list)
                self.assertGreater(len(fighter["moves"]), 0, f"'{fighter_id}' deve ter ao menos um golpe.")
                
                move_names = []
                has_basic_free_move = False

                for move in fighter["moves"]:
                    self._assert_move(move, context=f"lutador '{fighter_id}'", max_ki=fighter["ki_max"])
                    move_names.append(move["name"])
                    if move["type"] == "basic" and move.get("ki_cost") == 0:
                        has_basic_free_move = True

                # Unicidade de nomes de golpes por combatente
                self.assertEqual(
                    len(move_names),
                    len(set(move_names)),
                    f"'{fighter_id}' possui golpes com nomes duplicados: {move_names}"
                )

                # Golpe básico com custo zero obrigatório para compatibilidade da IA e fallback
                self.assertTrue(
                    has_basic_free_move,
                    f"'{fighter_id}' deve possuir pelo menos 1 golpe 'basic' com ki_cost == 0."
                )

                # Transformações (opcional)
                if "transformations" in fighter and fighter["transformations"]:
                    self.assertIsInstance(fighter["transformations"], list)
                    trans_names = []
                    for trans in fighter["transformations"]:
                        self._assert_non_empty_str(trans.get("name"), f"Nome de transformação em '{fighter_id}'")
                        trans_names.append(trans["name"])

                        self._assert_int(trans.get("required_ki"), f"required_ki de '{trans.get('name')}'", min_val=0)
                        self.assertLessEqual(
                            trans["required_ki"],
                            fighter["ki_max"],
                            f"Transformação '{trans['name']}' exige mais Ki ({trans['required_ki']}) que o ki_max de '{fighter_id}' ({fighter['ki_max']})."
                        )

                        self._assert_num(trans.get("hp_threshold_pct"), f"hp_threshold_pct de '{trans.get('name')}'", min_val=0.01, max_val=1.0)

                        self.assertIn("stat_multipliers", trans)
                        multipliers = trans["stat_multipliers"]
                        self.assertIsInstance(multipliers, dict)
                        for stat, mult in multipliers.items():
                            self.assertIn(
                                stat,
                                ALLOWED_STAT_MULTIPLIERS,
                                f"Atributo inválido '{stat}' em stat_multipliers da transformação '{trans['name']}'."
                            )
                            self._assert_num(mult, f"Multiplicador {stat} em '{trans['name']}'", min_val=0.01)

                    self.assertEqual(
                        len(trans_names),
                        len(set(trans_names)),
                        f"'{fighter_id}' possui transformações com nomes duplicados: {trans_names}"
                    )

    # --- Testes de Itens: Equipamentos e Consumíveis ---

    def test_equipment_integrity(self):
        """Valida que todos os equipamentos em items.yml possuem esquema estrito e campos válidos."""
        self.assertIn("equipment", self.items_data)
        equipment = self.items_data["equipment"]
        self.assertGreater(len(equipment), 0)

        for eq_key, eq in equipment.items():
            with self.subTest(equipment=eq_key):
                self._assert_non_empty_str(eq.get("id"), f"id de {eq_key}")
                self.assertEqual(eq_key, eq["id"], f"Chave de equipamento '{eq_key}' deve coincidir com seu id.")
                self._assert_non_empty_str(eq.get("name"), f"name de {eq_key}")
                self._assert_non_empty_str(eq.get("description"), f"description de {eq_key}")

                if "stat_multipliers" in eq and eq["stat_multipliers"]:
                    self.assertIsInstance(eq["stat_multipliers"], dict)
                    for stat, mult in eq["stat_multipliers"].items():
                        self.assertIn(
                            stat,
                            ALLOWED_STAT_MULTIPLIERS,
                            f"Atributo desconhecido '{stat}' em stat_multipliers de '{eq_key}'."
                        )
                        self._assert_num(mult, f"{eq_key}.stat_multipliers.{stat}", min_val=0.01)

                if "stat_bonuses" in eq and eq["stat_bonuses"]:
                    self.assertIsInstance(eq["stat_bonuses"], dict)
                    for stat, bonus in eq["stat_bonuses"].items():
                        self.assertIn(
                            stat,
                            ALLOWED_STAT_BONUSES,
                            f"Atributo desconhecido '{stat}' em stat_bonuses de '{eq_key}'."
                        )
                        self._assert_int(bonus, f"{eq_key}.stat_bonuses.{stat}")

                if "granted_moves" in eq and eq["granted_moves"]:
                    self.assertIsInstance(eq["granted_moves"], list)
                    for move in eq["granted_moves"]:
                        self._assert_move(move, context=f"equipamento '{eq_key}'")

    def test_consumables_integrity(self):
        """Valida consumíveis em items.yml com campos obrigatórios e opcionais conformes."""
        self.assertIn("consumables", self.items_data)
        consumables = self.items_data["consumables"]
        self.assertGreater(len(consumables), 0)

        for item_key, item in consumables.items():
            with self.subTest(consumable=item_key):
                self._assert_non_empty_str(item.get("id"), f"id de {item_key}")
                self.assertEqual(item_key, item["id"], f"Chave '{item_key}' deve coincidir com seu id.")
                self._assert_non_empty_str(item.get("name"), f"name de {item_key}")
                self._assert_non_empty_str(item.get("description"), f"description de {item_key}")
                self._assert_int(item.get("default_quantity"), f"{item_key}.default_quantity", min_val=1)

                if "hp_restore_pct" in item:
                    self._assert_num(item["hp_restore_pct"], f"{item_key}.hp_restore_pct", min_val=0.0, max_val=1.0)
                if "hp_restore_fixed" in item:
                    self._assert_int(item["hp_restore_fixed"], f"{item_key}.hp_restore_fixed", min_val=0)
                if "ki_restore_amount" in item:
                    self._assert_int(item["ki_restore_amount"], f"{item_key}.ki_restore_amount", min_val=0)

    def test_granted_moves_do_not_collide_with_fighter_base_moves(self):
        """
        Garante que nenhum golpe concedido por equipamento colida em nome com os golpes
        básicos de combatentes, prevenindo que unequip_item remova acidentalmente golpes nativos.
        """
        equipment = self.items_data.get("equipment", {})
        fighters = self._get_fighters()

        granted_move_names = {}
        for eq_id, eq in equipment.items():
            for move in eq.get("granted_moves", []):
                granted_move_names[move["name"]] = eq_id

        for fighter_id, fighter in fighters.items():
            fighter_moves = {m["name"] for m in fighter.get("moves", [])}
            collision = fighter_moves.intersection(set(granted_move_names.keys()))
            self.assertFalse(
                collision,
                f"Lutador '{fighter_id}' possui golpes nativos que colidem com golpes concedidos por equipamentos: {collision}"
            )

    # --- Testes de Campanhas e Referências Cruzadas ---

    def test_campaign_yaml_integrity_and_cross_references(self):
        """Valida campaign.yml e referências cruzadas com characters.yml e items.yml."""
        self.assertIn("campaigns", self.campaign_data)
        campaigns = self.campaign_data["campaigns"]
        self.assertGreater(len(campaigns), 0)

        fighters = self._get_fighters()
        equipments = self.items_data.get("equipment", {})
        consumables = self.items_data.get("consumables", {})

        for camp_key, campaign in campaigns.items():
            with self.subTest(campaign=camp_key):
                self._assert_non_empty_str(campaign.get("id"), f"id de {camp_key}")
                self.assertEqual(camp_key, campaign["id"], f"Chave '{camp_key}' deve coincidir com id.")
                self._assert_non_empty_str(campaign.get("name"), f"name de {camp_key}")
                self._assert_non_empty_str(campaign.get("description"), f"description de {camp_key}")
                self.assertIn("stages", campaign)

                stages = campaign["stages"]
                self.assertIsInstance(stages, list)
                self.assertGreater(len(stages), 0)

                for idx, stage in enumerate(stages, start=1):
                    with self.subTest(campaign=camp_key, stage_index=idx):
                        self._assert_int(stage.get("stage"), f"stage em fase {idx}", min_val=1)
                        self.assertEqual(stage.get("stage"), idx, f"Estágio na posição {idx} deve ter stage={idx}.")
                        self._assert_non_empty_str(stage.get("name"), f"name da fase {idx}")
                        self._assert_non_empty_str(stage.get("enemy"), f"enemy da fase {idx}")

                        # Referência cruzada: enemy deve ser um combatente válido
                        self.assertIn(
                            stage["enemy"],
                            fighters,
                            f"Inimigo '{stage['enemy']}' da fase {idx} não existe em characters.yml."
                        )

                        # Recuperação (opcional conforme docs/campaign_template.md)
                        if "recovery" in stage and stage["recovery"]:
                            rec = stage["recovery"]
                            self.assertIsInstance(rec, dict)
                            if "hp_pct" in rec:
                                self._assert_num(rec["hp_pct"], f"recovery.hp_pct fase {idx}", min_val=0.0, max_val=1.0)
                            if "hp_fixed" in rec:
                                self._assert_int(rec["hp_fixed"], f"recovery.hp_fixed fase {idx}", min_val=0)
                            if "ki_bonus" in rec:
                                self._assert_int(rec["ki_bonus"], f"recovery.ki_bonus fase {idx}", min_val=0)

                        # Drop table (opcional conforme docs/campaign_template.md)
                        if "drop_table" in stage and stage["drop_table"]:
                            self.assertIsInstance(stage["drop_table"], list)
                            for drop in stage["drop_table"]:
                                self._assert_non_empty_str(drop.get("item_id"), f"item_id em drop fase {idx}")
                                self.assertIn(drop.get("item_type"), ("equipment", "consumable"))
                                self._assert_num(drop.get("chance"), f"chance em drop fase {idx}", min_val=0.01, max_val=1.0)

                                if drop["item_type"] == "consumable":
                                    if "quantity" in drop:
                                        self._assert_int(drop["quantity"], f"quantity em drop fase {idx}", min_val=1)
                                    self.assertIn(
                                        drop["item_id"],
                                        consumables,
                                        f"Consumível '{drop['item_id']}' no drop não existe em items.yml."
                                    )
                                elif drop["item_type"] == "equipment":
                                    self.assertIn(
                                        drop["item_id"],
                                        equipments,
                                        f"Equipamento '{drop['item_id']}' no drop não existe em items.yml."
                                    )


if __name__ == "__main__":
    unittest.main()

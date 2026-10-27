# Arquitetura

| Arquivo | Responsabilidade |
| --- | --- |
| `characters.yml` | Lutadores, técnicas, transformações, parâmetros de defesa |
| `items.yml` | Equipamentos e consumíveis |
| `character_template.md` | Esquema de lutadores |
| `data_loader.py` | Único ponto de I/O YAML; `create_initial_inventory` |
| `main.py` | CLI, menu, inicialização via `data_loader` |
| `battle_engine.py` | Loop de turnos (`battle`, `battle_team`), menus e todo texto de UI |
| `ai_controller.py` | Decisão heurística da IA (Ki, HP, defesa) |
| `models/__init__.py` | Fachada: exporta `Character`, `Team` |
| `models/character.py` | Stats, `_recalculate_stats`, equip/unequip, consumíveis, transformação, `execute_move`, `apply_incoming_damage` |
| `models/team.py` | Tag Team: ativo, `get_bench_members`, `switch_member`, `auto_switch_next_alive` |
| `tests/test_character.py` | Atributos, transformações, itens |
| `tests/test_team.py` | Rotação e KO |
| `tests/test_combat_flow.py` | Ações, Ki, defesas |
| `tests/test_domain_purity.py` | AST: pureza de `models/` |
| `run_tests.py` | Roda `tests/`; console = resumo + falhas; log completo em `logs/log_<fase>.txt` |
| `ROADMAP.md` | Itens pendentes |
| `.agents/rules/` | Regras do agente |

**Dependências:** yml → `data_loader` → `main` / `tests` → `battle_engine` → `models`, `ai_controller`.

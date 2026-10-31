# Arquitetura

| Arquivo | Responsabilidade |
| --- | --- |
| `data/characters.yml` | Lutadores, técnicas, transformações, parâmetros de defesa |
| `data/items.yml` | Equipamentos e consumíveis |
| `data/campaign.yml` | Campanhas, fases sequenciais, oponentes e tabelas de drops |
| `docs/character_template.md` | Esquema de lutadores |
| `docs/campaign_template.md` | Esquema de campanhas e drops |
| `docs/ROADMAP_v1.md` | Histórico de fases concluídas (Versão 1.0 CLI) |
| `engine/__init__.py` | Fachada: exporta funções de `data_loader`, `battle_engine` e `ai_controller` |
| `engine/data_loader.py` | I/O YAML (`data/`) e save/load de `save.json`; `create_initial_inventory` |
| `engine/battle_engine.py` | Loop de turnos (`battle`, `battle_team`), modo campanha, menus e todo texto de UI |
| `engine/ai_controller.py` | Decisão heurística da IA (Ki, HP, defesa) |
| `main.py` | CLI, menu, inicialização via `engine` |
| `models/__init__.py` | Fachada: exporta `Character`, `Team`, `Campaign` |
| `models/character.py` | Stats, `_recalculate_stats`, equip/unequip, consumíveis, recuperação, transformação, serialização (`to_dict`/`load_state`), `execute_move`, `apply_incoming_damage` |
| `models/team.py` | Tag Team: ativo, `get_bench_members`, `switch_member`, `auto_switch_next_alive` |
| `models/campaign.py` | Entidade de campanha: fases, resolução de drops, recuperação e serialização |
| `tests/test_character.py` | Atributos, transformações, itens |
| `tests/test_team.py` | Rotação e KO |
| `tests/test_campaign.py` | Progressão de campanha, drops e recuperação |
| `tests/test_save_state.py` | Serialização e restauração de save state (personagem e campanha) |
| `tests/test_combat_flow.py` | Ações, Ki, defesas |
| `tests/test_ai.py` | Decisão da IA por personalidade (agressivo, defensivo, tático) |
| `tests/test_domain_purity.py` | AST: pureza de `models/` |
| `tests/test_data_integrity.py` | Integridade e validação de esquemas e referências cruzadas dos YAMLs |
| `run_tests.py` | Roda `tests/`; console = resumo + falhas; log completo em `logs/log_<fase>.txt` |
| `.github/workflows/tests.yml` | Pipeline de CI/CD: execução automatizada de testes no GitHub Actions |
| `ROADMAP.md` | Roadmap ativo (Versão 2.0 Web Game Boy) |
| `.agents/rules/` | Regras do agente |

**Dependências:** `data/*.yml` → `engine.data_loader` → `main` / `tests` → `engine.battle_engine` → `models`, `engine.ai_controller`.

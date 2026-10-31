# Arquitetura

| Arquivo | Responsabilidade |
| --- | --- |
| `characters.yml` | Lutadores, técnicas, transformações, parâmetros de defesa |
| `items.yml` | Equipamentos e consumíveis |
| `campaign.yml` | Campanhas, fases sequenciais, oponentes e tabelas de drops |
| `character_template.md` | Esquema de lutadores |
| `campaign_template.md` | Esquema de campanhas e drops |
| `data_loader.py` | I/O YAML e save/load de `save.json`; `create_initial_inventory` |
| `main.py` | CLI, menu, inicialização via `data_loader` |
| `battle_engine.py` | Loop de turnos (`battle`, `battle_team`), modo campanha, menus e todo texto de UI |
| `ai_controller.py` | Decisão heurística da IA (Ki, HP, defesa) |
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
| `run_tests.py` | Roda `tests/`; console = resumo + falhas; log completo em `logs/log_<fase>.txt` |
| `.github/workflows/tests.yml` | Pipeline de CI/CD: execução automatizada de testes no GitHub Actions |
| `ROADMAP.md` | Roadmap ativo (Versão 2.0 Web Game Boy) |
| `ROADMAP_v1.md` | Histórico de fases concluídas (Versão 1.0 CLI) |
| `.agents/rules/` | Regras do agente |

**Dependências:** yml → `data_loader` → `main` / `tests` → `battle_engine` → `models`, `ai_controller`.

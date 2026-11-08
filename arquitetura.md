# Arquitetura

| Arquivo | Responsabilidade |
| --- | --- |
| `data/characters.yml` | Lutadores, técnicas, transformações, parâmetros de defesa |
| `data/items.yml` | Equipamentos e consumíveis |
| `data/campaign.yml` | Campanhas, fases sequenciais, oponentes e tabelas de drops |
| `docs/character_template.md` | Esquema de lutadores |
| `docs/campaign_template.md` | Esquema de campanhas e drops |
| `docs/ROADMAP_v1.md` | Histórico de fases concluídas (Versão 1.0 CLI) |
| `docs/plans/` | Relatórios de execução (um por item do ROADMAP) |
| `engine/__init__.py` | Fachada: exporta funções de `data_loader`, `battle_engine` e `ai_controller` |
| `engine/data_loader.py` | I/O YAML (`data/`) e save/load de `save.json`; `create_initial_inventory` |
| `engine/battle_engine.py` | Loop de turnos (`battle`, `battle_team`), modo campanha, menus e todo texto de UI |
| `engine/ai_controller.py` | Decisão heurística da IA (Ki, HP, defesa) |
| `main.py` | CLI, menu, inicialização via `engine` |
| `models/__init__.py` | Fachada: exporta `Character`, `Team`, `Campaign` |
| `models/character.py` | Stats, `_recalculate_stats`, equip/unequip, consumíveis, recuperação, transformação, serialização (`to_dict`/`load_state`), `execute_move`, `apply_incoming_damage` |
| `models/team.py` | Tag Team: ativo, `get_bench_members`, `switch_member`, `auto_switch_next_alive` |
| `models/campaign.py` | Entidade de campanha: fases, resolução de drops, recuperação e serialização |
| `web/__init__.py` | Pacote da camada Web (Flask) |
| `web/app.py` | API Flask: rotas REST de batalha (1v1 e Tag Team via `Team`), catálogo, turnos de IA e save state |
| `web/templates/index.html` | Template HTML5 da carcaça do Game Boy (visor superior e controles inferiores) |
| `web/static/css/gameboy.css` | Folha de estilos retrô Game Boy mobile-first com paleta DMG e botões táteis |
| `web/static/js/gamepad.js` | Controlador unificado de input virtual touch, teclado e feedback haptic |
| `web/static/js/battle.js` | Módulo de animação e sincronização da arena de batalha (barras de HP/Ki e dano) |
| `web/static/js/menu.js` | Navegação e máquina de estados do menu 2x2 estilo Pokémon via D-Pad e A/B |
| `tests/test_character.py` | Atributos, transformações, itens |
| `tests/test_team.py` | Rotação e KO |
| `tests/test_campaign.py` | Progressão de campanha, drops e recuperação |
| `tests/test_save_state.py` | Serialização e restauração de save state (personagem e campanha) |
| `tests/test_combat_flow.py` | Ações, Ki, defesas |
| `tests/test_ai.py` | Decisão da IA por personalidade (agressivo, defensivo, tático) |
| `tests/test_domain_purity.py` | AST: pureza de `models/` |
| `tests/test_data_integrity.py` | Integridade e validação de esquemas e referências cruzadas dos YAMLs |
| `tests/test_properties.py` | Testes baseados em propriedades (Hypothesis): invariantes de domínio |
| `tests/test_web_api.py` | Testes de integração da API Flask (endpoints REST, turnos, save/load) |
| `tests/test_web_e2e.py` | Testes ponta a ponta (E2E) com servidor Flask ativo e requisições HTTP reais |
| `tests/test_web_layout.py` | Testes de renderização do layout HTML5 e assets estáticos da carcaça Game Boy |
| `tests/test_web_battle_arena.py` | Testes da arena de batalha, barras animadas e módulo frontend BattleUI |
| `tests/test_web_controller.py` | Testes do módulo de controle virtual (touch, teclado e data-attributes) |
| `tests/test_web_menu_2x2.py` | Testes da grade de ações 2x2, cursor retrô e integração de navegação |
| `tests/test_web_submenus.py` | Testes dos submenus de combate, transição de telas e controle por gamepad |
| `run_tests.py` | Roda `tests/`; console = resumo + falhas + cobertura; logs detalhados em `logs/` |
| `pyproject.toml` | Metadados do projeto e declaração de dependências gerenciadas via `uv` |
| `uv.lock` | Lockfile multiplataforma de dependências do `uv` |
| `.github/workflows/tests.yml` | Pipeline de CI/CD: execução automatizada de testes no GitHub Actions |
| `ROADMAP.md` | Roadmap ativo (Versão 2.0 Web Game Boy) |
| `.agents/rules/` | Regras do agente |

**Dependências:** `data/*.yml` → `engine.data_loader` → `main` / `web.app` / `tests` → `engine.battle_engine` / `web.app` → `models`, `engine.ai_controller`.

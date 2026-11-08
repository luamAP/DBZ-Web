# fase2 — Sincronização Dinâmica dos Submenus com Dados dos YAMLs

Status: concluído

## Objetivo
Tornar os submenus 100% orientados a dados (data-driven), consumindo dinamicamente as definições dos YAMLs (`characters.yml` e `items.yml`) via API, eliminando opções estáticas/mockadas no frontend.

## Arquivos
- `web/app.py` — Enriquecer o payload de estado da batalha (`serialize_battle`) com `defense_mechanics` e catálogo de `consumables` carregados dos YAMLs, além de auto-inicializar a sessão padrão no endpoint de inicialização/HTML.
- `web/static/js/battle.js` — Inicializar automaticamente a batalha na carga da página chamando a API e propagando metadados completos para o menu.
- `web/static/js/menu.js` — Gerar dinamicamente as listas de LUTAR, DEFENDER, KI/FORMA e ITENS/EQUIPE exclusivamente a partir dos dados fornecidos pela API (sem fallbacks com listas fictícias).
- `web/templates/index.html` — Injetar `initialBattleData` para renderização imediata na carga da página.
- `tests/test_web_submenus.py` — Testes validando que adições e alterações em `characters.yml` e `items.yml` são refletidas nos submenus da aplicação web.

## Passos
- [x] Atualizar `serialize_battle` em `web/app.py` para incluir as regras ativas de `defense_mechanics` e catálogo de `consumables` do YAML
- [x] Garantir inicialização e sincronização da batalha padrão (Goku vs Vegeta) na inicialização em `web/app.py` e `web/static/js/battle.js`
- [x] Refatorar `getSubmenuItems` em `web/static/js/menu.js` para renderizar dinamicamente técnicas, defesas, transformações e itens a partir dos metadados da sessão, removendo itens inventados
- [x] Atualizar `tests/test_web_submenus.py` para validar a sincronização dinâmica e a ausência de dados mockados estáticos
- [x] Validar a suíte com `uv run python run_tests.py fase2` e checar `tests/test_domain_purity.py`

## Desvios
—

## Testes
OK: 93 testes | 0 falhas | 0 erros | 0 ignorados
Cobertura: 55.7% | Relatório: logs/coverage_geral.txt

## Validar
uv run python run_tests.py fase2

## Commit
feat(web): sincronizar submenus dinamicamente com yaml de personagens e itens

# fase1 — API Flask integrada ao domínio puro

Status: concluído

## Objetivo
Implementar a API REST em Flask (`web/app.py`) conectando os modelos de combate (`models/`), I/O e save/load (`engine/data_loader.py`) e decisões heurísticas da IA (`engine/ai_controller.py`).

## Arquivos
- `requirements.txt` — Adicionar `Flask>=3.0.0`
- `web/__init__.py` — Pacote da camada Web
- `web/app.py` — Servidor Flask com rotas de batalha, turnos, catálogo e save state
- `tests/test_domain_purity.py` — Blindagem contra imports de `engine` ou `flask` dentro de `models/`
- `tests/test_web_api.py` — Suíte de testes de integração da API Web
- `tests/test_web_e2e.py` — Testes ponta a ponta (E2E) com servidor Flask ativo e chamadas HTTP reais
- `arquitetura.md` — Mapeamento dos novos arquivos
- `ROADMAP.md` — Conclusão do item 1 da Fase 1

## Passos
- [x] Adicionar `Flask>=3.0.0` a `requirements.txt` e instalar dependências
- [x] Atualizar `tests/test_domain_purity.py` para validar proibição de imports de `engine` ou `flask` em `models/`
- [x] Criar pacote `web/` com `web/__init__.py` e `web/app.py`
- [x] Implementar rotas `/api/characters`, `/api/items` e `/api/campaign`
- [x] Implementar rotas `/api/battle/new`, `/api/battle/state` e `/api/battle/action`
- [x] Implementar rotas `/api/save` e `/api/load`
- [x] Criar suíte de testes de integração em `tests/test_web_api.py`
- [x] Criar testes E2E reais via socket HTTP em `tests/test_web_e2e.py`
- [x] Atualizar `arquitetura.md` e `ROADMAP.md`

## Desvios
- Ação `switch` (Tag Team), prevista no plano, ficou de fora da primeira entrega e o relatório registrou "—" por engano. Corrigido depois: `/api/battle/new` aceita `player_ids`/`enemy_ids`, a batalha usa `Team`, existe a ação `switch` e há troca automática em KO (inclusive KO por contra-ataque).
- Ação `transform` passava o nome (string) para `Character.transform`, que espera o dict da transformação; quebraria em uso real. Corrigida e coberta por teste.
- `run_tests.py` não media cobertura de `web/`; incluído em `source`.
- `app.extensions["battles"]` expõe o estado em memória para testes determinísticos de KO.

## Testes
OK: 76 testes | 0 falhas | 0 erros | 0 ignorados
Cobertura: 54.4% total | `web/app.py` 83% | Relatório: logs/coverage_fase1.txt

## Validar
Executar `.venv/bin/python run_tests.py fase1` e `.venv/bin/python -m unittest tests/test_domain_purity.py`.

## Commit
feat(fase1): implementar api flask integrada ao dominio puro e ia

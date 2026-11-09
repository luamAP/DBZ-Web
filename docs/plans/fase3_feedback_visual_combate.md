# fase3 — Feedback Visual de Combate e Animações

Status: concluído

## Objetivo
Implementar feedback visual retrô na arena de batalha com auras dinâmicas ao carregar Ki, efeitos de dano com piscar/tremer e animações de feixes e impactos para ataques especiais.

## Arquivos
- `web/templates/index.html` — Camada de efeitos visuais na arena (`battle-effects-layer`) e elementos de aura nos sprites
- `web/static/css/gameboy.css` — Estilização e keyframes retrô para aura de Ki, projeção de ataques especiais (beam/blast), impactos e números de dano
- `web/static/js/battle.js` — Orquestração sequencial dos efeitos visuais (carregamento de Ki, disparo de ataque especial, impacto e dano) vinculados a `player_event` e `ai_event`
- `tests/test_web_battle_arena.py` — Testes de validação dos elementos de efeitos, regras CSS de aura/ataques especiais e métodos de animação
- `arquitetura.md` — Documentação das capacidades de animação e efeitos visuais da arena

## Passos
- [x] Adicionar camada de efeitos e containers de aura nos sprites em `web/templates/index.html`
- [x] Criar regras CSS e keyframes em `web/static/css/gameboy.css` para auras de Ki (pulso de energia e brilho), rajadas de energia de golpes especiais e impacto
- [x] Implementar em `web/static/js/battle.js` métodos para acionar aura de Ki (`playKiAura`), disparar feixe de golpe especial (`playSpecialAttackAnimation`) e feedback numérico/shake de dano
- [x] Integrar a orquestração sequencial de turnos em `handleActionExecute` para disparar os efeitos do jogador e em seguida da IA com delays sincronizados
- [x] Atualizar `tests/test_web_battle_arena.py` cobrindo a camada de efeitos, animações e métodos de feedback
- [x] Atualizar `arquitetura.md` com a nova camada visual

## Desvios
—

## Testes
OK: 97 testes | 0 falhas | 0 erros | 0 ignorados
Cobertura: 56.1% | Relatório: logs/coverage_fase3.txt

## Validar
Executar `uv run python run_tests.py fase3` e verificar efeitos de animação e renderização.

## Commit
feat(web): implementar feedback visual de combate com auras, ataques especiais e dano

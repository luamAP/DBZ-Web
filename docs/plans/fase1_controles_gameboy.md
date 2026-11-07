# fase1 — Controles virtuais touch e teclado (D-Pad, A/B, Start/Select)

Status: concluído

## Objetivo
Implementar o módulo unificado de controle virtual em JavaScript (`web/static/js/gamepad.js`) com suporte simultâneo a toques virtuais na tela (mobile com vibração haptic) e teclado físico (desktop), integrando espelhamento visual e eventos customizados (`gb-input`).

## Arquivos
- `web/static/js/gamepad.js` — Módulo GamepadController com mapeamento de teclado, touch/pointer e haptic feedback
- `web/templates/index.html` — Inclusão do script, atributos `data-btn` nos botões e legenda de atalhos
- `web/static/css/gameboy.css` — Estilização de feedback de pressão `.pressed` e legenda de teclas
- `tests/test_web_controller.py` — Testes automatizados do script de controle e do DOM
- `arquitetura.md` — Mapeamento dos novos arquivos
- `ROADMAP.md` — Conclusão do item 3 e finalização da Fase 1

## Passos
- [x] Criar `web/static/js/gamepad.js` com classe `GamepadController`
- [x] Mapear teclado físico (Setas/WASD para D-Pad, Z/Enter para A, X/Esc para B, Shift para Select, Espaço/1 para Start)
- [x] Implementar espelhamento visual de teclas pressionadas nos botões físicos virtuais
- [x] Adicionar suporte a vibração tátil mobile (`navigator.vibrate`)
- [x] Disparar eventos desacoplados `gb-input` para integração com menus de batalha
- [x] Atualizar `web/templates/index.html` com atributos `data-btn` e script
- [x] Adicionar estilos de estado `.pressed` e legenda em `web/static/css/gameboy.css`
- [x] Criar suíte de testes em `tests/test_web_controller.py`
- [x] Atualizar `arquitetura.md` e `ROADMAP.md`

## Desvios
—

## Testes
OK: 81 testes | 0 falhas | 0 erros | 0 ignorados
Cobertura: 55.2% total | `web/app.py` 84% | Relatório: logs/coverage_fase1.txt

## Validar
Executar `.venv/bin/python run_tests.py fase1` e verificar `tests/test_web_controller.py`.

## Commit
feat(fase1): implementar controles virtuais touch e teclado com d-pad e botoes a/b/start/select

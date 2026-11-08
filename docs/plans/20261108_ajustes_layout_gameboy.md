# 20261108 — Ajustes de Layout e Espaçamento dos Controles

Status: concluído

## Objetivo
Remover o indicador de bateria, header do visor, branding e legenda de teclado, além de ajustar o espaçamento dos botões e proporções da tela LCD.

## Arquivos
- `web/templates/index.html` — Remoção de `battery-indicator`, `screen-bezel-header`, `console-branding` e `keyboard-legend`
- `web/static/css/gameboy.css` — Ajuste de proporção da tela LCD, remoção de regras obsoletas e espaçamento lateral dos botões
- `tests/test_web_layout.py` — Validação do layout do visor e controles
- `tests/test_web_controller.py` — Atualização da asserção de botões sem a legenda de teclado

## Passos
- [x] Remover marcação HTML de `battery-indicator` em `web/templates/index.html`
- [x] Remover regras CSS obsoletas de `.battery-indicator` e `.battery-led` em `web/static/css/gameboy.css`
- [x] Aumentar o distanciamento vertical e espaçamento entre o D-Pad e as teclas Select e Start em `web/static/css/gameboy.css`
- [x] Remover `screen-bezel-header`, `console-branding` e `keyboard-legend`
- [x] Ajustar dimensões, gap e proporções da tela LCD em `web/static/css/gameboy.css`
- [x] Atualizar asserções de layout em `tests/test_web_layout.py` e `tests/test_web_controller.py`
- [x] Validar testes da suíte

## Desvios
—

## Testes
OK: 84 testes | 0 falhas | 0 erros | 0 ignorados
Cobertura: 54.5% | Relatório: logs/coverage_geral.txt

## Validar
Executar `uv run python run_tests.py` e verificar `tests/test_web_layout.py`.

## Commit
style(web): equalizar dimensoes de desktop com proporcoes mobile e ajustar layout dos controles

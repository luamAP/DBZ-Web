# 20261108 — Ajustes de Layout e Espaçamento dos Controles

Status: concluído

## Objetivo
Remover o indicador de bateria e aumentar o espaçamento entre o D-Pad e as teclas de START e SELECT na carcaça do Game Boy.

## Arquivos
- `web/templates/index.html` — Remoção do container `battery-indicator`
- `web/static/css/gameboy.css` — Remoção dos estilos de bateria e aumento do espaçamento/distância entre D-Pad e teclas Select/Start
- `tests/test_web_layout.py` — Atualização dos testes de layout para refletir a remoção do led de bateria

## Passos
- [x] Remover marcação HTML de `battery-indicator` em `web/templates/index.html`
- [x] Remover regras CSS obsoletas de `.battery-indicator` e `.battery-led` em `web/static/css/gameboy.css`
- [x] Aumentar o distanciamento vertical e espaçamento entre o D-Pad e as teclas Select e Start em `web/static/css/gameboy.css`
- [x] Atualizar asserções de layout em `tests/test_web_layout.py`
- [x] Validar testes da suíte

## Desvios
—

## Testes
OK: 84 testes | 0 falhas | 0 erros | 0 ignorados
Cobertura: 55.4% | Relatório: logs/coverage_geral.txt

## Validar
Executar `uv run python run_tests.py` e verificar `tests/test_web_layout.py`.

## Commit
style(web): remover indicador de bateria e espaçar direcionais das teclas select e start

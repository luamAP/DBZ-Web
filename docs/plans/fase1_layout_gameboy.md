# fase1 — Layout HTML5/CSS3 responsivo estilo Game Boy

Status: concluído

## Objetivo
Implementar a carcaça retrô mobile-first do Game Boy em HTML5 e CSS3, com o visor e display LCD Pixel Art na metade superior e a área física dos controles na metade inferior.

## Arquivos
- `web/templates/index.html` — Estrutura semântica HTML5 com visor, HUD de batalha e controles
- `web/static/css/gameboy.css` — Estilização retrô DMG, paleta LCD esverdeada, botões táteis e responsividade
- `web/app.py` — Rota raiz `GET /` renderizando o template ou servindo JSON sob demanda
- `tests/test_web_layout.py` — Testes de renderização do layout e arquivos estáticos
- `arquitetura.md` — Mapeamento dos novos arquivos
- `ROADMAP.md` — Conclusão do item 2 da Fase 1

## Passos
- [x] Criar template HTML5 `web/templates/index.html` com estrutura de carcaça, visor e botões
- [x] Criar folha de estilo `web/static/css/gameboy.css` mobile-first com paleta Game Boy DMG clássica
- [x] Atualizar rota `GET /` em `web/app.py` para renderizar o template HTML mantendo suporte a `?format=json`
- [x] Criar suíte de testes em `tests/test_web_layout.py`
- [x] Atualizar `arquitetura.md` e `ROADMAP.md`

## Desvios
—

## Testes
OK: 79 testes | 0 falhas | 0 erros | 0 ignorados
Cobertura: 55.2% total | `web/app.py` 84% | Relatório: logs/coverage_fase1.txt

## Validar
Executar `.venv/bin/python run_tests.py fase1` e verificar `tests/test_web_layout.py`.

## Commit
feat(fase1): implementar layout html5 e css3 responsivo estilo game boy

# fase4 — Tela de Título e Seleção de Modos Web

Status: concluído

## Objetivo
Implementar a tela de título e o menu principal estilo Game Boy com as opções de modos de jogo alinhadas ao main.py (1v1 Vegeta, 1v1 Freeza, Tag Team 2v2, Modo Campanha e Carregar Jogo).

## Arquivos
- `web/templates/index.html` — Estrutura HTML da tela de título retrô e do menu principal vertical de seleção de modos
- `web/static/css/gameboy.css` — Estilos visuais do logotipo retrô de DBZ, layout da tela de título e cursores do menu principal
- `web/static/js/menu.js` — Máquina de estados para suportar o estado `title` e `main_menu`, navegação vertical via D-Pad e disparo de ações com Botão A
- `web/static/js/battle.js` — Integração do início de batalha dinâmica (1v1 Vegeta, 1v1 Freeza, 2v2 Tag Team) a partir do menu principal
- `tests/test_web_layout.py` — Testes de renderização da tela de título e opções do menu principal
- `tests/test_web_menu_2x2.py` — Testes de navegação e seleção dos modos de jogo no menu principal
- `arquitetura.md` — Atualização da responsabilidade dos arquivos da camada web

## Passos
- [x] Adicionar no HTML (`web/templates/index.html`) o contêiner da tela de título e lista de opções do menu principal
- [x] Criar regras CSS em `web/static/css/gameboy.css` para a tela de título retrô Pixel Art e menu de modos
- [x] Atualizar `web/static/js/menu.js` com o fluxo inicial de tela de título, navegação por D-Pad e seleção de modos
- [x] Conectar em `web/static/js/battle.js` o acionamento de nova batalha via `/api/battle/new` (1v1 Vegeta, 1v1 Freeza e Tag Team 2v2) e `/api/campaign/start`
- [x] Implementar testes cobrindo a renderização e o fluxo de seleção de modos em `tests/test_web_layout.py` e `tests/test_web_menu_2x2.py`
- [x] Atualizar `arquitetura.md` com a nova estrutura de telas

## Desvios
—

## Testes
OK: 100 testes | 0 falhas | 0 erros | 0 ignorados
Cobertura: 58.5% | Relatório: logs/coverage_fase4.txt

## Validar
Executar `uv run python run_tests.py fase4` e iniciar servidor (`uv run flask --app web.app run --port 5000`) para testar a navegação da tela de título.

## Commit
feat(web): implementar tela de titulo e menu principal retro com selecao de modos

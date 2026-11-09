# fase3 — Integração Visual do Modo Campanha e Save/Load Web

Status: concluído

## Objetivo
Integrar o Modo Campanha na interface gráfica com transição entre fases e tela de drops de recompensas, além de disponibilizar Save/Load de jogo (`save.json`) via menu do console acionado por Start/Select.

## Arquivos
- `web/app.py` — Endpoints REST para gerenciamento de campanha (`/api/campaign/start`, `/api/campaign/next`), resolução de drops, aplicação de recuperação e persistência de save/load com estado da campanha
- `web/templates/index.html` — Modal/overlay retrô de transição de fase, resumo de drops obtidos e menu de sistema do console (Salvar/Carregar/Campanha)
- `web/static/css/gameboy.css` — Estilização do menu do console (estilo pause retrô), overlay de vitória de fase e painel de drops de itens
- `web/static/js/menu.js` — Máquina de estados para abrir o menu de sistema ao pressionar Start/Select, permitindo salvar, carregar ou iniciar modo campanha
- `web/static/js/battle.js` — Captura de eventos de vitória em fase de campanha, exibição da tela de drops e transição sequencial de adversários
- `tests/test_web_api.py` — Testes de integração dos endpoints de campanha e persistência de save/load
- `tests/test_web_menu_2x2.py` — Testes do menu do sistema acionado por Start/Select e feedback na interface
- `arquitetura.md` — Documentação das rotas de campanha e menus de sistema

## Passos
- [x] Adicionar endpoints na API Flask (`web/app.py`) para iniciar campanha (`/api/campaign/start`), avançar fase com drops/recuperação (`/api/campaign/next`) e incluir campanha no payload de `/api/save` e `/api/load`
- [x] Adicionar no HTML (`web/templates/index.html`) a estrutura do menu de sistema (Start/Select) e o modal retrô de vitória de fase e exibição de drops
- [x] Estilizar em `web/static/css/gameboy.css` o menu de sistema do console, overlay de drops e animações de transição de fase estilo Game Boy
- [x] Implementar em `web/static/js/menu.js` a abertura e controle do menu do console com botões Start/Select (Salvar, Carregar, Modo Campanha, Fechar)
- [x] Implementar em `web/static/js/battle.js` a detecção de vitória em fase de campanha, acionamento da tela de drops e carregamento do próximo oponente
- [x] Criar testes cobrindo as rotas de campanha, save/load e integração do menu do sistema em `tests/test_web_api.py` e `tests/test_web_menu_2x2.py`
- [x] Atualizar `arquitetura.md`

## Desvios
—

## Testes
OK: 99 testes | 0 falhas | 0 erros | 0 ignorados
Cobertura: 57.8% | Relatório: logs/coverage_fase3.txt

## Validar
Executar `uv run python run_tests.py fase3` e verificar fluxo completo de campanha, drops e save/load.

## Commit
feat(web): integrar modo campanha com transicao de fases, drops e save load pelo console

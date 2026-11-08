# fase2 — Submenus Interativos de Combate

Status: concluído

## Objetivo
Implementar os submenus interativos de combate (golpes especiais, posturas defensivas, transformações/recarga de Ki, uso de itens e troca de equipe) navegáveis via D-Pad, com confirmação por A e retorno por B ao menu 2x2.

## Arquivos
- `web/templates/index.html` — Estrutura do painel de submenu retrô com paginação/lista de opções dentro da caixa de diálogo
- `web/static/css/gameboy.css` — Estilos pixel art para listas de submenus, indicadores de custo de Ki/quantidade e retorno
- `web/static/js/menu.js` — Máquina de estados para submenus com pilha de navegação (`pushSubmenu`/`popSubmenu`), suporte a navegação D-Pad em listas e retorno via botão B
- `web/static/js/battle.js` — Integração com dados do combatente ativo e orquestração do envio de ações para a API
- `arquitetura.md` — Registro de `tests/test_web_submenus.py`
- `tests/test_web_submenus.py` — Testes de renderização dos submenus, navegação e fluxo de retorno com B

## Passos
- [x] Adicionar container de submenus retrô (`battleSubmenu`) em `web/templates/index.html` com suporte a visualização de golpes, defesas, Ki/transformações e itens/equipe
- [x] Estilizar os submenus em `web/static/css/gameboy.css` com lista pixel art DMG, detalhe de custo de Ki/descrição e cursor `▶`
- [x] Estender `web/static/js/menu.js` implementando sistema de telas/submenus: transição ao confirmar ação no menu 2x2, navegação vertical/horizontal nas opções e retorno ao menu raiz ao pressionar B
- [x] Conectar os submenus aos dados do lutador ativo (técnicas, transformações, inventário e membros da equipe) em `web/static/js/battle.js` e `web/static/js/menu.js`
- [x] Criar suíte de testes em `tests/test_web_submenus.py` validando estrutura, classes, controle por gamepad e integração com os endpoints de batalha
- [x] Atualizar `arquitetura.md` com os novos componentes

## Desvios
—

## Testes
OK: 90 testes | 0 falhas | 0 erros | 0 ignorados | Cobertura: 55.3% (fase2) / 54.5% (geral)

## Validar
uv run python run_tests.py fase2

## Commit
feat(web): implementar submenus interativos de combate navegaveis por d-pad e retorno por botao b

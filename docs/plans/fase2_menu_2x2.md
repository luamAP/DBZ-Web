# fase2 — Menu de Ações 2x2 Retrô

Status: concluído

## Objetivo
Implementar a caixa de diálogo e o menu de ações principal 2x2 estilo Pokémon (LUTAR, DEFENDER, KI / FORMA, ITENS / EQUIPE) navegável via D-Pad e botões A/B.

## Arquivos
- `web/templates/index.html` — Estrutura HTML da caixa de diálogo com texto de prompt e grade 2x2 de comandos com cursor indicador
- `web/static/css/gameboy.css` — Estilos visuais do menu 2x2, cursor retrô estilo Game Boy e responsividade
- `web/static/js/menu.js` — Módulo de navegação do menu 2x2 via eventos do gamepad (D-Pad, A, B) e seleção de ações
- `arquitetura.md` — Registro de `web/static/js/menu.js` e `tests/test_web_menu_2x2.py`
- `tests/test_web_menu_2x2.py` — Testes de estrutura e integração do menu 2x2 e listeners de navegação

## Passos
- [x] Criar a estrutura HTML da caixa de diálogo dividida em área de texto narrativo e grade de ações 2x2 (`LUTAR`, `DEFENDER`, `KI / FORMA`, `ITENS / EQUIPE`) em `web/templates/index.html`
- [x] Implementar os estilos CSS para layout 2x2 com moldura pixel art e cursor direcional `▶` em `web/static/css/gameboy.css`
- [x] Implementar módulo `web/static/js/menu.js` com navegação bidimensional (linhas/colunas 0-1) reagindo aos eventos `gamepad:press` do D-Pad, confirmação (A) e cancelamento (B)
- [x] Integrar o script `menu.js` em `web/templates/index.html` e conectar com o estado da arena
- [x] Criar suíte de testes em `tests/test_web_menu_2x2.py` validando os nós da grade, labels das ações e integração com o controlador
- [x] Atualizar `arquitetura.md` com os novos arquivos

## Desvios
—

## Testes
OK: 87 testes | 0 falhas | 0 erros | 0 ignorados | Cobertura: 55.4% (fase2) / 54.6% (geral)

## Validar
uv run python run_tests.py fase2

## Commit
feat(web): implementar menu de acoes 2x2 estilo pokemon navegavel via gamepad

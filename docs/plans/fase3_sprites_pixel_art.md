# fase3 — Retratos e Sprites em Pixel Art Mapeados via YAML

Status: concluído

## Objetivo
Mapear e renderizar retratos e sprites em Pixel Art 16-bits dos lutadores e de suas transformações via YAML na arena de batalha estilo Game Boy.

## Arquivos
- `data/characters.yml` — Mapeamento das chaves de sprites (front, back, portrait) para Goku, Vegeta, Frieza e suas transformações
- `docs/character_template.md` — Especificação do esquema de sprites nos lutadores e transformações
- `web/static/img/sprites/*.svg` — Assets gráficos em Pixel Art 16-bits vetorizados com estilo retrô para lutadores e formas
- `models/character.py` — Armazenamento do mapeamento de sprites e resolução dos sprites ativos conforme transformação atual
- `web/app.py` — Inclusão dos sprites ativos na serialização do combatente (`serialize_character`)
- `web/templates/index.html` — Estrutura de exibição dos sprites do jogador e oponente na arena
- `web/static/css/gameboy.css` — Estilização e regras de renderização pixelada (`image-rendering: pixelated`) dos sprites
- `web/static/js/battle.js` — Atualização dinâmica dos sprites dos combatentes durante a batalha e transformações
- `tests/test_data_integrity.py` — Validação de integridade dos campos de sprites em `characters.yml` e checagem de existência dos assets
- `tests/test_web_battle_arena.py` — Testes de renderização dos sprites na arena e serialização na API Flask
- `tests/test_character.py` — Testes de unidade para resolução de sprites e troca em transformação
- `arquitetura.md` — Mapeamento dos novos diretórios e arquivos de sprites

## Passos
- [x] Criar assets SVG em Pixel Art retrô para Goku (base e SSJ), Vegeta (base e SSJ) e Frieza (1ª forma e Final) em `web/static/img/sprites/`
- [x] Configurar os caminhos de sprites (front, back, portrait) em `data/characters.yml` para cada combatente e transformação
- [x] Atualizar `docs/character_template.md` com a documentação do novo esquema de sprites
- [x] Suportar campo `sprites` em `models/character.py` e método para obter os sprites da forma ativa
- [x] Expor sprites do combatente ativo na serialização de `web/app.py`
- [x] Atualizar marcação em `web/templates/index.html` e classes em `web/static/css/gameboy.css` para renderizar as imagens com fidelidade pixelada
- [x] Integrar troca e atualização dinâmica dos sprites no módulo `web/static/js/battle.js`
- [x] Implementar testes em `tests/test_data_integrity.py` e `tests/test_web_battle_arena.py` validando esquema, assets e integração web
- [x] Atualizar `arquitetura.md` com os novos arquivos

## Desvios
—

## Testes
OK: 97 testes | 0 falhas | 0 erros | 0 ignorados
Cobertura: 55.4% | Relatório: logs/coverage_fase3.txt

## Validar
Executar `uv run python run_tests.py fase3` e verificar integridade dos assets e rotas de sprites.

## Commit
feat(web): mapear e renderizar retratos e sprites em pixel art via yaml

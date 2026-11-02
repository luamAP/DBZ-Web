---
trigger: model_decision
description: Ao criar, mover ou remover arquivos/diretórios, ou adicionar dependências.
---
# Governança do Repositório

- Raiz: só `main.py`, `run_tests.py`, `README.md`, `arquitetura.md`, `ROADMAP.md`, `requirements.txt` e dotfiles.
- Pastas: `models/` domínio · `engine/` motor, IO, IA · `web/` Flask · `data/` YAMLs · `docs/` esquemas e apoio · `docs/plans/` relatórios de execução · `tests/` testes.
- Pasta nova de primeiro nível: só com aprovação.
- Arquivo/diretório criado, movido ou removido: atualizar `arquitetura.md` na mesma iteração (exceto arquivos em `docs/plans/`).
- Dependência externa nova: adicionar a `requirements.txt` com versão mínima (`>=`).
- `.gitignore` contém `logs/`, `__pycache__/`, `.env` e temporários.

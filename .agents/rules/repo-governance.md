---
trigger: model_decision
description: Ao criar, mover ou remover arquivos/diretórios, ou adicionar dependências.
---
# Governança do Repositório

- Raiz: só `main.py`, `run_tests.py`, `README.md`, `arquitetura.md`, `ROADMAP.md`, `pyproject.toml`, `uv.lock` e dotfiles.
- Pastas: `models/` domínio · `engine/` motor, IO, IA · `web/` Flask · `data/` YAMLs · `docs/` esquemas e apoio · `docs/plans/` relatórios de execução · `tests/` testes.
- Pasta nova de primeiro nível: só com aprovação.
- Arquivo/diretório criado, movido ou removido: atualizar `arquitetura.md` na mesma iteração (exceto arquivos em `docs/plans/`).
- Dependência externa nova: adicionar com `uv add` em `pyproject.toml` (com versão mínima `>=`) e atualizar `uv.lock`.
- `.gitignore` contém `logs/`, `__pycache__/`, `.env` e temporários.

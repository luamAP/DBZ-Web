---
trigger: model_decision
description: Ao criar arquivos/diretórios ou adicionar dependências.
---
# Governança do Repositório

- `logs/`, `__pycache__/`, `.env` e temporários no `.gitignore`.
- Dependência externa nova vai para `requirements.txt`.
- Arquivo ou diretório novo: atualizar `arquitetura.md` na mesma iteração.
- Raiz limpa: só entrypoints (`main.py`, `run_tests.py`), `README.md`, `arquitetura.md`, `ROADMAP.md`, `requirements.txt` e dotfiles. Domínio em `models/`, motor/IO/IA em `engine/`, YAMLs em `data/`, esquemas e documentos de apoio em `docs/`, testes em `tests/`. Pasta nova de primeiro nível só com aprovação.

---
trigger: model_decision
description: Aplicar ao criar arquivos/diretórios, adicionar dependências ou preparar commits.
---
# Governança do Repositório

- Temporários, `logs/`, `__pycache__/` e `.env` ficam no `.gitignore`.
- Nova dependência externa entra no `requirements.txt`.
- Novo arquivo ou diretório: atualizar `arquitetura.md` na mesma iteração.
- Entrega validada por testes é versionada conforme a Etapa 4 do `workflow.md`.

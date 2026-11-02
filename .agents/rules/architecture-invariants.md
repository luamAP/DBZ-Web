---
trigger: always_on
---
# Invariantes de Arquitetura

- **Data-driven:** valores de mecânica (Ki, mitigação, multiplicadores, atributos de itens, taxas) ficam em `data/`, nunca como constantes no Python.
  - `characters.yml` combatentes e defesas · `items.yml` itens · `campaign.yml` campanhas.
  - Esquema novo: arquivo próprio em `data/` + documentação em `docs/`.
- **Domínio puro (`models/`):** sem `print`, `input`, `time.sleep` nem imports de `engine/` ou `flask` (checado por `tests/test_domain_purity.py`). Ações retornam `(bool, dict)` com metadados semânticos, ex.: `(False, {"reason": "already_equipped", "item_id": ...})`.
- **Texto de UI** só na apresentação: `engine/battle_engine.py` (CLI) e `web/` (v2).
- **Assinaturas:** ao alterar uma, atualizar todos os chamadores no mesmo ciclo e listar métodos interdependentes afetados.
- **Testes:** toda funcionalidade nova tem testes em `tests/`.

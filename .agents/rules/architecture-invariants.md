---
trigger: always_on
---
# Invariantes de Arquitetura

- **Data-driven:** nenhuma mecânica (Ki, mitigação, multiplicadores, atributos de itens, taxas) como constante no Python. Combatentes e defesas em `characters.yml`; itens em `items.yml`. Novo esquema exige arquivo próprio e documentação.
- **Domínio puro (`models/`):** sem `print`, `input`, `time.sleep` (checado por `tests/test_domain_purity.py`). Ações retornam `(bool, dict)` com metadados semânticos, ex.: `{"reason": "already_equipped", "item_id": ...}`. Texto de UI só em `battle_engine.py`.
- **Assinaturas:** ao alterar uma, atualizar todos os chamadores no mesmo ciclo e avisar sobre métodos interdependentes afetados.
- **Testes:** toda funcionalidade nova tem testes em `tests/`.

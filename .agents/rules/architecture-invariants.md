---
trigger: always_on
---
# Invariantes de Arquitetura

- **Data-driven:** nenhuma mecânica (custos de Ki, mitigação, multiplicadores,
  atributos de itens, taxas de acerto) pode ser constante fixa no código Python.
- **Domínios de dados:** combatentes e defesas globais em `characters.yml`; itens em
  `items.yml`. Novos esquemas exigem documentação e arquivos dedicados.
- **Domínio puro (`models/`):** sem `print`, `input` nem `time.sleep`. Métodos de
  ação/mutação retornam `(bool, dict)` com metadados semânticos
  (ex.: `{"reason": "already_equipped", "item_id": ...}`). Texto de interface só
  existe em `battle_engine.py`.
- **Consistência:** ao mudar uma assinatura, atualizar todos os chamadores no mesmo
  ciclo (evita `TypeError`/`AttributeError`). Se métodos interdependentes forem
  afetados, avisar o usuário, sem precisar aguardar aprovação.
- **Responsabilidades:** respeitar a divisão descrita em `arquitetura.md`.
- **Testes:** toda funcionalidade nova vem com testes automatizados.
  Destino-alvo: `tests/` (migração prevista para a próxima fase; hoje em
  `test_combat.py`). `python run_tests.py` deve passar antes de avançar.

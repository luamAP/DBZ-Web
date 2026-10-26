---
trigger: model_decision
description: Aplicar ao criar, alterar ou propor regras e skills do projeto.
---
# Como escrever regras neste projeto

- **Uma responsabilidade por arquivo.** Se o título precisar de "e", divida.
- **Curta e imperativa.** Meta: até ~40 linhas, sem justificativa longa.
- **Verificável.** Prefira regras que um teste, linter ou CI consiga checar. Se não
  for verificável, diga como o agente deve confirmar o cumprimento.
- **Sem duplicação.** Cada fato mora em um só arquivo; os demais apontam para ele.
- **Tipo certo.** Regra = restrição/invariante. Skill = procedimento de vários
  passos. Preferência da máquina local = config global, nunca no repositório.
- **Mudanças só por proposta.** O agente nunca edita regras sozinho: propõe via
  `/learn` (artefato `learning_proposal.md`) com diff e justificativa, e aplica
  apenas após aprovação.
- **Poda.** Ao propor uma regra nova, verificar se alguma existente ficou obsoleta
  ou conflitante e propor sua remoção.

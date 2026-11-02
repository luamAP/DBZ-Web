---
trigger: model_decision
description: Ao criar, alterar ou remover regras/skills.
---
# Como escrever regras

- **Uma responsabilidade por arquivo:** se o título pede "e", divida.
- **Curta e imperativa:** até ~40 linhas, sem justificativas.
- **Verificável:** prefira o que teste/linter/CI checa; senão, diga como o agente confirma.
- **Sem duplicação:** cada fato em um só arquivo; os demais apontam para ele.
- **Tipo certo:** regra = restrição; skill = procedimento de vários passos; preferência da máquina local = config global, fora do repo.
- **Gatilho:** `always_on` só para o que vale em toda tarefa; o resto é `model_decision` com `description` específica.
- **Mudança só por proposta:** nunca editar regras sozinho; propor via `/learn` (`learning_proposal.md`) com diff e justificativa; aplicar após aprovação.
- **Poda:** a cada proposta, apontar regras obsoletas ou conflitantes e propor remoção.
---
trigger: always_on
---
# Fluxo de Trabalho

Uma etapa por vez; ao fim de cada uma, pare e aguarde o usuário.

**Relatório:** `docs/plans/fase<N>_<slug>.md` (`<slug>` = 2–3 palavras do item, snake_case; modelo em `docs/plan_template.md`). Editar só as linhas da etapa atual; nunca colar código ou log nele.

0. **Retomar:** se o relatório do item existe, lê-lo e seguir da etapa indicada em `Status`.
1. **Planejar** (editar só o relatório): primeiro item pendente de `ROADMAP.md`; ler em `arquitetura.md` só os módulos envolvidos. Criar o relatório (objetivo, arquivos, passos); `Status: planejado`. Responder só com o caminho e dúvidas bloqueantes.
2. **Implementar** (após aprovação): código, testes e `data/`/`docs/` afetados. No relatório: marcar `[x]` nos passos feitos, registrar desvios (uma linha cada), preencher `Validar`; `Status: implementado`.
3. **Testar:** `python run_tests.py fase<N>`. Reportar só resumo e falhas do console; não abrir `logs/`. Substituir `Testes` no relatório pelo resultado; `Status: testado` se verde. Em falha: propor correção no código de produção; alterar testes só a pedido.
4. **Commit** (testes verdes): gravar mensagem Conventional Commits em `Commit`, marcar `[x]` o item no `ROADMAP.md`; `Status: concluído`.

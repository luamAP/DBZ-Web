---
trigger: always_on
---
# Fluxo de Trabalho

Ao fim de cada etapa, pare e aguarde o usuário.

1. **Planejamento** (sem editar código): pegar o primeiro item pendente de `ROADMAP.md`; abrir de `arquitetura.md` só os módulos envolvidos. Apresentar objetivo, arquivos afetados e plano.
2. **Implementação:** após aprovação. Entregar código, testes, esquema de dados alterado (se houver) e o que validar.
3. **Testes:** executar `python run_tests.py <fase>` e reportar a saída do console (não abrir o log). Em falha, propor correção no código de produção e aguardar; alterar testes só se o usuário pedir.
4. **Commit:** com testes verdes, sugerir mensagem Conventional Commits. Não executar git.

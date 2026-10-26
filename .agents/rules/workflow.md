---
trigger: always_on
---

# Fluxo de Trabalho em Etapas

Cada etapa termina aguardando confirmação do usuário, exceto onde indicado.

1. **Planejamento:** ler `arquitetura.md` e `README.md`, identificar o próximo item não concluído do roadmap e analisar o código existente. NÃO modificar código.
   - Apresentar: objetivo técnico, arquivos afetados (e o que muda em cada um) e plano resumido. Aguardar aprovação.

2. **Implementação:** somente após aprovação.

3. **Testes:** executar `python run_tests.py` e reportar um resumo dos resultados. NÃO corrigir testes automaticamente.
   - **3.1 Correção:** somente após confirmação. Se o usuário fornecer correções, aplicá-las nos testes; caso contrário, revisar o código de produção (Etapa 2).
   - Executar `python run_tests.py` novamente e reportar o resumo.

4. **Versionamento:** somente após confirmação. `git add`, `git commit` (mensagem semântica clara) e `git push origin main`. Se o push falhar, informar o erro e aguardar instruções.

## Formato da resposta de implementação

1. Regras adicionadas e esquema de dados adotado.
2. Código e testes correspondentes.
3. O que precisa ser testado para validar a entrega.
4. Bloco de comandos Git (branch `main`).
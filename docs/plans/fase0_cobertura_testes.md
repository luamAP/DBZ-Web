# fase0 — Cobertura de testes (coverage.py)

Status: concluído

## Objetivo
Integrar medição de cobertura de testes com `coverage.py` ao executor `run_tests.py` e ao pipeline de CI, gerando resumo objetivo no console e relatório detalhado em `logs/coverage_<fase>.txt`.

## Arquivos
- `requirements.txt` — Adicionar `coverage>=7.0.0`
- `run_tests.py` — Integrar instrumentação de cobertura para `models` e `engine`
- `arquitetura.md` — Atualizar descrição do `run_tests.py`
- `ROADMAP.md` — Marcar item de cobertura como concluído

## Passos
- [x] Adicionar `coverage>=7.0.0` ao `requirements.txt` e instalar dependência
- [x] Instrumentar `run_tests.py` para inicializar medição antes do discovery e registrar `logs/coverage_<phase>.txt`
- [x] Exibir percentual resumido no console mantendo o padrão minimalista
- [x] Atualizar mapeamento em `arquitetura.md` e marcar item no `ROADMAP.md`

## Desvios
—

## Testes
OK: 59 testes | 0 falhas | 0 erros | 0 ignorados
Cobertura: 45.4% | Relatório: logs/coverage_fase0.txt
(Camada de domínio `models/` atingiu ~93% de cobertura)

## Validar
Executar `.venv/bin/python run_tests.py fase0` e verificar se os testes passam, o resumo é impresso e `logs/coverage_fase0.txt` é gerado.

## Commit
test(fase0): integrar relatorio de cobertura com coverage.py ao run_tests

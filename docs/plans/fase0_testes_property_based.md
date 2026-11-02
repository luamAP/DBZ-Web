# fase0 — Testes property-based (hypothesis)

Status: concluído

## Objetivo
Implementar testes baseados em propriedades com Hypothesis cobrindo limites de HP/Ki, integridade de inventário, reversibilidade de equipamentos e idempotência de serialização.

## Arquivos
- `requirements.txt` — Adicionar `hypothesis>=6.0.0`
- `tests/test_properties.py` — Implementar testes property-based com Hypothesis
- `arquitetura.md` — Mapear `tests/test_properties.py`

## Passos
- [x] Adicionar `hypothesis>=6.0.0` ao `requirements.txt` e instalar dependência
- [x] Mapear `tests/test_properties.py` em `arquitetura.md`
- [x] Criar `tests/test_properties.py` com propriedades de invariantes de HP e Ki dentro dos limites `[0, max]`
- [x] Criar propriedades garantindo que quantidades de inventário nunca fiquem negativas
- [x] Criar propriedades verificando que equipar e desequipar item restaura atributos e técnicas originais
- [x] Criar propriedades verificando que `to_dict` -> `load_state` -> `to_dict` é idempotente

## Desvios
—

## Testes
OK: 59 testes | 0 falhas | 0 erros | 0 ignorados

## Validar
Executar `python run_tests.py fase0` e verificar se toda a suíte incluindo `tests/test_properties.py` passa sem erros.

## Commit
test(fase0): adicionar testes property-based com hypothesis

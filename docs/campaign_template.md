# 📖 Guia de Criação e Configuração de Campanhas

Este documento descreve a especificação de esquema utilizada em `data/campaign.yml` para a adição de novas campanhas, fases e tabelas de drops à arquitetura *Data-Driven* do jogo.

---

## 📌 Especificação dos Campos

### Nível da Campanha

| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| `id` | String | Identificador único da campanha |
| `name` | String | Título exibido para a campanha |
| `description` | String | Breve contextualização do enredo |
| `stages` | Lista | Lista ordenada de fases sequenciais |

### Nível da Fase (`stages`)

| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| `stage` | Inteiro | Número ordinal da fase |
| `name` | String | Título do confronto |
| `enemy` | String | Chave do oponente cadastrado em `data/characters.yml` |
| `recovery` | Objeto (opcional) | Recuperação concedida ao guerreiro após vitória (`hp_pct`, `ki_bonus`) |
| `drop_table` | Lista (opcional) | Lista de itens passíveis de drop ao concluir a fase |

### Nível do Drop (`drop_table`)

| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| `item_id` | String | Chave do item cadastrado em `data/items.yml` |
| `item_type` | String | Tipo do item (`consumable` ou `equipment`) |
| `chance` | Float (0.0 a 1.0) | Probabilidade de obtenção do item |
| `quantity` | Inteiro (opcional) | Quantidade entregue (padrão: 1) |

---

## 🧬 Modelo Base / Template

```yaml
campaigns:
  nome_da_campanha:
    id: "nome_da_campanha"
    name: "Nome da Campanha"
    description: "Descrição da jornada e desafios."
    stages:
      - stage: 1
        name: "Fase 1: O Primeiro Desafio"
        enemy: "Vegeta"
        recovery:
          hp_pct: 0.20
          ki_bonus: 20
        drop_table:
          - item_id: "senzu_bean"
            item_type: "consumable"
            chance: 0.50
            quantity: 1
```

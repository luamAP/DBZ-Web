# 📖 Guia de Criação e Configuração de Personagens

Este documento descreve a especificação de esquema utilizada em `data/characters.yml` para a adição de novos combatentes à arquitetura *Data-Driven* do jogo.

---

## 📌 Especificação dos Campos

### Configurações Globais de Combate (`combat_mechanics`)

| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| `charge_ki.min` / `max` | Inteiro | Faixa mínima e máxima de Ki recuperado ao concentrar energia |
| `damage_variance.basic.min` / `max` | Inteiro | Variação somada ao dano base no golpe básico |
| `damage_variance.combo.min` / `max` | Inteiro | Variação somada ao dano base de cada golpe do combo |
| `damage_variance.special.min` / `max` | Inteiro | Variação somada ao dano base no golpe especial |

### Combatentes

| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| `name` | String | Nome visível do guerreiro em combate |
| `ai_profile` | String (opcional) | Perfil comportamental da IA (`agressivo`, `defensivo`, `tatico`). Padrão: `tatico` |
| `hp` | Inteiro | Pontos de vida máximos iniciais |
| `attack` | Inteiro | Poder ofensivo base para cálculo de dano físico e técnicas |
| `defense` | Inteiro | Capacidade de absorção e mitigação de dano |
| `ki_max` | Inteiro | Capacidade máxima de armazenamento de Ki |
| `speed` | Inteiro | Determina a ordem de iniciativa de turnos |
| `transformations` | Lista | Formas evolutivas disponíveis com seus respectivos requisitos e bônus |
| `moves` | Lista | Conjunto de técnicas (golpe básico, combos de múltiplos acertos e 3 especiais) |

---

## 📐 Regras de Padronização para `moves`

Todo combatente deve conter a seguinte estrutura balanceada:

1. **1 Golpe Básico (`type: basic`):** Custo 0 de Ki, dano constante (`multiplier: 1.0`).
2. **Combos (`type: combo`):** Custo baixo/moderado de Ki, múltiplos golpes (`hits`), taxa de acerto por golpe (`hit_chance`) e dano proporcional (`multiplier`).
3. **Exatamente 3 Golpes Especiais (`type: special`):**
   * *Nível 1 (Menor custo):* Dano moderado (ex: Kaio-ken, Galick Gun, Death Beam).
   * *Nível 2 (Intermediário):* Dano elevado (ex: Kamehameha, Big Bang Attack).
   * *Nível 3 (Supremo):* Alto custo de Ki e multiplicador destrutivo (ex: Spirit Bomb, Final Flash, Death Ball).

---

## 🧬 Modelo Base / Template

Copie o bloco abaixo e cole em `data/characters.yml` preenchendo os valores:

```yaml
NomeDoLutador:
  name: "Nome do Lutador"
  ai_profile: "tatico"
  hp: 100
  attack: 20
  defense: 30
  ki_max: 100
  speed: 80
  transformations:
    - name: "Nome da Transformação"
      required_ki: 50
      hp_threshold_pct: 1.0
      stat_multipliers:
        attack: 1.25
        defense: 1.15
        speed: 1.20
  moves:
    - name: "Ataque Básico"
      ki_cost: 0
      multiplier: 1.0
      type: basic
    - name: "Investida Rápida"
      ki_cost: 10
      multiplier: 0.50
      hits: 3
      hit_chance: 0.85
      type: combo
    - name: "Técnica Especial Menor"
      ki_cost: 25
      multiplier: 1.40
      type: special
    - name: "Técnica Especial Média"
      ki_cost: 45
      multiplier: 1.75
      type: special
    - name: "Técnica Suprema"
      ki_cost: 75
      multiplier: 2.40
      type: special
```

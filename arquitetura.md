# 🏛️ Arquitetura do Sistema - Dragon Ball Z Text Battle

Este documento descreve a topologia estrutural, papéis de componentes, contratos de dados e dependências do projeto para permitir carregamento contextual sob demanda[span_0](start_span)[span_0](end_span).

---

## 📂 Visão Geral da Estrutura de Diretórios

```text
├── characters.yml           # Base de dados de lutadores e mecânicas defensivas
├── items.yml                # Base de dados de equipamentos e consumíveis
├── character_template.md    # Especificação do esquema de lutadores
├── arquitetura.md           # Mapeamento arquitetural de componentes (este arquivo)
├── diretrizes.md            # Regras operacionais e fluxo de trabalho
├── README.md                # Visão geral, roadmap e instruções de execução
├── data_loader.py           # Centralizador de I/O para leitura de arquivos YAML e inventários
├── main.py                  # Ponto de entrada CLI e menus principais
├── battle_engine.py         # Motor de combate e loop de turnos (Camada de Apresentação)
├── ai_controller.py         # Tomada de decisão da IA de combate parametrizada via dados
├── test_combat.py           # Suíte de testes unitários automatizados
├── run_tests.py             # Script utilitário para execução e logs de testes
└── models/                  # Pacote de domínio e modelos de entidades
    ├── __init__.py          # Fachada e exportação pública (Character, Team)
    ├── character.py         # Modelo de entidade do combatente individual
    └── team.py              # Modelo de entidade para equipes (Tag Team)

```
## 🧩 Papéis e Responsabilidades dos Módulos
### 1. Camada de Dados (Data-Driven Configuration)
 * **characters.yml**: Define atributos base de combatentes, conjuntos de técnicas (basic, combo, special), transformações e parâmetros globais do sistema de defesa (block, counter, dodge, vanish).
 * **items.yml**: Catálogo de itens equipáveis (equipment), bônus/multiplicadores de status, técnicas concedidas e catálogo de itens consumíveis (consumables).
### 2. Camada de Acesso a Dados e Utilidades
 * **data_loader.py**:
   * Centraliza o acesso I/O do sistema de arquivos para carregar configurações YAML com caminhos determinísticos.
   * Fornece geradores utilitários de estado inicial (ex.: create_initial_inventory).
   * Elimina duplicações de I/O em pontos de entrada da aplicação e suítes de teste.
### 3. Camada de Domínio (models/)
 * **models/character.py**:
   * Entidade central do combatente.
   * Gerencia cálculo e recálculo dinâmico de atributos (_recalculate_stats), aplicação de multiplicadores em cascata de itens e transformações.
   * Executa mutações de status causadas por consumo de itens e golpes recebidos.
 * **models/team.py**:
   * Entidade agregadora para mecânicas de Tag Team.
   * Gerencia integridade do time, seleção do guerreiro ativo, reservas vivos (get_bench_members), trocas voluntárias e substituições automáticas por nocaute.
 * **models/__init__.py**:
   * Fachada (*Facade*) que expõe explicitamente as classes Character e Team, blindando o restante do sistema contra caminhos internos de importação.
### 4. Camada de Apresentação e Orquestração
 * **battle_engine.py**:
   * Orquestra o ciclo de batalha por turnos (battle_team e battle).
   * Renderiza interfaces de texto, submenus de ação (técnicas, defesa, uso de itens, transformações e troca de lutadores).
   * Controla o fluxo de temporização visual e exibição de status dos combatentes.
 * **ai_controller.py**:
   * Algoritmo de decisão heurística para lutadores controlados pelo computador.
   * Avalia níveis de Ki, pontos de vida e estado defensivo para escolher a melhor ação sem código embutido de regras (*unhardcoded*).
 * **main.py**:
   * Ponto de entrada (CLI) da aplicação.
   * Apresenta o menu principal, orquestra a inicialização das bases de dados via data_loader e despacha para os modos de jogo (1v1, Tag Team, customização).
### 5. Garantia da Qualidade
 * **test_combat.py**: Suíte de testes automatizados unitários cobrindo regras de negócio, cálculos matemáticos, mecânicas de defesa, uso de itens, transformações e fluxo de Tag Team.
 * **run_tests.py**: Utilitário de automação para executar a suíte de testes e direcionar os relatórios para o diretório logs/.
## 🔄 Fluxo de Dependências
```text
[characters.yml / items.yml]
            │
            ▼
    [data_loader.py]
      │           │
      ▼           ▼
  [main.py]   [test_combat.py]
      │               │
      ├───────┬───────┤
      ▼       ▼       ▼
[battle_engine.py]  [models/] (character.py, team.py)
      │
      ▼
[ai_controller.py]

```

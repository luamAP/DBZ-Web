# 🐉 Dragon Ball Z Text Battle (Python CLI)

Um simulador de combate por turnos no universo de Dragon Ball Z, concebido sob os princípios de **Clean Code**, **SOLID** e arquitetura estritamente **Orientada a Dados (Data-Driven)**.

---

## 🏗️ Arquitetura do Projeto

O ecossistema é projetado sob os princípios de **Clean Code**, **SOLID** e uma arquitetura estritamente **Orientada a Dados (Data-Driven)**, desacoplando regras matemáticas e catálogo de entidades do código de execução da aplicação.

Para a documentação completa dos componentes, contratos de dados, fluxo de dependências e responsabilidades de cada módulo:
👉 **[Documentação Arquitetural Completa (`arquitetura.md`)](arquitetura.md)**

---

## 🚀 Roadmap e Fases de Desenvolvimento

### ✅ Fase 1: Fundação Principal (CONCLUÍDO)

* [x] Ciclo básico de combate em turnos (Atacar, Defender, Carregar Ki).
* [x] Arquitetura orientada a objetos (Classe genérica `Character`).
* [x] Ordem de turnos baseada na velocidade relativa (`speed`).
* [x] Gestão de Ki (relação risco/recompensa para ataques especiais).
* [x] Tomada de decisão básica da IA.
* [x] Separação de dados via `characters.yml`.

### ✅ Fase 2: Mecânicas Profundas de Combate (CONCLUÍDO)

* [x] **Conjuntos de Técnicas Padronizados:** Técnicas básicas, combos com múltiplos golpes e 3 ataques especiais por guerreiro.
* [x] **Opções Avançadas de Defesa:** Submenu interativo com Bloqueio, Contra-Ataque com dano refletido, Esquiva probabilística e Teleporte Instantâneo.
* [x] **Transformações (Super Saiyajin / Formas):** Condições de ativação por Ki/HP e modificadores multiplicativos de atributos.

### ✅ Fase 3: Equipamentos e Customização (CONCLUÍDO)

* [x] **Itens Equipáveis (Cápsulas e Brincos):** Pré-seleção de itens que alteram atributos ou concedem técnicas únicas.
* [x] **Inventário de Consumíveis:** Uso de Sementes dos Deuses (*Senzu Beans*) e Cápsulas de Ki durante os turnos de combate.
* [x] **Desacoplamento de Esquemas:** Criação de `items.yml` isolando o catálogo de inventário da ficha de lutadores.

### 🔄 Fase 4: Batalhas em Equipe e Reestruturação Arquitetural (EM PROGRESSO)

* [x] **Montagem de Equipes (Tag Team):** Seleção de equipes com múltiplos lutadores e mecânica de rotação durante a batalha ou por derrota.
* [x] **Modularização de Domínio:** Subdivisão de `models.py` no pacote `models/` com os módulos especializados `character.py` e `team.py`.
* [x] **Centralização de Carregamento de Dados (`data_loader.py`):** Eliminação de código duplicado de I/O de arquivos YAML e inventários entre a aplicação e os testes.
* [x] **Purificação do Domínio (Clean Architecture):** Remoção de mensagens de apresentação e desacoplamento total das entidades, retornando dados estruturados de eventos para exibição na camada de apresentação (`battle_engine.py`).
* [x] **Modularização da Suíte de Testes (`tests/`):** Desmembramento dos testes automatizados em suítes focadas (`tests/test_character.py`, `tests/test_team.py`, `tests/test_combat_flow.py`), incluindo um teste de pureza do domínio (via AST) que garanta a ausência de `print`, `input` e `time.sleep` em `models/`.
* [ ] **IA Baseada em Personalidade:** Perfis comportamentais no YAML (`agressivo`, `defensivo`, `tático`) para respostas dinâmicas no combate.

### 🌟 Fase 5: Polimento e Expansão

* [ ] **Modo Campanha / História:** Batalhas sequenciais e atribuição de recompensas/drops após as vitórias.
* [ ] **Save State:** Persistência do inventário e progresso em um arquivo `save.json`.
* [ ] **Interface Visual:** Retratos ASCII e feedback visual das técnicas de Ki.

---

## 🛠️ Extensão de Personagens

O ecossistema é totalmente orientado a dados, permitindo a inclusão de lutadores sem alteração no código Python.

Para consultar a especificação completa dos campos, regras de balanceamento de técnicas e copiar o template YAML pronto para uso, consulte:
👉 **[Guia de Criação de Personagens (`character_template.md`)](character_template.md)**

---

## 🧪 Execução e Testes Automatizados

### Executar o Jogo

```bash
python main.py
```

### Executar a Suíte de Testes com `run_tests.py`

Para rodar os testes e gerar os logs de forma automática:

```bash
python run_tests.py
```

* O script garante a existência da pasta `logs/` e salva o relatório detalhado em `logs/log.txt`.

### Executar via Terminal Manualmente

```bash
python -m unittest discover tests
```

Para redirecionar manualmente para o arquivo de log:

* **Linux / macOS / Git Bash:**

  ```bash
  mkdir -p logs
  python -m unittest discover tests > logs/log.txt 2>&1
  ```

* **Windows (PowerShell):**

  ```powershell
  if (!(Test-Path "logs")) { New-Item -ItemType Directory -Name "logs" }
  python -m unittest discover tests *>&1 | Out-File -FilePath logs/log.txt
  ```

### Executar via Interface Gráfica da IDE

1. **VS Code:** Abra o painel de **Testing** (ícone de tubo de ensaio), configure para `unittest` na pasta de testes e execute pelo painel.
2. **PyCharm:** Clique com o botão direito sobre o diretório de testes ou `run_tests.py` e escolha **Run**.

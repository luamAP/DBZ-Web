# 🐉 Dragon Ball Z Text Battle (Python CLI)

Um simulador de combate por turnos no universo de Dragon Ball Z, concebido sob os princípios de **Clean Code**, **SOLID** e arquitetura estritamente **Orientada a Dados (Data-Driven)**.

---

## 🏗️ Arquitetura do Projeto

* `characters.yml`: Catálogo descritivo de combatentes, atributos-base, mecânicas defensivas e técnicas de combate.
* `items.yml`: Repositório desacoplado de equipamentos passivos, brincos Potara e itens consumíveis de suporte.
* `models.py`: Modelos de domínio (`Character`), gestão de estado e cálculos determinísticos de atributos e dano.
* `battle_engine.py`: Motor de combate, gestão do ciclo de turnos e submenus CLI.
* `ai_controller.py`: Módulo de tomada de decisão não-jogável parametrizada.
* `main.py`: Ponto de entrada da aplicação e orquestração do loop principal.
* `test_combat.py`: Suíte de validação e garantia de qualidade com testes unitários automatizados.
* `run_tests.py`: Script utilitário para automação da suíte de testes com geração estruturada de logs.
* `character_template.md`: Guia de especificação de esquema e modelo para criação de novos combatentes.

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

### 🤝 Fase 4: Batalhas em Equipe e IA (PRÓXIMA ETAPA)
* [ ] **Montagem de Equipes (Tag Team):** Seleção de equipes com múltiplos lutadores e mecânica de troca durante a batalha ou por derrota.
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
python -m unittest test_combat.py
```

Para redirecionar manualmente para o arquivo de log:
* **Linux / macOS / Git Bash:**
  ```bash
  mkdir -p logs
  python -m unittest test_combat.py > logs/log.txt 2>&1
  ```
* **Windows (PowerShell):**
  ```powershell
  if (!(Test-Path "logs")) { New-Item -ItemType Directory -Name "logs" }
  python -m unittest test_combat.py *>&1 | Out-File -FilePath logs/log.txt
  ```

### Executar via Interface Gráfica da IDE
1. **VS Code:** Abra o painel de **Testing** (ícone de tubo de ensaio), configure para `unittest` na raiz `.` e execute pelo painel.
2. **PyCharm:** Clique com o botão direito sobre `test_combat.py` ou `run_tests.py` e escolha **Run**.

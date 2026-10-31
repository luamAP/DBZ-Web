# 📜 Roadmap Histórico — Versão 1.0 (Python CLI)

Registro completo das fases de desenvolvimento concluídas na **Versão 1.0 (CLI Text Battle)** do projeto.

---

## ✅ Fase 1: Fundação Principal (CONCLUÍDO)

* [x] Ciclo básico de combate em turnos (Atacar, Defender, Carregar Ki).
* [x] Arquitetura orientada a objetos (Classe genérica `Character`).
* [x] Ordem de turnos baseada na velocidade relativa (`speed`).
* [x] Gestão de Ki (relação risco/recompensa para ataques especiais).
* [x] Tomada de decisão básica da IA.
* [x] Separação de dados via `characters.yml`.

## ✅ Fase 2: Mecânicas Profundas de Combate (CONCLUÍDO)

* [x] **Conjuntos de Técnicas Padronizados:** Técnicas básicas, combos com múltiplos golpes e 3 ataques especiais por guerreiro.
* [x] **Opções Avançadas de Defesa:** Submenu interativo com Bloqueio, Contra-Ataque com dano refletido, Esquiva probabilística e Teleporte Instantâneo.
* [x] **Transformações (Super Saiyajin / Formas):** Condições de ativação por Ki/HP e modificadores multiplicativos de atributos.

## ✅ Fase 3: Equipamentos e Customização (CONCLUÍDO)

* [x] **Itens Equipáveis (Cápsulas e Brincos):** Pré-seleção de itens que alteram atributos ou concedem técnicas únicas.
* [x] **Inventário de Consumíveis:** Uso de Sementes dos Deuses (*Senzu Beans*) e Cápsulas de Ki durante os turnos de combate.
* [x] **Desacoplamento de Esquemas:** Criação de `items.yml` isolando o catálogo de inventário da ficha de lutadores.

## ✅ Fase 4: Batalhas em Equipe e Reestruturação Arquitetural (CONCLUÍDO)

* [x] **Montagem de Equipes (Tag Team):** Seleção de equipes com múltiplos lutadores e mecânica de rotação durante a batalha ou por derrota.
* [x] **Modularização de Domínio:** Subdivisão de `models.py` no pacote `models/` com os módulos especializados `character.py` e `team.py`.
* [x] **Centralização de Carregamento de Dados (`data_loader.py`):** Eliminação de código duplicado de I/O de arquivos YAML e inventários entre a aplicação e os testes.
* [x] **Purificação do Domínio (Clean Architecture):** Remoção de mensagens de apresentação e desacoplamento total das entidades, retornando dados estruturados de eventos para exibição na camada de apresentação (`battle_engine.py`).
* [x] **Modularização da Suíte de Testes (`tests/`):** Desmembramento dos testes automatizados em suítes focadas (`tests/test_character.py`, `tests/test_team.py`, `tests/test_combat_flow.py`), incluindo um teste de pureza do domínio (via AST) que garanta a ausência de `print`, `input` e `time.sleep` em `models/`.
* [x] **IA Baseada em Personalidade:** Perfis comportamentais no YAML (`agressivo`, `defensivo`, `tático`) para respostas dinâmicas no combate.

## ✅ Fase 5: Modo Campanha e Persistência (CONCLUÍDO)

* [x] **Modo Campanha / História:** Batalhas sequenciais e atribuição de recompensas/drops após as vitórias (`campaign.yml`).
* [x] **Save State:** Persistência do inventário, equipamentos e progresso em `save.json`.

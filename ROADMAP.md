# 🎮 Roadmap — Versão 2.0 (Web Game Boy / Pokémon Style)

Evolução do projeto para uma interface gráfica **Web Mobile-First** inspirada no **Game Boy / Pokémon**, mantendo o domínio puro em Python (`models/` e YAMLs) no backend via **Flask**.

---

## Fase 1: Servidor Flask e Carcaça Game Boy Mobile-First

- [ ] API Flask (`app.py`) integrada ao domínio puro (`models/`, `data_loader.py` e `ai_controller.py`).
- [ ] Layout HTML5/CSS3 responsivo estilo portátil (visor Pixel Art na metade superior e controles na metade inferior).
- [ ] Controle virtual touch/teclado com **D-Pad (▲ ▼ ◄ ►)**, botões **A** (Confirmar) e **B** (Voltar), além de **Start/Select**.

## Fase 2: Interface de Combate Estilo Pokémon (Menu 2x2)

- [ ] Arena de batalha com posicionamento clássico (inimigo no topo direito, jogador na base esquerda) e barras animadas de HP e Ki.
- [ ] Caixa de diálogo retrô e grade de ações **2x2** (`LUTAR`, `DEFENDER`, `KI / FORMA`, `ITENS / EQUIPE`) navegável via D-Pad + A/B.
- [ ] Submenus interativos para golpes especiais, posturas defensivas, transformações, uso de cápsulas e troca de equipe (Tag Team).

## Fase 3: Pixel Art, Animações de Ki, Campanha e Save Web

- [ ] Retratos/sprites em **Pixel Art 16-bits** dos guerreiros e das transformações (Super Saiyajin, Formas de Frieza) mapeados via YAML.
- [ ] Feedback visual de combate (efeitos de aura ao carregar Ki, piscar ao receber dano e animações de ataques especiais).
- [ ] Integração visual do **Modo Campanha** (transição de fases, tela de drops) e **Save/Load** (`save.json`) pelo menu do console.

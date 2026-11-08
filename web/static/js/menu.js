/**
 * Dragon Ball Z - Game Boy Edition
 * Módulo de Navegação e Menus Retrô Estilo Pokémon (BattleMenu)
 */

(function () {
    'use strict';

    // Mapeamento da grade de ações 2x2
    const MENU_ACTIONS = [
        ['fight', 'defend'],
        ['ki_form', 'items_team'],
    ];

    const ACTION_LABELS = {
        fight: 'LUTAR',
        defend: 'DEFENDER',
        ki_form: 'KI / FORMA',
        items_team: 'ITENS / EQUIPE',
    };

    class BattleMenu {
        constructor() {
            this.row = 0;
            this.col = 0;
            this.enabled = true;
            this.visible = true;
            this.gridElement = null;
            this.dialogueTextEl = null;
            this.buttons = [];
            this.init();
        }

        init() {
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', () => this.setup());
            } else {
                this.setup();
            }
        }

        setup() {
            this.gridElement = document.getElementById('battleMenuGrid');
            this.dialogueTextEl = document.getElementById('dialogueText');
            this.cacheButtons();
            this.bindGamepadEvents();
            this.updateSelectionVisuals();
        }

        cacheButtons() {
            if (!this.gridElement) return;
            this.buttons = Array.from(this.gridElement.querySelectorAll('.menu-action-btn'));

            // Permite seleção e ativação por toque/clique direto
            this.buttons.forEach((btn) => {
                btn.addEventListener('click', (e) => {
                    e.preventDefault();
                    if (!this.enabled) return;
                    const r = parseInt(btn.getAttribute('data-row'), 10);
                    const c = parseInt(btn.getAttribute('data-col'), 10);
                    if (!isNaN(r) && !isNaN(c)) {
                        this.setSelection(r, c);
                        this.selectCurrent();
                    }
                });
            });
        }

        bindGamepadEvents() {
            document.addEventListener('gb-input', (e) => {
                if (!this.enabled || !this.visible) return;
                const { button, state } = e.detail || {};
                if (state !== 'pressed') return;

                switch (button) {
                    case 'UP':
                    case 'DOWN':
                    case 'LEFT':
                    case 'RIGHT':
                        this.navigate(button);
                        break;
                    case 'A':
                        this.selectCurrent();
                        break;
                    case 'B':
                        this.cancel();
                        break;
                    default:
                        break;
                }
            });
        }

        /**
         * Move a seleção na grade 2x2 com base na direção do D-Pad
         */
        navigate(direction) {
            let changed = false;
            if (direction === 'UP' && this.row > 0) {
                this.row--;
                changed = true;
            } else if (direction === 'DOWN' && this.row < 1) {
                this.row++;
                changed = true;
            } else if (direction === 'LEFT' && this.col > 0) {
                this.col--;
                changed = true;
            } else if (direction === 'RIGHT' && this.col < 1) {
                this.col++;
                changed = true;
            }

            if (changed) {
                this.updateSelectionVisuals();
                this.emitEvent('battle:menu-move', {
                    row: this.row,
                    col: this.col,
                    action: this.getSelectedAction(),
                });
            }
        }

        /**
         * Define manualmente a célula selecionada
         */
        setSelection(row, col) {
            if (row >= 0 && row <= 1 && col >= 0 && col <= 1) {
                this.row = row;
                this.col = col;
                this.updateSelectionVisuals();
            }
        }

        /**
         * Retorna a chave da ação selecionada
         */
        getSelectedAction() {
            return MENU_ACTIONS[this.row][this.col];
        }

        /**
         * Retorna o label amigável da ação atual
         */
        getSelectedLabel() {
            const action = this.getSelectedAction();
            return ACTION_LABELS[action] || action;
        }

        /**
         * Atualiza as classes CSS e os cursores indicadores (▶)
         */
        updateSelectionVisuals() {
            if (!this.buttons || this.buttons.length === 0) return;

            this.buttons.forEach((btn) => {
                const r = parseInt(btn.getAttribute('data-row'), 10);
                const c = parseInt(btn.getAttribute('data-col'), 10);
                const isSelected = r === this.row && c === this.col;
                btn.classList.toggle('selected', isSelected);

                const cursor = btn.querySelector('.menu-cursor');
                if (cursor) {
                    cursor.textContent = isSelected ? '▶' : ' ';
                    cursor.style.visibility = isSelected ? 'visible' : 'hidden';
                }
            });
        }

        /**
         * Confirma a ação selecionada (Botão A)
         */
        selectCurrent() {
            const action = this.getSelectedAction();
            const label = this.getSelectedLabel();

            const eventData = {
                action: action,
                label: label,
                row: this.row,
                col: this.col,
            };

            this.emitEvent('battle:action-select', eventData);
            return eventData;
        }

        /**
         * Cancela / Retorna ao nível anterior (Botão B)
         */
        cancel() {
            this.emitEvent('battle:menu-cancel', {
                row: this.row,
                col: this.col,
                action: this.getSelectedAction(),
            });
        }

        /**
         * Atualiza o texto na área narrativa da caixa de diálogo
         */
        setMessage(text) {
            if (this.dialogueTextEl) {
                this.dialogueTextEl.textContent = text;
            }
        }

        /**
         * Oculta a grade do menu (útil durante mensagens de turno ou animação de dano)
         */
        hide() {
            this.visible = false;
            if (this.gridElement) {
                this.gridElement.classList.add('hidden');
            }
        }

        /**
         * Exibe a grade do menu quando o jogador precisa agir
         */
        show() {
            this.visible = true;
            if (this.gridElement) {
                this.gridElement.classList.remove('hidden');
            }
            this.updateSelectionVisuals();
        }

        /**
         * Habilita ou desabilita a aceitação de inputs pelo menu
         */
        setEnabled(enabled) {
            this.enabled = !!enabled;
            if (this.gridElement) {
                this.gridElement.classList.toggle('disabled', !this.enabled);
            }
        }

        emitEvent(name, detail) {
            const event = new CustomEvent(name, {
                detail: detail,
                bubbles: true,
            });
            document.dispatchEvent(event);
        }
    }

    // Instanciação e exportação
    window.BattleMenu = BattleMenu;
    window.MENU_ACTIONS = MENU_ACTIONS;
    window.ACTION_LABELS = ACTION_LABELS;
    window.battleMenu = new BattleMenu();
})();

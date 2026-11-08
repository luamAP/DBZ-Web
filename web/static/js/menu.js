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
            this.currentScreen = 'root'; // 'root' (grade 2x2) ou 'submenu'
            this.activeCategory = null;
            this.submenuIndex = 0;
            this.submenuItems = [];

            this.gridElement = null;
            this.submenuElement = null;
            this.submenuTitleEl = null;
            this.submenuListEl = null;
            this.submenuBackBtn = null;
            this.dialogueTextEl = null;
            this.buttons = [];

            this.combatantData = {
                player: null,
                team: null,
                inventory: null,
            };

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
            this.submenuElement = document.getElementById('battleSubmenu');
            this.submenuTitleEl = document.getElementById('submenuTitle');
            this.submenuListEl = document.getElementById('submenuList');
            this.submenuBackBtn = document.getElementById('submenuBackBtn');
            this.dialogueTextEl = document.getElementById('dialogueText');

            this.cacheButtons();
            this.bindSubmenuEvents();
            this.bindGamepadEvents();
            this.updateSelectionVisuals();
        }

        cacheButtons() {
            if (!this.gridElement) return;
            this.buttons = Array.from(this.gridElement.querySelectorAll('.menu-action-btn'));

            // Permite seleção e ativação por toque/clique direto na grade 2x2
            this.buttons.forEach((btn) => {
                btn.addEventListener('click', (e) => {
                    e.preventDefault();
                    if (!this.enabled || this.currentScreen !== 'root') return;
                    const r = parseInt(btn.getAttribute('data-row'), 10);
                    const c = parseInt(btn.getAttribute('data-col'), 10);
                    if (!isNaN(r) && !isNaN(c)) {
                        this.setSelection(r, c);
                        this.selectCurrent();
                    }
                });
            });
        }

        bindSubmenuEvents() {
            if (this.submenuBackBtn) {
                this.submenuBackBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    this.closeSubmenu();
                });
            }
        }

        bindGamepadEvents() {
            document.addEventListener('gb-input', (e) => {
                if (!this.enabled || !this.visible) return;
                const { button, state } = e.detail || {};
                if (state !== 'pressed') return;

                if (this.currentScreen === 'root') {
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
                } else if (this.currentScreen === 'submenu') {
                    switch (button) {
                        case 'UP':
                        case 'DOWN':
                            this.navigateSubmenu(button);
                            break;
                        case 'A':
                            this.selectSubmenuItem();
                            break;
                        case 'B':
                            this.closeSubmenu();
                            break;
                        default:
                            break;
                    }
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
         * Define manualmente a célula selecionada na grade 2x2
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
         * Atualiza as classes CSS e os cursores indicadores (▶) na grade 2x2
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
         * Confirma a ação selecionada na grade (Botão A) abrindo o submenu correspondente
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
            this.openSubmenu(action);
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

        /* ==========================================================================
           Lógica de Submenus (Golpes, Defesas, Ki/Forma, Itens/Equipe)
           ========================================================================== */

        /**
         * Retorna os itens de um submenu específico baseado no estado do combate
         */
        getSubmenuItems(category) {
            const p = this.combatantData.player;
            const t = this.combatantData.team;
            const items = [];

            switch (category) {
                case 'fight':
                    if (p && Array.isArray(p.moves) && p.moves.length > 0) {
                        p.moves.forEach((m) => {
                            const name = typeof m === 'string' ? m : (m.name || m.id || 'Ataque');
                            const cost = m.ki_cost !== undefined ? m.ki_cost : (m.cost || 0);
                            items.push({
                                id: name.toLowerCase().replace(/\s+/g, '_'),
                                label: name.toUpperCase(),
                                info: `${cost} KI`,
                                type: 'move',
                                raw: m,
                            });
                        });
                    } else {
                        items.push(
                            { id: 'punch', label: 'SOCO / GOLPE', info: '0 KI', type: 'move' },
                            { id: 'kamehameha', label: 'KAMEHAMEHA', info: '20 KI', type: 'move' },
                            { id: 'kaioken_rush', label: 'COMBO METEORO', info: '15 KI', type: 'move' },
                            { id: 'ki_blast', label: 'ESFERAS DE KI', info: '10 KI', type: 'move' }
                        );
                    }
                    break;

                case 'defend':
                    items.push(
                        { id: 'block', label: 'BLOQUEIO FIRME', info: 'MITIGA DANO', type: 'defense' },
                        { id: 'dodge', label: 'ESQUIVA RÁPIDA', info: 'CHANCE DESVIO', type: 'defense' },
                        { id: 'counter', label: 'CONTRA-ATAQUE', info: 'DEVOLVE DANO', type: 'defense' }
                    );
                    break;

                case 'ki_form':
                    items.push(
                        { id: 'charge_ki', label: 'CONCENTRAR KI', info: '+25 KI', type: 'ki' }
                    );
                    if (p && Array.isArray(p.transformations) && p.transformations.length > 0) {
                        p.transformations.forEach((tr) => {
                            const name = typeof tr === 'string' ? tr : (tr.name || tr.id || 'Forma');
                            const cost = tr.ki_cost !== undefined ? tr.ki_cost : (tr.cost || 30);
                            items.push({
                                id: name.toLowerCase().replace(/\s+/g, '_'),
                                label: name.toUpperCase(),
                                info: `${cost} KI`,
                                type: 'transformation',
                                raw: tr,
                            });
                        });
                    } else {
                        items.push(
                            { id: 'kaioken', label: 'KAIOKEN', info: '15 KI', type: 'transformation' },
                            { id: 'super_saiyajin', label: 'SUPER SAIYAJIN', info: '50 KI', type: 'transformation' }
                        );
                    }
                    break;

                case 'items_team':
                    // Itens do inventário
                    const inv = this.combatantData.inventory || (p && p.inventory);
                    if (inv && Object.keys(inv).length > 0) {
                        for (const [itemId, qty] of Object.entries(inv)) {
                            if (qty > 0) {
                                items.push({
                                    id: itemId,
                                    label: itemId.replace(/_/g, ' ').toUpperCase(),
                                    info: `QTD: ${qty}`,
                                    type: 'item',
                                });
                            }
                        }
                    }
                    if (items.length === 0) {
                        items.push(
                            { id: 'senzu_bean', label: 'SEMENTE DOS DEUSES', info: '100% HP', type: 'item' },
                            { id: 'capsule_ki', label: 'CÁPSULA DE KI', info: '+50 KI', type: 'item' }
                        );
                    }

                    // Troca de Combatente (Tag Team)
                    if (t && Array.isArray(t.members) && t.members.length > 1) {
                        t.members.forEach((m) => {
                            if (m.index !== t.active_index && m.is_alive) {
                                items.push({
                                    id: `switch_${m.index}`,
                                    label: `TROCAR: ${m.name.toUpperCase()}`,
                                    info: `${m.hp} HP`,
                                    type: 'switch_member',
                                    targetIndex: m.index,
                                });
                            }
                        });
                    } else {
                        items.push({
                            id: 'switch_member',
                            label: 'TROCAR GUERREIRO',
                            info: 'TAG TEAM',
                            type: 'switch_member',
                        });
                    }
                    break;

                default:
                    break;
            }

            return items;
        }

        /**
         * Abre o submenu da categoria solicitada
         */
        openSubmenu(category) {
            this.activeCategory = category;
            this.currentScreen = 'submenu';
            this.submenuIndex = 0;
            this.submenuItems = this.getSubmenuItems(category);

            if (this.submenuTitleEl) {
                const label = ACTION_LABELS[category] || category.toUpperCase();
                this.submenuTitleEl.textContent = `[${label}]`;
            }

            this.renderSubmenuList();

            // Oculta grade principal e exibe submenu
            if (this.gridElement) {
                this.gridElement.classList.add('hidden');
            }
            if (this.submenuElement) {
                this.submenuElement.classList.remove('hidden');
            }

            this.updateSubmenuVisuals();
            this.emitEvent('battle:submenu-open', {
                category: category,
                items: this.submenuItems,
            });
        }

        /**
         * Renderiza a lista de itens dentro de #submenuList
         */
        renderSubmenuList() {
            if (!this.submenuListEl) return;
            this.submenuListEl.innerHTML = '';

            this.submenuItems.forEach((item, idx) => {
                const btn = document.createElement('button');
                btn.type = 'button';
                btn.className = 'submenu-item';
                btn.setAttribute('data-index', idx);
                btn.setAttribute('role', 'option');

                btn.innerHTML = `
                    <div class="submenu-item-left">
                        <span class="menu-cursor" aria-hidden="true">${idx === 0 ? '▶' : '&nbsp;'}</span>
                        <span class="submenu-item-label">${item.label}</span>
                    </div>
                    <span class="submenu-item-info">${item.info}</span>
                `;

                btn.addEventListener('click', (e) => {
                    e.preventDefault();
                    if (!this.enabled || this.currentScreen !== 'submenu') return;
                    this.submenuIndex = idx;
                    this.updateSubmenuVisuals();
                    this.selectSubmenuItem();
                });

                this.submenuListEl.appendChild(btn);
            });
        }

        /**
         * Atualiza os indicadores de seleção no submenu
         */
        updateSubmenuVisuals() {
            if (!this.submenuListEl) return;
            const items = Array.from(this.submenuListEl.querySelectorAll('.submenu-item'));

            items.forEach((itemEl, idx) => {
                const isSelected = idx === this.submenuIndex;
                itemEl.classList.toggle('selected', isSelected);

                const cursor = itemEl.querySelector('.menu-cursor');
                if (cursor) {
                    cursor.textContent = isSelected ? '▶' : ' ';
                    cursor.style.visibility = isSelected ? 'visible' : 'hidden';
                }

                if (isSelected) {
                    itemEl.scrollIntoView({ block: 'nearest' });
                }
            });
        }

        /**
         * Move a navegação verticalmente no submenu
         */
        navigateSubmenu(direction) {
            if (!this.submenuItems || this.submenuItems.length === 0) return;
            let changed = false;

            if (direction === 'UP' && this.submenuIndex > 0) {
                this.submenuIndex--;
                changed = true;
            } else if (direction === 'DOWN' && this.submenuIndex < this.submenuItems.length - 1) {
                this.submenuIndex++;
                changed = true;
            }

            if (changed) {
                this.updateSubmenuVisuals();
                this.emitEvent('battle:submenu-move', {
                    index: this.submenuIndex,
                    item: this.submenuItems[this.submenuIndex],
                    category: this.activeCategory,
                });
            }
        }

        /**
         * Executa o item atualmente selecionado no submenu (Botão A)
         */
        selectSubmenuItem() {
            if (!this.submenuItems || this.submenuItems.length === 0) return;
            const selectedItem = this.submenuItems[this.submenuIndex];

            const eventData = {
                category: this.activeCategory,
                item: selectedItem,
                index: this.submenuIndex,
            };

            this.emitEvent('battle:submenu-select', eventData);
            this.emitEvent('battle:action-execute', eventData);

            this.setMessage(`Goku escolheu ${selectedItem.label}!`);
            return eventData;
        }

        /**
         * Fecha o submenu e retorna para a grade 2x2 (Botão B)
         */
        closeSubmenu() {
            this.currentScreen = 'root';
            this.activeCategory = null;

            if (this.submenuElement) {
                this.submenuElement.classList.add('hidden');
            }
            if (this.gridElement) {
                this.gridElement.classList.remove('hidden');
            }

            this.updateSelectionVisuals();
            this.emitEvent('battle:submenu-close', {
                row: this.row,
                col: this.col,
            });
        }

        /**
         * Atualiza os dados de combatente para sincronizar as opções de submenus
         */
        setCombatantData(playerData, teamData, inventoryData) {
            if (playerData) this.combatantData.player = playerData;
            if (teamData) this.combatantData.team = teamData;
            if (inventoryData) this.combatantData.inventory = inventoryData;

            if (this.currentScreen === 'submenu' && this.activeCategory) {
                this.submenuItems = this.getSubmenuItems(this.activeCategory);
                this.renderSubmenuList();
                this.updateSubmenuVisuals();
            }
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
         * Oculta a área de menus (grade e submenus)
         */
        hide() {
            this.visible = false;
            if (this.gridElement) this.gridElement.classList.add('hidden');
            if (this.submenuElement) this.submenuElement.classList.add('hidden');
        }

        /**
         * Exibe a área de menus
         */
        show() {
            this.visible = true;
            if (this.currentScreen === 'root') {
                if (this.gridElement) this.gridElement.classList.remove('hidden');
                if (this.submenuElement) this.submenuElement.classList.add('hidden');
                this.updateSelectionVisuals();
            } else {
                if (this.gridElement) this.gridElement.classList.add('hidden');
                if (this.submenuElement) this.submenuElement.classList.remove('hidden');
                this.updateSubmenuVisuals();
            }
        }

        /**
         * Habilita ou desabilita a aceitação de inputs pelo menu
         */
        setEnabled(enabled) {
            this.enabled = !!enabled;
            if (this.gridElement) {
                this.gridElement.classList.toggle('disabled', !this.enabled);
            }
            if (this.submenuElement) {
                this.submenuElement.classList.toggle('disabled', !this.enabled);
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

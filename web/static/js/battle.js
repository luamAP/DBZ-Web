/**
 * Dragon Ball Z - Game Boy Edition
 * Módulo de Interface e Animação da Arena de Batalha (BattleUI)
 */

(function () {
    'use strict';

    class BattleUI {
        constructor() {
            this.elements = {};
            this.state = {
                player: null,
                enemy: null,
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
            this.cacheElements();
            this.bindEvents();
            this.initData();
        }

        initData() {
            const initialEl = document.getElementById('initialBattleData');
            if (initialEl && initialEl.textContent.trim()) {
                try {
                    const data = JSON.parse(initialEl.textContent);
                    if (data && (data.player || data.battle)) {
                        this.updateFromState(data.battle || data);
                        return;
                    }
                } catch (e) {
                    console.error('Erro ao ler initialBattleData:', e);
                }
            }
            this.fetchBattleState();
        }

        cacheElements() {
            this.elements = {
                // Jogador
                playerName: document.getElementById('playerName'),
                playerForm: document.getElementById('playerForm'),
                playerStance: document.getElementById('playerStance'),
                playerHpBar: document.getElementById('playerHpBar'),
                playerHpValues: document.getElementById('playerHpValues'),
                playerKiBar: document.getElementById('playerKiBar'),
                playerKiValues: document.getElementById('playerKiValues'),
                playerSprite: document.getElementById('playerSprite'),
                playerSpriteImg: document.getElementById('playerSpriteImg'),
                playerSpriteFallback: document.getElementById('playerSpriteFallback'),
                playerHud: document.getElementById('playerHud'),

                // Oponente
                enemyName: document.getElementById('enemyName'),
                enemyForm: document.getElementById('enemyForm'),
                enemyStance: document.getElementById('enemyStance'),
                enemyHpBar: document.getElementById('enemyHpBar'),
                enemyHpValues: document.getElementById('enemyHpValues'),
                enemyKiBar: document.getElementById('enemyKiBar'),
                enemySprite: document.getElementById('enemySprite'),
                enemySpriteImg: document.getElementById('enemySpriteImg'),
                enemySpriteFallback: document.getElementById('enemySpriteFallback'),
                opponentHud: document.getElementById('opponentHud'),

                // Diálogo
                dialogueText: document.getElementById('dialogueText'),
            };
        }

        bindEvents() {
            // Escuta eventos customizados disparados por ações de combate
            document.addEventListener('battle-update', (e) => {
                if (e.detail && e.detail.state) {
                    this.updateFromState(e.detail.state);
                }
            });

            document.addEventListener('battle-damage', (e) => {
                if (e.detail && e.detail.target) {
                    this.animateDamage(e.detail.target);
                }
            });

            document.addEventListener('battle:action-execute', (e) => {
                if (e.detail) {
                    this.handleActionExecute(e.detail);
                }
            });
        }

        /**
         * Calcula percentual seguro entre 0 e 100
         */
        calculatePercentage(current, max) {
            if (!max || max <= 0) return 0;
            const pct = (current / max) * 100;
            return Math.max(0, Math.min(100, Math.round(pct)));
        }

        /**
         * Retorna a classe de status baseada no percentual de vida
         */
        getHpStatusClass(percentage) {
            if (percentage <= 0) return 'hp-critical';
            if (percentage < 20) return 'hp-low';
            if (percentage <= 50) return 'hp-mid';
            return 'hp-high';
        }

        /**
         * Atualiza os dados e animações do combatente (jogador ou inimigo)
         */
        updateCombatant(target, data) {
            if (!data) return;

            const isPlayer = target === 'player';
            const nameEl = isPlayer ? this.elements.playerName : this.elements.enemyName;
            const formEl = isPlayer ? this.elements.playerForm : this.elements.enemyForm;
            const stanceEl = isPlayer ? this.elements.playerStance : this.elements.enemyStance;
            const hpBar = isPlayer ? this.elements.playerHpBar : this.elements.enemyHpBar;
            const hpVal = isPlayer ? this.elements.playerHpValues : this.elements.enemyHpValues;
            const kiBar = isPlayer ? this.elements.playerKiBar : this.elements.enemyKiBar;
            const kiVal = isPlayer ? this.elements.playerKiValues : null;

            // Nome
            if (nameEl && data.name) {
                nameEl.textContent = data.name.toUpperCase();
            }

            // Sprite Pixel Art
            const spriteContainer = isPlayer ? this.elements.playerSprite : this.elements.enemySprite;
            const spriteImg = isPlayer ? this.elements.playerSpriteImg : this.elements.enemySpriteImg;
            const spriteFallback = isPlayer ? this.elements.playerSpriteFallback : this.elements.enemySpriteFallback;

            if (spriteContainer && spriteImg) {
                const sprites = data.sprites || {};
                const spriteSrc = isPlayer ? (sprites.back || sprites.front) : (sprites.front || sprites.back);
                if (spriteSrc) {
                    if (spriteImg.getAttribute('src') !== spriteSrc) {
                        spriteImg.src = spriteSrc;
                    }
                    spriteImg.style.display = 'block';
                    spriteContainer.classList.add('has-sprite');
                    if (spriteFallback) spriteFallback.style.display = 'none';
                } else {
                    spriteImg.style.display = 'none';
                    spriteContainer.classList.remove('has-sprite');
                    if (spriteFallback) {
                        spriteFallback.style.display = 'block';
                        spriteFallback.textContent = `[${(data.name || (isPlayer ? 'JOGADOR' : 'OPONENTE')).toUpperCase()}]`;
                    }
                }
            }

            // Forma / Transformação
            if (formEl) {
                if (data.current_transformation) {
                    formEl.textContent = `[${data.current_transformation.toUpperCase()}]`;
                    formEl.classList.add('visible');
                } else {
                    formEl.textContent = '';
                    formEl.classList.remove('visible');
                }
            }

            // Postura defensiva
            if (stanceEl) {
                if (data.defensive_stance) {
                    const stanceLabels = {
                        guard: 'DEF',
                        dodge: 'EVA',
                        counter: 'CTR',
                    };
                    stanceEl.textContent = stanceLabels[data.defensive_stance] || data.defensive_stance.toUpperCase();
                    stanceEl.classList.add('visible');
                } else {
                    stanceEl.textContent = '';
                    stanceEl.classList.remove('visible');
                }
            }

            // Atualiza barra e valores de HP com transição suave
            if (hpBar) {
                const hp = typeof data.hp === 'number' ? Math.max(0, data.hp) : 0;
                const maxHp = typeof data.max_hp === 'number' && data.max_hp > 0 ? data.max_hp : 100;
                const hpPct = this.calculatePercentage(hp, maxHp);

                hpBar.style.width = `${hpPct}%`;
                hpBar.classList.remove('hp-high', 'hp-mid', 'hp-low', 'hp-critical');
                hpBar.classList.add(this.getHpStatusClass(hpPct));

                if (hpVal) {
                    hpVal.textContent = isPlayer ? `${hp} / ${maxHp}` : `${hpPct}%`;
                }
            }

            // Atualiza barra e valores de Ki
            if (kiBar) {
                const ki = typeof data.ki === 'number' ? Math.max(0, data.ki) : 0;
                const maxKi = typeof data.max_ki === 'number' && data.max_ki > 0 ? data.max_ki : 100;
                const kiPct = this.calculatePercentage(ki, maxKi);

                kiBar.style.width = `${kiPct}%`;

                if (kiVal) {
                    kiVal.textContent = `${ki} / ${maxKi}`;
                }
            }

            this.state[target] = data;
        }

        /**
         * Dispara feedback visual de dano (shake + flash) no alvo
         */
        animateDamage(target) {
            const isPlayer = target === 'player';
            const sprite = isPlayer ? this.elements.playerSprite : this.elements.enemySprite;
            const hud = isPlayer ? this.elements.playerHud : this.elements.opponentHud;

            [sprite, hud].forEach((el) => {
                if (!el) return;
                el.classList.remove('damaged');
                // Força reflow para permitir reiniciar a animação
                void el.offsetWidth;
                el.classList.add('damaged');
                setTimeout(() => el.classList.remove('damaged'), 360);
            });
        }

        /**
         * Dispara efeito visual de carregamento de Ki
         */
        pulseKi(target, duration = 600) {
            const isPlayer = target === 'player';
            const kiBar = isPlayer ? this.elements.playerKiBar : this.elements.enemyKiBar;
            if (!kiBar) return;

            kiBar.classList.add('charging');
            setTimeout(() => kiBar.classList.remove('charging'), duration);
        }

        /**
         * Atualiza toda a arena a partir do estado completo da batalha
         */
        updateFromState(state) {
            if (!state) return;
            const battle = state.battle || state;
            const player = battle.player;
            const enemy = battle.enemy || battle.opponent;

            if (player) {
                this.updateCombatant('player', player);
                if (window.battleMenu && typeof window.battleMenu.setCombatantData === 'function') {
                    window.battleMenu.setCombatantData(
                        player,
                        battle.player_team || battle.team,
                        player.inventory,
                        battle.defense_mechanics,
                        battle.consumables
                    );
                }
            }

            if (enemy) {
                this.updateCombatant('enemy', enemy);
            }

            const message = battle.message || (battle.log && battle.log.length > 0 ? battle.log[battle.log.length - 1] : null);
            if (message && this.elements.dialogueText) {
                this.elements.dialogueText.textContent = message;
            }
        }

        /**
         * Executa uma ação de combate enviando a requisição para a API Flask
         */
        async handleActionExecute(detail) {
            if (!detail || !detail.item) return;
            const category = detail.category;
            const item = detail.item;
            let payload = { session_id: 'default' };

            if (category === 'fight') {
                payload.action = 'move';
                payload.move_name = item.raw ? item.raw.name : item.label;
            } else if (category === 'defend') {
                payload.action = 'defend';
                payload.stance = item.id;
            } else if (category === 'ki_form') {
                if (item.type === 'ki') {
                    payload.action = 'charge_ki';
                } else if (item.type === 'transformation') {
                    payload.action = 'transform';
                    payload.transformation_name = item.raw ? item.raw.name : item.label;
                }
            } else if (category === 'items_team') {
                if (item.type === 'item') {
                    payload.action = 'item';
                    payload.item_id = item.id;
                } else if (item.type === 'switch_member') {
                    payload.action = 'switch';
                    payload.target_index = item.targetIndex;
                }
            }

            try {
                const response = await fetch('/api/battle/action', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload),
                });
                const data = await response.json();
                if (response.ok && data.success && data.battle) {
                    this.updateFromState(data.battle);
                } else if (data.error && this.elements.dialogueText) {
                    this.elements.dialogueText.textContent = data.error;
                }
            } catch (err) {
                console.error('Erro ao executar ação na API:', err);
            }
        }

        /**
         * Busca o estado ativo da API Flask e sincroniza a arena
         */
        async fetchBattleState(sessionId = 'default') {
            try {
                const response = await fetch(`/api/battle/state?session_id=${encodeURIComponent(sessionId)}`);
                if (!response.ok) return null;
                const data = await response.json();
                const battleData = data.battle || (data.status === 'ok' ? data : null);
                if (battleData) {
                    this.updateFromState(battleData);
                    return battleData;
                }
            } catch (err) {
                console.error('Erro ao sincronizar arena de batalha:', err);
            }
            return null;
        }
    }

    // Exportação global
    window.BattleUI = BattleUI;
    window.battleUI = new BattleUI();
})();

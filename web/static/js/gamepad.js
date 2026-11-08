/**
 * Dragon Ball Z - Game Boy Edition
 * Módulo de Controle Virtual e Teclado (GamepadController)
 */

(function () {
    'use strict';

    // Mapeamento de botões virtuais
    const BUTTON_NAMES = {
        UP: 'UP',
        DOWN: 'DOWN',
        LEFT: 'LEFT',
        RIGHT: 'RIGHT',
        A: 'A',
        B: 'B',
        SELECT: 'SELECT',
        START: 'START',
    };

    // Mapeamento de teclas físicas (KeyboardEvent.code)
    const KEY_CODE_MAP = {
        // D-Pad (Setas ou WASD)
        ArrowUp: BUTTON_NAMES.UP,
        KeyW: BUTTON_NAMES.UP,
        ArrowDown: BUTTON_NAMES.DOWN,
        KeyS: BUTTON_NAMES.DOWN,
        ArrowLeft: BUTTON_NAMES.LEFT,
        KeyA: BUTTON_NAMES.LEFT,
        ArrowRight: BUTTON_NAMES.RIGHT,
        KeyD: BUTTON_NAMES.RIGHT,

        // Botão A (Confirmar)
        KeyZ: BUTTON_NAMES.A,
        KeyJ: BUTTON_NAMES.A,
        Enter: BUTTON_NAMES.A,

        // Botão B (Voltar/Cancelar)
        KeyX: BUTTON_NAMES.B,
        KeyK: BUTTON_NAMES.B,
        Escape: BUTTON_NAMES.B,
        Backspace: BUTTON_NAMES.B,

        // Select
        ShiftLeft: BUTTON_NAMES.SELECT,
        ShiftRight: BUTTON_NAMES.SELECT,
        Tab: BUTTON_NAMES.SELECT,

        // Start
        Space: BUTTON_NAMES.START,
        Digit1: BUTTON_NAMES.START,
    };

    // Teclas que devem ter comportamento padrão prevenido (ex: rolagem com setas)
    const PREVENT_DEFAULT_KEYS = new Set([
        'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight',
        'Space', 'Tab'
    ]);

    class GamepadController {
        constructor() {
            this.buttonElements = new Map();
            this.activeButtons = new Set();
            this.dialogueEl = null;
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
            this.dialogueEl = document.getElementById('dialogueText');
            this.bindVirtualButtons();
            this.bindKeyboard();
        }

        /**
         * Mapeia elementos virtuais do DOM com base em data-btn
         */
        bindVirtualButtons() {
            const buttons = document.querySelectorAll('[data-btn]');
            buttons.forEach((el) => {
                const btnName = el.getAttribute('data-btn').toUpperCase();
                this.buttonElements.set(btnName, el);

                // Pointer Events unificam touch, mouse e stylus
                el.addEventListener('pointerdown', (e) => {
                    e.preventDefault();
                    this.pressButton(btnName);
                });

                el.addEventListener('pointerup', (e) => {
                    e.preventDefault();
                    this.releaseButton(btnName);
                });

                el.addEventListener('pointercancel', () => this.releaseButton(btnName));
                el.addEventListener('pointerleave', () => this.releaseButton(btnName));
            });
        }

        /**
         * Escuta eventos de teclado físico com espelhamento visual
         */
        bindKeyboard() {
            window.addEventListener('keydown', (e) => {
                if (PREVENT_DEFAULT_KEYS.has(e.code)) {
                    e.preventDefault();
                }

                if (e.repeat) return; // Evita disparo duplicado por retenção da tecla

                const btn = KEY_CODE_MAP[e.code];
                if (btn) {
                    this.pressButton(btn);
                }
            });

            window.addEventListener('keyup', (e) => {
                const btn = KEY_CODE_MAP[e.code];
                if (btn) {
                    this.releaseButton(btn);
                }
            });
        }

        /**
         * Ativa o botão, aplica feedback visual/haptic e emite evento
         */
        pressButton(btnName) {
            if (this.activeButtons.has(btnName)) return;
            this.activeButtons.add(btnName);

            // Feedback visual no elemento virtual da carcaça
            const el = this.buttonElements.get(btnName);
            if (el) {
                el.classList.add('pressed');
            }

            // Haptic Feedback (Vibração tátil em smartphones compatíveis)
            if (typeof navigator !== 'undefined' && navigator.vibrate) {
                try {
                    navigator.vibrate(15);
                } catch (_) {
                    // Ignora se não for suportado/permitido
                }
            }

            // Exibição amigável na tela do visor
            this.updateDialogueFeedback(btnName, 'pressed');

            // Dispara evento customizado para ser consumido pela mecânica de combate (Fase 2)
            const event = new CustomEvent('gb-input', {
                detail: {
                    button: btnName,
                    state: 'pressed',
                    timestamp: Date.now(),
                },
            });
            document.dispatchEvent(event);
        }

        /**
         * Desativa o botão e remove o estado visual ativo
         */
        releaseButton(btnName) {
            if (!this.activeButtons.has(btnName)) return;
            this.activeButtons.delete(btnName);

            const el = this.buttonElements.get(btnName);
            if (el) {
                el.classList.remove('pressed');
            }

            const event = new CustomEvent('gb-input', {
                detail: {
                    button: btnName,
                    state: 'released',
                    timestamp: Date.now(),
                },
            });
            document.dispatchEvent(event);
        }

        updateDialogueFeedback(btnName, state) {
            // Se o menu de combate 2x2 estiver presente, a navegação é gerenciada pelo menu
            if (document.getElementById('battleMenuGrid')) return;
            if (!this.dialogueEl) return;
            const labels = {
                UP: '▲ CIMA',
                DOWN: '▼ BAIXO',
                LEFT: '◄ ESQUERDA',
                RIGHT: '► DIREITA',
                A: 'Ⓐ CONFIRMAR',
                B: 'Ⓑ VOLTAR',
                SELECT: 'SELECT',
                START: 'START',
            };
            const label = labels[btnName] || btnName;
            this.dialogueEl.textContent = `[Comando: ${label}] - Pronto para batalha!`;
        }
    }

    // Instanciação global e exportação para a janela
    window.gamepadController = new GamepadController();
    window.GamepadController = GamepadController;
    window.BUTTON_NAMES = BUTTON_NAMES;
    window.KEY_CODE_MAP = KEY_CODE_MAP;
})();

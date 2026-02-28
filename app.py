import streamlit as st
import streamlit.components.v1 as components

# 1. Configuración para que el juego use TODA la pantalla y se vea grande
st.set_page_config(
    page_title="Mi Portal de Juegos",
    layout="wide", # Esto expande el juego hacia los lados
    initial_sidebar_state="collapsed"
)

# Título del portal
st.markdown("<h1 style='text-align: center; color: #ff6b6b;'>🎮 Mi Arcade Interactivo</h1>", unsafe_allow_html=True)

# 2. Tu código de juego de memoria con ajustes de tamaño (CSS actualizado)
codigo_juego = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Memoria - Animales</title>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <style>
        :root {
            --primary: #ff6b6b;
            --secondary: #4ecdc4;
            --bg-game: #f0f9ff;
            --card-back: #45b7d1;
        }

        body {
            font-family: 'Comic Sans MS', cursive, sans-serif;
            background-color: var(--bg-game);
            display: flex;
            flex-direction: column;
            align-items: center;
            margin: 0;
            padding: 20px;
        }

        /* AJUSTE: El tablero ahora permite que las cartas crezcan más */
        .game-board {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 20px;
            max-width: 1200px;
            width: 95%;
            margin-top: 20px;
        }

        .card {
            aspect-ratio: 1 / 1;
            position: relative;
            cursor: pointer;
            transform-style: preserve-3d;
            transition: transform 0.6s;
            border-radius: 20px;
            box-shadow: 0 8px 15px rgba(0,0,0,0.1);
        }

        .card.flipped { transform: rotateY(180deg); }

        .card-face {
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
            border-radius: 20px;
            border: 5px solid white;
        }

        /* AJUSTE: Dibujo de la huella más grande */
        .card-front {
            background: var(--card-back);
            color: white;
            font-size: 5rem;
        }

        .card-back {
            background: white;
            transform: rotateY(180deg);
            text-align: center;
        }

        /* AJUSTE: Emojis y Texto mucho más grandes */
        .card-emoji { font-size: 6rem; }
        .card-text { font-size: 2.2rem; color: var(--card-back); font-weight: bold; }

        h1 { color: #2c3e50; font-size: 3rem; margin-bottom: 10px; }
    </style>
</head>
<body>

    <div class="game-board" id="board"></div>

    <script>
        const animals = [
            { name: "Perro", emoji: "🐶" },
            { name: "Gato", emoji: "🐱" },
            { name: "Conejo", emoji: "🐰" },
            { name: "Hamster", emoji: "🐹" },
            { name: "Tortuga", emoji: "🐢" },
            { name: "Loro", emoji: "🦜" },
            { name: "Pez", emoji: "🐠" },
            { name: "Gallina", emoji: "🐔" },
            { name: "Caballo", emoji: "🐴" },
            { name: "Vaca", emoji: "🐮" }
        ];

        let flippedCards = [];
        let matchedPairs = 0;
        const board = document.getElementById('board');

        function initGame() {
            let deck = [];
            animals.forEach(a => {
                deck.push({ type: 'text', value: a.name, id: a.name });
                deck.push({ type: 'emoji', value: a.emoji, id: a.name });
            });

            deck.sort(() => Math.random() - 0.5);

            deck.forEach(item => {
                const card = document.createElement('div');
                card.className = 'card';
                card.dataset.id = item.id;
                card.innerHTML = `
                    <div class="card-face card-front">🐾</div>
                    <div class="card-face card-back">
                        ${item.type === 'text' ? `<span class="card-text">${item.value}</span>` : `<span class="card-emoji">${item.value}</span>`}
                    </div>
                `;
                card.addEventListener('click', flipCard);
                board.appendChild(card);
            });
        }

        function flipCard() {
            if (flippedCards.length < 2 && !this.classList.contains('flipped')) {
                this.classList.add('flipped');
                flippedCards.push(this);
                if (flippedCards.length === 2) checkMatch();
            }
        }

        function checkMatch() {
            const [c1, c2] = flippedCards;
            if (c1.dataset.id === c2.dataset.id) {
                matchedPairs++;
                confetti({ particleCount: 100, spread: 70, origin: { y: 0.6 } });
                flippedCards = [];
            } else {
                setTimeout(() => {
                    c1.classList.remove('flipped');
                    c2.classList.remove('flipped');
                    flippedCards = [];
                }, 1000);
            }
        }

        initGame();
    </script>
</body>
</html>
"""

# 3. Renderizar el juego con una altura generosa para que no salga el scroll
components.html(codigo_juego, height=1100, scrolling=False)

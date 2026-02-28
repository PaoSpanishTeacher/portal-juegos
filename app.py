import streamlit as st
import streamlit.components.v1 as components

# 1. Configuración de pantalla completa
st.set_page_config(
    page_title="Memoria: Animales Domésticos",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Tu código HTML exacto (Optimizado para Streamlit)
codigo_html = r"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Memoria Animales Domésticos - PaoSpanishTeacher</title>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka+One&family=Quicksand:wght@500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --verde-suave: #a7c957;
            --verde-oscuro: #386641;
            --cielo: #f2e8cf;
            --rojo-granja: #bc4749;
            --amarillo-sol: #ffb703;
            --azul-claro: #8ecae6;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }

        body {
            font-family: 'Quicksand', sans-serif;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: #f7f1e3;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(167, 201, 87, 0.2) 0%, transparent 40%),
                linear-gradient(to bottom, #8ecae6 0%, #8ecae6 30%, #a7c957 30%, #a7c957 100%);
            padding: 20px;
        }

        header { text-align: center; margin-bottom: 20px; }

        h1 {
            font-family: 'Fredoka One', cursive;
            font-size: 3rem;
            color: var(--verde-oscuro);
            text-shadow: 4px 4px 0px white;
        }

        .game-board {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            max-width: 900px;
            width: 100%;
            perspective: 1000px;
        }

        @media (min-width: 600px) {
            .game-board { grid-template-columns: repeat(5, 1fr); }
        }

        .card {
            aspect-ratio: 1 / 1.2;
            cursor: pointer;
            position: relative;
            transform-style: preserve-3d;
            transition: transform 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        .card.flipped { transform: rotateY(180deg); }

        .card-face {
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            border-radius: 20px;
            border: 5px solid white;
            box-shadow: 0 8px 15px rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .card-back { background: var(--amarillo-sol); color: white; font-size: 3.5rem; }
        .card-back::after { content: '🐾'; }

        .card-front { background: white; transform: rotateY(180deg); }
        .text-card { font-weight: 700; font-size: 1.6rem; color: var(--verde-oscuro); text-transform: capitalize; }
        .image-card { font-size: 4.5rem; }

        #final-screen {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(255,255,255,0.95);
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 200;
            text-align: center;
        }
        #final-screen.active { display: flex; }

        .btn-restart {
            background: var(--rojo-granja);
            color: white;
            border: none;
            padding: 15px 40px;
            font-size: 1.8rem;
            font-family: 'Fredoka One', cursive;
            border-radius: 50px;
            cursor: pointer;
            box-shadow: 0 6px 0 #8d2e2f;
        }

        .feedback-pop {
            position: fixed;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            font-family: 'Fredoka One', cursive;
            font-size: 4rem;
            color: var(--amarillo-sol);
            -webkit-text-stroke: 2px white;
            opacity: 0;
            pointer-events: none;
        }
        .feedback-pop.show { animation: popIn 0.8s ease forwards; opacity: 1; }

        @keyframes popIn {
            0% { transform: translate(-50%, -50%) scale(0); }
            50% { transform: translate(-50%, -50%) scale(1.2); }
            100% { transform: translate(-50%, -50%) scale(1); opacity: 0; }
        }
    </style>
</head>
<body>
    <header>
        <h1>Animales Domésticos</h1>
        <p style="color: white; font-weight: bold;">PaoSpanishTeacher</p>
    </header>

    <div class="game-board" id="board"></div>
    <div class="feedback-pop" id="feedback">¡Excelente!</div>

    <div id="final-screen">
        <h2 style="font-family: 'Fredoka One'; font-size: 3rem; color: #386641;">¡Felicidades!</h2>
        <p style="font-size: 1.5rem; margin: 20px 0;">Has encontrado todos los animales.</p>
        <button class="btn-restart" onclick="location.reload()">Jugar otra vez</button>
    </div>

    <script>
        const ANIMALS = [
            { name: "perro", icon: "🐶" }, { name: "gato", icon: "🐱" },
            { name: "conejo", icon: "🐰" }, { name: "hamster", icon: "🐹" },
            { name: "tortuga", icon: "🐢" }, { name: "loro", icon: "🦜" },
            { name: "pez", icon: "🐠" }, { name: "gallina", icon: "🐔" },
            { name: "caballo", icon: "🐴" }, { name: "vaca", icon: "🐮" }
        ];

        let firstCard = null, secondCard = null, lockBoard = false, matchedPairs = 0;

        function createBoard() {
            const board = document.getElementById('board');
            let deck = [];
            ANIMALS.forEach(a => {
                deck.push({ type: 'text', val: a.name, id: a.name });
                deck.push({ type: 'image', val: a.icon, id: a.name });
            });
            deck.sort(() => Math.random() - 0.5);
            deck.forEach(item => {
                const card = document.createElement('div');
                card.classList.add('card');
                card.dataset.id = item.id;
                card.innerHTML = `
                    <div class="card-face card-back"></div>
                    <div class="card-face card-front ${item.type === 'text' ? 'text-card' : 'image-card'}">${item.val}</div>
                `;
                card.onclick = flipCard;
                board.appendChild(card);
            });
        }

        function flipCard() {
            if (lockBoard || this === firstCard) return;
            this.classList.add('flipped');
            if (!firstCard) { firstCard = this; return; }
            secondCard = this;
            checkMatch();
        }

        function checkMatch() {
            let match = firstCard.dataset.id === secondCard.dataset.id;
            if (match) {
                matchedPairs++;
                document.getElementById('feedback').classList.add('show');
                setTimeout(() => document.getElementById('feedback').classList.remove('show'), 800);
                firstCard.onclick = null; secondCard.onclick = null;
                reset();
                if (matchedPairs === ANIMALS.length) {
                    setTimeout(() => {
                        confetti();
                        document.getElementById('final-screen').classList.add('active');
                    }, 800);
                }
            } else {
                lockBoard = true;
                setTimeout(() => {
                    firstCard.classList.remove('flipped');
                    secondCard.classList.remove('flipped');
                    reset();
                }, 1000);
            }
        }

        function reset() { [firstCard, secondCard, lockBoard] = [null, null, false]; }

        createBoard();
    </script>
</body>
</html>
"""

# 3. Renderizar el juego con espacio suficiente
components.html(codigo_html, height=1000, scrolling=False)

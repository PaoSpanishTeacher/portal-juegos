import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Memoria: Animales Domésticos", layout="wide")

# El código HTML con la corrección de audio
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

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            user-select: none;
        }

        body {
            font-family: 'Quicksand', sans-serif;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: #f7f1e3;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(167, 201, 87, 0.2) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(167, 201, 87, 0.2) 0%, transparent 40%),
                linear-gradient(to bottom, #8ecae6 0%, #8ecae6 30%, #a7c957 30%, #a7c957 100%);
            padding: 20px;
            overflow-x: hidden;
            position: relative;
        }

        header {
            text-align: center;
            margin-bottom: 20px;
            z-index: 10;
        }

        h1 {
            font-family: 'Fredoka One', cursive;
            font-size: 3rem;
            color: var(--verde-oscuro);
            text-shadow: 4px 4px 0px white;
            margin-bottom: 5px;
        }

        .brand-name {
            font-size: 1.3rem;
            color: var(--rojo-granja);
            font-weight: 700;
            font-style: italic;
        }

        .game-board {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            max-width: 800px;
            width: 100%;
            perspective: 1000px;
            margin-bottom: 30px;
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

        .card:hover { transform: scale(1.05); }
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

        .card-back {
            background: var(--amarillo-sol);
            background-image: radial-gradient(circle at 50% 50%, rgba(255,255,255,0.3) 0%, transparent 60%);
            color: white;
            font-size: 3rem;
        }
        .card-back::after { content: '🐾'; }

        .card-front { background: white; transform: rotateY(180deg); }
        .text-card { font-weight: 700; font-size: 1.3rem; color: var(--verde-oscuro); text-transform: capitalize; padding: 10px; text-align: center; }
        .image-card { font-size: 4rem; }

        .feedback-pop {
            position: fixed;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            font-family: 'Fredoka One', cursive;
            font-size: 4rem;
            color: var(--amarillo-sol);
            -webkit-text-stroke: 2px white;
            z-index: 100;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.3s;
        }
        .feedback-pop.show { opacity: 1; animation: popIn 0.8s ease forwards; }

        @keyframes popIn {
            0% { transform: translate(-50%, -50%) scale(0); }
            50% { transform: translate(-50%, -50%) scale(1.5); }
            100% { transform: translate(-50%, -50%) scale(1); opacity: 0; }
        }

        #final-screen {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(255,255,255,0.9);
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 200;
            text-align: center;
            padding: 20px;
        }
        #final-screen.active { display: flex; }

        .final-msg { font-family: 'Fredoka One', cursive; font-size: 3rem; color: var(--verde-oscuro); margin-bottom: 20px; }

        .btn-restart {
            background: var(--rojo-granja);
            color: white;
            border: none;
            padding: 20px 50px;
            font-size: 1.8rem;
            font-family: 'Fredoka One', cursive;
            border-radius: 50px;
            cursor: pointer;
            box-shadow: 0 8px 0 #8d2e2f;
            transition: all 0.2s;
        }
        .btn-restart:active { transform: translateY(4px); box-shadow: 0 4px 0 #8d2e2f; }

        .watermark {
            position: fixed;
            bottom: 15px;
            right: 20px;
            font-style: italic;
            color: rgba(56, 102, 65, 0.4);
            font-size: 0.9rem;
            pointer-events: none;
            z-index: 5;
        }

        .balloon {
            position: absolute;
            bottom: -100px;
            width: 50px;
            height: 70px;
            border-radius: 50%;
            z-index: 150;
            animation: float 6s ease-in infinite;
        }

        @keyframes float {
            0% { transform: translateY(0) rotate(0); opacity: 1; }
            100% { transform: translateY(-110vh) rotate(20deg); opacity: 0; }
        }

        .star-effect {
            position: absolute;
            pointer-events: none;
            color: gold;
            animation: stars 0.6s forwards;
            z-index: 100;
        }

        @keyframes stars {
            0% { transform: scale(0); opacity: 1; }
            100% { transform: scale(2); opacity: 0; }
        }
    </style>
</head>
<body>

    <header>
        <h1>Memoria - Animales Domésticos</h1>
        <div class="brand-name">PaoSpanishTeacher</div>
    </header>

    <div class="game-board" id="board"></div>

    <div class="feedback-pop" id="feedback">¡Excelente!</div>

    <div id="final-screen">
        <h2 class="final-msg">¡Felicidades! Has encontrado todos los animales domésticos.</h2>
        <p style="font-size: 1.5rem; margin-bottom: 30px; font-weight: 700; color: var(--verde-oscuro);">Juego creado por PaoSpanishTeacher</p>
        <button class="btn-restart" onclick="restartGame()">Jugar otra vez</button>
    </div>

    <div class="watermark">PaoSpanishTeacher</div>

    <!-- Audios con manejo de errores -->
    <audio id="audio-success" preload="auto" src="https://assets.mixkit.co/active_storage/sfx/2013/2013-preview.mp3"></audio>
    <audio id="audio-error" preload="auto" src="https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3"></audio>
    <audio id="audio-celebrate" preload="auto" src="https://assets.mixkit.co/active_storage/sfx/1435/1435-preview.mp3"></audio>

    <script>
        const ANIMALS = [
            { name: "perro", icon: "🐶" },
            { name: "gato", icon: "🐱" },
            { name: "conejo", icon: "🐰" },
            { name: "hamster", icon: "🐹" },
            { name: "tortuga", icon: "🐢" },
            { name: "loro", icon: "🦜" },
            { name: "pez", icon: "🐠" },
            { name: "gallina", icon: "🐔" },
            { name: "caballo", icon: "🐴" },
            { name: "vaca", icon: "🐮" }
        ];

        let firstCard = null;
        let secondCard = null;
        let lockBoard = false;
        let matchedPairs = 0;

        // Función para reproducir audio de forma segura
        function safePlay(audioId) {
            const audio = document.getElementById(audioId);
            if (audio) {
                audio.play().catch(e => {
                    console.warn(`Audio ${audioId} no pudo reproducirse:`, e.message);
                });
            }
        }

        function shuffle(array) {
            for (let i = array.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [array[i], array[j]] = [array[j], array[i]];
            }
            return array;
        }

        function createBoard() {
            const board = document.getElementById('board');
            board.innerHTML = '';
            
            let deck = [];
            ANIMALS.forEach(animal => {
                deck.push({ type: 'text', val: animal.name, id: animal.name });
                deck.push({ type: 'image', val: animal.icon, id: animal.name });
            });

            shuffle(deck);

            deck.forEach(item => {
                const card = document.createElement('div');
                card.classList.add('card');
                card.dataset.id = item.id;

                card.innerHTML = `
                    <div class="card-face card-back"></div>
                    <div class="card-face card-front ${item.type === 'text' ? 'text-card' : 'image-card'}">
                        ${item.val}
                    </div>
                `;

                card.addEventListener('click', flipCard);
                board.appendChild(card);
            });
        }

        function flipCard() {
            if (lockBoard) return;
            if (this === firstCard) return;

            this.classList.add('flipped');

            if (!firstCard) {
                firstCard = this;
                return;
            }

            secondCard = this;
            checkForMatch();
        }

        function checkForMatch() {
            let isMatch = firstCard.dataset.id === secondCard.dataset.id;
            isMatch ? disableCards() : unflipCards();
        }

        function disableCards() {
            matchedPairs++;
            safePlay('audio-success');
            
            createStarEffect(firstCard);
            createStarEffect(secondCard);

            const pop = document.getElementById('feedback');
            pop.classList.add('show');
            setTimeout(() => pop.classList.remove('show'), 800);

            firstCard.removeEventListener('click', flipCard);
            secondCard.removeEventListener('click', flipCard);

            resetBoard();

            if (matchedPairs === ANIMALS.length) {
                setTimeout(endGame, 1000);
            }
        }

        function createStarEffect(element) {
            const rect = element.getBoundingClientRect();
            const star = document.createElement('div');
            star.className = 'star-effect';
            star.innerHTML = '⭐';
            star.style.left = (rect.left + rect.width/2) + 'px';
            star.style.top = (rect.top + rect.height/2) + 'px';
            document.body.appendChild(star);
            setTimeout(() => star.remove(), 600);
        }

        function unflipCards() {
            lockBoard = true;
            safePlay('audio-error');

            setTimeout(() => {
                if(firstCard) firstCard.classList.remove('flipped');
                if(secondCard) secondCard.classList.remove('flipped');
                resetBoard();
            }, 1200);
        }

        function resetBoard() {
            [firstCard, secondCard] = [null, null];
            lockBoard = false;
        }

        function endGame() {
            const finalScreen = document.getElementById('final-screen');
            finalScreen.classList.add('active');
            
            safePlay('audio-celebrate');
            speakResult();

            confetti({
                particleCount: 150,
                spread: 70,
                origin: { y: 0.6 }
            });

            for(let i=0; i<15; i++){
                setTimeout(createBalloon, i * 200);
            }
        }

        function createBalloon() {
            const colors = ['#bc4749', '#ffb703', '#8ecae6', '#a7c957', '#fb8500'];
            const b = document.createElement('div');
            b.classList.add('balloon');
            b.style.left = Math.random() * 90 + 'vw';
            b.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            b.style.animationDuration = (Math.random() * 2 + 4) + 's';
            document.body.appendChild(b);
            setTimeout(() => b.remove(), 6000);
        }

        function speakResult() {
            if ('speechSynthesis' in window) {
                const synth = window.speechSynthesis;
                const utter = new SpeechSynthesisUtterance("Muy bien, sigue aprendiendo español.");
                utter.lang = 'es-ES';
                utter.rate = 0.9;
                synth.speak(utter);
            }
        }

        function restartGame() {
            matchedPairs = 0;
            document.getElementById('final-screen').classList.remove('active');
            const celebrateAudio = document.getElementById('audio-celebrate');
            if (celebrateAudio) {
                celebrateAudio.pause();
                celebrateAudio.currentTime = 0;
            }
            createBoard();
        }

        // Inicializar juego
        window.addEventListener('DOMContentLoaded', createBoard);
    </script>
</body>
</html>
"""

components.html(codigo_html, height=1000, scrolling=False)

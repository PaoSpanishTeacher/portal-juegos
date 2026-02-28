import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Memoria: Animales Domésticos", layout="wide")

# El código HTML con la corrección de audio
codigo_html = r"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Fredoka+One&family=Quicksand:wght@500;700&display=swap" rel="stylesheet">
    <style>
        :root { --verde: #386641; --amarillo: #ffb703; --rojo: #bc4749; }
        body { font-family: 'Quicksand', sans-serif; background: #f7f1e3; display: flex; flex-direction: column; align-items: center; padding: 20px; min-height: 100vh; margin: 0; }
        h1 { font-family: 'Fredoka One', cursive; color: var(--verde); text-shadow: 2px 2px white; font-size: 2.5rem; }
        .game-board { display: grid; grid-template-columns: repeat(5, 1fr); gap: 15px; max-width: 900px; width: 100%; margin-top: 20px; }
        .card { aspect-ratio: 1/1.2; cursor: pointer; position: relative; transform-style: preserve-3d; transition: transform 0.5s; }
        .card.flipped { transform: rotateY(180deg); }
        .card-face { position: absolute; width: 100%; height: 100%; backface-visibility: hidden; border-radius: 15px; border: 4px solid white; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        .card-back { background: var(--amarillo); font-size: 3rem; color: white; }
        .card-back::after { content: '🐾'; }
        .card-front { background: white; transform: rotateY(180deg); }
        .image-card { font-size: 4rem; }
        .text-card { font-size: 1.5rem; font-weight: bold; color: var(--verde); text-transform: capitalize; }
        #final-screen { position: fixed; inset: 0; background: rgba(255,255,255,0.9); display: none; flex-direction: column; align-items: center; justify-content: center; z-index: 100; text-align: center; }
        #final-screen.active { display: flex; }
        .btn { background: var(--rojo); color: white; border: none; padding: 15px 30px; font-family: 'Fredoka One'; font-size: 1.5rem; border-radius: 50px; cursor: pointer; margin-top: 20px; }
    </style>
</head>
<body>
    <h1>Animales Domésticos</h1>
    <div class="game-board" id="board"></div>

    <div id="final-screen">
        <h2 style="font-family: 'Fredoka One'; font-size: 3rem; color: var(--verde);">¡Excelente Trabajo!</h2>
        <p style="font-size: 1.5rem;">Has encontrado todas las parejas.</p>
        <button class="btn" onclick="location.reload()">Jugar de nuevo</button>
    </div>

    <audio id="snd-success" src="https://assets.mixkit.co/active_storage/sfx/2013/2013-preview.mp3"></audio>
    <audio id="snd-error" src="https://assets.mixkit.co/active_storage/sfx/2571/2571-preview.mp3"></audio>

    <script>
        const ANIMALS = [
            {n:"perro", i:"🐶"}, {n:"gato", i:"🐱"}, {n:"conejo", i:"🐰"},
            {n:"hamster", i:"🐹"}, {n:"tortuga", i:"🐢"}, {n:"loro", i:"🦜"},
            {n:"pez", i:"🐠"}, {n:"gallina", i:"🐔"}, {n:"caballo", i:"🐴"}, {n:"vaca", i:"🐮"}
        ];

        let first = null, second = null, lock = false, pairs = 0;

        function createBoard() {
            const board = document.getElementById('board');
            let deck = [];
            ANIMALS.forEach(a => {
                deck.push({t:'text', v:a.n, id:a.n});
                deck.push({t:'img', v:a.i, id:a.n});
            });
            deck.sort(() => Math.random() - 0.5);
            deck.forEach(item => {
                const card = document.createElement('div');
                card.className = 'card';
                card.dataset.id = item.id;
                card.innerHTML = `<div class="card-face card-back"></div><div class="card-face card-front ${item.t === 'img' ? 'image-card' : 'text-card'}">${item.v}</div>`;
                card.onclick = flip;
                board.appendChild(card);
            });
        }

        function flip() {
            // Activar audio en el primer clic (truco para navegadores)
            document.getElementById('snd-success').play().then(() => {
                document.getElementById('snd-success').pause();
                document.getElementById('snd-success').currentTime = 0;
            }).catch(() => {});

            if (lock || this === first) return;
            this.classList.add('flipped');
            if (!first) { first = this; return; }
            second = this;
            check();
        }

        function check() {
            if (first.dataset.id === second.dataset.id) {
                document.getElementById('snd-success').play();
                pairs++;
                reset(true);
                if (pairs === ANIMALS.length) setTimeout(win, 500);
            } else {
                document.getElementById('snd-error').play();
                lock = true;
                setTimeout(() => {
                    first.classList.remove('flipped');
                    second.classList.remove('flipped');
                    reset(false);
                }, 1000);
            }
        }

        function reset(isMatch) {
            if(isMatch) { first.onclick = null; second.onclick = null; }
            [first, second, lock] = [null, null, false];
        }

        function win() {
            confetti({ particleCount: 200, spread: 70, origin: { y: 0.6 } });
            document.getElementById('final-screen').classList.add('active');
            
            // Voz de felicitación
            if ('speechSynthesis' in window) {
                const msg = new SpeechSynthesisUtterance("¡Felicidades! Has encontrado todos los animales domésticos. ¡Muy bien!");
                msg.lang = 'es-ES';
                msg.rate = 0.9;
                window.speechSynthesis.speak(msg);
            }
        }

        createBoard();
    </script>
</body>
</html>
"""

components.html(codigo_html, height=1000, scrolling=False)

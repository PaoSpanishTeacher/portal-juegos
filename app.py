import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Mi Portal de Juegos", layout="wide")

# El código HTML/JS de tu juego de animales
codigo_juego = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Memoria - Animales</title>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <style>
        :root { --primary: #ff6b6b; --secondary: #4ecdc4; --bg-game: #f0f9ff; --card-back: #45b7d1; }
        body { font-family: 'Comic Sans MS', cursive, sans-serif; background-color: var(--bg-game); display: flex; flex-direction: column; align-items: center; padding: 20px; }
        .game-board { display: grid; grid-template-columns: repeat(5, 1fr); gap: 15px; max-width: 900px; width: 100%; }
        .card { aspect-ratio: 1/1; position: relative; cursor: pointer; transform-style: preserve-3d; transition: transform 0.6s; border-radius: 15px; }
        .card.flipped { transform: rotateY(180deg); }
        .card-face { position: absolute; width: 100%; height: 100%; backface-visibility: hidden; display: flex; justify-content: center; align-items: center; border-radius: 15px; border: 4px solid white; }
        .card-front { background: var(--card-back); font-size: 3rem; color: white; }
        .card-back { background: white; transform: rotateY(180deg); font-size: 1.4rem; color: var(--card-back); text-align: center; }
    </style>
</head>
<body>
    <h1>🐾 Memoria Animal</h1>
    <div class="game-board" id="board"></div>
    <script>
        const animals = [{n:"Perro",e:"🐶"},{n:"Gato",e:"🐱"},{n:"Conejo",e:"🐰"},{n:"Hamster",e:"🐹"},{n:"Tortuga",e:"🐢"},{n:"Loro",e:"🦜"},{n:"Pez",e:"🐠"},{n:"Gallina",e:"🐔"},{n:"Caballo",e:"🐴"},{n:"Vaca",e:"🐮"}];
        let flipped = [], matched = 0, board = document.getElementById('board');
        function init(){
            let deck = []; animals.forEach(a=>{ deck.push({v:a.n,id:a.n,t:'t'}); deck.push({v:a.e,id:a.n,t:'e'}); });
            deck.sort(()=>Math.random()-0.5);
            deck.forEach(i=>{
                const c = document.createElement('div'); c.className='card'; c.dataset.id=i.id;
                c.innerHTML=`<div class="card-face card-front">🐾</div><div class="card-face card-back">${i.v}</div>`;
                c.onclick=flip; board.appendChild(c);
            });
        }
        function flip(){
            if(flipped.length<2 && !this.classList.contains('flipped')){
                this.classList.add('flipped'); flipped.push(this);
                if(flipped.length==2) setTimeout(check, 700);
            }
        }
        function check(){
            if(flipped[0].dataset.id==flipped[1].dataset.id){ matched++; confetti(); }
            else { flipped[0].classList.remove('flipped'); flipped[1].classList.remove('flipped'); }
            flipped=[];
        }
        init();
    </script>
</body>
</html>
"""

# Renderizar el juego
components.html(codigo_juego, height=800, scrolling=True)

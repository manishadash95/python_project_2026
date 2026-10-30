from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

PAGE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>NOCTURNE | The Last Run</title>

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --cyan: #6df7ff;
    --pink: #ff477e;
    --white: #eefaff;
}

html, body {
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: #03050b;
    color: var(--white);
    font-family: Arial, Helvetica, sans-serif;
}

body {
    display: grid;
    place-items: center;
}

.game {
    position: relative;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: #050914;
}

canvas {
    display: block;
    width: 100%;
    height: 100%;
}

.vignette {
    position: absolute;
    inset: 0;
    pointer-events: none;
    background: radial-gradient(
        ellipse at center,
        transparent 30%,
        rgba(0,0,0,.8) 120%
    );
}

.scanlines {
    position: absolute;
    inset: 0;
    pointer-events: none;
    opacity: .12;
    background: repeating-linear-gradient(
        to bottom,
        transparent 0 3px,
        rgba(255,255,255,.06) 4px
    );
}

.topbar {
    position: absolute;
    top: 35px;
    left: 5%;
    right: 5%;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
}

.brand {
    color: var(--cyan);
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 5px;
}

.brand small {
    display: block;
    margin-top: 9px;
    color: #8195ac;
    font-size: 9px;
    letter-spacing: 2px;
}

.hud {
    display: flex;
    gap: 35px;
    text-align: right;
}

.metric label {
    display: block;
    margin-bottom: 8px;
    color: #8195ac;
    font-size: 9px;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.metric strong {
    font-size: 24px;
    letter-spacing: 2px;
}

.metric strong span {
    color: var(--cyan);
}

.intro {
    position: absolute;
    top: 23%;
    left: 50%;
    width: 90%;
    text-align: center;
    transform: translateX(-50%);
    transition: opacity .4s;
    pointer-events: none;
}

.eyebrow {
    color: var(--cyan);
    font-size: 10px;
    font-weight: bold;
    letter-spacing: 5px;
}

h1 {
    margin: 18px 0;
    font-size: clamp(48px, 8vw, 105px);
    line-height: .9;
    letter-spacing: -5px;
    font-weight: 900;
    text-shadow: 0 0 35px rgba(109,247,255,.2);
}

h1 span {
    color: transparent;
    -webkit-text-stroke: 1px white;
}

.subtitle {
    color: #9aaabd;
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
}

.bottom {
    position: absolute;
    bottom: 35px;
    left: 5%;
    right: 5%;
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 15px;
}

.controls {
    color: #91a1b5;
    font-size: 10px;
    line-height: 2;
    letter-spacing: 1px;
}

.key {
    display: inline-block;
    padding: 5px 9px;
    margin-right: 5px;
    border: 1px solid #42576c;
    border-radius: 4px;
    color: white;
}

button {
    padding: 15px 25px;
    border: 1px solid rgba(109,247,255,.7);
    background: rgba(4,16,26,.8);
    color: white;
    font-size: 10px;
    font-weight: bold;
    letter-spacing: 3px;
    text-transform: uppercase;
    cursor: pointer;
    box-shadow: 0 0 25px rgba(109,247,255,.12);
    transition: .25s;
}

button:hover {
    background: rgba(20,65,75,.9);
    box-shadow: 0 0 35px rgba(109,247,255,.3);
    transform: translateY(-2px);
}

.overlay {
    position: absolute;
    inset: 0;
    display: grid;
    place-items: center;
    background: rgba(2,5,12,.6);
    backdrop-filter: blur(6px);
    opacity: 0;
    visibility: hidden;
    transition: .3s;
    text-align: center;
}

.overlay.show {
    opacity: 1;
    visibility: visible;
}

.panel {
    width: min(90%, 450px);
    padding: 35px;
    border: 1px solid rgba(109,247,255,.3);
    background: linear-gradient(
        145deg,
        rgba(8,19,33,.96),
        rgba(3,7,15,.96)
    );
    box-shadow: 0 0 70px rgba(0,0,0,.6);
}

.panel h2 {
    margin: 20px 0 10px;
    font-size: 50px;
    letter-spacing: -2px;
    text-transform: uppercase;
}

.panel p {
    color: #9baabd;
    font-size: 12px;
    line-height: 2;
}

.final-score {
    margin: 25px 0;
    color: var(--cyan);
    font-size: 22px;
    font-weight: bold;
}

.progress {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 2px;
    background: rgba(255,255,255,.08);
}

.progress span {
    display: block;
    width: 0;
    height: 100%;
    background: var(--cyan);
    box-shadow: 0 0 12px var(--cyan);
}

.hidden {
    opacity: 0;
}

@media(max-width: 600px) {
    .topbar {
        top: 20px;
    }

    .hud {
        gap: 15px;
    }

    .metric strong {
        font-size: 17px;
    }

    .bottom {
        bottom: 20px;
    }

    .controls {
        font-size: 8px;
    }

    button {
        padding: 12px;
        letter-spacing: 1px;
    }

    .intro {
        top: 30%;
    }
}
</style>
</head>

<body>

<div class="game">

    <canvas id="scene"></canvas>

    <div class="vignette"></div>
    <div class="scanlines"></div>

    <div class="topbar">

        <div class="brand">
            N / NOCTURNE
            <small>ENDLESS RUNNER · SECTOR 01</small>
        </div>

        <div class="hud">

            <div class="metric">
                <label>Distance</label>
                <strong id="score">00000</strong>
            </div>

            <div class="metric">
                <label>Best Run</label>
                <strong><span id="best">00000</span></strong>
            </div>

        </div>

    </div>

    <div class="intro" id="intro">

        <div class="eyebrow">THE WORLD WENT QUIET</div>

        <h1>
            THE LAST<br>
            <span>RUN</span>
        </h1>

        <div class="subtitle">
            One runner. No second chances.
        </div>

    </div>

    <div class="bottom" id="bottom">

        <div class="controls">
            <span class="key">SPACE</span>
            <span class="key">↑</span> Jump<br>
            <span class="key">R</span> Restart · Avoid what comes next
        </div>

        <button id="startBtn">▶ Begin Run</button>

    </div>

    <div class="overlay" id="gameOver">

        <div class="panel">

            <div class="eyebrow">
                SIGNAL LOST · RUN TERMINATED
            </div>

            <h2>Run Over.</h2>

            <p>
                The horizon is still out there.<br>
                Take a breath. Try again.
            </p>

            <div class="final-score">
                DISTANCE &nbsp;
                <span id="finalScore">00000</span>
            </div>

            <button id="retryBtn">↻ Run It Back</button>

        </div>

    </div>

    <div class="progress">
        <span id="progress"></span>
    </div>

</div>

<script>
const canvas = document.getElementById("scene");
const ctx = canvas.getContext("2d");

const scoreEl = document.getElementById("score");
const bestEl = document.getElementById("best");
const intro = document.getElementById("intro");
const bottom = document.getElementById("bottom");
const overlay = document.getElementById("gameOver");
const finalScore = document.getElementById("finalScore");
const progress = document.getElementById("progress");

let W, H, ground, dpr;
let running = false;
let started = false;
let dead = false;

let score = 0;
let best = Number(localStorage.getItem("nocturne-best") || 0);
let speed = 330;
let last = 0;
let spawn = 0;
let shake = 0;

let obstacles = [];
let particles = [];
let stars = [];
let buildings = [];

const player = {
    x: 100,
    y: 0,
    w: 44,
    h: 52,
    vy: 0,
    onGround: true,
    runTime: 0
};

bestEl.textContent = String(best).padStart(5, "0");


function resize() {

    const rect = canvas.getBoundingClientRect();

    dpr = Math.min(window.devicePixelRatio || 1, 2);

    W = rect.width;
    H = rect.height;

    canvas.width = Math.round(W * dpr);
    canvas.height = Math.round(H * dpr);

    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    ground = H * 0.79;

    player.x = Math.max(45, W * 0.13);

    makeWorld();
}


function makeWorld() {

    stars = Array.from({ length: 110 }, () => ({
        x: Math.random() * W,
        y: Math.random() * H * 0.58,
        r: Math.random() * 1.5 + 0.25,
        a: Math.random() * 0.65 + 0.15,
        tw: Math.random() * 5
    }));

    buildings = [];

    let x = -5;

    while (x < W + 100) {

        const w = 18 + Math.random() * 55;
        const h = 35 + Math.random() * H * 0.25;

        buildings.push({
            x,
            w,
            h,
            seed: Math.random()
        });

        x += w + 5;
    }
}


function drawBackground(t) {

    // Cinematic night sky

    const sky = ctx.createLinearGradient(0, 0, 0, H);

    sky.addColorStop(0, "#050813");
    sky.addColorStop(0.55, "#10172b");
    sky.addColorStop(1, "#241329");

    ctx.fillStyle = sky;
    ctx.fillRect(0, 0, W, H);


    // Glowing eclipse

    const mx = W * 0.72;
    const my = H * 0.35;
    const mr = Math.min(W, H) * 0.105;

    const glow = ctx.createRadialGradient(
        mx, my, mr * 0.15,
        mx, my, mr * 2.5
    );

    glow.addColorStop(0, "rgba(255,71,126,.2)");
    glow.addColorStop(1, "rgba(255,71,126,0)");

    ctx.fillStyle = glow;

    ctx.fillRect(
        mx - mr * 2.5,
        my - mr * 2.5,
        mr * 5,
        mr * 5
    );

    ctx.save();

    ctx.shadowBlur = 35;
    ctx.shadowColor = "#ff477e";
    ctx.fillStyle = "#f5a4bd";

    ctx.beginPath();
    ctx.arc(mx, my, mr, 0, Math.PI * 2);
    ctx.fill();

    ctx.restore();

    ctx.fillStyle = "#11172a";

    ctx.beginPath();
    ctx.arc(
        mx + mr * 0.28,
        my - mr * 0.16,
        mr * 0.94,
        0,
        Math.PI * 2
    );

    ctx.fill();


    // Stars

    stars.forEach(s => {

        ctx.globalAlpha =
            s.a * (0.75 + 0.25 * Math.sin(t * 0.001 + s.tw));

        ctx.fillStyle = "#d6faff";

        ctx.fillRect(s.x, s.y, s.r, s.r);

    });

    ctx.globalAlpha = 1;


    // Futuristic city skyline

    buildings.forEach((b, i) => {

        ctx.fillStyle =
            i % 3 === 0 ? "#101a2b" : "#0a1120";

        ctx.fillRect(
            b.x,
            ground - b.h,
            b.w,
            b.h
        );

        ctx.fillStyle = "rgba(109,247,255,.28)";

        for (
            let yy = ground - b.h + 10;
            yy < ground - 8;
            yy += 12
        ) {

            for (
                let xx = b.x + 6;
                xx < b.x + b.w - 4;
                xx += 10
            ) {

                if (Math.sin(xx * 3 + yy + b.seed * 20) > 0.45) {

                    ctx.fillRect(xx, yy, 2, 3);

                }

            }

        }

    });


    // Horizon fog

    const fog = ctx.createLinearGradient(
        0, ground - H * 0.22,
        0, ground + 12
    );

    fog.addColorStop(0, "rgba(255,71,126,0)");
    fog.addColorStop(1, "rgba(255,71,126,.18)");

    ctx.fillStyle = fog;
    ctx.fillRect(0, ground - H * 0.25, W, H * 0.28);


    // Glowing horizon

    ctx.strokeStyle = "rgba(109,247,255,.55)";
    ctx.lineWidth = 1;

    ctx.beginPath();
    ctx.moveTo(0, ground);
    ctx.lineTo(W, ground);
    ctx.stroke();


    // Perspective grid

    ctx.save();

    ctx.beginPath();
    ctx.rect(0, ground, W, H - ground);
    ctx.clip();

    const gridH = H - ground;

    for (let i = 0; i < 14; i++) {

        const p = (
            i / 14 + (t * 0.00012 * speed / 330)
        ) % 1;

        const y = ground + Math.pow(p, 2) * gridH;

        ctx.strokeStyle = `rgba(109,247,255,${0.04 + p * 0.16})`;

        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(W, y);
        ctx.stroke();

    }

    const offset = (t * 0.07 * speed / 330) % 100;

    for (let x = -W; x < W * 2; x += 100) {

        ctx.strokeStyle = "rgba(109,247,255,.12)";

        ctx.beginPath();

        ctx.moveTo(
            W / 2 + (x - W / 2) * 0.02,
            ground
        );

        ctx.lineTo(x - offset, H);

        ctx.stroke();

    }

    ctx.restore();


    // Dark foreground

    const g = ctx.createLinearGradient(0, ground, 0, H);

    g.addColorStop(0, "rgba(5,10,20,.05)");
    g.addColorStop(1, "rgba(2,4,10,.95)");

    ctx.fillStyle = g;
    ctx.fillRect(0, ground, W, H - ground);

}


function drawDino() {

    const x = player.x;
    const y = player.y;
    const h = player.h;

    ctx.save();

    ctx.translate(x, y);

    const bob = player.onGround && running
        ? Math.sin(player.runTime * 18) * 2
        : 0;

    ctx.translate(0, bob);

    ctx.shadowBlur = 18;
    ctx.shadowColor = "#6df7ff";

    ctx.fillStyle = "#bdfcff";
    ctx.strokeStyle = "#6df7ff";
    ctx.lineWidth = 1.5;


    // Tail

    ctx.beginPath();
    ctx.moveTo(7, h - 17);
    ctx.lineTo(-7, h - 11);
    ctx.lineTo(3, h - 7);
    ctx.lineTo(14, h - 11);
    ctx.closePath();
    ctx.fill();


    // Body

    ctx.beginPath();
    ctx.roundRect(7, h - 30, 25, 20, 5);
    ctx.fill();


    // Neck

    ctx.beginPath();
    ctx.moveTo(23, h - 25);
    ctx.lineTo(23, h - 43);
    ctx.lineTo(34, h - 43);
    ctx.lineTo(34, h - 25);
    ctx.closePath();
    ctx.fill();


    // Head

    ctx.beginPath();
    ctx.roundRect(24, h - 52, 23, 18, 5);
    ctx.fill();


    // Snout

    ctx.beginPath();
    ctx.moveTo(40, h - 43);
    ctx.lineTo(52, h - 39);
    ctx.lineTo(46, h - 33);
    ctx.lineTo(36, h - 34);
    ctx.closePath();
    ctx.fill();


    // Eye

    ctx.shadowBlur = 0;
    ctx.fillStyle = "#07101b";

    ctx.beginPath();
    ctx.arc(39, h - 46, 2, 0, Math.PI * 2);
    ctx.fill();


    // Arms

    ctx.strokeStyle = "#bdfcff";
    ctx.lineWidth = 3;

    ctx.beginPath();
    ctx.moveTo(27, h - 27);
    ctx.lineTo(34, h - 23);
    ctx.stroke();


    // Animated legs

    const step = player.onGround && running
        ? Math.sin(player.runTime * 18) * 7
        : 0;

    ctx.strokeStyle = "#bdfcff";
    ctx.lineWidth = 5;
    ctx.lineCap = "round";

    ctx.beginPath();
    ctx.moveTo(13, h - 12);
    ctx.lineTo(12 + step, h - 2);
    ctx.lineTo(5 + step, h - 2);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(27, h - 12);
    ctx.lineTo(28 - step, h - 2);
    ctx.lineTo(36 - step, h - 2);
    ctx.stroke();

    ctx.restore();


    // Ground shadow

    ctx.fillStyle = "rgba(109,247,255,.18)";

    ctx.beginPath();

    ctx.ellipse(
        x + 22,
        ground + 3,
        30,
        4,
        0,
        0,
        Math.PI * 2
    );

    ctx.fill();

}


function drawObstacle(o) {

    ctx.save();

    ctx.translate(o.x, o.y);

    ctx.shadowBlur = 14;
    ctx.shadowColor = "#ff477e";

    ctx.strokeStyle = "#ff6e96";
    ctx.fillStyle = "rgba(255,71,126,.18)";
    ctx.lineWidth = 2;


    // Glowing crystal obstacle

    if (o.type === 0) {

        ctx.beginPath();

        ctx.moveTo(0, o.h);
        ctx.lineTo(3, 8);
        ctx.lineTo(o.w * 0.45, 0);
        ctx.lineTo(o.w * 0.55, o.h * 0.48);
        ctx.lineTo(o.w - 2, 10);
        ctx.lineTo(o.w, o.h);

        ctx.closePath();
        ctx.fill();
        ctx.stroke();

        ctx.strokeStyle = "rgba(255,180,200,.7)";

        ctx.beginPath();
        ctx.moveTo(o.w * 0.25, o.h * 0.55);
        ctx.lineTo(o.w * 0.75, o.h * 0.55);
        ctx.stroke();

    } else {

        // Futuristic block

        ctx.beginPath();

        ctx.moveTo(0, o.h);
        ctx.lineTo(0, 18);
        ctx.lineTo(o.w * 0.28, 18);
        ctx.lineTo(o.w * 0.28, 0);
        ctx.lineTo(o.w * 0.72, 0);
        ctx.lineTo(o.w * 0.72, 26);
        ctx.lineTo(o.w, 26);
        ctx.lineTo(o.w, o.h);

        ctx.closePath();
        ctx.fill();
        ctx.stroke();

    }

    ctx.restore();

}


function spawnObstacle() {

    const tall = Math.random() > 0.35;
    const h = tall ? 34 + Math.random() * 24 : 25;

    obstacles.push({

        x: W + 35,
        y: ground - h,
        w: tall ? 25 + Math.random() * 12 : 30,
        h: h,
        type: Math.random() > 0.3 ? 0 : 1

    });

}


function burst(x, y) {

    for (let i = 0; i < 28; i++) {

        particles.push({

            x,
            y,

            vx: (Math.random() - 0.5) * 360,
            vy: (Math.random() - 0.6) * 320,

            life: 0.5 + Math.random() * 0.6,
            max: 0.9,
            size: 1 + Math.random() * 3

        });

    }

}


function start() {

    score = 0;
    speed = 330;
    spawn = 0.8;

    obstacles = [];
    particles = [];

    player.y = ground - player.h;
    player.vy = 0;
    player.onGround = true;
    player.runTime = 0;

    running = true;
    started = true;
    dead = false;

    last = performance.now();

    intro.classList.add("hidden");

    bottom.style.opacity = 0;
    bottom.style.pointerEvents = "none";

    overlay.classList.remove("show");

    requestAnimationFrame(loop);

}


function jump() {

    if (running && player.onGround) {

        player.vy = -Math.min(690, H * 0.95);

        player.onGround = false;

    }

}


function endGame() {

    running = false;
    dead = true;
    shake = 12;

    burst(player.x + 25, player.y + 25);

    const final = Math.floor(score);

    if (final > best) {

        best = final;

        localStorage.setItem("nocturne-best", best);

    }

    bestEl.textContent = String(best).padStart(5, "0");

    finalScore.textContent = String(final).padStart(5, "0");

    overlay.classList.add("show");

}


function update(dt) {

    score += dt * speed * 0.055;

    speed = Math.min(720, 330 + score * 0.7);

    scoreEl.textContent = String(
        Math.floor(score)
    ).padStart(5, "0");

    progress.style.width = (score % 1000) / 10 + "%";


    // Gravity and jumping

    player.runTime += dt;

    player.vy += 1550 * dt;
    player.y += player.vy * dt;

    if (player.y >= ground - player.h) {

        player.y = ground - player.h;
        player.vy = 0;
        player.onGround = true;

    }


    // Create new obstacles

    spawn -= dt;

    if (spawn <= 0) {

        spawnObstacle();

        spawn = Math.max(
            0.56,
            1.2 - Math.random() * 0.28 - score * 0.0005
        );

    }


    // Move obstacles

    obstacles.forEach(o => {

        o.x -= speed * dt;

    });

    obstacles = obstacles.filter(o => o.x + o.w > -10);


    // Collision detection

    const px = player.x + 7;
    const py = player.y + 7;
    const pw = player.w - 12;
    const ph = player.h - 9;

    for (const o of obstacles) {

        if (
            px < o.x + o.w - 3 &&
            px + pw > o.x + 3 &&
            py < o.y + o.h - 2 &&
            py + ph > o.y + 3
        ) {

            endGame();
            break;

        }

    }


    // Particle effects

    particles.forEach(p => {

        p.x += p.vx * dt;
        p.y += p.vy * dt;

        p.vy += 450 * dt;
        p.life -= dt;

    });

    particles = particles.filter(p => p.life > 0);

}


function render(t) {

    ctx.save();

    if (shake > 0) {

        ctx.translate(
            (Math.random() - 0.5) * shake,
            (Math.random() - 0.5) * shake
        );

        shake *= 0.86;

    }


    drawBackground(t);

    obstacles.forEach(drawObstacle);

    if (started && !dead) {

        drawDino();

    } else {

        player.y = ground - player.h;
        drawDino();

    }


    // Glowing particles

    particles.forEach(p => {

        ctx.globalAlpha = Math.max(0, p.life / p.max);

        ctx.fillStyle = "#6df7ff";
        ctx.shadowBlur = 10;
        ctx.shadowColor = "#6df7ff";

        ctx.fillRect(p.x, p.y, p.size, p.size);

    });

    ctx.globalAlpha = 1;


    // Cinematic speed streaks

    if (running) {

        for (let i = 0; i < 5; i++) {

            const x = (
                (t * 0.55 + i * W / 5) % (W + 100)
            ) - 50;

            ctx.strokeStyle = "rgba(109,247,255,.13)";

            ctx.beginPath();
            ctx.moveTo(x, H * 0.15 + i * 20);
            ctx.lineTo(x - 28, H * 0.15 + i * 20);
            ctx.stroke();

        }

    }

    ctx.restore();

}


function loop(now) {

    if (!running) return;

    const dt = Math.min((now - last) / 1000, 0.035);

    last = now;

    update(dt);
    render(now);

    if (running) {

        requestAnimationFrame(loop);

    } else {

        render(now);

    }

}


function idle(now) {

    if (!running) {

        render(now);

        requestAnimationFrame(idle);

    }

}


// Buttons

document.getElementById("startBtn").addEventListener(
    "click",
    start
);

document.getElementById("retryBtn").addEventListener(
    "click",
    start
);


// Keyboard controls

window.addEventListener("keydown", e => {

    if (["Space", "ArrowUp"].includes(e.code)) {

        e.preventDefault();

        if (!started || dead) {

            start();

        } else {

            jump();

        }

    }

    if (e.key.toLowerCase() === "r") {

        start();

    }

});


// Mouse and touch controls

canvas.addEventListener("pointerdown", () => {

    if (!started || dead) {

        start();

    } else {

        jump();

    }

});


window.addEventListener("resize", resize);

resize();

player.y = ground - player.h;

requestAnimationFrame(idle);

</script>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(PAGE)


@app.route("/api/status")
def status():
    return jsonify({
        "game": "NOCTURNE",
        "status": "online",
        "controls": ["Space", "ArrowUp", "R"]
    })


if __name__ == "__main__":
    app.run(debug=True)
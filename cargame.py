
from flask import Flask, render_template_string

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Ultimate Supercar Racing</title>

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    overflow: hidden;
    background: #050811;
    font-family: Arial, sans-serif;
    color: white;
}

canvas {
    display: block;
}

#hud {
    position: absolute;
    top: 20px;
    left: 20px;
    right: 20px;
    display: flex;
    justify-content: space-between;
    pointer-events: none;
    gap: 10px;
}

.panel {
    background: rgba(5, 12, 25, .82);
    border: 1px solid #344b64;
    padding: 15px 22px;
    border-radius: 12px;
    backdrop-filter: blur(10px);
}

.panel h2 {
    font-size: 12px;
    color: #69dfff;
    margin-bottom: 7px;
}

.panel p {
    font-size: 19px;
    font-weight: bold;
}

#level {
    color: #ffb72b;
}

#instructions {
    position: absolute;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(0,0,0,.8);
    padding: 12px 25px;
    border-radius: 10px;
    text-align: center;
    color: #c7d8e9;
    width: max-content;
    max-width: 95%;
}

#message {
    position: absolute;
    inset: 0;
    background: rgba(0,0,0,.82);
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    z-index: 10;
}

.message-box {
    background: #111e30;
    padding: 40px;
    border: 1px solid #42cfff;
    border-radius: 20px;
    width: 360px;
    max-width: 90%;
}

.message-box h1 {
    color: #4edaff;
    margin-bottom: 15px;
}

button {
    background: linear-gradient(90deg,#00aaff,#0066ff);
    color: white;
    border: none;
    padding: 14px 35px;
    border-radius: 8px;
    margin-top: 20px;
    cursor: pointer;
    font-weight: bold;
    font-size: 16px;
}

#progress {
    width: 160px;
    height: 7px;
    background: #26384d;
    border-radius: 10px;
    margin-top: 8px;
    overflow: hidden;
}

#bar {
    height: 100%;
    width: 0%;
    background: #00d9ff;
}

#mobileControls {
    display: none;
    position: absolute;
    bottom: 85px;
    left: 0;
    right: 0;
    justify-content: space-between;
    padding: 0 25px;
}

#mobileControls button {
    width: 65px;
    height: 55px;
    padding: 0;
    margin: 0;
    background: #102c47;
}

@media(max-width:700px) {
    #hud { top: 8px; left: 8px; right: 8px; }
    .panel { padding: 9px; }
    .panel p { font-size: 14px; }
    .panel h2 { font-size: 9px; }
    #mobileControls { display: flex; }
    #instructions { bottom: 10px; font-size: 11px; }
}
</style>
</head>

<body>

<div id="hud">
    <div class="panel">
        <h2>SUPER CAR RACING</h2>
        <p id="level">LEVEL 1</p>
    </div>

    <div class="panel">
        <h2>SPEED</h2>
        <p><span id="speed">0</span> KM/H</p>
    </div>

    <div class="panel">
        <h2>DISTANCE</h2>
        <p><span id="distance">0</span> M</p>
    </div>

    <div class="panel">
        <h2>ENVIRONMENT</h2>
        <p id="environment">SNOW</p>
        <div id="progress"><div id="bar"></div></div>
    </div>
</div>

<div id="instructions">
    USE ← → OR A / D TO STEER |
    W / ↑ TO ACCELERATE |
    S / ↓ TO BRAKE
</div>

<div id="mobileControls">
    <button id="left">◀</button>
    <button id="right">▶</button>
</div>

<div id="message">
    <div class="message-box">
        <h1 id="title">ULTIMATE SUPERCAR</h1>
        <p id="description">
            Experience the ultimate 3D racing adventure.
            <br><br>
            Three levels. Three environments.
            Only supercars.
        </p>
        <button id="start">START RACING</button>
    </div>
</div>

<script type="importmap">
{
    "imports": {
        "three": "https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js"
    }
}
</script>

<script type="module">

import * as THREE from 'three';
import { GLTFLoader } from
'https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/loaders/GLTFLoader.js';

// ----------------------------------
// GAME CONFIGURATION
// ----------------------------------

const scene = new THREE.Scene();

scene.background = new THREE.Color(0x9cc9df);
scene.fog = new THREE.Fog(0x9cc9df, 35, 160);

const camera = new THREE.PerspectiveCamera(
    65,
    window.innerWidth / window.innerHeight,
    0.1,
    500
);

camera.position.set(0, 7, 13);
camera.lookAt(0, 1, -5);

const renderer = new THREE.WebGLRenderer({
    antialias: true
});

renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

document.body.appendChild(renderer.domElement);

// ----------------------------------
// LIGHTING
// ----------------------------------

const ambient = new THREE.HemisphereLight(
    0xffffff, 0x46515c, 2
);

scene.add(ambient);

const sunlight = new THREE.DirectionalLight(
    0xffffff, 3
);

sunlight.position.set(-10, 20, 10);
sunlight.castShadow = true;
scene.add(sunlight);

// ----------------------------------
// GAME VARIABLES
// ----------------------------------

let gameRunning = false;
let gameOver = false;

let level = 1;
let distance = 0;
let speed = 0;
let score = 0;

let maxSpeed = 35;
let roadSpeed = 25;

let playerX = 0;
let targetX = 0;

let currentEnvironment = "SNOW";

const keys = {};

const obstacles = [];
const roadSegments = [];
const scenery = [];

const loader = new GLTFLoader();

let playerCar;

// ----------------------------------
// CREATE MATERIALS
// ----------------------------------

function material(color, metalness=0, roughness=.5) {

    return new THREE.MeshStandardMaterial({
        color,
        metalness,
        roughness
    });

}

// ----------------------------------
// CREATE SUPERCAR
// ----------------------------------

function createSupercar(color, levelNumber) {

    const car = new THREE.Group();

    const bodyMaterial = material(color, .8, .2);
    const black = material(0x10141d, .4, .25);
    const glass = new THREE.MeshPhysicalMaterial({
        color: 0x152e46,
        metalness: .7,
        roughness: .12,
        transparent: true,
        opacity: .85
    });

    // Main body

    const body = new THREE.Mesh(
        new THREE.BoxGeometry(2, .55, 4),
        bodyMaterial
    );

    body.position.y = .8;
    body.castShadow = true;
    car.add(body);

    // Front bonnet

    const bonnet = new THREE.Mesh(
        new THREE.BoxGeometry(1.9, .2, 1.1),
        bodyMaterial
    );

    bonnet.position.set(0, 1.1, -1.35);
    car.add(bonnet);

    // Cabin

    const cabin = new THREE.Mesh(
        new THREE.BoxGeometry(1.45, .7, 1.8),
        glass
    );

    cabin.position.set(0, 1.35, .15);
    cabin.castShadow = true;
    car.add(cabin);

    // Rear spoiler

    const spoiler = new THREE.Mesh(
        new THREE.BoxGeometry(2.2, .12, .35),
        black
    );

    spoiler.position.set(0, 1.25, 1.9);
    car.add(spoiler);

    // Wheels

    const wheels = [];

    for (let x of [-1.05, 1.05]) {
        for (let z of [-1.35, 1.35]) {

            const wheel = new THREE.Mesh(
                new THREE.CylinderGeometry(.42,.42,.3,24),
                black
            );

            wheel.rotation.z = Math.PI / 2;
            wheel.position.set(x,.45,z);

            wheel.castShadow = true;
            car.add(wheel);

            wheels.push(wheel);
        }
    }

    // Headlights

    for (let x of [-.7,.7]) {

        const light = new THREE.Mesh(
            new THREE.BoxGeometry(.4,.15,.08),
            new THREE.MeshBasicMaterial({
                color: 0x9ffcff
            })
        );

        light.position.set(x,.95,-2.03);
        car.add(light);

    }

    car.userData.wheels = wheels;

    // Upgrade visual features

    if(levelNumber >= 2) {

        const stripe = new THREE.Mesh(
            new THREE.BoxGeometry(.22,.025,3.5),
            material(0xffffff,.3,.2)
        );

        stripe.position.set(0,1.09,0);
        car.add(stripe);

    }

    if(levelNumber >= 3) {

        const wing = new THREE.Mesh(
            new THREE.BoxGeometry(2.6,.12,.4),
            material(0xffcc00,.8,.2)
        );

        wing.position.set(0,1.8,1.7);
        car.add(wing);

    }

    return car;

}

// ----------------------------------
// LOAD BLENDER MODEL
// ----------------------------------

function loadCarModel(levelNumber, color) {

    if(playerCar) {
        scene.remove(playerCar);
    }

    const colors = [0xff2020,0xff7b00,0x101820];

    const fallback = createSupercar(
        colors[levelNumber-1],
        levelNumber
    );

    fallback.position.set(0,0,5);
    scene.add(fallback);

    playerCar = fallback;

    const paths = [
        "/static/cars/level1.glb",
        "/static/cars/level2.glb",
        "/static/cars/level3.glb"
    ];

    loader.load(
        paths[levelNumber-1],

        function(gltf) {

            if(!gameRunning && !playerCar) return;

            scene.remove(playerCar);

            const model = gltf.scene;

            model.scale.set(1,1,1);
            model.position.set(0,0,5);

            model.traverse(function(child) {
                if(child.isMesh) {
                    child.castShadow = true;
                    child.receiveShadow = true;
                }
            });

            scene.add(model);
            playerCar = model;

        },

        undefined,

        function() {
            // Built-in 3D car remains active
        }
    );

}

// ----------------------------------
// ROAD
// ----------------------------------

function createRoadSegment(z, type) {

    const group = new THREE.Group();

    let groundColor;

    if(type === "SNOW") groundColor = 0xe7f4ff;
    if(type === "MUD") groundColor = 0x55402a;
    if(type === "HIGHWAY") groundColor = 0x262a32;

    const ground = new THREE.Mesh(
        new THREE.BoxGeometry(12,.2,45),
        material(groundColor)
    );

    ground.position.y = -.15;
    ground.receiveShadow = true;
    group.add(ground);

    // Road surface

    const roadColor =
        type === "SNOW" ? 0xd7e6ee :
        type === "MUD" ? 0x79583a :
        0x171a21;

    const road = new THREE.Mesh(
        new THREE.BoxGeometry(9,.15,45),
        material(roadColor)
    );

    road.position.y = 0;
    road.receiveShadow = true;
    group.add(road);

    // Road markings

    for(let zPos=-20; zPos<22; zPos+=8) {

        const line = new THREE.Mesh(
            new THREE.BoxGeometry(.12,.025,3),
            material(0xffffff)
        );

        line.position.set(0,.1,zPos);
        group.add(line);

    }

    group.position.z = z;
    scene.add(group);

    roadSegments.push(group);

}

// ----------------------------------
// ENVIRONMENT
// ----------------------------------

function getEnvironment() {

    const segment = Math.floor(distance / 300) % 3;

    if(segment === 0) return "SNOW";
    if(segment === 1) return "MUD";

    return "HIGHWAY";

}

function updateEnvironment() {

    const env = getEnvironment();

    if(env === currentEnvironment) return;

    currentEnvironment = env;

    document.getElementById("environment").innerText = env;

    if(env === "SNOW") {

        scene.background.set(0x9cc9df);
        scene.fog.color.set(0x9cc9df);

    }

    if(env === "MUD") {

        scene.background.set(0x65513d);
        scene.fog.color.set(0x65513d);

    }

    if(env === "HIGHWAY") {

        scene.background.set(0x111b2d);
        scene.fog.color.set(0x111b2d);

    }

    // Rebuild road segments

    roadSegments.forEach(segment => {
        scene.remove(segment);
    });

    roadSegments.length = 0;

    for(let i=0;i<5;i++) {

        createRoadSegment(
            -i*45,
            env
        );

    }

}

// ----------------------------------
// OBSTACLES
// ----------------------------------

function createObstacle() {

    const group = new THREE.Group();

    const box = new THREE.Mesh(
        new THREE.BoxGeometry(1.4,1.3,1.4),
        material(
            currentEnvironment === "SNOW"
            ? 0x9bdcff
            : currentEnvironment === "MUD"
            ? 0x8d4d24
            : 0xff3030
        )
    );

    box.position.y = .7;
    group.add(box);

    group.position.set(
        [-3,0,3][Math.floor(Math.random()*3)],
        0,
        -120
    );

    scene.add(group);

    obstacles.push(group);

}

// ----------------------------------
// SCENERY
// ----------------------------------

function createTree(x,z) {

    const tree = new THREE.Group();

    const trunk = new THREE.Mesh(
        new THREE.CylinderGeometry(.15,.25,2,8),
        material(0x50351f)
    );

    trunk.position.y = 1;
    tree.add(trunk);

    const leaves = new THREE.Mesh(
        new THREE.ConeGeometry(1.2,3,8),
        material(
            currentEnvironment === "SNOW"
            ? 0xe8f5ff
            : 0x17632e
        )
    );

    leaves.position.y = 3;
    tree.add(leaves);

    tree.position.set(x,0,z);

    scene.add(tree);
    scenery.push(tree);

}

// ----------------------------------
// INITIALIZE WORLD
// ----------------------------------

for(let i=0;i<5;i++) {

    createRoadSegment(-i*45,"SNOW");

}

for(let i=0;i<15;i++) {

    createTree(-9, -i*12);
    createTree(9, -i*12);

}

// ----------------------------------
// LEVEL SYSTEM
// ----------------------------------

function updateLevel() {

    let newLevel = 1;

    if(distance >= 500) newLevel = 2;
    if(distance >= 1000) newLevel = 3;

    if(newLevel !== level) {

        level = newLevel;

        if(level === 1) {
            maxSpeed = 35;
        }

        if(level === 2) {
            maxSpeed = 55;
        }

        if(level === 3) {
            maxSpeed = 80;
        }

        loadCarModel(level);

        document.getElementById("level").innerText =
            "LEVEL " + level;

        document.getElementById("title").innerText =
            "LEVEL " + level + " UNLOCKED!";

        document.getElementById("description").innerText =
            level === 2
            ? "Performance Supercar unlocked! More speed awaits."
            : "ULTIMATE HYPERCAR unlocked! Maximum power!";

        document.getElementById("message").style.display = "flex";

        gameRunning = false;

        document.getElementById("start").innerText =
            "CONTINUE RACING";

    }

}

// ----------------------------------
// COLLISION
// ----------------------------------

function checkCollision() {

    if(!playerCar) return;

    for(const obstacle of obstacles) {

        const dx = Math.abs(playerCar.position.x -
                            obstacle.position.x);

        const dz = Math.abs(playerCar.position.z -
                            obstacle.position.z);

        if(dx < 1.45 && dz < 2.1) {

            endGame();

        }

    }

}

// ----------------------------------
// GAME OVER
// ----------------------------------

function endGame() {

    gameRunning = false;
    gameOver = true;

    document.getElementById("title").innerText =
        "RACE OVER!";

    document.getElementById("description").innerHTML =
        "Your score: " + Math.floor(distance) +
        " meters<br>Level reached: " + level;

    document.getElementById("start").innerText =
        "RESTART GAME";

    document.getElementById("message").style.display =
        "flex";

}

// ----------------------------------
// RESET GAME
// ----------------------------------

function resetGame() {

    obstacles.forEach(o => scene.remove(o));
    obstacles.length = 0;

    level = 1;
    distance = 0;
    speed = 0;
    score = 0;

    maxSpeed = 35;
    playerX = 0;
    targetX = 0;

    currentEnvironment = "SNOW";

    loadCarModel(1);

    updateEnvironment();

    gameOver = false;
    gameRunning = true;

    document.getElementById("message").style.display =
        "none";

    document.getElementById("level").innerText =
        "LEVEL 1";

}

// ----------------------------------
// INPUT CONTROLS
// ----------------------------------

window.addEventListener("keydown", e => {

    keys[e.key.toLowerCase()] = true;

});

window.addEventListener("keyup", e => {

    keys[e.key.toLowerCase()] = false;

});

document.getElementById("left").addEventListener(
    "touchstart", e => {
        e.preventDefault();
        targetX = Math.max(-3,targetX-3);
    }
);

document.getElementById("right").addEventListener(
    "touchstart", e => {
        e.preventDefault();
        targetX = Math.min(3,targetX+3);
    }
);

document.getElementById("start").addEventListener(
    "click", () => {

        if(gameOver) {
            resetGame();
        } else {
            gameRunning = true;
            document.getElementById("message").style.display =
                "none";
        }

    }
);

// ----------------------------------
// MAIN GAME LOOP
// ----------------------------------

let lastObstacle = 0;

function animate() {

    requestAnimationFrame(animate);

    const delta = Math.min(clock.getDelta(), .05);

    if(gameRunning) {

        // Acceleration and braking

        if(keys["w"] || keys["arrowup"]) {
            speed += 25 * delta;
        } else {
            speed -= 8 * delta;
        }

        if(keys["s"] || keys["arrowdown"]) {
            speed -= 45 * delta;
        }

        speed = THREE.MathUtils.clamp(
            speed,0,maxSpeed
        );

        roadSpeed = 18 + speed * .6;

        // Steering

        if(keys["a"] || keys["arrowleft"]) {
            targetX -= 7 * delta;
        }

        if(keys["d"] || keys["arrowright"]) {
            targetX += 7 * delta;
        }

        targetX = THREE.MathUtils.clamp(
            targetX,-3,3
        );

        playerX = THREE.MathUtils.lerp(
            playerX,targetX,5*delta
        );

        if(playerCar) {

            playerCar.position.x = playerX;

            playerCar.position.y =
                Math.sin(performance.now()*.01)*.025;

            if(playerCar.userData.wheels) {
                playerCar.userData.wheels.forEach(w => {
                    w.rotation.x += speed*delta*.08;
                });
            }

        }

        // Camera follows car

        camera.position.x = THREE.MathUtils.lerp(
            camera.position.x,playerX*.3,2*delta
        );

        // Move road

        roadSegments.forEach(segment => {

            segment.position.z += roadSpeed*delta;

            if(segment.position.z > 45) {
                segment.position.z -= 225;
            }

        });

        // Move scenery

        scenery.forEach(tree => {

            tree.position.z += roadSpeed*delta;

            if(tree.position.z > 15) {
                tree.position.z = -160;
            }

        });

        // Spawn obstacles

        lastObstacle += delta;

        if(lastObstacle > 1.7) {
            createObstacle();
            lastObstacle = 0;
        }

        // Move obstacles

        for(let i=obstacles.length-1;i>=0;i--) {

            const obstacle = obstacles[i];

            obstacle.position.z += roadSpeed*delta;

            if(obstacle.position.z > 15) {

                scene.remove(obstacle);
                obstacles.splice(i,1);

                score += 10;

            }

        }

        checkCollision();

        // Distance

        distance += speed * delta * .4;

        updateLevel();
        updateEnvironment();

        // HUD

        document.getElementById("speed").innerText =
            Math.floor(speed*4);

        document.getElementById("distance").innerText =
            Math.floor(distance);

        document.getElementById("bar").style.width =
            (distance % 500 / 500 * 100) + "%";

    }

    renderer.render(scene,camera);

}

const clock = new THREE.Clock();

animate();

// ----------------------------------
// RESPONSIVE SCREEN
// ----------------------------------

window.addEventListener("resize", () => {

    camera.aspect =
        window.innerWidth/window.innerHeight;

    camera.updateProjectionMatrix();

    renderer.setSize(
        window.innerWidth,
        window.innerHeight
    );

});

</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)

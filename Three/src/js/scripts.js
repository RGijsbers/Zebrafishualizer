// Import modules
import * as THREE from 'three';
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls.js';
import * as dat from 'dat.gui';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
// Import objects
const loader = new GLTFLoader();
const monkeyUrl = new URL('../assets/monkey.glb', import.meta.url);

// Create basic scene elements
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(
    45,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
);
camera.position.set(-10, 30, 30);

const orbit = new OrbitControls(camera, renderer.domElement);
orbit.update();

// Create helpers
const axesHelper = new THREE.AxesHelper(5);
scene.add(axesHelper);
const gridHelper = new THREE.GridHelper(30);
scene.add(gridHelper);


// Main body
loader.load(monkeyUrl.href,  //aanpassen naar juiste object
    function(gltf){
        const model = gltf.scene;
        scene.add(model);
        model.position.set(-12, 4, 10);
    }, undefined, function(error){
    console.error(error);
});


// // Create options gui
// const gui = new dat.GUI();
// const options = {

// };
// gui.add(options, ...);


// Animation loop
function animate(time) {
    renderer.render(scene, camera);
}
renderer.setAnimationLoop(animate);

// Update view when window is resized
window.addEventListener('resize', function() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});
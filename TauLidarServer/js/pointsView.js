import * as THREE from './three.module.js';
import { OrbitControls } from './OrbitControls.js';


// Scene
var scene = new THREE.Scene();


// Camera
var camera = new THREE.PerspectiveCamera(15, window.innerWidth / window.innerHeight, 1, 1000);
camera.position.set(0, 0, -5);


// The renderer
var renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);

// Render the scene
function render() {
    renderer.render(scene, camera);
}

// Setup controls
var controls = new OrbitControls(camera, renderer.domElement);
controls.addEventListener('change', render);


// Render loop
function animate() {
    requestAnimationFrame( animate );
    controls.update(); // only required if controls.enableDamping = true, or if controls.autoRotate = true
    render();
}

// Build the scene
var pointSize = 0.05;

var material = new THREE.PointsMaterial({size:pointSize, vertexColors:true})
var geometry = new THREE.Geometry({dynamic:true})
var pointcloud = new THREE.Points(geometry, material)


function buildScene() {

    if (scene.children.length === 0)
        scene.add(pointcloud)

    render();
}

var container = document.getElementById('pointsView');
container.appendChild(renderer.domElement);


window.ws.onmessage = function (event) {
    var points = JSON.parse(event.data);
    

    var colors = []
    var vertices = []
    var faces = []

    for(var i = 0; i < points.length; i++) {
        var point = points[i];
        var x = point[0];
        var y = point[1];
        var z = point[2];

        var r = point[3];
        var g = point[4];
        var b = point[5];
        var rgb_str = `rgb(${r}, ${g}, ${b})`

        vertices.push(new THREE.Vector3(x, y, z));
        colors.push(new THREE.Color(rgb_str));
    }

    geometry.vertices = vertices
    geometry.colors = colors

    geometry.verticesNeedUpdate = true
    geometry.colorsNeedUpdate = true
    
    buildScene()

};

render();
animate();

window.material = material
window.controls = controls
window.camera = camera
window.scene = scene
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
var geometry = new THREE.Geometry({dynamic:false})
var pointcloud = new THREE.Points(geometry, material)


function buildScene() {

    pointcloud = new THREE.Points(geometry, material)
    scene = new THREE.Scene();
    scene.add(pointcloud)

    render();
}

var container = document.getElementById('pointsView');
container.appendChild(renderer.domElement);


window.ws.onmessage = function (event) {
    var data = JSON.parse(event.data);
    var height = data.h
    var width = data.w

    if (data.points !== undefined) {
        var colors = []
        var vertices = []
    
        for(var i = 0; i < data.points.length; i++) {
            var point = data.points[i];
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

        geometry = new THREE.Geometry({dynamic:false})

        geometry.vertices = vertices
        geometry.colors = colors
    
        geometry.verticesNeedUpdate = true
        geometry.colorsNeedUpdate = true
        
        buildScene()
    }

    if (data.depth !== undefined) {

        var canvas = document.createElement('canvas')
        var context = canvas.getContext('2d')
        var imgData = context.createImageData(width, height)

        canvas.height = height;
        canvas.width = width;

        for (var i=0;i<imgData.data.length;i+=4) {
            imgData.data[i] = data.depth[i/4*3 + 2] // R
            imgData.data[i+1] = data.depth[i/4*3 + 1] // G
            imgData.data[i+2] = data.depth[i/4*3] // B

            imgData.data[i+3] = 255
        }

        context.putImageData(imgData, 0, 0)

        var imgSrc = canvas.toDataURL('image/png')

        document.getElementById("depthView").src = imgSrc
    }

    if (data.amplitude !== undefined) {


        var canvas = document.createElement('canvas')
        var context = canvas.getContext('2d')
        var imgData = context.createImageData(width, height)

        canvas.height = height;
        canvas.width = width;

        for (var i=0;i<imgData.data.length;i+=4) {
            imgData.data[i] = data.amplitude[i/4] // R
            imgData.data[i+1] = data.amplitude[i/4] // G
            imgData.data[i+2] = data.amplitude[i/4] // B
            imgData.data[i+3] = 255
        }

        context.putImageData(imgData, 0, 0)

        var imgSrc = canvas.toDataURL('image/png')

        document.getElementById("amplitudeView").src = imgSrc
    }
};

render();
animate();

window.material = material
window.controls = controls
window.camera = camera
window.scene = scene
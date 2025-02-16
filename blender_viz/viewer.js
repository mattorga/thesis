// Scene setup
const scene = new THREE.Scene();
scene.add(new THREE.AxesHelper(5));

const light = new THREE.PointLight(0xffffff, 1);
light.position.set(10, 10, 10);
scene.add(light);

const ambientLight = new THREE.AmbientLight(0x404040);
scene.add(ambientLight);

const camera = new THREE.PerspectiveCamera(
	75,
	window.innerWidth / window.innerHeight,
	0.1,
	1000
);
camera.position.set(2, 2, 5);

const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Orbit Controls
const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;

let mixer;
let clock = new THREE.Clock();
let duration = 0;

// Initial state
let isPlaying = false;
let centerAnimation = true;
let animatedObject; // Reference to the loaded object
let timeScaleBuffer = 1; // Buffer for timeScale

// Get references to the controls
const centerAnimationCheckbox = document.getElementById(
	"centerAnimationCheckbox"
);
const animationSpeedSelector = document.getElementById("animationSpeed");
const playPauseBtn = document.getElementById("playPause");
const rewindBtn = document.getElementById("rewind");
const forwardBtn = document.getElementById("forward");
const seekBar = document.getElementById("seekBar");

// Load FBX file
const loader = new THREE.FBXLoader();
loader.load(
	"http://localhost:8000/Users/mattheworga/Documents/Git/DLSU/thesis/blender_viz/untitled.fbx",
	(object) => {
		object.scale.set(0.01, 0.01, 0.01);

		if (centerAnimation) {
			// Compute the bounding box
			const box = new THREE.Box3().setFromObject(object);
			const center = box.getCenter(new THREE.Vector3());

			// Offset the model to center it at the origin
			object.position.sub(center);
		}

		scene.add(object);
		animatedObject = object; // Save reference for tracking

		// Create animation mixer
		mixer = new THREE.AnimationMixer(object);
		const action = mixer.clipAction(object.animations[0]);
		action.play();
		mixer.timeScale = 0; // Start animation paused

		// Get animation duration
		duration = object.animations[0].duration;

		// Update seekbar max value
		seekBar.max = duration.toFixed(2); // Max value with two decimal places
		seekBar.step = 0.01; // Granularity of 0.01 seconds

		// Listen for loop events to reset seekbar
		mixer.addEventListener("loop", () => {
			if (isPlaying) {
				seekBar.value = 0; // Reset seekbar position on loop
				mixer.setTime(0);
			}
		});
	},
	(xhr) => console.log((xhr.loaded / xhr.total) * 100 + "% loaded"),
	(error) => console.error(error)
);

// Resize handler
window.addEventListener("resize", () => {
	camera.aspect = window.innerWidth / window.innerHeight;
	camera.updateProjectionMatrix();
	renderer.setSize(window.innerWidth, window.innerHeight);
});

// Play/Pause functionality
playPauseBtn.addEventListener("click", () => {
	if (isPlaying) {
		mixer.timeScale = 0; // Pause animation
		isPlaying = false;
		playPauseBtn.textContent = "▶️";
	} else {
		mixer.timeScale = timeScaleBuffer; // Resume animation
		isPlaying = true;
		playPauseBtn.textContent = "⏸️";
	}
});

// Rewind functionality
rewindBtn.addEventListener("click", () => {
	if (mixer) {
		//console.log(`[Backward] Current mixer.time: ${mixer.time}, timeScale: ${timeScaleBuffer}`);

		if (isPlaying) {
			mixer.timeScale = 1; // resume animation temporarily, if i dont do this, weird things happen, dont ask me why
			mixer.setTime(Math.max(0, mixer.time - 1)); // Go back 1 second
			//console.log(`[Backward part2] Current mixer.time: ${mixer.time}, timeScale: ${timeScaleBuffer}`);

			seekBar.value = mixer.time; // Sync seekbar
			mixer.timeScale = timeScaleBuffer; // resume with the correct speed
		} else {
			mixer.timeScale = 1; // resume animation temporarily, if i dont do this, weird things happen, dont ask me why
			mixer.setTime(Math.max(0, mixer.time - 1)); // Go back 1 second
			seekBar.value = mixer.time; // Sync seekbar
			mixer.timeScale = 0; // Pause animation
		}
	}
});

// Forward functionality
forwardBtn.addEventListener("click", () => {
	if (mixer) {
		console.log(
			`[Forward] Current mixer.time: ${mixer.time}, timeScale: ${timeScaleBuffer}`
		);
		if (isPlaying) {
			mixer.timeScale = 1; // resume animation temporarily, if i dont do this, weird things happen, dont ask me why
			mixer.setTime(Math.min(duration, mixer.time + 1)); // Go forward 1 second
			seekBar.value = mixer.time; // Sync seekbar
			mixer.timeScale = timeScaleBuffer; // resume with the correct speed
		} else {
			mixer.timeScale = 1; // resume animation temporarily, if i dont do this, weird things happen, dont ask me why
			mixer.setTime(Math.min(duration, mixer.time + 1)); // Go forward 1 second
			seekBar.value = mixer.time; // Sync seekbar
			mixer.timeScale = 0; // Pause animation
		}
	}
});

// Seekbar functionality
seekBar.addEventListener("input", (e) => {
	let newTime = parseFloat(e.target.value); // Parse value with higher precision
	if (mixer) {
		switch (timeScaleBuffer) {
			case 0.25:
				console.log("Time scale is 0.25x");
				newTime = newTime * 4;
				break;
			case 0.5:
				console.log("Time scale is 0.5x");
				newTime = newTime * 2;
				break;
			case 1:
				console.log("Time scale is 1x (normal speed)");
				break;
			case 2:
				console.log("Time scale is 2x (double speed)");
				newTime = newTime / 2;
				break;
			default:
				console.log("Unknown time scale");
		}
		//console.log(`[Seekbar] Current mixer.time: ${mixer.time}, timeScale: ${timeScaleBuffer}, New Time: ${newTime}`);
		if (!isPlaying) {
			mixer.timeScale = timeScaleBuffer; // Resume animation temporarily
			mixer.setTime(newTime); // Update the animation time

			mixer.timeScale = 0; // Pause animation
		} else {
			mixer.setTime(newTime); // Update the animation time
		}
	}
});

// Center animation checkbox
centerAnimationCheckbox.addEventListener("change", () => {
	centerAnimation = centerAnimationCheckbox.checked;
});

// Update animation speed based on selector value
animationSpeedSelector.addEventListener("change", () => {
	const speed = parseFloat(animationSpeedSelector.value);
	timeScaleBuffer = speed;
	if (isPlaying) {
		mixer.timeScale = speed;
	}
});

// Create a raycaster and mouse vector
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
let highlightedBone = null;
const originalMaterials = new Map();
let lastClickTime = 0;

const jointInfoBox = document.getElementById("jointInfoBox");

function updateJointInfo() {
	if (highlightedBone && mixer) {
		let fps = 30;
		const currentFrame = Math.floor(mixer.time * fps);
		jointInfoBox.innerHTML = `Joint: <strong>${highlightedBone.name}</strong><br>Frame: <strong>${currentFrame}</strong>`;
		jointInfoBox.style.display = "block"; // Show info box
	} else {
		jointInfoBox.style.display = "none"; // Hide info box when no joint is selected
	}
}
function onClick(event) {
	const now = Date.now();
	const doubleClick = now - lastClickTime < 300; // Detect double click (300ms threshold)
	lastClickTime = now;

	mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
	mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
	raycaster.setFromCamera(mouse, camera);

	if (animatedObject) {
		const intersects = raycaster.intersectObject(animatedObject, true);

		if (intersects.length > 0) {
			const clickedBone = intersects[0].object;

			console.log("Clicked on:", clickedBone.name);

			// Remove previous highlight
			if (highlightedBone) {
				highlightedBone.material =
					originalMaterials.get(highlightedBone) || highlightedBone.material;
			}

			// Save original material
			if (!originalMaterials.has(clickedBone)) {
				originalMaterials.set(clickedBone, clickedBone.material);
			}

			// Apply highlight effect
			clickedBone.material = new THREE.MeshStandardMaterial({
				color: 0xff0000,
				emissive: 0x550000,
				wireframe: false,
			});

			highlightedBone = clickedBone;
			updateJointInfo(); // Update display immediately
		} else if (doubleClick) {
			// Remove highlight on double-click
			if (highlightedBone) {
				highlightedBone.material =
					originalMaterials.get(highlightedBone) || highlightedBone.material;
				highlightedBone = null;
				updateJointInfo(); // Clear display
			}
		}
	}
}

// Listen for mouse clicks
window.addEventListener("click", onClick);

// Animation loop
function animate() {
	requestAnimationFrame(animate);

	const delta = clock.getDelta();
	if (mixer) {
		mixer.update(delta);
		updateJointInfo();
		// Sync seekbar with animation time if playing
		if (isPlaying) {
			// const currentTime = mixer.time % duration; // Ensure time is within bounds
			// seekBar.value = currentTime.toFixed(2); // Update seekbar position
			const currentTime = (mixer.time % duration).toFixed(2); // Round to 2 decimal places
			seekBar.value = currentTime; // Update seekbar position

			//console.log(`[Animation Loop] Current mixer.time: ${mixer.time}, timeScale: ${timeScaleBuffer}`);
		}
	}

	const dampingFactor = 0.1; // Adjust for smoother or faster movement
	if (centerAnimation && animatedObject) {
		const box = new THREE.Box3().setFromObject(animatedObject);
		const center = box.getCenter(new THREE.Vector3());

		// Smoothly interpolate the camera's target
		controls.target.lerp(center, dampingFactor);
	}

	controls.update();
	renderer.render(scene, camera);
}

// Update joint info when playback controls are used
document.getElementById("playPause").addEventListener("click", updateJointInfo);
document.getElementById("rewind").addEventListener("click", updateJointInfo);
document.getElementById("forward").addEventListener("click", updateJointInfo);
document.getElementById("seekBar").addEventListener("input", updateJointInfo);
document.getElementById("replay").addEventListener("click", updateJointInfo);

// Start the animation
animate();

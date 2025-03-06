// Scene setup
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x2a2a2a);

// Set gray background
scene.background = new THREE.Color(0x888888);

// Add ambient light
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambientLight);

// Add directional light
const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
directionalLight.position.set(10, 10, 10);
directionalLight.castShadow = true;
scene.add(directionalLight);

// Add point light for additional detail
const light = new THREE.PointLight(0xffffff, 0.6);
light.position.set(-10, 15, 5);
scene.add(light);

// Camera setup
const camera = new THREE.PerspectiveCamera(
	45,
	window.innerWidth / window.innerHeight,
	0.1,
	1000
);
camera.position.set(-1, 1, 2);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
document.body.appendChild(renderer.domElement);

// Add tile floor
function createTileFloor() {
	const floorSize = 20;
	const tileSize = 1;
	const floorGeometry = new THREE.PlaneGeometry(
		floorSize,
		floorSize,
		floorSize,
		floorSize
	);

	// Create subtle checkerboard material
	const materials = [
		new THREE.MeshStandardMaterial({ color: 0xe0e0e0, roughness: 0.9 }),
		new THREE.MeshStandardMaterial({ color: 0xd0d0d0, roughness: 0.9 }),
	];

	// Assign materials to create checkerboard pattern
	const floor = new THREE.Mesh(floorGeometry, materials[0]);
	floor.rotation.x = -Math.PI / 2; // Rotate to be horizontal
	floor.position.y = -0.01; // Slightly below origin to avoid z-fighting
	floor.receiveShadow = true;

	// Create grid for checkerboard pattern (more subtle)
	const grid = new THREE.GridHelper(floorSize, floorSize, 0x000000, 0x000000);
	grid.position.y = 0;
	grid.material.opacity = 0.1; // Reduced opacity for subtlety
	grid.material.transparent = true;

	// Create tiled texture using a parent object
	const tiledFloor = new THREE.Group();
	tiledFloor.add(floor);
	tiledFloor.add(grid);

	// Create individual tiles with alternating colors
	for (
		let x = -floorSize / 2 + tileSize / 2;
		x < floorSize / 2;
		x += tileSize
	) {
		for (
			let z = -floorSize / 2 + tileSize / 2;
			z < floorSize / 2;
			z += tileSize
		) {
			// Determine if this should be a dark or light tile
			const isOffset =
				(Math.floor(x + floorSize / 2) + Math.floor(z + floorSize / 2)) % 2 ===
				0;
			const tileGeometry = new THREE.PlaneGeometry(
				tileSize - 0.05,
				tileSize - 0.05
			);
			const tileMaterial = materials[isOffset ? 1 : 0];
			const tile = new THREE.Mesh(tileGeometry, tileMaterial);

			tile.rotation.x = -Math.PI / 2;
			tile.position.set(x, 0, z);
			tile.receiveShadow = true;

			tiledFloor.add(tile);
		}
	}

	return tiledFloor;
}

// Add the floor to the scene
const floor = createTileFloor();
scene.add(floor);

// New variables for toggleable features
let centerAnimation = true; // Default to true, matching the initial button state
let axisVisible = false; // Default to false, matching the initial button state
let axisHelper = null; // Will hold the reference to the axis helper object

// Function to toggle center animation feature
function setCenterAnimation(enabled) {
	centerAnimation = enabled;
	console.log(`Center animation set to: ${enabled}`);
}

// Function to toggle axis visibility
function setAxisVisible(visible) {
	axisVisible = visible;
	console.log(`Axis visibility set to: ${visible}`);

	// Create or remove axis helper based on visibility setting
	if (visible && !axisHelper) {
		// Create axes helper if it doesn't exist and should be visible
		axisHelper = new THREE.AxesHelper(5); // Size of the axes (5 units long)
		scene.add(axisHelper);
	} else if (!visible && axisHelper) {
		// Remove axes helper if it exists and should not be visible
		scene.remove(axisHelper);
		axisHelper = null;
	}
}

// Function to create axis helper on initial load
function initializeAxisHelper() {
	// Create the axes helper with the default visibility
	if (axisVisible) {
		axisHelper = new THREE.AxesHelper(5);
		scene.add(axisHelper);
	}
}

// Initialize axis helper
initializeAxisHelper();

// Expose these functions to be called from PyQt
window.setCenterAnimation = setCenterAnimation;
window.setAxisVisible = setAxisVisible;

// Orbit Controls
const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.minDistance = 1.5; // Increased minimum distance to prevent too close zoom
controls.maxDistance = 15; // Increased maximum zoom distance
controls.target.set(0, 0.6, 0); // Lower the target point to match lower camera
controls.update();

let mixer;
let clock = new THREE.Clock();
let duration = 0;
let currentTime = 0; // Track current time without seek bar

// Initial state
let isPlaying = false;
let animatedObject; // Reference to the loaded object
let timeScaleBuffer = 1; // Buffer for timeScale
let pyQtControlled = false; // Flag to prevent feedback loops

// Set up error handling function
function handleLoadError(error) {
	console.error("Error loading FBX:", error);
	alert("Failed to load FBX model. Check the console for details.");
}

// Load FBX file - using relative URL path for better compatibility
const loader = new THREE.FBXLoader();
loader.load(
	// Use a relative path instead of absolute
	"Sample_working.fbx",
	(object) => {
		// Hide the loading screen once the model is loaded
		if (typeof hideLoading === "function") {
			hideLoading();
		}

		// Scale down the model
		object.scale.set(0.01, 0.01, 0.01);

		// Enable shadows for all meshes in the model
		object.traverse(function (child) {
			if (child.isMesh) {
				child.castShadow = true;
				child.receiveShadow = true;
			}
		});

		if (centerAnimation) {
			// Compute the bounding box
			const box = new THREE.Box3().setFromObject(object);
			const center = box.getCenter(new THREE.Vector3());

			// Position to center horizontally but keep vertical position
			object.position.x = -center.x;
			object.position.z = -center.z;
			// Don't center vertically - keep model on the floor
			object.position.y = 0;
		}

		scene.add(object);
		animatedObject = object; // Save reference for tracking

		console.log(
			"Object loaded successfully. Animations:",
			object.animations.length
		);

		// Only create mixer if animations exist
		if (object.animations && object.animations.length > 0) {
			// Create animation mixer
			mixer = new THREE.AnimationMixer(object);
			const action = mixer.clipAction(object.animations[0]);
			action.play();
			mixer.timeScale = 0; // Start animation paused

			// Get animation duration
			duration = object.animations[0].duration;

			// Listen for loop events
			mixer.addEventListener("loop", () => {
				if (isPlaying) {
					currentTime = 0;
					mixer.setTime(0);
				}
			});

			// console.log(`Animation loaded. Duration: ${duration} seconds`);
		} else {
			console.warn("No animations found in the model");
		}
	},
	(xhr) => console.log((xhr.loaded / xhr.total) * 100 + "% loaded"),
	handleLoadError
);

// Resize handler
window.addEventListener("resize", () => {
	camera.aspect = window.innerWidth / window.innerHeight;
	camera.updateProjectionMatrix();
	renderer.setSize(window.innerWidth, window.innerHeight);
});

// Function to be called from PyQt to set the animation time
function setAnimationTime(normalizedTime) {
	if (!mixer || !duration) return;

	// Set the flag to prevent feedback loops
	pyQtControlled = true;

	try {
		// Calculate the actual time based on the normalized value (0.0 to 1.0)
		const targetTime = normalizedTime * duration;

		// Update the current time tracking
		currentTime = targetTime;

		// Update the animation time
		if (!isPlaying) {
			mixer.timeScale = timeScaleBuffer; // Resume animation temporarily
			mixer.setTime(targetTime); // Update the animation time
			mixer.timeScale = 0; // Pause animation
		} else {
			mixer.setTime(targetTime); // Update the animation time
		}

		// Update the joint info display if a joint is selected
		updateJointInfo();
	} finally {
		// Reset the flag
		setTimeout(() => {
			pyQtControlled = false;
		}, 50);
	}
}

// Expose the function to the window object so PyQt can call it
window.setAnimationTime = setAnimationTime;

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

		// Update current time tracking if playing
		if (isPlaying) {
			currentTime = mixer.time % duration;

			// Notify PyQt about the time change if playing and not controlled by PyQt
			if (
				!pyQtControlled &&
				window.qt &&
				typeof window.qt.updateSliderFromWeb === "function"
			) {
				window.qt.updateSliderFromWeb(currentTime);
			}
		}
	}

	const dampingFactor = 0.1; // Adjust for smoother or faster movement
	// Only update camera target if centerAnimation is enabled
	if (centerAnimation && animatedObject) {
		// Compute the bounding box
		const box = new THREE.Box3().setFromObject(animatedObject);
		const center = box.getCenter(new THREE.Vector3());

		// Add height offset to look at the model's center, not its feet
		center.y += 0.1; // Lowered to match the camera height

		// Smoothly interpolate the camera's target
		controls.target.lerp(center, dampingFactor);
	}

	controls.update();
	renderer.render(scene, camera);
}

// Function to set the playing state from outside (PyQt)
function setPlaying(playing) {
	if (playing && !isPlaying) {
		// Start playing
		if (mixer) {
			mixer.timeScale = timeScaleBuffer; // Resume with current speed
			isPlaying = true;

			// If we're at the end, loop back to beginning
			if (mixer.time >= duration) {
				mixer.setTime(0);
				currentTime = 0;
			}
		}
	} else if (!playing && isPlaying) {
		// Pause
		if (mixer) {
			mixer.timeScale = 0; // Pause animation
			isPlaying = false;
		}
	}

	// Log the state change for debugging
	console.log(`Animation playback set to: ${isPlaying ? "playing" : "paused"}`);
}

// Expose function to window object so PyQt can access it
window.setPlaying = setPlaying;

// Start the animation
animate();

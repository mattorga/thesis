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
	floor.position.y = -0.01; // Lower the floor to be below the hips
	floor.receiveShadow = true;

	// Create grid for checkerboard pattern (more subtle)
	const grid = new THREE.GridHelper(floorSize, floorSize, 0x000000, 0x000000);
	grid.position.y = 0; // Position slightly above floor to avoid z-fighting
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
			tile.position.set(x, 0, z); // Position tiles at the same level as grid
			tile.receiveShadow = true;

			tiledFloor.add(tile);
		}
	}

	return tiledFloor;
}

// Add the floor to the scene
const floor = createTileFloor();
scene.add(floor);

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
const replayBtn = document.getElementById("replay");

// Set up error handling function
function handleLoadError(error) {
	console.error("Error loading FBX:", error);
	alert("Failed to load FBX model. Check the console for details.");
}

function loadFbxModel(fbxPath) {
    console.log("Loading FBX from path:", fbxPath);
    
    // Clear existing model if any
    if (animatedObject) {
        scene.remove(animatedObject);
        animatedObject = null;
    }
    
    // Reset mixer
    if (mixer) {
        mixer.stopAllAction();
        mixer = null;
    }
    
    // Load the new FBX file
    const loader = new THREE.FBXLoader();
    loader.load(
        fbxPath,
        (object) => {
            object.scale.set(0.01, 0.01, 0.01);

			if (centerAnimation) {
				// Compute the bounding box
				const box = new THREE.Box3().setFromObject(object);
				const center = box.getCenter(new THREE.Vector3());
			
				// Offset the model to center it at the origin
				object.position.sub(center);
				
				// Adjust vertical position to ensure it's above the floor
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

                console.log(`Animation loaded. Duration: ${duration} seconds`);
                
                // Notify PyQt if available
                if (window.qt && typeof window.qt.updateSliderFromWeb === 'function') {
                    window.qt.updateSliderFromWeb(0);
                }
            } else {
                console.warn("No animations found in the model");
            }
        },
        (xhr) => console.log((xhr.loaded / xhr.total) * 100 + "% loaded"),
        handleLoadError
    );
}
let defaultFbxPath = "Sample_working.fbx";

if (window.pendingFbxPath) {
    defaultFbxPath = window.pendingFbxPath;
    window.pendingFbxPath = null;
}

// Load the default or specified FBX
loadFbxModel(defaultFbxPath);


// Resize handler
window.addEventListener("resize", () => {
	camera.aspect = window.innerWidth / window.innerHeight;
	camera.updateProjectionMatrix();
	renderer.setSize(window.innerWidth, window.innerHeight);
});

// Play/Pause functionality
playPauseBtn.addEventListener("click", () => {
	if (!mixer) return;

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
	if (!mixer) return;

	console.log(
		`[Backward] Current mixer.time: ${mixer.time}, timeScale: ${timeScaleBuffer}`
	);

	if (isPlaying) {
		mixer.timeScale = 1; // resume animation temporarily
		mixer.setTime(Math.max(0, mixer.time - 1)); // Go back 1 second
		seekBar.value = mixer.time; // Sync seekbar
		mixer.timeScale = timeScaleBuffer; // resume with the correct speed
	} else {
		mixer.timeScale = 1; // resume animation temporarily
		mixer.setTime(Math.max(0, mixer.time - 1)); // Go back 1 second
		seekBar.value = mixer.time; // Sync seekbar
		mixer.timeScale = 0; // Pause animation
	}
});

// Forward functionality
forwardBtn.addEventListener("click", () => {
	if (!mixer) return;

	console.log(
		`[Forward] Current mixer.time: ${mixer.time}, timeScale: ${timeScaleBuffer}`
	);

	if (isPlaying) {
		mixer.timeScale = 1; // resume animation temporarily
		mixer.setTime(Math.min(duration, mixer.time + 1)); // Go forward 1 second
		seekBar.value = mixer.time; // Sync seekbar
		mixer.timeScale = timeScaleBuffer; // resume with the correct speed
	} else {
		mixer.timeScale = 1; // resume animation temporarily
		mixer.setTime(Math.min(duration, mixer.time + 1)); // Go forward 1 second
		seekBar.value = mixer.time; // Sync seekbar
		mixer.timeScale = 0; // Pause animation
	}
});

// Replay functionality
replayBtn.addEventListener("click", () => {
	if (!mixer) return;

	mixer.setTime(0); // Reset to beginning
	seekBar.value = 0; // Reset seekbar

	if (!isPlaying) {
		mixer.timeScale = timeScaleBuffer;
		isPlaying = true;
		playPauseBtn.textContent = "⏸️";
	}
});

// Seekbar functionality
seekBar.addEventListener("input", (e) => {
	if (!mixer) return;

	let newTime = parseFloat(e.target.value); // Parse value with higher precision

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

	if (!isPlaying) {
		mixer.timeScale = timeScaleBuffer; // Resume animation temporarily
		mixer.setTime(newTime); // Update the animation time
		mixer.timeScale = 0; // Pause animation
	} else {
		mixer.setTime(newTime); // Update the animation time
	}
});




// Center animation checkbox
centerAnimationCheckbox.addEventListener("change", () => {
	centerAnimation = centerAnimationCheckbox.checked;
});

// Update animation speed based on selector value
animationSpeedSelector.addEventListener("change", () => {
	if (!mixer) return;

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
			const currentTime = (mixer.time % duration).toFixed(2); // Round to 2 decimal places
			seekBar.value = currentTime; // Update seekbar position
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
playPauseBtn.addEventListener("click", updateJointInfo);
rewindBtn.addEventListener("click", updateJointInfo);
forwardBtn.addEventListener("click", updateJointInfo);
seekBar.addEventListener("input", updateJointInfo);
replayBtn.addEventListener("click", updateJointInfo);

// Start the animation
animate();

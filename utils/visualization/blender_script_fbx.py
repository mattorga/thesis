import bpy
import os
import zipfile

# Path to the Pose2Sim ZIP file
POSE2SIM_ZIP = "/path/to/Pose2Sim_Blender.zip"

# Blender's add-ons directory
addon_dir = bpy.utils.user_resource('SCRIPTS', path="addons")

# Remove all default objects (Camera, Cube, Light)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Set file paths (CHANGE THESE TO YOUR PATHS)
base_path = r"D:\Miro Hernandez\Documents\openpose-1.7.0-binaries-win64-gpu-python3.7-flir-3d_recommended\davidpagnon Pose2Sim_Blender main Examples"
toml_file = os.path.join(base_path, "Pose2Sim_cameras.toml")
trc_file = os.path.join(base_path, "Pose2Sim_markers.trc")
osim_file = os.path.join(base_path, "Pose2Sim_model.osim")
csv_file = os.path.join(base_path, "Pose2Sim_motion.csv")
fbx_output = os.path.join(base_path, "exported_pose2sim.fbx")  # Output path
framerate = 30  # Set the desired framerate

### -------------------- Install Pose2Sim -------------------- ###
def install_pose2sim(zip_path, extract_to):
    print(f"Installing Pose2Sim to: {extract_to}")

    # Ensure the add-ons directory exists
    os.makedirs(extract_to, exist_ok=True)

    # Extract the ZIP file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

    print("Pose2Sim installed successfully.")

### -------------------- Enable Pose2Sim -------------------- ###
def enable_pose2sim():
    print("Enabling Pose2Sim add-on...")

    # Refresh and enable the add-on
    bpy.ops.preferences.addon_refresh()
    addon_name = "Pose2Sim_Blender"  # Adjust if needed
    bpy.ops.preferences.addon_enable(module=addon_name)

    # Save preferences
    bpy.ops.wm.save_userpref()
    print("Pose2Sim enabled successfully.")

### -------------------- Read TRC Frame Count -------------------- ###
def get_trc_num_frames(trc_path):
    try:
        with open(trc_path, 'r') as f:
            lines = f.readlines()
            if len(lines) >= 4:
                # The 4th line (index 3) contains frame info
                header_parts = lines[3].strip().split()
                if len(header_parts) >= 3:
                    num_frames = int(header_parts[2])  # NumFrames is the 3rd value
                    print(f"Number of frames from TRC header: {num_frames}")
                    return num_frames
    except Exception as e:
        print(f"Error reading TRC file: {e}")
    
    print("Could not extract frame count from TRC header")
    return 0

# Enable Pose2Sim
enable_pose2sim()

# Import TOML (camera calibration)
bpy.ops.mesh.add_cam_cal(filepath=toml_file)

# Get frame count from TRC before importing
max_frame = get_trc_num_frames(trc_file)

# Import TRC (marker data)
bpy.ops.mesh.add_osim_markers(
    filepath=trc_file,
    target_framerate=framerate,
    files=[{"name": "Pose2Sim_markers.trc", "name": "Pose2Sim_markers.trc"}],
    directory=base_path
)

# Import OSIM (model)
bpy.ops.mesh.add_osim_model(filepath=osim_file)

# Import CSV (motion)
bpy.ops.mesh.add_osim_motion(filepath=csv_file, target_framerate=framerate)

# Set the frame range
if max_frame > 0:
    bpy.context.scene.frame_end = max_frame
    print(f"Frame end set to: {max_frame}")
else:
    print("Warning: Could not determine max frame from TRC file.")

# Export to FBX
bpy.ops.export_scene.fbx(
    filepath=fbx_output,
    use_selection=False,          # Export everything
    use_visible=True,             # Only export visible objects
    bake_anim=True,               # Bake animation
    bake_anim_use_nla_strips=False,
    bake_anim_use_all_actions=False
)

print(f"Exported FBX: {fbx_output}")

## Command for starting blender (paste in cmd):
## "D:\Program Files\blender.exe" --background --python "D:\Miro Hernandez\Documents\openpose-1.7.0-binaries-win64-gpu-python3.7-flir-3d_recommended\davidpagnon Pose2Sim_Blender main Examples\blender_script_v2.py"
import os
import shutil
import subprocess
import sys
import Pose2Sim

def main():
    """Build the GaitScape executable using PyInstaller"""
    print("Starting build process for GaitScape...")
    
    # Make sure we're in the right directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Find Pose2Sim path and save it to a temp file for the spec to use
    pose2sim_path = os.path.dirname(Pose2Sim.__file__)
    print(f"Found Pose2Sim at: {pose2sim_path}")
    
    # Write the path to a temporary file
    with open("pose2sim_path.txt", "w") as f:
        f.write(pose2sim_path)
    
    # Verify main.py exists
    if not os.path.exists("main.py"):
        print("Error: main.py not found in the current directory")
        return
    
    # Run PyInstaller
    print("Running PyInstaller...")
    try:
        # Use the spec file if it exists
        if os.path.exists("GaitScape.spec"):
            subprocess.run(["pyinstaller", "GaitScape.spec"], check=True)
        else:
            print("Error: GaitScape.spec not found")
            return
    except subprocess.CalledProcessError as e:
        print(f"PyInstaller failed: {str(e)}")
        return
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return
    
    # Clean up temp file
    if os.path.exists("pose2sim_path.txt"):
        os.remove("pose2sim_path.txt")
    
    print("Build completed successfully!")
    print(f"Executable should be available in {os.path.join(script_dir, 'dist', 'GaitScape.exe')}")

if __name__ == "__main__":
    main()
import toml
import subprocess
import os
import signal
from pathlib import Path

class OpenPoseRunner:
    def __init__(self):
        self.openpose_path = ""
        self.config = {}
        self.process = None
        self.input_directory = ""
        self.output_directory = ""
        self.model_folder = ""

    def set_openpose_path(self, path):
        """Set the path to the OpenPoseDemo.exe"""
        if os.path.exists(path):
            self.openpose_path = path
        else:
            raise FileNotFoundError(f"OpenPoseDemo.exe not found at {path}")

    def set_input_directory(self, path):
        """Set the input directory containing videos"""
        if os.path.isdir(path):
            self.input_directory = path
        else:
            raise NotADirectoryError(f"Input directory not found: {path}")

    def set_output_directory(self, path):
        """Set the output directory for JSON files"""
        Path(path).mkdir(parents=True, exist_ok=True)
        self.output_directory = path

    def set_model_folder(self, path):
        """Set the model folder path"""
        if os.path.isdir(path):
            self.model_folder = path
        else:
            raise NotADirectoryError(f"Model folder not found: {path}")

    def load_config(self, config_path):
        """Load the TOML configuration file"""
        with open(config_path, 'r') as f:
            self.config = toml.load(f)

    def build_command(self, video_path, output_path):
        """Build the command string based on the configuration"""
        cmd = [self.openpose_path]
        cmd.extend(['--video', video_path])
        cmd.extend(['--write_json', output_path])
        cmd.extend(['--display', '0'])
        cmd.extend(['--render_pose', '0'])

        # Add the model folder to the command
        if self.model_folder:
            cmd.extend(['--model_folder', self.model_folder])

        # Add other parameters from the config
        if 'face' in self.config and self.config['face']:
            cmd.append('--face')
        if 'hand' in self.config and self.config['hand']:
            cmd.append('--hand')
        if 'net_resolution' in self.config:
            cmd.extend(['--net_resolution', self.config['net_resolution']])
        if 'model_pose' in self.config:
            cmd.extend(['--model_pose', self.config['model_pose']])
        if 'number_people_max' in self.config:
            cmd.extend(['--number_people_max', str(self.config['number_people_max'])])

        return cmd

    def process_videos(self):
        """Process all videos in the input directory"""
        if not self.openpose_path:
            raise ValueError("OpenPose path not set. Call set_openpose_path() first.")
        if not self.input_directory:
            raise ValueError("Input directory not set. Call set_input_directory() first.")
        if not self.output_directory:
            raise ValueError("Output directory not set. Call set_output_directory() first.")
        if not self.model_folder:
            raise ValueError("Model folder path not set. Call set_model_folder() first.")

        # Initialize folder counter
        folder_counter = 1

        for video_file in os.listdir(self.input_directory):
            if video_file.endswith(('.mp4', '.avi', '.mov')):  # Add more video formats if needed
                video_path = os.path.join(self.input_directory, video_file)
                
                # Create unique output folder for each video
                output_folder_name = f"output_json_{folder_counter}"
                output_path = os.path.join(self.output_directory, output_folder_name)
                Path(output_path).mkdir(parents=True, exist_ok=True)
                
                cmd = self.build_command(video_path, output_path)
                print(f"Processing video: {video_file}")
                print(f"Running command: {' '.join(cmd)}")
                
                process = subprocess.Popen(cmd)
                process.wait()  # Wait for the process to complete before moving to the next video
                
                # Increment folder counter
                folder_counter += 1

    def interrupt_process(self):
        """Interrupt the running OpenPose process"""
        if self.process:
            os.kill(self.process.pid, signal.SIGTERM)
            self.process = None
            print("OpenPose process interrupted.")
        else:
            print("No OpenPose process running.")


# Example usage:
if __name__ == "__main__":
    runner = OpenPoseRunner()
    runner.set_openpose_path(r"D:\Miro Hernandez\Documents\openpose-1.7.0-binaries-win64-gpu-python3.7-flir-3d_recommended\openpose\bin\OpenPoseDemo.exe")
    runner.set_input_directory(r"D:\Miro Hernandez\Documents\openpose-1.7.0-binaries-win64-gpu-python3.7-flir-3d_recommended\sample vid walking")
    runner.set_output_directory(r"D:\Miro Hernandez\Documents\openpose-1.7.0-binaries-win64-gpu-python3.7-flir-3d_recommended\Openpose_local_output")
    runner.load_config(r"D:\Miro Hernandez\Documents\openpose-1.7.0-binaries-win64-gpu-python3.7-flir-3d_recommended\Useful Scripts\OpenPose_Config.toml")
    runner.set_model_folder(r"D:\Miro Hernandez\Documents\openpose-1.7.0-binaries-win64-gpu-python3.7-flir-3d_recommended\openpose\models")
    runner.process_videos()

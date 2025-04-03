import toml
import subprocess
import os
import signal
import json
from pathlib import Path
import time
import sys


class OpenPoseRunner:
    def __init__(self):
        self.openpose_path = ""
        self.config = {}
        self.process = None
        self.input_directory = ""
        self.output_directory = ""
        self.model_folder = ""
        self.verbose = True  # Set to False to disable detailed logging

    def set_openpose_path(self, path):
        """Set the path to the OpenPoseDemo.exe or equivalent executable"""
        if os.path.exists(path):
            self.openpose_path = path
            if self.verbose:
                print(f"OpenPose path set to: {path}")
        else:
            raise FileNotFoundError(f"OpenPose executable not found at {path}")

    def set_input_directory(self, path):
        """Set the input directory containing videos"""
        if os.path.isdir(path):
            self.input_directory = path
            if self.verbose:
                print(f"Input directory set to: {path}")
        else:
            raise NotADirectoryError(f"Input directory not found: {path}")

    def set_output_directory(self, path):
        """Set the output directory for JSON files"""
        Path(path).mkdir(parents=True, exist_ok=True)
        self.output_directory = path
        if self.verbose:
            print(f"Output directory set to: {path}")

    def set_model_folder(self, path):
        """Set the model folder path"""
        if os.path.isdir(path):
            self.model_folder = path
            if self.verbose:
                print(f"Model folder set to: {path}")
        else:
            raise NotADirectoryError(f"Model folder not found: {path}")

    def load_config(self, config_path):
        """Load the TOML configuration file"""
        try:
            with open(config_path, 'r') as f:
                loaded_config = toml.load(f)
                
                # Extract openpose section if it exists
                if 'openpose' in loaded_config:
                    self.config.update(loaded_config['openpose'])
                else:
                    # Otherwise use the whole config
                    self.config.update(loaded_config)
                    
                # Special handling for specific fields to ensure they are prioritized
                # This ensures that the net_resolution from the config file is used
                if 'net_resolution' in loaded_config:
                    self.config['net_resolution'] = loaded_config['net_resolution']
                elif 'openpose' in loaded_config and 'net_resolution' in loaded_config['openpose']:
                    self.config['net_resolution'] = loaded_config['openpose']['net_resolution']
                    
                if self.verbose:
                    print(f"Loaded configuration from {config_path}")
                    print("Applied OpenPose configuration:")
                    for key, value in self.config.items():
                        print(f"  {key}: {value}")
        except Exception as e:
            print(f"Error loading config from {config_path}: {str(e)}")
            # Continue with default config

    def build_command(self, video_path, output_path):
        """Build the command string based on the configuration"""
        cmd = [self.openpose_path]
        
        # Core parameters
        cmd.extend(['--video', video_path])
        cmd.extend(['--write_json', output_path])
        
        # Default to no display and no rendering for headless operation
        if '--display' not in self.config:
            cmd.extend(['--display', '1'])
        if '--render_pose' not in self.config:
            cmd.extend(['--render_pose', '1'])

        # Add the model folder to the command
        if self.model_folder:
            cmd.extend(['--model_folder', self.model_folder])

        # Add parameters from the config
        for key, value in self.config.items():
            # Skip keys that are already handled or not relevant to command line
            if key in ['OpenPose_path', 'model_path']:
                continue
                
            if isinstance(value, bool):
                if value:  # Only add flag if it's True
                    cmd.append(f'--{key}')
            else:
                cmd.extend([f'--{key}', str(value)])

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

        # Check if input directory contains videos
        video_files = [f for f in os.listdir(self.input_directory) 
                      if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.wmv'))]
        
        if not video_files:
            raise ValueError(f"No video files found in {self.input_directory}")
        
        print(f"Found {len(video_files)} video files to process")

        # Initialize folder counter
        folder_counter = 1
        processed_count = 0

        for video_file in video_files:
            video_path = os.path.join(self.input_directory, video_file)
            
            # Create output folder name based on video name without extension
            video_name = os.path.splitext(video_file)[0]
            output_folder_name = f"{video_name}_json"
            output_path = os.path.join(self.output_directory, output_folder_name)
            
            # Check if output folder already exists and contains JSON files
            if os.path.exists(output_path) and any(f.endswith('.json') for f in os.listdir(output_path)):
                print(f"Skipping {video_file} - output folder already contains JSON files")
                processed_count += 1
                continue
                
            # Create output directory if it doesn't exist
            Path(output_path).mkdir(parents=True, exist_ok=True)
            
            # Build and run command
            cmd = self.build_command(video_path, output_path)
            print(f"Processing video [{processed_count+1}/{len(video_files)}]: {video_file}")
            if self.verbose:
                print(f"Running command: {' '.join(cmd)}")
            
            try:
                # Start the process and wait for it to complete
                start_time = time.time()
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                self.process = process
                
                # Monitor progress
                while process.poll() is None:
                    # Optional: implement progress monitoring logic here
                    time.sleep(1)
                    
                    # Periodically check for JSON output to confirm progress
                    if (time.time() - start_time) % 10 < 1:  # Check roughly every 10 seconds
                        json_count = len([f for f in os.listdir(output_path) if f.endswith('.json')])
                        if json_count > 0:
                            print(f"  Progress: {json_count} frames processed")
                
                # Check return code
                if process.returncode != 0:
                    stdout, stderr = process.communicate()
                    print(f"Warning: OpenPose returned non-zero code {process.returncode}")
                    print(f"STDOUT: {stdout.decode('utf-8', errors='ignore')}")
                    print(f"STDERR: {stderr.decode('utf-8', errors='ignore')}")
                
                # Verify that JSON files were created
                json_files = [f for f in os.listdir(output_path) if f.endswith('.json')]
                if not json_files:
                    print(f"Warning: No JSON files were created for {video_file}")
                else:
                    print(f"Successfully processed {video_file} - created {len(json_files)} JSON files")
                    
                    # Verify JSON file integrity by checking one file
                    try:
                        with open(os.path.join(output_path, json_files[0]), 'r') as f:
                            json.load(f)  # This will raise an exception if JSON is invalid
                    except Exception as e:
                        print(f"Warning: JSON validation failed for {json_files[0]}: {str(e)}")
                
                processed_count += 1
                
            except Exception as e:
                print(f"Error processing {video_file}: {str(e)}")
                import traceback
                traceback.print_exc()
            finally:
                # Ensure process is terminated even if an exception occurs
                if self.process and self.process.poll() is None:
                    self.process.terminate()
                    try:
                        self.process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        self.process.kill()
                self.process = None
            
            # Increment folder counter
            folder_counter += 1
        
        return processed_count

    def interrupt_process(self):
        """Interrupt the running OpenPose process"""
        if self.process and self.process.poll() is None:
            print("Interrupting OpenPose process...")
            if sys.platform == "win32":
                # On Windows, use taskkill to forcefully terminate process tree
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(self.process.pid)])
            else:
                # On Unix-like systems
                os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
            
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                if sys.platform == "win32":
                    subprocess.call(['taskkill', '/F', '/T', '/PID', str(self.process.pid)])
                else:
                    os.killpg(os.getpgid(self.process.pid), signal.SIGKILL)
            
            self.process = None
            print("OpenPose process interrupted.")
        else:
            print("No OpenPose process running.")


if __name__ == "__main__":
    # Example usage:
    runner = OpenPoseRunner()
    
    # You can modify these paths for testing
    runner.set_openpose_path(r"D:\path\to\openpose\bin\OpenPoseDemo.exe")
    runner.set_input_directory(r"D:\path\to\videos")
    runner.set_output_directory(r"D:\path\to\output")
    runner.set_model_folder(r"D:\path\to\openpose\models")
    
    # Either load config from TOML file
    # runner.load_config(r"D:\path\to\OpenPose_Config.toml")
    
    # Or set config directly
    runner.config = {
        'face': False,
        'hand': False,
        'net_resolution': '520x240',
        'model_pose': 'BODY_25',
        'number_people_max': 5
    }
    
    # Process videos
    runner.process_videos()
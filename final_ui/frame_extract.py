import cv2
from pathlib import Path

def extract_single_frame(video_path, output_dir):
    """
    Extract a single frame from an AVI video file and save it as a JPEG image.
    
    Args:
        video_path (str): Path to the input AVI video file
        output_dir (str): Directory where the frame will be saved
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        raise ValueError("Error: Could not open video file")
    
    try:
        # Read first frame
        ret, frame = cap.read()
        
        if not ret:
            raise ValueError("Error: Could not read frame from video")
            
        # Generate output filename
        output_filename = "pose_cam3.png"
        output_path = f'frames/{output_filename}'
        
        # Save frame as JPEG
        cv2.imwrite(output_path, frame)
        print(f"Saved frame to {output_path}")
    
    finally:
        # Release resources
        cap.release()

def main():
    # Example usage
    video_path = "/Users/mattheworga/Documents/GaitScape/S02_IvyHill/P01_Molo_Carlos/T03_normal_2.0/pose/normal_3_pose.mp4"
    
    try:
        extract_single_frame(video_path, "frames")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
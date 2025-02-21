import cv2
import os
from pathlib import Path

def extract_frames_per_second(video_path, output_dir):
    """
    Extract one frame per second from an AVI video file and save them as JPEG images.
    
    Args:
        video_path (str): Path to the input AVI video file
        output_dir (str): Directory where frames will be saved
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        raise ValueError("Error: Could not open video file")
    
    try:
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_count = 0
        second_count = 0
        
        while True:
            # Read frame
            ret, frame = cap.read()
            
            # Break if we've reached the end of the video
            if not ret:
                break
            
            # Extract one frame per second
            if frame_count % fps == 0:
                # Generate output filename
                output_filename = f"cam01_0{second_count}_int.jpg"
                output_path = os.path.join(output_dir, output_filename)
                
                # Save frame as JPEG
                cv2.imwrite(output_path, frame)
                
                print(f"Saved frame for second {second_count}")
                second_count += 1
            
            frame_count += 1
    
    finally:
        # Release resources
        cap.release()
        
    print(f"Extraction complete. Total seconds processed: {second_count}")

def main():
    # Example usage
    video_path = "/Users/mattheworga/Documents/Git/DLSU/thesis/final_ui/intrinsics.avi"
    output_dir = "output_frames"
    
    try:
        extract_frames_per_second(video_path, output_dir)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
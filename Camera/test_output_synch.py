import cv2
import time

def play_videos_side_by_side(video_path1, video_path2, video_path3):
    # Open the two videos    
    start_1 = time.time()
    cap1 = cv2.VideoCapture(video_path1)
    end_1 = time.time()
    #print(f"Cap 1 Total Time: {end_1 - start_1}s")


    start_2 = time.time()
    cap2 = cv2.VideoCapture(video_path2)
    end_2 = time.time()

    cap3 = cv2.VideoCapture(video_path3)

    #print(f"Cap 2 Total Time: {end_2 - start_2}s")

    #print(f"Delay between cap1 and cap2: {end_2-start_1}s")

    # Get the total number of frames in each video
    total_frames1 = int(cap1.get(cv2.CAP_PROP_FRAME_COUNT))
    total_frames2 = int(cap2.get(cv2.CAP_PROP_FRAME_COUNT))
    total_frames3 = int(cap3.get(cv2.CAP_PROP_FRAME_COUNT))


    # Get the frame rate (frames per second) of each video
    fps1 = cap1.get(cv2.CAP_PROP_FPS)
    fps2 = cap2.get(cv2.CAP_PROP_FPS)
    fps3 = cap3.get(cv2.CAP_PROP_FPS)

    # Calculate the duration of each video
    duration1 = total_frames1 / fps1
    duration2 = total_frames2 / fps2
    duration3 = total_frames3 / fps3


    print(f"Video 1: {total_frames1} frames, {fps1} FPS, {duration1} seconds")
    print(f"Video 2: {total_frames2} frames, {fps2} FPS, {duration2} seconds")
    #print(f"Video 3: {total_frames3} frames, {fps3} FPS, {duration3} seconds")


    while True:
        # Read the next frame from each video
        start_3 = time.time()
        ret1, frame1 = cap1.read()
        end_3 = time.time()

        start_4 = time.time()
        ret2, frame2 = cap2.read()
        end_4 = time.time()

        ret3, frame3 = cap3.read()

        #print(f"Delay between frame1 and frame2: {end_4-start_3}s")


        # If we couldn't read a frame from either video, break the loop
        if not ret1 or not ret2 or not ret3:
            break
        
        #frame3_resized = cv2.resize(frame3, (frame1.shape[1], frame1.shape[0]))

        # Concatenate the frames horizontally and show them
        both = cv2.hconcat([frame1, frame2])

        cv2.imshow('Both Videos', both)

        # If the user presses 'q', break the loop
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break

    # Release the video captures and destroy the window
    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()

# Use the function
play_videos_side_by_side('output_0.mp4', 'output_1.mp4', 'output_2.mp4')

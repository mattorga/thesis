from CameraManager import CameraManager

if __name__ == '__main__':
    camManager = CameraManager()
    # camManager.addCamera(0, 'output_1.mp4')
    camManager.addCamera(1, 'output_2.mp4')
    camManager.addCamera(2, 'output_3.mp4')

    # TODO: Start cameras but to not record

    # Start recording on all cameras
    camManager.startAll()

    # Wait for user input to stop recording
    input("Press Enter to stop recording...")

    # Stop recording on all cameras
    camManager.stopAll()

    # Wait for all processes to finish
    camManager.joinAll()

    print("All recordings have been stopped.")

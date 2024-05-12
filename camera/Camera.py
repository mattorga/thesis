import cv2

class Camera:
    def __init__(self, cam_ID, vidFilePath, stop_event):
        self.cam_ID = cam_ID
        self.vidFilePath = vidFilePath
        self.stop_event = stop_event

    def startAndStopRecording(self):
        print(f"Starting recording on camera {self.cam_ID}...")
        vid = cv2.VideoCapture(self.cam_ID)
        width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(self.vidFilePath, fourcc, 20.0, (width, height))

        while not self.stop_event.is_set(): # While no key is pressed, keep recording
            ret, frame = vid.read()
            cv2.imshow(f'frame {self.cam_ID}', frame) 
            out.write(frame)
            
            key = cv2.waitKey(20)
            if key == 27:  # exit on ESC
                break

        print(f"Stopping recording on camera {self.cam_ID}...\n")
        vid.release()
        out.release()
        cv2.destroyAllWindows()

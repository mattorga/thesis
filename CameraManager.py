import multiprocessing as mp
import time
from Camera import Camera

class CameraManager:
    def __init__(self):
        self.cameras = []
        self.processes = []
        self.stop_event = mp.Event()

    def addCamera(self, cam_ID, vidFilePath):
        self.cameras.append(Camera(cam_ID, vidFilePath, self.stop_event))

    def startAll(self):
        for cam in self.cameras:
            p = mp.Process(target=cam.startAndStopRecording)
            self.processes.append(p)
            start = time.time()
            p.start()
            end = time.time()
            print(f"Camera {cam.cam_ID} Start Time: {end-start}")

    def stopAll(self):
        print("Reached stopAll()")
        self.stop_event.set()

    def joinAll(self):
        print("Reached joinAll()")
        for p in self.processes:
            p.join()

from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap
import cv2
import os

class Camera(QThread):
    ImageUpdate = pyqtSignal(QImage)

    def __init__(self, camera_number=0):
        super().__init__()
        self.camera_number = camera_number
        self.threadActive = True

    def run(self):
        self.isRecording = False
        self.videoWriter = None

        cap = cv2.VideoCapture(self.camera_number)
        if not cap.isOpened():
            print(f"Error: Could not open camera {self.camera_number}")
            return
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        
        # After cap = cv2.VideoCapture(self.camera_number)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        while self.threadActive:
            ret, frame = cap.read()
            if ret:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                if self.isRecording:
                    if self.videoWriter is None:
                        filename = self.get_unique_filename(self.camera_number)
                        self.videoWriter = cv2.VideoWriter(
                            filename, 
                            fourcc, 
                            30.0, 
                            (frame_width, frame_height)
                        )
                    self.videoWriter.write(frame)

                flippedImage = cv2.flip(image, 1)
                ConvertToQtFormat = QImage(
                    flippedImage.data,            
                    flippedImage.shape[1], 
                    flippedImage.shape[0],
                    QImage.Format_RGB888
                )
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
                
        if self.videoWriter is not None:
            self.videoWriter.release()
        cap.release()

    def stop(self):
        self.threadActive = False
        if self.videoWriter is not None:
            self.videoWriter.release()
        self.wait()

    def start_recording(self):
        self.isRecording = True

    def stop_recording(self):
        self.isRecording = False
        if self.videoWriter is not None:
            print(f"{self.camera_number} stopped recording...")
            self.videoWriter.release()
            self.videoWriter = None

    def get_unique_filename(self, base_number):
        counter = 0
        while True:
            if counter == 0:
                filename = f'output_{base_number}.avi'
            else:
                filename = f'output_{base_number}_{counter}.avi'
                
            if not os.path.exists(filename):
                return filename
            counter += 1
        
class CameraManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.camera_workers = {}
        self.camera_labels = {
            0: main_window.ui.camera1Label,
            1: main_window.ui.camera2Label,
            2: main_window.ui.camera3Label
        }
        self.available_cameras = []
        self.framerates = []

    def detect_available_cameras(self, max_cameras=3):
        for i in range(max_cameras):
            cap = cv2.VideoCapture(i)
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            if cap.isOpened():
                ret, _ = cap.read()
                if ret:
                    self.available_cameras.append(i)
                    self.framerates.append(fps)
            cap.release()
            
        self.main_window.ui.camerasValue.setText(str(len(self.available_cameras)))
        self.main_window.ui.frameRateValue.setText(str(self.framerates))
        
        for camera_index in self.available_cameras:
            worker = Camera(camera_index)
            worker.ImageUpdate.connect(
                lambda image, idx=camera_index: self.update_camera_feed(image, idx)
            )
            worker.start()
            self.camera_workers[camera_index] = worker

    def update_camera_feed(self, image, camera_index):
        self.camera_labels[camera_index].setPixmap(QPixmap.fromImage(image))

    def close_all_cameras(self):
        for worker in self.camera_workers.values():
            worker.stop()
            worker.wait() 
        self.camera_workers.clear()
        self.available_cameras.clear()
        self.main_window.ui.camerasValue.setText(str(len(self.available_cameras)))

    def start_recording_all_cameras(self):
        for worker in self.camera_workers.values():
            worker.start_recording()

    def stop_recording_all_cameras(self):
        for worker in self.camera_workers.values():
            worker.stop_recording()
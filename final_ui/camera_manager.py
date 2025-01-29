from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap
import cv2

class Camera(QThread):
    ImageUpdate = pyqtSignal(QImage)

    def __init__(self, camera_number=0):
        super().__init__()
        self.camera_number = camera_number
        self.threadActive = True

    def run(self):
        self.isRecording = False

        cap = cv2.VideoCapture(self.camera_number)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(f'output_{self.camera_number}.avi', fourcc, 20.0, (640, 480))
        
        while self.threadActive == True:
            ret, frame = cap.read()
            if ret:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                if self.isRecording:
                    out.write(image)

                flippedImage = cv2.flip(image, 1)
                ConvertToQtFormat = QImage(
                    flippedImage.data,            
                    flippedImage.shape[1], 
                    flippedImage.shape[0],
                    QImage.Format_RGB888
                )
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
        cap.release()

    def stop(self):
        self.threadActive = False
        self.wait()

    def start_recording(self):
        self.isRecording = True

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

    def detect_available_cameras(self, max_cameras=3):
        for i in range(max_cameras):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, _ = cap.read()
                if ret:
                    self.available_cameras.append(i)
                cap.release()
            
        self.main_window.ui.camerasValue.setText(str(len(self.available_cameras)))
        
        for camera_index in self.available_cameras:
            worker = Camera(camera_index)
            worker.ImageUpdate.connect(
                lambda image, idx=camera_index: self.update_camera_feed(image, idx)
            )
            worker.start()
            self.camera_workers[camera_index] = worker
    
    def stop_all_cameras(self):
        for worker in self.camera_workers.values():
            print(worker)
            worker.stop()
            worker.wait() 
        self.camera_workers.clear()

    def update_camera_feed(self, image, camera_index):
       self.camera_labels[camera_index].setPixmap(QPixmap.fromImage(image))

    def start_recording_all_cameras(self):
       for worker in self.camera_workers.values():
            worker.start_recording()

    def stop_recording(self):
       pass
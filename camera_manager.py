from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap
import cv2
import os

class Camera(QThread):
    ImageUpdate = pyqtSignal(QImage)

    def __init__(self, camera_number=0, save_directory=None, file_name=None):
        super().__init__()
        self.camera_number = camera_number
        self.threadActive = True
        self.save_directory = save_directory
        self.file_name = file_name

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
                # Rotate the original frame
                rotated_frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
                # Convert to RGB for display
                image = cv2.cvtColor(rotated_frame, cv2.COLOR_BGR2RGB)

                if self.isRecording:
                    if self.videoWriter is None:
                        filename = self.get_unique_filename(self.camera_number)
                        # Note the swapped width and height for rotated dimensions
                        self.videoWriter = cv2.VideoWriter(
                            filename, 
                            fourcc, 
                            30.0, 
                            (frame_height, frame_width)  # Swap dimensions for rotation
                        )
                    self.videoWriter.write(rotated_frame)

                ConvertToQtFormat = QImage(
                    image.data,            
                    image.shape[1], 
                    image.shape[0],
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

    def get_unique_filename(self, camera_number):
        counter = 0
        
        # Check if save_directory is provided
        if self.save_directory:
            # Create a videos subdirectory within the trial directory
            videos_dir = os.path.join(self.save_directory, "videos")
            
            # Create the videos directory if it doesn't exist
            if not os.path.exists(videos_dir):
                os.makedirs(videos_dir)
                print(f"Created videos directory: {videos_dir}")
            
            # Generate filename with the videos directory
            while True:
                filename = f'{self.file_name}_cam{camera_number+1}.avi'
                filepath = os.path.join(videos_dir, filename)
                
                if not os.path.exists(filepath):
                    print(f"Saving video to: {filepath}")
                    return filepath
                
                # If file already exists, add counter to filename
                counter += 1
                filename = f'{self.file_name}_cam{camera_number+1}_{counter}.avi'
                filepath = os.path.join(videos_dir, filename)
                
                if not os.path.exists(filepath):
                    print(f"Saving video to: {filepath}")
                    return filepath
        else:
            # Fallback to current directory if no save_directory provided
            while True:
                filename = f'{self.file_name}_cam{camera_number+1}.avi'
                
                if not os.path.exists(filename):
                    return filename
                
                counter += 1
                filename = f'{self.file_name}_cam{camera_number+1}_{counter}.avi'
                
                if not os.path.exists(filename):
                    return filename

class CameraManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self._available_cameras = []
        self._framerates = []
        self._resolution = []
        self._camera_workers = {}
        self._save_directory = None
        self._file_name = None

    @property
    def file_name(self):
        return self._file_name
    
    @file_name.setter
    def file_name(self, file_name):
        self._file_name = file_name
        for worker in self._camera_workers.values():
            worker.file_name = file_name

    @property
    def save_directory(self):
        """Directory where camera recordings will be saved."""
        return self._save_directory

    @save_directory.setter 
    def save_directory(self, directory):
        """Set the directory for saving camera recordings."""
        if directory and not os.path.exists(directory):
            raise ValueError("Save directory must exist")
        self._save_directory = directory

        for worker in self._camera_workers.values():
            worker.save_directory = directory

    # --- Available Cameras Property --- #
    @property
    def available_cameras(self):
        """List of indices for currently available cameras."""
        return self._available_cameras.copy()

    @available_cameras.setter
    def available_cameras(self, cameras):
        if not isinstance(cameras, list):
            raise ValueError("Available cameras must be a list")
        if not all(isinstance(x, int) for x in cameras):
            raise ValueError("Camera indices must be integers")
        self._available_cameras = cameras.copy()

    # --- Framerates Property --- #
    @property
    def framerates(self):
        """List of framerates for detected cameras."""
        return self._framerates.copy()

    @framerates.setter 
    def framerates(self, rates):
        """Set framerates for cameras.
        
        Args:
            rates (list): List of framerates (integers or floats)
        """
        if not isinstance(rates, list):
            raise ValueError("Framerates must be a list")
        if not all(isinstance(x, (int, float)) for x in rates):
            raise ValueError("Framerates must be numbers")
        self._framerates = rates.copy()

    # --- Resolution Property --- #
    @property
    def resolution(self):
        """List of resolutions for detected cameras."""
        return self._resolution.copy()

    @resolution.setter
    def resolution(self, resolutions):
        """Set resolutions for cameras.
        
        Args:
            resolutions (list): List of (width, height) tuples
        """
        if not isinstance(resolutions, list):
            raise ValueError("Resolutions must be a list")
        if not all(isinstance(x, tuple) and len(x) == 2 for x in resolutions):
            raise ValueError("Each resolution must be a (width, height) tuple")
        self._resolution = resolutions.copy()

    # --- Camera Slots Property --- #
    @property
    def camera_slots(self):
        """Dictionary mapping camera indices to UI slots."""
        return self._camera_slots.copy()

    @camera_slots.setter
    def camera_slots(self, slots):
        """Set camera slot mappings.
        
        Args:
            slots (dict): Dictionary mapping camera indices to UI slots
        """
        if not isinstance(slots, dict):
            raise ValueError("Camera slots must be a dictionary")
        self._camera_slots = slots.copy()

    # --- Camera Count Property --- #
    @property
    def camera_count(self):
        """Number of currently available cameras."""
        return len(self._available_cameras)

    def detect_available_cameras(self, max_cameras=2):
        """Detect and initialize available cameras."""
        temp_cameras = []
        temp_framerates = []
        temp_resolutions = []

        for i in range(max_cameras):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, _ = cap.read()
                if ret:
                    temp_cameras.append(i)
                    temp_framerates.append(int(cap.get(cv2.CAP_PROP_FPS)))
                    temp_resolutions.append((
                        int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    ))
            cap.release()
        
        # Update all properties at once to maintain consistency
        self.available_cameras = temp_cameras
        self.framerates = temp_framerates
        self.resolution = temp_resolutions
        
        # Initialize camera workers
        for camera_index in self._available_cameras:
            worker = Camera(camera_index, self._save_directory, self.file_name)
            worker.ImageUpdate.connect(
                lambda image, idx=camera_index: self.update_camera_feed(image, idx)
            )
            worker.start()
            self._camera_workers[camera_index] = worker

    def update_camera_feed(self, image, camera_index):
        """Update camera feed in UI slot."""
        if camera_index in self._camera_slots:
            self._camera_slots[camera_index].setPixmap(QPixmap.fromImage(image))

    def close_all_cameras(self):
        """Close all active camera workers."""
        for worker in self._camera_workers.values():
            worker.stop()
            worker.wait() 
        self._camera_workers.clear()
        self.available_cameras = []
        self.framerates = []
        self.resolution = []

    def start_recording_all_cameras(self):
        """Start recording on all active cameras."""
        for worker in self._camera_workers.values():
            worker.start_recording()

    def stop_recording_all_cameras(self):
        """Stop recording on all active cameras."""
        for worker in self._camera_workers.values():
            worker.stop_recording()
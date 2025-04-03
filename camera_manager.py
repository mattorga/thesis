from PyQt5.QtCore import (
    QThread, 
    pyqtSignal, 
    Qt, 
    QPropertyAnimation, 
    QEasingCurve, 
    QVariantAnimation,
    QSequentialAnimationGroup
)
from PyQt5.QtGui import QImage, QPixmap, QColor
from PyQt5.QtWidgets import QPushButton, QMessageBox
import cv2
import os

class GlowingButton(QPushButton):
    """A button that can display a pulsating glow effect while recording is active."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Store the default style so we can revert back when not glowing
        self.default_style = self.styleSheet()
        
        # Create a sequential animation group for the proper pulsating effect
        self.animation_group = QSequentialAnimationGroup()
        
        # Create the glow up animation
        self.glow_up_animation = QVariantAnimation()
        self.glow_up_animation.setStartValue(0)
        self.glow_up_animation.setEndValue(100)
        self.glow_up_animation.setDuration(1000)  # 1 second to glow up
        self.glow_up_animation.setEasingCurve(QEasingCurve.InQuad)  # Ease in
        self.glow_up_animation.valueChanged.connect(self.update_glow)
        
        # Create the glow down animation
        self.glow_down_animation = QVariantAnimation()
        self.glow_down_animation.setStartValue(100)
        self.glow_down_animation.setEndValue(0)
        self.glow_down_animation.setDuration(1000)  # 1 second to fade down
        self.glow_down_animation.setEasingCurve(QEasingCurve.OutQuad)  # Ease out
        self.glow_down_animation.valueChanged.connect(self.update_glow)
        
        # Add both animations to the sequential group
        self.animation_group.addAnimation(self.glow_up_animation)
        self.animation_group.addAnimation(self.glow_down_animation)
        
        # Set the group to loop infinitely
        self.animation_group.setLoopCount(-1)
        
        # Flag to track if we're in recording state
        self.is_recording = False
    
    def start_glowing(self):
        """Start the glowing animation."""
        if not self.is_recording:
            self.is_recording = True
            self.animation_group.start()
            
            # Change the button text to indicate it's recording
            self.setText("Recording...")
    
    def stop_glowing(self):
        """Stop the glowing animation with a smooth fade-out."""
        if self.is_recording:
            self.is_recording = False
            
            # Stop the pulsing animation group
            self.animation_group.stop()
            
            # Create a fade-out animation
            self.fade_animation = QVariantAnimation()
            
            # Get current value to start from for smooth transition
            current_value = 0
            if self.animation_group.currentAnimation() == self.glow_up_animation:
                current_value = self.glow_up_animation.currentValue()
            else:
                current_value = self.glow_down_animation.currentValue()
            
            self.fade_animation.setStartValue(current_value)
            self.fade_animation.setEndValue(0)
            self.fade_animation.setDuration(500)   # Half-second fade
            self.fade_animation.setEasingCurve(QEasingCurve.OutQuad)  # Smooth fade out
            
            # Connect the fade animation
            self.fade_animation.valueChanged.connect(self.update_glow)
            
            # When fade completes, restore the original state
            self.fade_animation.finished.connect(self.restore_original_state)
            
            # Start the fade animation
            self.fade_animation.start()
    
    def restore_original_state(self):
        """Restore the button to its original state after animation finishes."""
        # Apply the original style
        self.setStyleSheet(self.default_style)
        
        # Restore the button text
        self.setText("Start Recording")
    
    def update_glow(self, value):
        """Update the button's glow effect based on the current animation value."""
        # Calculate the intensity of the glow (0-100)
        intensity = value
        
        # Create colors for the background gradient
        start_color = QColor(37, 31, 28)  # The dark color from styles.qss (#251F1C)
        end_color = QColor(255, 255, 255)  # White for maximum glow
        
        # Interpolate between the colors based on intensity
        r = start_color.red() + ((end_color.red() - start_color.red()) * intensity / 100)
        g = start_color.green() + ((end_color.green() - start_color.green()) * intensity / 100)
        b = start_color.blue() + ((end_color.blue() - start_color.blue()) * intensity / 100)
        
        # Create a color that's a blend between the start and end colors
        blend_color = QColor(int(r), int(g), int(b))
        
        # Determine text color based on background brightness
        # Use black text on light backgrounds, white text on dark backgrounds
        text_color = "black" if intensity > 50 else "white"
        
        # Set the new style with the blended color while maintaining the border
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {blend_color.name()};
                color: {text_color};
                border-radius: 6px;
                border: 1px solid #D0D0D0;
            }}
        """)
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
        self._is_recording = False
        
        # Replace the start recording button with a glowing button
        self.setup_glowing_record_button()
        
        # Initialize UI button states correctly
        self.update_ui_button_states()

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
        # Update UI button states whenever camera list changes
        self.update_ui_button_states()

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

    # --- Is Recording Property --- #
    @property
    def is_recording(self):
        """Whether recording is currently in progress."""
        return self._is_recording
        
    @is_recording.setter
    def is_recording(self, value):
        """Set the recording state.
        
        Args:
            value (bool): Whether recording is active
        """
        self._is_recording = value
        # Update UI button states whenever recording state changes
        self.update_ui_button_states()

    def setup_glowing_record_button(self):
        """Replace the standard recording button with a glowing one."""
        # Get reference to the original button
        original_button = self.main_window.ui.startRecordingButton
        
        # Create a new glowing button with the same properties
        glowing_button = GlowingButton("Start Recording", self.main_window.ui.camerasPage)
        glowing_button.setGeometry(original_button.geometry())
        glowing_button.setFont(original_button.font())
        glowing_button.setObjectName("startRecordingButton")
        
        # Connect the new button to the original function
        # We'll use a lambda to have access to both buttons
        glowing_button.clicked.connect(lambda: self.on_start_recording_with_glow(glowing_button))
        
        # Store the original button's click handler
        self.original_start_recording = self.main_window.on_start_recording
        
        # Override the main window's start_recording method to use our glowing button
        self.main_window.on_start_recording = lambda: self.on_start_recording_with_glow(glowing_button)
        
        # Also store the original stop_recording method
        self.original_stop_recording = self.main_window.on_stop_recording
        
        # Override the main window's stop_recording method
        self.main_window.on_stop_recording = lambda: self.on_stop_recording_with_glow(glowing_button)
        
        # Hide the original button
        original_button.hide()
        
        # Show the new button
        glowing_button.show()
        
        # Store a reference to both buttons
        self.original_record_button = original_button
        self.glowing_record_button = glowing_button
        
        # Initially disable the Start Recording button (will be enabled when cameras are detected)
        glowing_button.setEnabled(False)

    def on_start_recording_with_glow(self, button):
        """Start recording with glowing effect, with overwrite confirmation."""
        try:
            # Check if there are existing video files in the save directory
            if self._save_directory:
                videos_dir = os.path.join(self._save_directory, "videos")
                if os.path.exists(videos_dir):
                    # Look for .avi files
                    avi_files = [f for f in os.listdir(videos_dir) if f.lower().endswith('.avi')]
                    
                    # If .avi files exist, prompt for confirmation
                    if avi_files:
                        reply = QMessageBox.question(
                            self.main_window,
                            "Existing Recordings",
                            f"There are {len(avi_files)} existing video recordings in this trial folder. Do you want to continue and record new videos?",
                            QMessageBox.Yes | QMessageBox.No,
                            QMessageBox.No  # Default to No to prevent accidental overwriting
                        )
                        
                        # If user chooses not to continue, abort recording
                        if reply == QMessageBox.No:
                            return
                        
                        # User chose to continue - modify camera workers to overwrite files
                        for worker in self._camera_workers.values():
                            # Override the get_unique_filename method to force overwriting
                            worker.get_unique_filename = lambda camera_number: os.path.join(
                                videos_dir, 
                                f'{self._file_name}_cam{camera_number+1}.avi'
                            )
            
            # Proceed with original recording function
            self.original_start_recording()
            
            # Start the glowing effect
            button.start_glowing()
            
            # Set recording state to true
            self.is_recording = True
            
        except Exception as e:
            print(f"Error in on_start_recording_with_glow: {str(e)}")
            # Ensure we call the original function even if our addition fails
            self.original_start_recording()
            button.start_glowing()
            self.is_recording = True
        
    def on_stop_recording_with_glow(self, button):
        """Stop recording and stop the glowing effect."""
        # Call the original stop recording function
        self.original_stop_recording()
        
        # Stop the glowing effect
        button.stop_glowing()
        
        # Set recording state to false
        self.is_recording = False

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
            
        # Update UI buttons based on camera availability
        self.update_ui_button_states()

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
        
        # Make sure to update button states after closing cameras
        self.update_ui_button_states()

    def start_recording_all_cameras(self):
        """Start recording on all active cameras."""
        for worker in self._camera_workers.values():
            worker.start_recording()

    def stop_recording_all_cameras(self):
        """Stop recording on all active cameras."""
        for worker in self._camera_workers.values():
            worker.stop_recording()
            
    def update_ui_button_states(self):
        """Update UI button states based on camera availability and recording status."""
        has_cameras = len(self._available_cameras) > 0
        is_recording = self.is_recording
        
        # Get references to UI buttons
        start_recording_button = self.glowing_record_button
        close_cameras_button = self.main_window.ui.closeCamerasButton
        stop_recording_button = self.main_window.ui.stopRecordingButton
        
        # Enable/disable buttons based on state
        start_recording_button.setEnabled(has_cameras and not is_recording)
        close_cameras_button.setEnabled(has_cameras and not is_recording)
        stop_recording_button.setEnabled(has_cameras and is_recording)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QMessageBox, QProgressDialog
from enum import Enum, auto

class ProcessState(Enum):
    """Enum to track the current state of processing"""
    POSE_ESTIMATION = auto()
    SYNCHRONIZATION = auto()
    TRIANGULATION = auto()
    FILTERING = auto()
    KINEMATICS = auto()
    COMPLETED = auto()
    ERROR = auto()

class ProcessWorker(QThread):
    """Worker thread for handling Pose2Sim processing pipeline"""
    
    # Signals for communication
    progressChanged = pyqtSignal(str, int)  # (status message, progress percentage)
    stateChanged = pyqtSignal(ProcessState)  # Current process state
    errorOccurred = pyqtSignal(str)  # Error message
    completed = pyqtSignal()  # Processing completed successfully
    
    def __init__(self, session_config, trial_config):
        super().__init__()
        self.session_config = session_config
        self.trial_config = trial_config
        self._is_running = True
        self.current_state = None

    def run(self):
        """Main processing loop"""
        try:
            # Define processing steps
            steps = [
                # (ProcessState.POSE_ESTIMATION, self._run_pose_estimation, "Running pose estimation"),
                # (ProcessState.SYNCHRONIZATION, self._run_synchronization, "Running synchronization"),
                # (ProcessState.TRIANGULATION, self._run_triangulation, "Running triangulation"),
                (ProcessState.FILTERING, self._run_filtering, "Running filtering"),
                # (ProcessState.KINEMATICS, self._run_kinematics, "Running kinematics")
            ]
            
            # Execute steps sequentially
            for i, (state, func, message) in enumerate(steps):
                if not self._is_running:
                    return
                
                self.current_state = state
                self.stateChanged.emit(state)
                self.progressChanged.emit(message, (i * 20))
                
                # Run the process step
                func()
                
                # Update progress
                self.progressChanged.emit(f"Completed {message.lower()}", ((i + 1) * 20))
            
            # Signal completion
            self.current_state = ProcessState.COMPLETED
            self.stateChanged.emit(ProcessState.COMPLETED)
            self.progressChanged.emit("Processing completed", 100)
            self.completed.emit()
            
        except Exception as e:
            self.current_state = ProcessState.ERROR
            self.stateChanged.emit(ProcessState.ERROR)
            self.errorOccurred.emit(str(e))

    def stop(self):
        """Stop the processing"""
        self._is_running = False
        self.wait()

    # def _run_pose_estimation(self):
    #     """Run pose estimation step"""
    #     if not self._is_running:
    #         return
    #     try:
    #         from Pose2Sim import Pose2Sim
    #         Pose2Sim.poseEstimation(self.trial_config)
    #     except Exception as e:
    #         raise Exception(f"Error in pose estimation: {str(e)}")

    def _run_synchronization(self):
        """Run synchronization step"""
        if not self._is_running:
            return
        try:
            from Pose2Sim import Pose2Sim
            Pose2Sim.synchronization(self.trial_config)
        except Exception as e:
            raise Exception(f"Error in synchronization: {str(e)}")

    def _run_triangulation(self):
        """Run triangulation step"""
        if not self._is_running:
            return
        try:
            from Pose2Sim import Pose2Sim
            Pose2Sim.triangulation(self.trial_config)
        except Exception as e:
            raise Exception(f"Error in triangulation: {str(e)}")

    def _run_filtering(self):
        """Run filtering step"""
        if not self._is_running:
            return
        try:
            from Pose2Sim import Pose2Sim
            Pose2Sim.filtering(self.trial_config)
        except Exception as e:
            raise Exception(f"Error in filtering: {str(e)}")

    def _run_kinematics(self):
        """Run kinematics step"""
        if not self._is_running:
            return
        try:
            from Pose2Sim import Pose2Sim
            Pose2Sim.kinematics(self.trial_config)
        except Exception as e:
            raise Exception(f"Error in kinematics: {str(e)}")

class ProcessManager:
    """Manages the processing pipeline and UI interactions"""
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.worker = None
        self.progress_dialog = None
        
    def start_processing(self, session_config, trial_config):
        """Start the processing pipeline"""
        # Create and configure the progress dialog
        self.progress_dialog = QProgressDialog("Initializing processing...", "Cancel", 0, 100, self.main_window)
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setWindowTitle("Processing")
        self.progress_dialog.setAutoClose(False)
        self.progress_dialog.setAutoReset(False)
        
        # Create and configure the worker
        self.worker = ProcessWorker(session_config, trial_config)
        
        # Connect signals
        self.worker.progressChanged.connect(self._update_progress)
        self.worker.errorOccurred.connect(self._handle_error)
        self.worker.completed.connect(self._handle_completion)
        self.progress_dialog.canceled.connect(self.worker.stop)
        
        # Start processing
        self.worker.start()
        self.progress_dialog.show()
    
    def _update_progress(self, message, progress):
        """Update the progress dialog"""
        if self.progress_dialog:
            self.progress_dialog.setLabelText(message)
            self.progress_dialog.setValue(progress)
    
    def _handle_error(self, error_message):
        """Handle processing errors"""
        if self.progress_dialog:
            self.progress_dialog.close()
            
        QMessageBox.critical(
            self.main_window,
            "Processing Error",
            f"An error occurred during processing:\n{error_message}"
        )
    
    def _handle_completion(self):
        """Handle successful completion"""
        if self.progress_dialog:
            self.progress_dialog.close()
            
        QMessageBox.information(
            self.main_window,
            "Processing Complete",
            "All processing steps completed successfully!"
        )
    
    def cleanup(self):
        """Clean up resources"""
        if self.worker:
            self.worker.stop()
            self.worker = None
        
        if self.progress_dialog:
            self.progress_dialog.close()
            self.progress_dialog = None
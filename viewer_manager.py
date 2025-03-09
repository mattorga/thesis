import sys
import threading
import http.server
import socketserver
import os
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QUrl, pyqtSlot, QTimer, QObject, pyqtSignal


class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP request handler with CORS support"""
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()


class CustomWebEnginePage(QWebEnginePage):
    """Custom WebEnginePage to capture JavaScript console logs"""
    
    @pyqtSlot(int, str, int, str)
    def javaScriptConsoleMessage(self, level, message, line, source):
        levels = ["Info", "Warning", "Error"]
        level_name = levels[level] if level < len(levels) else "Unknown"
        print(f"[JS {level_name}] {source}:{line} - {message}")


class WebBridge(QObject):
    """Bridge between PyQt and JavaScript"""
    
    # Signal to update the PyQt slider
    sliderUpdateSignal = pyqtSignal(float)
    
    @pyqtSlot(float)
    def updateSliderFromWeb(self, time_value):
        """Slot to receive time updates from JavaScript"""
        self.sliderUpdateSignal.emit(time_value)


class ViewerManager:
    """Manages the 3D FBX viewer integration"""
    
    def __init__(self, visualization_widget):
        """
        Initialize the viewer manager
        
        Args:
            visualization_widget: The widget to embed the viewer in
        """
        self.visualization_widget = visualization_widget
        self.port = 8000
        self.server_thread = None
        self.web_bridge = WebBridge()
        
        # Clear any existing layout
        if self.visualization_widget.layout():
            self._clear_layout(self.visualization_widget.layout())
        
        # Create a new layout
        self.layout = QVBoxLayout(self.visualization_widget)
        self.visualization_widget.setLayout(self.layout)
        
        # Create WebEngineView
        self.browser = QWebEngineView(self.visualization_widget)
        self.page = CustomWebEnginePage(self.browser)
        self.browser.setPage(self.page)
        
        # Add browser to layout
        self.layout.addWidget(self.browser)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Start server if not already running
        self._start_server()
    
    def _clear_layout(self, layout):
        """Clear all items from a layout"""
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self._clear_layout(item.layout())
    
    def _start_server(self):
        """Start a local HTTP server for serving viewer files"""
        def run_server():
            # Try to start the server on the specified port
            try:
                with socketserver.TCPServer(("", self.port), CORSRequestHandler) as httpd:
                    # print(f"FBX Viewer server started on port {self.port}")
                    httpd.serve_forever()
            except OSError as e:
                print(f"Failed to start server on port {self.port}: {e}")
                # Try an alternative port
                alternate_port = 8080
                try:
                    with socketserver.TCPServer(("", alternate_port), CORSRequestHandler) as httpd:
                        self.port = alternate_port
                        print(f"FBX Viewer server started on alternative port {self.port}")
                        httpd.serve_forever()
                except Exception as e2:
                    print(f"Failed to start server on alternative port: {e2}")
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
        
        # Give the server a moment to start
        QTimer.singleShot(500, self.initialize_viewer)
    
    def initialize_viewer(self):
        """Initialize the viewer by loading the HTML page"""
        # Create a path relative to the current file (viewer_manager.py)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(current_dir, "web", "viewer.html")
        
        # Convert to file URL format
        if os.name == 'nt':  # Windows
            viewer_url = QUrl.fromLocalFile(html_path)
        else:  # macOS, Linux
            viewer_url = QUrl("file://" + html_path)
        
        print(f"Loading viewer from: {viewer_url.toString()}")
        self.browser.load(viewer_url)
        
        # After the page loads, we can interact with it
        self.browser.loadFinished.connect(self._on_page_loaded)
    
    def _on_page_loaded(self, success):
        """Called when the viewer page finishes loading"""
        if success:
            print("Viewer page loaded successfully")
            # Set up the two-way communication bridge with JavaScript
            self._setup_js_bridge()
        else:
            print("Failed to load viewer page")
    
    def _setup_js_bridge(self):
        """Set up the communication bridge between PyQt and JavaScript"""
        # First, create and register the web channel
        channel = QWebChannel(self.page)
        channel.registerObject("pyQtBridge", self.web_bridge)
        self.page.setWebChannel(channel)
        
        # After the channel is set up, run the JavaScript to connect to it
        js_channel_connection = """
        // Create a callback for when the qt web channel is ready
        new QWebChannel(qt.webChannelTransport, function(channel) {
            // Store the bridge object globally
            window.pyQtBridge = channel.objects.pyQtBridge;
            
            // Now that we have the bridge, set up the connection for sending time updates
            window.qt.updateSliderFromWeb = function(timeValue) {
                console.log("Sending time update to PyQt:", timeValue);
                if (window.pyQtBridge) {
                    window.pyQtBridge.updateSliderFromWeb(timeValue);
                } else {
                    console.error("pyQtBridge not available");
                }
            };
            
            console.log("JavaScript bridge initialized successfully");
        });
        """
        
        # First make sure QWebChannel script is loaded
        self.page.runJavaScript("""
        if (typeof QWebChannel === 'undefined') {
            console.log("Loading QWebChannel script...");
            var script = document.createElement('script');
            script.src = 'qrc:///qtwebchannel/qwebchannel.js';
            script.onload = function() {
                console.log("QWebChannel script loaded");
            };
            document.head.appendChild(script);
        } else {
            console.log("QWebChannel already available");
        }
        """)
        

        
        # Initialize a temporary qt object if it doesn't exist yet
        self.page.runJavaScript("""
        if (!window.qt) {
            window.qt = {
                updateSliderFromWeb: function(timeValue) {
                    console.log("Temporary function - waiting for bridge to initialize");
                }
            };
        }
        """)
        
        # Connect the signal to the main window's slot
        if hasattr(self.visualization_widget.window(), 'update_slider_from_web'):
            self.web_bridge.sliderUpdateSignal.connect(
                self.visualization_widget.window().update_slider_from_web
            )
    
    def sync_with_slider(self, value, max_value):
        """
        Synchronize the 3D animation with the slider value
        
        Args:
            value (int): The current slider value
            max_value (int): The maximum slider value
        """
        # Calculate normalized time (0.0 to 1.0)
        if max_value > 0:
            normalized_time = value / max_value
            
            # Set the animation time via JavaScript
            js_code = f"if (typeof setAnimationTime === 'function') {{ setAnimationTime({normalized_time}); }}"
            self.page.runJavaScript(js_code)
    
    def set_playing(self, is_playing):
      """
      Set the play/pause state of the 3D animation
      
      Args:
          is_playing (bool): True to play, False to pause
      """
      # Update the animation state via JavaScript
      js_code = f"""
      if (typeof setPlaying === 'function') {{ 
          setPlaying({str(is_playing).lower()}); 
      }}
      """
      self.page.runJavaScript(js_code)
  
    def set_speed(self, speed_multiplier):
        """
        Set the animation playback speed in the 3D viewer
        
        Args:
            speed_multiplier (float): Playback speed multiplier (e.g., 0.5, 1.0, 2.0)
        """
        # Update the animation speed via JavaScript
        js_code = f"""
        if (typeof window.animationSpeedSelector !== 'undefined') {{
            // Try to find the closest speed in the selector
            const selector = document.getElementById('animationSpeed');
            if (selector) {{
                // Look for exact match first
                let found = false;
                for (let i = 0; i < selector.options.length; i++) {{
                    if (parseFloat(selector.options[i].value) === {speed_multiplier}) {{
                        selector.selectedIndex = i;
                        found = true;
                        break;
                    }}
                }}
                
                // If no exact match, set the custom value
                if (!found && typeof timeScaleBuffer !== 'undefined') {{
                    timeScaleBuffer = {speed_multiplier};
                    if (isPlaying && mixer) {{
                        mixer.timeScale = {speed_multiplier};
                    }}
                }}
                
                // Trigger the change event
                const event = new Event('change');
                selector.dispatchEvent(event);
            }}
        }}
        """
        self.page.runJavaScript(js_code)

    def set_center_animation(self, is_center_enabled):
      """
      Set whether the animation should be centered in the view
      
      Args:
          is_center_enabled (bool): True to center animation, False to disable centering
      """
      # Update the center animation state via JavaScript
      js_code = f"""
      if (typeof setCenterAnimation === 'function') {{ 
          setCenterAnimation({str(is_center_enabled).lower()}); 
      }}
      """
      self.page.runJavaScript(js_code)
      
    def set_axis_visible(self, is_visible):
        """
        Set whether the x,y,z axes should be visible
        
        Args:
            is_visible (bool): True to show axes, False to hide them
        """
        # Update the axis visibility via JavaScript
        js_code = f"""
        if (typeof setAxisVisible === 'function') {{ 
            setAxisVisible({str(is_visible).lower()}); 
        }}
        """
        self.page.runJavaScript(js_code)
    def set_fbx_path(self, fbx_path):
        """
        Set the path to the FBX file to load
        
        Args:
            fbx_path (str): Path to the FBX file
        """
        # Normalize the path for JavaScript
        normalized_path = fbx_path.replace('\\', '/')
        
        # After the page loads, set the FBX path via JavaScript
        js_code = f"""
        if (typeof loadFbxModel === 'function') {{
            loadFbxModel('{normalized_path}');
        }} else {{
            // If loadFbxModel is not available yet, store the path for later use
            window.pendingFbxPath = '{normalized_path}';
        }}
        """
        self.page.runJavaScript(js_code)
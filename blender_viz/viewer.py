import sys
import threading
import http.server
import socketserver
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl, pyqtSlot


class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()


class CustomWebEnginePage(QWebEnginePage):
    """ Custom WebEnginePage to capture JavaScript console logs """

    @pyqtSlot(int, str, int, str)
    def javaScriptConsoleMessage(self, level, message, line, source):
        levels = ["Info", "Warning", "Error"]
        level_name = levels[level] if level < len(levels) else "Unknown"
        print(f"[JS {level_name}] {source}:{line} - {message}")


class FBXViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FBX Viewer with Controls")

        # Create a WebEngineView and set a custom page to capture console logs
        self.browser = QWebEngineView()
        self.page = CustomWebEnginePage(self.browser)
        self.browser.setPage(self.page)

        # Load the HTML file
        self.browser.load(QUrl("file:///D:/Miro Hernandez/Documents/openpose-1.7.0-binaries-win64-gpu-python3.7-flir-3d_recommended/davidpagnon Pose2Sim_Blender main Examples/viewer.html"))

        # Set up the layout
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Start local server in a separate thread
        self.start_server()

    def start_server(self):
        """Start local server with CORS support in a separate thread"""
        def run_server():
            with socketserver.TCPServer(("", 8000), CORSRequestHandler) as httpd:
                print("Serving at port 8000")
                httpd.serve_forever()

        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()

    def closeEvent(self, event):
        """Cleanup on window close"""
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = FBXViewer()
    viewer.resize(800, 600)
    viewer.show()
    sys.exit(app.exec_())

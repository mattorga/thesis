import sys
from styles import Styles
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, 
                            QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPalette, QColor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GaitScape")
        
        # Set size constraints
        self.setMinimumSize(1280, 800)
        self.setFixedSize(1280, 800)
        
        # Create central widget and main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QHBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
  
        ### Initialize UI components
        # Sidebar
        self.sidebar = Sidebar()
        self.layout.addWidget(self.sidebar)

        self.main_content = QWidget()
        self.main_content.setStyleSheet("""
          background-color: #FFFCF8;
        """)
        self.layout.addWidget(self.main_content)

class Sidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.expanded = False
        self.animation = None
        self.collapsed_width = 67
        self.expanded_width = 195

        self.setFixedWidth(self.collapsed_width)
        self.setAutoFillBackground(True)
        
        # Create layout for the sidebar
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # Create container widget
        self.container = QWidget()
        self.container.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
            }
        """)
        
        # Create and configure drop shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(5)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 255))  # Last parameter is opacity (0-255)
        
        # Apply drop shadow to container
        self.container.setGraphicsEffect(shadow)
        self.layout.addWidget(self.container)
        
    def enterEvent(self, event):
        self.animate_sidebar(self.expanded_width)

    def leaveEvent(self, event):
        self.animate_sidebar(self.collapsed_width)

    def animate_sidebar(self, target_width):
        if self.animation and self.animation.state() == QPropertyAnimation.Running:
          self.animation.stop()
        
        self.animation = QPropertyAnimation(self, b"minimumWidth")
        self.animation.setDuration(200)
        self.animation.setStartValue(self.width())
        self.animation.setEndValue(target_width)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
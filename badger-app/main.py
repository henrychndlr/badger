import sys
import serial
import serial.tools.list_ports
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer, QByteArray
from PyQt6.QtGui import QImage, QPixmap

BADGER_VID = 0x2E8A  # Raspberry Pi (Pimoroni)
BADGER_PID = 0x0005  # MicroPython Board

class BadgerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Badger 2040 W Manager")
        self.setGeometry(200, 200, 600, 400)
        self.setStyleSheet("background-color: #121212; color: #FFFFFF;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.status_label = QLabel("Searching for Badger 2040 W...")
        self.status_label.setStyleSheet("font-size: 16px; padding: 10px;")
        self.layout.addWidget(self.status_label)

        self.screen_label = QLabel()  # For displaying the screen image
        self.layout.addWidget(self.screen_label)

        self.central_widget.setLayout(self.layout)

        self.badger_port = None
        self.serial_conn = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.detect_badger)
        self.timer.start(2000)  # Check every 2 seconds

    def detect_badger(self):
        """Scan for Badger 2040 W USB connection."""
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if port.vid == BADGER_VID and port.pid == BADGER_PID:
                self.badger_port = port.device
                self.status_label.setText(f"Badger 2040 W connected: {self.badger_port}")
                self.timer.stop()
                self.start_reading()
                return
        self.status_label.setText("Badger 2040 W not found. Please connect via USB.")

    def start_reading(self):
        """Initialize USB communication and start screen capture loop."""
        try:
            self.serial_conn = serial.Serial(self.badger_port, 115200, timeout=1)
            self.status_label.setText("Connected! Fetching screen data...")
            self.screen_timer = QTimer()
            self.screen_timer.timeout.connect(self.request_screen)
            self.screen_timer.start(500)  # Refresh every 500ms
        except Exception as e:
            self.status_label.setText(f"Error connecting: {e}")

    def request_screen(self):
        """Request screen data from Badger 2040 W."""
        if self.serial_conn and self.serial_conn.is_open:
            try:
                self.serial_conn.write(b'CAPTURE\r\n')
                self.serial_conn.flush()
                raw_data = self.serial_conn.read(2960)  # Expected screen buffer size
                if raw_data:
                    self.update_screen(raw_data)
            except Exception as e:
                self.status_label.setText(f"Error reading screen: {e}")

    def update_screen(self, raw_data):
        """Convert received raw screen data to an image and display it."""
        try:
            # Convert raw bytes to numpy array (Badger has a 296x128 1-bit screen)
            screen_array = np.frombuffer(raw_data, dtype=np.uint8)
            screen_array = np.unpackbits(screen_array)  # Convert to black/white pixels
            screen_array = screen_array[:296*128].reshape((128, 296)) * 255  # Reshape to match screen

            # Create QImage and display it
            height, width = screen_array.shape
            qimg = QImage(screen_array.data, width, height, width, QImage.Format.Format_Grayscale8)
            pixmap = QPixmap.fromImage(qimg)
            self.screen_label.setPixmap(pixmap)
        except Exception as e:
            self.status_label.setText(f"Error processing image: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BadgerApp()
    window.show()
    sys.exit(app.exec())

from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QThread, pyqtSignal


class WorkerThread(QThread):
    finished = pyqtSignal()

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

    def run(self):
        self.controller.start_browsers()
        self.finished.emit()


class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("SeleniumBase Automation")
        self.setGeometry(300, 200, 420, 220)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Automatización con SeleniumBase")
        self.label.setAlignment(Qt.AlignCenter)

        self.button = QPushButton("Abrir Navegadores")
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                font-size: 15px;
                padding: 10px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #1e7e34;
            }
        """)
        self.button.clicked.connect(self.start_process)

        layout.addWidget(self.label)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_process(self):
        self.label.setText("Ejecutando...")
        self.button.setEnabled(False)

        self.thread = WorkerThread(self.controller)
        self.thread.finished.connect(self.on_finished)
        self.thread.start()

    def on_finished(self):
        self.label.setText("Finalizado")
        self.button.setEnabled(True)

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt


class LoadingOverlay(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet("background: rgba(0,0,0,120);")

        layout = QVBoxLayout()
        label = QLabel("Загрузка...")
        label.setStyleSheet("color: white; font-size: 20px;")

        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

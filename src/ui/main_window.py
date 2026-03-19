from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QSplitter, QPushButton, QVBoxLayout
)
from PyQt6.QtCore import Qt

from src.ui.views.project_view import ProjectView
from src.ui.views.structure_panel import StructurePanel


class MainWindow(QMainWindow):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Система контроля версий НПА")
        self.resize(1200, 800)

        self._init_ui()

    def _init_ui(self):
        root = QWidget()
        layout = QVBoxLayout()

        # верхняя панель
        sync_btn = QPushButton("Синхронизировать")
        sync_btn.clicked.connect(self.sync)

        layout.addWidget(sync_btn)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        self.project_view = ProjectView(self.controller)
        self.structure_panel = StructurePanel()

        splitter.addWidget(self.project_view)
        splitter.addWidget(self.structure_panel)

        splitter.setSizes([900, 300])

        layout.addWidget(splitter)

        root.setLayout(layout)
        self.setCentralWidget(root)

    def sync(self):
        self.controller.sync_service.scan_project_files()

from pathlib import Path

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton, QFileDialog
)


class StartupDialog(QDialog):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("Выбор проекта")

        layout = QVBoxLayout()

        open_btn = QPushButton("Открыть проект")
        create_btn = QPushButton("Создать проект")

        open_btn.clicked.connect(self.open_project)
        create_btn.clicked.connect(self.create_project)

        layout.addWidget(open_btn)
        layout.addWidget(create_btn)

        self.setLayout(layout)

    def open_project(self):
        path = QFileDialog.getExistingDirectory(self)
        if path:
            self.controller.open_project(Path(path))
            self.accept()

    def create_project(self):
        path = QFileDialog.getExistingDirectory(self)
        if path:
            self.controller.create_project(Path(path))
            self.accept()

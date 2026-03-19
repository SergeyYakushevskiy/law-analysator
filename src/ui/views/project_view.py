from PyQt6.QtWidgets import QWidget, QHBoxLayout

from src.ui.views.version_selector import VersionSelector
from src.ui.views.diff_view import DiffView


class ProjectView(QWidget):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        layout = QHBoxLayout()

        self.left_selector = VersionSelector(controller)
        self.right_selector = VersionSelector(controller)

        self.diff_view = DiffView(controller)

        layout.addWidget(self.left_selector)
        layout.addWidget(self.right_selector)

        self.setLayout(layout)

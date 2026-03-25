from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget

class FileListWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("file_list")
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.list = QListWidget()
        self.list.setObjectName("file_list_widget")
        layout.addWidget(self.list)
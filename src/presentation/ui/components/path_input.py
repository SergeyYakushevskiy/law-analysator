from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton

class PathInput(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("path_input")
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.line_edit = QLineEdit()
        self.line_edit.setObjectName("path_line_edit")
        self.line_edit.setPlaceholderText("Путь к папке проекта...")
        layout.addWidget(self.line_edit, stretch=1)

        self.browse_button = QPushButton("Обзор")
        self.browse_button.setObjectName("browse_button")
        self.browse_button.setFixedWidth(100)
        layout.addWidget(self.browse_button)

    def set_path(self, path: str):
        self.line_edit.setText(path)

    def get_path(self) -> str:
        return self.line_edit.text()
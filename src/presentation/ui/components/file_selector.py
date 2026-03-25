from PyQt6.QtWidgets import QWidget, QHBoxLayout, QComboBox, QLabel, QSizePolicy, QSpacerItem


class FileSelector(QWidget):
    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("file_selector")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(title)
        layout.addWidget(self.label)

        layout.addStretch()

        self.combo = QComboBox()
        layout.addWidget(self.combo, stretch=1)

    def set_files(self, files: list[str]):
        self.combo.clear()
        self.combo.addItems(files)

    def get_selected(self) -> str:
        return self.combo.currentText()

from PyQt6.QtWidgets import QLabel

class SectionHeader(QLabel):
    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self.setObjectName("section_header")
        self.setFixedHeight(30)
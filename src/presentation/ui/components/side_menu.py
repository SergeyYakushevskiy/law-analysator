from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QButtonGroup

class SideMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("side_menu")
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 40, 0, 0)
        layout.setSpacing(5)

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

    def _create_button(self, text: str) -> QPushButton:
        button = QPushButton(text)
        button.setObjectName("menu_button")
        button.setCheckable(True)
        self.button_group.addButton(button)
        return button
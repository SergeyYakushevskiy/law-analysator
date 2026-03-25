from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton

class ActionButton(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("action_button")
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        layout.addStretch()

        # Основное действие (справа)
        self.primary_button = QPushButton()
        self.primary_button.setObjectName("primary_button")
        layout.addWidget(self.primary_button)
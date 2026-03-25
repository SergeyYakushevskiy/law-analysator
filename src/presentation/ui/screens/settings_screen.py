from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy, QComboBox, QHBoxLayout

from src.presentation.ui.components.action_buttons import ActionButton


class SettingsScreen(QWidget):
    apply_requested = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("settings_screen")
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(60, 60, 60, 60)
        layout.setSpacing(25)

        # Заголовок
        self.title_label = QLabel("Настройки приложения")
        self.title_label.setObjectName("screen_title")
        layout.addWidget(self.title_label)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Секция настроек
        self.settings_section = QWidget()
        self.theme_layout = QHBoxLayout(self.settings_section)
        self.theme_select = QComboBox()
        self.theme_select.addItems(["light", "dark"])

        self.theme_layout.addWidget(self.theme_select)
        layout.addWidget(self.settings_section)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Секция информации
        self.info_section = QWidget()

        self.info_layout = QVBoxLayout(self.info_section)

        self.app_name_label = QLabel()
        self.app_name_label.setObjectName("app_name_label")

        self.version_label = QLabel()
        self.version_label.setObjectName("version_label")

        self.info_layout.addWidget(self.app_name_label)
        self.info_layout.addWidget(self.version_label)

        layout.addWidget(self.info_section)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.actions = ActionButton()
        self.actions.primary_button.setText("Применить")

    def set_app_info(self, app_name: str, version: str):
        self.app_name_label.setText(app_name)
        self.version_label.setText(f"Версия: {version}")
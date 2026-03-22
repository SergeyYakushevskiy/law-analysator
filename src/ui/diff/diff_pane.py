from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPlainTextEdit

from src.ui.diff.render.highlighter import DocumentHighlights, DiffHighlighter
from src.ui.diff.styles import STYLESHEET


class DiffPane(QWidget):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self._highlighter = None  # Удержание ссылки для GC
        self._init_ui(title)

    def _init_ui(self, title: str):
        self.setStyleSheet(STYLESHEET)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.label = QLabel(title)
        self.editor = QPlainTextEdit()
        self.editor.setReadOnly(True)

        self.editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
        self.editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)

        layout.addWidget(self.label)
        layout.addWidget(self.editor)

    def set_content(self, text: str, highlights: DocumentHighlights, title: str):
        self.label.setText(title)
        self.editor.setPlainText(text)
        # Создаем подсветку и сохраняем ссылку
        self._highlighter = DiffHighlighter(self.editor.document(), highlights)

    def sync_scroll(self, value: int):
        self.editor.verticalScrollBar().setValue(value)
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit

from src.presentation.ui.features.highlighter import DiffHighlighter, DocumentHighlights


class DiffViewWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._highlighter = None
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.editor = QPlainTextEdit()
        self.editor.setReadOnly(True)

        self.editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
        self.editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)

        layout.addWidget(self.editor)

    def set_data(self, text: str, highlights: DocumentHighlights):
        self.editor.setPlainText(text)
        self._highlighter = DiffHighlighter(self.editor.document(), highlights)

    def sync_scroll(self, value: int):
        self.editor.verticalScrollBar().setValue(value)
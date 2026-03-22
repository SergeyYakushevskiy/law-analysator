from typing import Optional
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QScrollArea

from src.parser.document import ParsedDocument
from src.diff.change_set import ChangeSet
from src.ui.diff.diff_pane import DiffPane
from src.ui.diff.render.facade import DiffRenderer


class DiffViewWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._sync_lock = False
        self._init_ui()

    def _init_ui(self):
        self.left_pane = DiffPane("Старый документ")
        self.right_pane = DiffPane("Новый документ")

        # Синхронизация скролла с защитой от рекурсии
        self.left_pane.editor.verticalScrollBar().valueChanged.connect(self._on_left_scroll)
        self.right_pane.editor.verticalScrollBar().valueChanged.connect(self._on_right_scroll)

        inner_widget = QWidget()
        inner_layout = QHBoxLayout(inner_widget)
        inner_layout.setContentsMargins(0, 0, 0, 0)
        inner_layout.setSpacing(1)
        inner_layout.addWidget(self.left_pane)
        inner_layout.addWidget(self.right_pane)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll_area.setWidget(inner_widget)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll_area)

    def _on_left_scroll(self, value: int):
        if self._sync_lock:
            return
        self._sync_lock = True
        self.right_pane.sync_scroll(value)
        self._sync_lock = False

    def _on_right_scroll(self, value: int):
        if self._sync_lock:
            return
        self._sync_lock = True
        self.left_pane.sync_scroll(value)
        self._sync_lock = False

    def set_documents(self, old_doc: Optional[ParsedDocument], new_doc: Optional[ParsedDocument],
                      change_set: ChangeSet):
        renderer = DiffRenderer(old_doc, new_doc, change_set)

        left_res = renderer.render_old()
        right_res = renderer.render_new()

        self.left_pane.set_content(left_res.text, left_res.highlights, left_res.title)
        self.right_pane.set_content(right_res.text, right_res.highlights, right_res.title)
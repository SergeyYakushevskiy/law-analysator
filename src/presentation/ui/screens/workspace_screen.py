from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QSplitter

from src.presentation.ui.features.document_viewer import DocumentViewer
from src.presentation.ui.features.single_renderer import RenderResult
from src.presentation.ui.features.stats_panel import StatsPanel
from src.presentation.ui.features.toolbar import Toolbar


class WorkspaceScreen(QWidget):
    compare_requested = pyqtSignal(str, str)
    report_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("workspace_screen")
        self._sync_lock = False
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter()
        layout.addWidget(splitter)

        self.left_viewer = DocumentViewer("Документ 1")
        splitter.addWidget(self.left_viewer)

        self.right_viewer = DocumentViewer("Документ 2")
        splitter.addWidget(self.right_viewer)

        self.stats_panel = StatsPanel()
        self.stats_panel.hide()
        splitter.addWidget(self.stats_panel)

        self.toolbar = Toolbar()
        splitter.addWidget(self.toolbar)

    def _on_left_scroll(self, value: int):
        if self._sync_lock:
            return
        self._sync_lock = True
        self.right_viewer.sync_scroll(value)
        self._sync_lock = False

    def _on_right_scroll(self, value: int):
        if self._sync_lock:
            return
        self._sync_lock = True
        self.left_viewer.sync_scroll(value)
        self._sync_lock = False

    def _connect_signals(self):
        self.toolbar.stats_toggled.connect(self._toggle_stats)
        self.toolbar.report_requested.connect(self.report_requested)

        self.left_viewer.selector.combo.activated.connect(self._emit_compare)
        self.right_viewer.selector.combo.activated.connect(self._emit_compare)

        self._connect_scroll_sync()

    def _connect_scroll_sync(self):
        self._syncing = False

        left_scroll = self.left_viewer.diff_view.editor.verticalScrollBar()
        right_scroll = self.right_viewer.diff_view.editor.verticalScrollBar()

        left_scroll.valueChanged.connect(
            lambda value: self._on_left_scroll(value)
        )
        right_scroll.valueChanged.connect(
            lambda value: self._on_right_scroll(value)
        )

    def _emit_compare(self):
        left = self.left_viewer.get_selected()
        right = self.right_viewer.get_selected()

        if left and right:
            self.compare_requested.emit(left, right)

    def set_files(self, files: list[str]):
        self.left_viewer.set_files(files)
        self.right_viewer.set_files(files)

    def display_diff(self, old_render : RenderResult, new_render : RenderResult):
        self.left_viewer.diff_view.set_data(old_render.text, old_render.highlights)
        self.right_viewer.diff_view.set_data(new_render.text, new_render.highlights)

    def _toggle_stats(self, visible : bool):
        self.stats_panel.setVisible(visible)


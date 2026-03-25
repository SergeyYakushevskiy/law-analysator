from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTreeWidget

class DocumentTreeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("document_tree")
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.tree = QTreeWidget()
        self.tree.setObjectName("document_tree_widget")
        self.tree.setHeaderHidden(True)
        layout.addWidget(self.tree)
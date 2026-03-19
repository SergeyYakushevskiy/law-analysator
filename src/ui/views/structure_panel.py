from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget


class StructurePanel(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.list = QListWidget()

        layout.addWidget(self.list)

        self.setLayout(layout)

    def show_changes(self, change_set):
        self.list.clear()

        for change in change_set.changes:
            self.list.addItem(f"{change.change_type}: {change.node.text}")

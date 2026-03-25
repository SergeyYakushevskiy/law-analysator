from PyQt6.QtWidgets import QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt


class SortableListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sortable_list")

        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.setSelectionMode(QListWidget.SelectionMode.SingleSelection)

    def set_items(self, items: list[str]):
        self.clear()
        for item in items:
            QListWidgetItem(item, self)

    def get_items(self) -> list[str]:
        result = []
        for i in range(self.count()):
            result.append(self.item(i).text())
        return result

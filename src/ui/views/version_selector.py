from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget


class VersionSelector(QWidget):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        layout = QVBoxLayout()

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        self.setLayout(layout)

    def load_versions(self, document_id):
        self.list_widget.clear()
        versions = self.controller.version_repo.get_versions(document_id)

        for v in versions:
            self.list_widget.addItem(f"{v.id} | {v.created_at}")

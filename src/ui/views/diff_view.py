from PyQt6.QtWidgets import QWidget, QHBoxLayout, QTextEdit

from src.diff.diff_engine import DiffEngine
from src.diff.text_diff_strategy import TextDiffStrategy
from src.parser.parser_factory import ParserFactory


class DiffView(QWidget):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        layout = QHBoxLayout()

        self.left = QTextEdit()
        self.right = QTextEdit()

        layout.addWidget(self.left)
        layout.addWidget(self.right)

        self.setLayout(layout)

        self.engine = DiffEngine(TextDiffStrategy())

    def show_diff(self, path1, path2):
        parser1 = ParserFactory.get_parser(path1)
        parser2 = ParserFactory.get_parser(path2)

        doc1 = parser1.parse(path1)
        doc2 = parser2.parse(path2)

        changes = self.engine.diff(doc1, doc2)

        self.left.setText(path1.read_text())
        self.right.setText(path2.read_text())

from typing import Dict, List, Tuple
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QTextDocument

LineFormats = List[Tuple[int, int, QTextCharFormat]]
DocumentHighlights = Dict[int, LineFormats]  # Map: line_number -> formats


class DiffHighlighter(QSyntaxHighlighter):
    def __init__(self, parent: QTextDocument, highlights: DocumentHighlights):
        super().__init__(parent)
        self._highlights = highlights

    def highlightBlock(self, text: str) -> None:
        block = self.currentBlock()
        line_number = block.blockNumber()

        formats = self._highlights.get(line_number, [])
        for start, length, fmt in formats:
            self.setFormat(start, length, fmt)
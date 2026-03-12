from src.parser.document.document import ParsedDocument
from src.diff.base_strategy import BaseDiffStrategy
from src.diff.change_set import ChangeSet

class DiffEngine:
    def __init__(self, strategy: BaseDiffStrategy):
        self.strategy = strategy

    def diff(self, old_doc: ParsedDocument, new_doc: ParsedDocument) -> ChangeSet:
        return self.strategy.diff(old_doc, new_doc)

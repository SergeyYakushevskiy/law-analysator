from abc import ABC, abstractmethod
from src.parser.document.document import ParsedDocument
from src.diff.change_set import ChangeSet

class BaseDiffStrategy(ABC):
    @abstractmethod
    def diff(self, old_doc: ParsedDocument, new_doc: ParsedDocument) -> ChangeSet:
        """
        Сравнивает два ParsedDocument и возвращает ChangeSet
        """
        pass

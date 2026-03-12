from dataclasses import dataclass
from src.parser.document.node import DocumentNode
from src.diff.change_type import ChangeType

@dataclass
class Change:
    node: DocumentNode
    change_type: ChangeType
    old_text: str | None = None
    new_text: str | None = None

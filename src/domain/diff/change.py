from dataclasses import dataclass, field
from enum import Enum

from src.infrastructure.parser.structure.builder import TreeNode


class ChangeType(Enum):
    INSERT = "inserted"
    DELETE = "deleted"
    MODIFY = "modified"

    def __str__(self):
        return self.value

@dataclass
class TextChange:
    change_type: ChangeType
    start: int
    end: int

@dataclass
class NodeChange:
    node: TreeNode
    change_type: ChangeType
    text_diff: list[TextChange] = field(default_factory=list)

    def inserted(self):
        return [c for c in self.text_diff if c.change_type is ChangeType.INSERT]

    def modified(self):
        return [c for c in self.text_diff if c.change_type is ChangeType.MODIFY]

    def deleted(self):
        return [c for c in self.text_diff if c.change_type is ChangeType.DELETE]
from dataclasses import dataclass, field
from enum import Enum

from src.parser.structure.builder import TreeNode


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


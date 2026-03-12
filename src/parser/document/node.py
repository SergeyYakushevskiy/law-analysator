from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from src.parser.document.node_type import NodeType


@dataclass
class DocumentNode:
    node_type: NodeType
    text: str
    number: Optional[str] = None
    children: List["DocumentNode"] = field(default_factory=list)

    def add_child(self, node: "DocumentNode") -> None:
        self.children.append(node)

    def is_leaf(self) -> bool:
        return not self.children

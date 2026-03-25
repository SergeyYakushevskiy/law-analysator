from dataclasses import dataclass, field
from typing import List

from src.infrastructure.parser.structure.token import Token
from src.infrastructure.parser.structure.token_type import TokenType


@dataclass
class TreeNode:
    node_type: TokenType
    id: str
    level_class: int
    content: str = ""
    parent: 'TreeNode' = None
    children: List['TreeNode'] = field(default_factory=list)

    def __eq__(self, other):
        if not isinstance(other, TreeNode):
            return False
        return (
            self.node_type == other.node_type and
            self.id == other.id and
            self.level_class == other.level_class
        )

    def __hash__(self):
        return hash((self.node_type, self.id, self.level_class))

    def __repr__(self):
        return f"{self.node_type.name} (id={self.id}, level={self.level_class})"

    def add_child(self, child: 'TreeNode'):
        child.parent = self
        self.children.append(child)

    def add_content(self, text: str):
        self.content += text

class TreeBuilder:
    def __init__(self):
        self.root = TreeNode(node_type=TokenType.DOCUMENT_ROOT, id="", level_class=-1)
        self.stack: List[TreeNode] = [self.root]

    def build(self, tokens: List[Token]) -> TreeNode:
        for token in tokens:
            self._process_token(token)
        return self.root

    def _process_token(self, token):
        if token.type is TokenType.TEXT:
            if token.raw_value.strip():
                self.stack[-1].add_content(token.raw_value)
            return

        new_node = TreeNode(
            node_type=token.type,
            id=token.norm_id,
            level_class=token.level_class
        )

        if token.raw_value.strip():
            new_node.add_content(token.raw_value)

        if token.type is TokenType.PREAMBLE:
            self.root.add_child(new_node)
            self.stack = [self.root]

            return

        current_level = self.stack[-1].level_class

        if token.level_class > current_level:
            self.stack[-1].add_child(new_node)
            self.stack.append(new_node)
        else:
            while len(self.stack) > 1 and self.stack[-1].level_class >= token.level_class:
                self.stack.pop()

            parent = self.stack[-1]
            parent.add_child(new_node)
            self.stack.append(new_node)
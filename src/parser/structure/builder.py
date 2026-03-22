from dataclasses import dataclass, field
from typing import List

from src.parser.structure.token import Token
from src.parser.structure.token_type import TokenType


@dataclass
class TreeNode:
    node_type: TokenType
    id: str
    level_class: int
    content: str = ""
    children: List['TreeNode'] = field(default_factory=list)

    def add_child(self, child: 'TreeNode'):
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
            level_class=token.level_class  # <-- Сохраняем level_class
        )

        if token.raw_value.strip():
            new_node.add_content(token.raw_value)

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
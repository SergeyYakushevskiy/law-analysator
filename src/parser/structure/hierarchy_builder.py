from src.parser.document.node import DocumentNode
from src.parser.document.node_type import NodeType

from src.parser.structure.token_type import TokenType


class HierarchyBuilder:

    def build(self, tokens):

        root = DocumentNode(NodeType.DOCUMENT, "")

        stack = [root]

        for token in tokens:

            node = self._create_node(token)

            while len(stack) > 1 and not self._is_valid_parent(stack[-1], node):
                stack.pop()

            stack[-1].add_child(node)

            if token.type != TokenType.TEXT:
                stack.append(node)

        return root

    def _create_node(self, token):

        mapping = {
            TokenType.SECTION: NodeType.SECTION,
            TokenType.CHAPTER: NodeType.CHAPTER,
            TokenType.ARTICLE: NodeType.ARTICLE,
            TokenType.POINT: NodeType.POINT,
            TokenType.SUBPOINT: NodeType.SUBPOINT,
            TokenType.TEXT: NodeType.TEXT,
        }

        return DocumentNode(
            node_type=mapping[token.type],
            text=token.text,
            number=token.number
        )

    def _is_valid_parent(self, parent, child):

        hierarchy = {
            NodeType.DOCUMENT: {NodeType.SECTION, NodeType.CHAPTER, NodeType.ARTICLE, NodeType.TEXT},
            NodeType.SECTION: {NodeType.CHAPTER, NodeType.ARTICLE, NodeType.TEXT},
            NodeType.CHAPTER: {NodeType.ARTICLE, NodeType.TEXT},
            NodeType.ARTICLE: {NodeType.POINT, NodeType.TEXT},
            NodeType.POINT: {NodeType.POINT, NodeType.TEXT},
        }

        return child.node_type in hierarchy.get(parent.node_type, set())

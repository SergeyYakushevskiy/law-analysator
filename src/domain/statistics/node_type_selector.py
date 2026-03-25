from typing import Set

from src.domain.diff.change_set import ChangeSet
from src.infrastructure.parser.structure.token_type import TokenType


class NodeTypeSelector:

    def get_available_types(self, documents) -> Set[TokenType]:
        types = set()

        for doc in documents:
            for node in self._traverse(doc.root):
                types.add(node.node_type)

        types.difference_update({TokenType.DOCUMENT_ROOT, TokenType.PREAMBLE})
        return types

    from typing import List, Set

    def get_changed_types(self, change_sets: List[ChangeSet]) -> Set[TokenType]:
        changed_types: Set[TokenType] = set()
        for cs in change_sets:
            for nc in cs.changes:
                changed_types.add(nc.node.node_type)
        changed_types.difference_update({TokenType.PREAMBLE, TokenType.DOCUMENT_ROOT})
        return changed_types

    def get_common_types(self, documents) -> Set[TokenType]:
        sets = []

        for doc in documents:
            types = {node.node_type for node in self._traverse(doc.root)}
            sets.append(types)
        if not sets:
            return set()
        types = set.intersection(*sets)
        types.difference_update({TokenType.DOCUMENT_ROOT, TokenType.PREAMBLE})
        return  types

    def _traverse(self, root):
        stack = [root]
        while stack:
            node = stack.pop()
            yield node
            stack.extend(node.children)

from dataclasses import dataclass
from pathlib import Path

from src.parser.document.node import DocumentNode


@dataclass
class ParsedDocument:
    path: Path
    root: DocumentNode

    def iter_leaf_nodes(self):
        yield from self._collect_leaves(self.root)

    def _collect_leaves(self, node):
        if node.is_leaf():
            yield node
            return

        for child in node.children:
            yield from self._collect_leaves(child)

import logging
import re
from difflib import SequenceMatcher
from typing import List, Tuple

from src.domain.diff.change import ChangeType, NodeChange, TextChange
from src.domain.diff.change_set import ChangeSet
from src.domain.diff.node_matcher import NodeMatcher
from src.infrastructure.parser.document import ParsedDocument
from src.infrastructure.parser.structure.builder import TreeNode

logger = logging.getLogger(__name__)

TOKEN_PATTERN = re.compile(r'\w+|\S')

class DiffManager:

    codes = {
        "insert" : ChangeType.INSERT,
        "delete" : ChangeType.DELETE,
        "replace" : ChangeType.MODIFY
    }

    def __init__(self):
        self.matcher = NodeMatcher()

    def diff(self, old_doc: ParsedDocument, new_doc: ParsedDocument) -> ChangeSet:
        change_set = ChangeSet()

        if old_doc.root and new_doc.root:
            self._compare_nodes(old_doc.root, new_doc.root, change_set)
        elif old_doc.root and not new_doc.root:
            self._collect_deletions(old_doc.root, change_set)
        elif not old_doc.root and new_doc.root:
            self._collect_insertions(new_doc.root, change_set)

        return change_set

    def _compare_nodes(self, old_node: TreeNode, new_node: TreeNode, change_set: ChangeSet, depth: int = 0):
        pairs = self.matcher.match(old_node.children, new_node.children)

        for old_child, new_child in pairs:
            if old_child is None:
                change_set.add_change(NodeChange(change_type=ChangeType.INSERT, node=new_child))
            elif new_child is None:
                change_set.add_change(NodeChange(change_type=ChangeType.DELETE, node=old_child))
            else:
                self._compare_nodes(old_child, new_child, change_set, depth + 1)

        if old_node.content != new_node.content:
            change_set.add_all(self._analyze_text_diff(old_node,new_node))

    def _analyze_text_diff(self, old_node: TreeNode, new_node: TreeNode) -> list[NodeChange]:
        old_text = old_node.content or ""
        new_text = new_node.content or ""

        old_tokens = self._tokenize(old_text)
        new_tokens = self._tokenize(new_text)

        old_positions = self._get_token_positions(old_text)
        new_positions = self._get_token_positions(new_text)

        matcher = SequenceMatcher(None, old_tokens, new_tokens)
        opcodes = matcher.get_opcodes()

        old_change = []
        new_change = []

        for tag, i1, i2, j1, j2 in opcodes:
            if tag == 'equal':
                continue
            ch_type = self.codes[tag]

            if tag in ['delete', 'replace']:
                old_change.append(TextChange(ch_type, old_positions[i1][0], old_positions[i2 - 1][1]))
            if tag in ['insert', 'replace']:
                new_change.append(TextChange(ch_type, new_positions[j1][0], new_positions[j2 - 1][1]))

        result = []
        if old_change:
            result.append(NodeChange(old_node, ChangeType.MODIFY, old_change))
        if new_change:
            result.append(NodeChange(new_node, ChangeType.MODIFY, new_change))

        return result

    def _collect_deletions(self, node: TreeNode, change_set: ChangeSet):
        change_set.add_change(NodeChange(change_type=ChangeType.DELETE, node=node))
        for child in node.children:
            self._collect_deletions(child, change_set)

    def _collect_insertions(self, node: TreeNode, change_set: ChangeSet):
        change_set.add_change(NodeChange(change_type=ChangeType.INSERT, node=node))
        for child in node.children:
            self._collect_insertions(child, change_set)

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        return TOKEN_PATTERN.findall(text) if text else []

    @staticmethod
    def _get_token_positions(text: str) -> List[Tuple[int, int]]:
        """
        Возвращает список кортежей (start, end) для каждого токена в исходном тексте.
        Это нужно, чтобы перевести индексы токенов обратно в символы для подсветки.
        """
        positions = []
        for match in TOKEN_PATTERN.finditer(text):
            positions.append((match.start(), match.end()))
        return positions
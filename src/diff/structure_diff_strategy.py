import logging

from src.diff.base_strategy import BaseDiffStrategy
from src.diff.change_set import ChangeSet
from src.diff.change import Change
from src.diff.change_type import ChangeType
from src.parser.document.document import ParsedDocument
from src.parser.document.node import DocumentNode

logger = logging.getLogger(__name__)

class StructureDiffStrategy(BaseDiffStrategy):

    def diff(self, old_doc: ParsedDocument, new_doc: ParsedDocument) -> ChangeSet:
        change_set = ChangeSet()
        logger.debug('сравнение документов')
        logger.debug(f'1. {old_doc.path}')
        logger.debug(f'2. {new_doc.path}')
        self._compare_nodes(old_doc.root, new_doc.root, change_set)
        logger.debug(f'сравнение прошло успешно. Количество отличий: {len(change_set.changes)}')
        logger.debug(f'{ChangeType.INSERT}:{len(change_set.inserted())}')
        logger.debug(f'{ChangeType.MODIFY}:{len(change_set.modified())}')
        logger.debug(f'{ChangeType.DELETE}:{len(change_set.deleted())}')
        return change_set

    def _compare_nodes(self, old_node: DocumentNode, new_node: DocumentNode, change_set: ChangeSet):
        # сравнение типа и номера узла
        if old_node.node_type != new_node.node_type or old_node.number != new_node.number:
            change_set.add_change(Change(
                node=new_node,
                change_type=ChangeType.MODIFY,
                old_text=f"{old_node.node_type}:{old_node.number}",
                new_text=f"{new_node.node_type}:{new_node.number}"
            ))

        # сравниваем детей
        old_children = old_node.children
        new_children = new_node.children

        max_len = max(len(old_children), len(new_children))
        for i in range(max_len):
            if i >= len(old_children):
                change_set.add_change(Change(node=new_children[i], change_type=ChangeType.INSERT))
            elif i >= len(new_children):
                change_set.add_change(Change(node=old_children[i], change_type=ChangeType.DELETE))
            else:
                self._compare_nodes(old_children[i], new_children[i], change_set)

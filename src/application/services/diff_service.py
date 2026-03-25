import logging
from typing import List

from src.domain.diff.change import ChangeType
from src.domain.diff.change_set import ChangeSet
from src.domain.diff.diff_manager import DiffManager
from src.infrastructure.parser.document import ParsedDocument

logger = logging.getLogger(__name__)

class DiffService:

    def diff(self, old_doc:ParsedDocument, new_doc:ParsedDocument) -> ChangeSet:
        manager = DiffManager()

        logger.debug('Сравнение документов')
        logger.debug(f'1. {old_doc.path}')
        logger.debug(f'2. {new_doc.path}')

        changes = manager.diff(old_doc, new_doc)

        logger.debug(f'Сравнение прошло успешно. Количество отличий: {len(changes.changes)}')
        logger.debug(f'{ChangeType.INSERT}: {len(changes.inserted())}')
        logger.debug(f'{ChangeType.MODIFY}: {len(changes.modified())}')
        logger.debug(f'{ChangeType.DELETE}: {len(changes.deleted())}')
        logger.debug(f'ChangeSet:{changes}')
        return changes

    def compare_documents(self, documents: List) -> List[ChangeSet]:
        if len(documents) < 2:
            return []

        change_sets: List[ChangeSet] = []

        for i in range(len(documents) - 1):
            doc_a = documents[i]
            doc_b = documents[i + 1]

            change_set = self.diff(doc_a, doc_b)

            change_sets.append(change_set)

        return change_sets
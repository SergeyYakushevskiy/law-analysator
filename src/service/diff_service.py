import logging

from src.diff.change import ChangeType
from src.diff.change_set import ChangeSet
from src.diff.diff_manager import DiffManager
from src.parser.document import ParsedDocument

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

        return changes
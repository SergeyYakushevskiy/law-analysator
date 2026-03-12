import logging
from abc import ABC, abstractmethod
from pathlib import Path

from src.parser.document.document import ParsedDocument
from src.parser.exceptions import ParserError
from src.parser.structure.law_structure_parser import LawStructureParser

logger = logging.getLogger(__name__)

class BaseParser(ABC):
    def __init__(self):
        self.structure_parser = LawStructureParser()

    def parse(self, file_path: Path) -> ParsedDocument:

        logger.debug(f'парсинг файла: {file_path}')
        try:
            if not file_path.exists():
                raise ParserError(f'файл {file_path} не найден')
            raw_text = self._parse_file(file_path)
            root = self.structure_parser.parse(raw_text)
            logger.debug(f'файл {file_path} успешно считан')
            logger.debug(f'корень дерева: {root.text}')
            logger.debug(f'количество дочерних элементов: {len(root.children)}')
            return ParsedDocument(file_path, root)
        except Exception as e:
            raise ParserError(f"ошибка парсинга файла {file_path}: {e}") from e

    @abstractmethod
    def _parse_file(self, file_path: Path) -> str:
        pass

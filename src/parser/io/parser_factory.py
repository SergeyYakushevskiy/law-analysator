import logging
from pathlib import Path

from src.config import SUPPORTED_FORMATS
from src.parser.io.base_parser import BaseParser
from src.parser.io.exceptions import UnsupportedFormatError
from src.parser.io.odt_parser import OdtParser
from src.parser.io.txt_parser import TxtParser

logger = logging.getLogger(__name__)

class ParserFactory:
    _parsers = {
        ".txt": TxtParser,
        ".odt": OdtParser,
    }

    @classmethod
    def get_parser(cls, file_path: Path) -> BaseParser:
        logger.debug(f'определение парсера для файла {file_path}')
        ext = file_path.suffix.lower()
        parser_class = cls._parsers.get(ext)

        if not parser_class:
            raise UnsupportedFormatError(
                f"Неподдерживаемый формат документа: {ext}. Поддерживаемые форматы: {SUPPORTED_FORMATS}"
            )

        logger.debug(f'парсер для файла: {parser_class}')
        return parser_class()

import logging
from pathlib import Path

from src.parser.base_parser import BaseParser
from src.parser.txt_parser import TxtParser
from src.parser.pdf_parser import PdfParser
from src.parser.odt_parser import OdtParser
from src.parser.exceptions import UnsupportedFormatError
from src.config.base import SUPPORTED_FORMATS

logger = logging.getLogger(__name__)

class ParserFactory:
    _parsers = {
        ".txt": TxtParser,
        ".pdf": PdfParser,
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

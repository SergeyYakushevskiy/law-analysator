from pathlib import Path

from src.infrastructure.parser.io.base_parser import BaseParser
from src.infrastructure.parser.io.exceptions import ParserError
from src.infrastructure.config import settings

class TxtParser(BaseParser):

    def _parse_file(self, file_path: Path) -> str:
        for encoding in settings.encodings:
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    text = f.read()
                return text
            except UnicodeDecodeError:
                continue

        raise ParserError(f'не удалось определить кодировку для файла: {file_path}. Поддерживаемые кодировки: {settings.encodings}')
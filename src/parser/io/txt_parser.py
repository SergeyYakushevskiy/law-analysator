from pathlib import Path

from src.parser.io.base_parser import BaseParser
from src.parser.io.exceptions import ParserError
from src.config import ENCODINGS

class TxtParser(BaseParser):

    def _parse_file(self, file_path: Path) -> str:
        for encoding in ENCODINGS:
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    text = f.read()
                return text
            except UnicodeDecodeError:
                continue

        raise ParserError(f'не удалось определить кодировку для файла: {file_path}. Поддерживаемые кодировки: {ENCODINGS}')
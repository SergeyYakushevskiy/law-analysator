from pathlib import Path

from src.parser.base_parser import BaseParser
from src.parser.exceptions import ParserError


class TxtParser(BaseParser):

    ENCODINGS = (
        "utf-8",
        "windows-1251",
        "cp1251",
        "utf-16",
    )

    def _parse_file(self, file_path: Path) -> str:
        for encoding in self.ENCODINGS:
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    text = f.read()

                return text
            except UnicodeDecodeError:
                continue

        raise ParserError(f'не удалось определить кодировку для файла: {file_path}')
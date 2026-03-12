from pathlib import Path

from pdfminer.high_level import extract_text

from src.parser.base_parser import BaseParser


class PdfParser(BaseParser):

    def _parse_file(self, file_path: Path) -> str:
        text = extract_text(file_path)

        return text
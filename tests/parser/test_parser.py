from pathlib import Path

import pytest

from src.config.paths import get_resource
from src.parser.parser_factory import ParserFactory
from src.parser.document.document import ParsedDocument


def get_test_files():
    files = []

    versioned_files = get_resource('versioned_files')
    fl_152 = versioned_files / 'fl_152'

    for i in range(1, 4):
        for ext in ("txt", "odt", "pdf"):
            files.append(fl_152 / f"test_{i}.{ext}")

    return files


@pytest.mark.parametrize("file_path", get_test_files())
def test_parser_reads_file(file_path: Path):
    parser = ParserFactory.get_parser(file_path)

    document = parser.parse(file_path)

    assert isinstance(document, ParsedDocument)
    assert document.root is not None

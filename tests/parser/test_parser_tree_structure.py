from pathlib import Path

import pytest

from src.config.paths import get_asset
from src.parser.io.parser_factory import ParserFactory
from src.parser.document import ParsedDocument
from src.parser.model.node_type import NodeType


def get_test_files():
    versioned_files = get_asset('versioned_files')
    fl_152 = versioned_files / 'fl_152'

    files = []
    for i in range(1, 4):
        for ext in ("txt", "odt", "pdf"):
            files.append(fl_152 / f"test_{i}.{ext}")
    return files


@pytest.mark.parametrize("file_path", get_test_files())
def test_parser_tree_structure(file_path: Path):
    """
    Проверка построения дерева DocumentNode с учётом, что некоторые уровни могут отсутствовать.
    - Корень DOCUMENT обязателен
    - CHAPTER обязателен
    - ARTICLE/POINT/SUBPOINT/TEXT могут быть внутри CHAPTER
    """
    parser = ParserFactory.get_parser(file_path)
    document: ParsedDocument = parser.parse(file_path)

    root = document.root
    assert root.node_type == NodeType.DOCUMENT
    assert root.children, "Корень должен иметь хотя бы один дочерний узел"

    # Проверяем наличие хотя бы одного CHAPTER в корне или в секциях
    chapters = [c for c in root.children if c.node_type == NodeType.CHAPTER]

    # Если есть SECTION, ищем CHAPTER внутри неё
    if not chapters:
        for c in root.children:
            if c.node_type == NodeType.SECTION:
                chapters.extend([sc for sc in c.children if sc.node_type == NodeType.CHAPTER])

    assert chapters, "Должен быть хотя бы один CHAPTER в документе"

    # Проверка вложенности внутри CHAPTER
    def check_children(node):
        for child in node.children:
            # Вложение: ARTICLE, POINT, SUBPOINT, TEXT
            assert child.node_type in {NodeType.ARTICLE, NodeType.POINT, NodeType.SUBPOINT, NodeType.TEXT, NodeType.CHAPTER}, \
                f"Неподдерживаемый тип узла: {child.node_type}"
            check_children(child)

    for chapter in chapters:
        check_children(chapter)

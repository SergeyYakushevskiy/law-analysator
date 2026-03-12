from pathlib import Path
import pytest

from src.config.paths import get_resource
from src.parser.parser_factory import ParserFactory
from src.diff.diff_engine import DiffEngine
from src.diff.structure_diff_strategy import StructureDiffStrategy
from src.diff.text_diff_strategy import TextDiffStrategy
from src.diff.change_type import ChangeType
from src.parser.document.node_type import NodeType

@pytest.fixture(scope="module")
def parsed_documents():
    """
    Загружает все версии файлов (test_1.txt, test_2.txt, test_3.txt) и возвращает список ParsedDocument
    """
    parser_factory = ParserFactory()
    docs = []
    versioned_files = get_resource('versioned_files')
    fl_152 = versioned_files / 'fl_152'
    for i in range(1, 4):
        file_path = fl_152 / f"test_{i}.txt"
        parser = parser_factory.get_parser(file_path)
        parsed = parser.parse(file_path)
        docs.append(parsed)
    return docs

# -------------------------------
# Тест структуры документа между старой и новой версией
# -------------------------------
def test_structure_diff(parsed_documents):
    old_doc = parsed_documents[0]  # test_1.txt
    new_doc = parsed_documents[2]  # test_3.txt

    engine = DiffEngine(strategy=StructureDiffStrategy())
    change_set = engine.diff(old_doc, new_doc)

    assert not change_set.is_empty()
    # Проверяем, что есть модификации на уровне главы или статьи
    chapter_changes = [c for c in change_set.changes if c.node.node_type in (NodeType.CHAPTER, NodeType.ARTICLE)]
    assert chapter_changes, "Нет изменений структуры в новых версиях"

# -------------------------------
# Тест текста документа
# -------------------------------
def test_text_diff(parsed_documents):
    old_doc = parsed_documents[0]  # test_1.txt
    new_doc = parsed_documents[2]  # test_3.txt

    engine = DiffEngine(strategy=TextDiffStrategy())
    change_set = engine.diff(old_doc, new_doc)

    assert not change_set.is_empty()
    # Проверяем, что есть изменения текста в листовых узлах
    leaf_changes = [c for c in change_set.changes if c.node.node_type not in (NodeType.DOCUMENT, NodeType.CHAPTER, NodeType.ARTICLE)]
    assert leaf_changes, "Нет изменений текста в параграфах/пунктах"

# -------------------------------
# Комбинированный тест (структура + текст)
# -------------------------------
def test_diff_engine_combined(parsed_documents):
    old_doc = parsed_documents[0]  # test_1.txt
    new_doc = parsed_documents[2]  # test_3.txt

    # Структурный diff
    struct_engine = DiffEngine(strategy=StructureDiffStrategy())
    struct_changes = struct_engine.diff(old_doc, new_doc)
    assert struct_changes.changes

    # Текстовый diff
    text_engine = DiffEngine(strategy=TextDiffStrategy())
    text_changes = text_engine.diff(old_doc, new_doc)
    assert text_changes.changes

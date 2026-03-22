import logging
import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from src.config.config_loader import ensure_directories
from src.config.logger import setup_logging
from src.parser.parser import DocumentParser
from src.parser.structure.builder import TreeNode
from src.service.diff_service import DiffService
from src.ui.diff.diff_view import DiffViewWidget


def run_ui():
    app = QApplication(sys.argv)
    widget = DiffViewWidget()
    parser = DocumentParser()
    diff = DiffService()

    folder = Path("/devdata/projects/law-analysator/resources/versioned_files/fl_152")
    first = parser.parse(folder / 'test_1.txt')
    second = parser.parse(folder / 'test_2.txt')

    changes = diff.diff(first, second)

    widget.set_documents(first, second, changes)
    widget.show()

    app.exec()


def restore_text_from_tree(node: TreeNode, indent_size: int = 0) -> str:
    lines = []

    if node.content:
        indent = "\t" * indent_size
        lines.append(f"{indent}{node.content}")

    for child in node.children:
        child_text = restore_text_from_tree(child, indent_size + 1)
        if child_text:
            lines.append(child_text)

    return "\n".join(lines)

def print_tree_structure(node, depth=0, max_depth=3):
    """Выводит структуру дерева без контента"""
    indent = "  " * depth
    print(f"{indent}{node.node_type.name}:{node.id} (children: {len(node.children)})")
    if depth < max_depth:
        for child in node.children:
            print_tree_structure(child, depth + 1, max_depth)

def main():
    logger = logging.getLogger(__name__)
    logger.info("запуск приложения")

    # parser = DocumentParser()
    # diff = DiffManager()
    #
    # folder = Path("/devdata/projects/law-analysator/resources/versioned_files/fl_152")
    # first = parser.parse(folder / 'test_2.txt')
    # second = parser.parse(folder / 'test_3.txt')
    #
    # print_tree_structure(second.root)
    # changes = diff.diff(first, second)

    run_ui()

    logger.info('приложение успешно запущено')


if __name__ == "__main__":
    ensure_directories()
    setup_logging()
    main()

import logging

from src.config.config_loader import ensure_directories
from src.config.logger import setup_logging
from src.config.paths import get_resource
from src.diff.diff_engine import DiffEngine
from src.diff.structure_diff_strategy import StructureDiffStrategy
from src.diff.text_diff_strategy import TextDiffStrategy
from src.parser.parser_factory import ParserFactory


def main():
    logger = logging.getLogger(__name__)
    logger.info("запуск приложения")
    logger.info('приложение успешно запущено')
    try:
        files = [
            get_resource('versioned_files/fl_152/test_1.txt'),
            get_resource('versioned_files/fl_152/test_2.txt')
        ]
        files = [ParserFactory.get_parser(i).parse(i) for i in files]
        old_doc, new_doc = files

        struct_engine = DiffEngine(strategy=StructureDiffStrategy())
        struct_changes = struct_engine.diff(old_doc, new_doc)

        text_engine = DiffEngine(strategy=TextDiffStrategy())
        text_changes = text_engine.diff(old_doc, new_doc)

    except Exception as e:
        logger.exception(e)
if __name__ == "__main__":
    ensure_directories()
    setup_logging()
    main()

import logging
from pathlib import Path

from src.infrastructure.parser.io.parser_factory import ParserFactory
from src.infrastructure.parser.document import ParsedDocument
from src.infrastructure.parser.structure.builder import TreeBuilder, TreeNode
from src.infrastructure.parser.structure.tokenizer import Tokenizer

logger = logging.getLogger(__name__)

class DocumentParser:
    factory = ParserFactory()

    def parse(self, file_path:Path) -> ParsedDocument:
        tokenizer = Tokenizer()
        builder = TreeBuilder()

        parser = self.factory.get_parser(file_path)
        normalized_text = parser.parse(file_path)
        tokens = tokenizer.tokenize_text(normalized_text)
        structure = builder.build(tokens)
        return ParsedDocument(file_path, structure)
from pathlib import Path

from src.parser.io.parser_factory import ParserFactory
from src.parser.document import ParsedDocument
from src.parser.structure.builder import TreeBuilder
from src.parser.structure.tokenizer import Tokenizer


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

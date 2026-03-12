from src.parser.structure.text_preprocessor import TextPreprocessor
from src.parser.structure.tokenizer import Tokenizer
from src.parser.structure.hierarchy_builder import HierarchyBuilder


class LawStructureParser:

    def __init__(self):

        self.preprocessor = TextPreprocessor()
        self.tokenizer = Tokenizer()
        self.builder = HierarchyBuilder()

    def parse(self, text: str):

        lines = self.preprocessor.preprocess(text)

        tokens = self.tokenizer.tokenize(lines)

        root = self.builder.build(tokens)

        return root

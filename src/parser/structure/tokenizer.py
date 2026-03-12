from src.parser.structure.token import Token
from src.parser.structure.token_type import TokenType
from src.parser.structure.token_patterns import (
    SECTION_PATTERN,
    CHAPTER_PATTERN,
    ARTICLE_PATTERN,
    POINT_PATTERN,
    SUBPOINT_PATTERN
)


class Tokenizer:

    def tokenize(self, lines: list[str]) -> list[Token]:

        tokens = []

        for line in lines:

            if m := SECTION_PATTERN.match(line):
                tokens.append(Token(TokenType.SECTION, line, m.group(1)))
                continue

            if m := CHAPTER_PATTERN.match(line):
                tokens.append(Token(TokenType.CHAPTER, line, m.group(1)))
                continue

            if m := ARTICLE_PATTERN.match(line):
                tokens.append(Token(TokenType.ARTICLE, line, m.group(1)))
                continue

            if m := POINT_PATTERN.match(line):
                tokens.append(Token(TokenType.POINT, line, m.group(1)))
                continue

            if m := SUBPOINT_PATTERN.match(line):
                tokens.append(Token(TokenType.SUBPOINT, line, m.group(1)))
                continue

            tokens.append(Token(TokenType.TEXT, line))

        return tokens

# structure/tokenizer.py

from typing import List

from src.parser.structure.token import Token
from src.parser.structure.token_type import TokenType, PATTERNS_CONFIG


class Tokenizer:
    def __init__(self):
        self.line_num = 0

    def tokenize_text(self, text: str) -> List[Token]:
        tokens = []
        for line in text.splitlines():
            self.line_num += 1
            # tokenize_line теперь всегда возвращает токен (даже TEXT)
            token = self.tokenize_line(line)
            tokens.append(token)
        return tokens

    def tokenize_line(self, line: str) -> Token:
        line = line.strip()

        if not line:
            return Token(
                type=TokenType.TEXT,
                raw_value="",
                norm_id="",
                level_class=-1,
                line_number=self.line_num
            )

        for t_type, pattern, extractor, level_class in PATTERNS_CONFIG:  # ← Переименовали переменную
            match = pattern.match(line)
            if match:
                norm_id = extractor(match)

                return Token(
                    type=t_type,
                    raw_value=line,
                    norm_id=norm_id,
                    level_class=level_class,  # ← Прямо из PATTERNS_CONFIG
                    line_number=self.line_num
                )

        return Token(
            type=TokenType.TEXT,
            raw_value=line,
            norm_id="",
            level_class=-1,
            line_number=self.line_num
        )
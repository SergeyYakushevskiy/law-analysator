from enum import Enum


class TokenType(Enum):
    SECTION = "раздел"
    CHAPTER = "глава"
    ARTICLE = "статья"
    POINT = "пункт"
    SUBPOINT = "подпункт"
    TEXT = "текст"

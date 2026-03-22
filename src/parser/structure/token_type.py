import re
from enum import auto, Enum


class TokenType(Enum):
    DOCUMENT_ROOT = auto()
    PREAMBLE = auto()
    SECTION = auto()
    CHAPTER = auto()
    SUBCHAPTER = auto()
    PARAGRAPH = auto()
    ARTICLE = auto()
    PART = auto()
    POINT = auto()
    SUBPOINT = auto()
    TEXT = auto()


PATTERNS_CONFIG = [
    (TokenType.SUBPOINT,
     re.compile(r"^(?P<marker>[а-яёa-z]\)|\([а-яёa-z]\)|[а-яёa-z]\.)", re.IGNORECASE),
     lambda m: m.group('marker').replace(')', '').replace('(', '').replace('.', '').lower(),
     7),

    (TokenType.POINT,
     re.compile(r"^(?P<num>\d+(?:\.\d+)*)\)|^\((?P<num2>\d+(?:\.\d+)*)\)"),
     lambda m: m.group('num') or m.group('num2'),
     6),

    (TokenType.PART,
     re.compile(r"^(?P<num>\d+(?:\.\d+)*)\.(?=\s)"),
     lambda m: m.group('num'),
     5),

    (TokenType.PART,
     re.compile(r"^(?:часть|ч\.)\s*(?P<num>\d+)", re.IGNORECASE),
     lambda m: m.group('num'),
     5),

    (TokenType.ARTICLE,
     re.compile(r"^(?:Статья|ст\.)\s+(?P<num>\d+(?:\.\d+)*)", re.IGNORECASE),
     lambda m: m.group('num'),
     4),

    (TokenType.PARAGRAPH,
     re.compile(r"^(?:Параграф|§)\s+(?P<num>[\dIVXLC]+)", re.IGNORECASE),
     lambda m: m.group('num'),
     3),

    (TokenType.SUBCHAPTER,
     re.compile(r"^(?:Подраздел|Подглава)\s+(?P<num>[\d\w\.]+)", re.IGNORECASE),
     lambda m: m.group('num'),
     2),

    (TokenType.CHAPTER,
     re.compile(r"^(?:Глава|гл\.)\s+(?P<num>[\dIVXLC]+|[а-яА-ЯёЁ]+)", re.IGNORECASE),
     lambda m: m.group('num'),
     1),

    (TokenType.SECTION,
     re.compile(r"^Раздел\s+(?P<num>[\dIVXLC]+|[а-яА-ЯёЁ]+)", re.IGNORECASE),
     lambda m: m.group('num'),
     0),

    (TokenType.PREAMBLE,
     re.compile(r"^(Российская Федерация|Настоящий Федеральный закон|Указ|Постановление)", re.IGNORECASE),
     lambda m: "preamble",
     -1),
]
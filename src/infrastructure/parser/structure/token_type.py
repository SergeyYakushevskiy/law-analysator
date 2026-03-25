import re
from enum import IntEnum


class TokenType(IntEnum):
    DOCUMENT_ROOT = 0
    PREAMBLE = 1
    SECTION = 1
    CHAPTER = 2
    SUBCHAPTER = 3
    PARAGRAPH = 4
    ARTICLE = 5
    PART = 6
    POINT = 7
    SUBPOINT = 8
    TEXT = 9


PATTERNS_CONFIG = [
    (TokenType.SUBPOINT,
     re.compile(r"^(?P<marker>[а-яёa-z]\)|\([а-яёa-z]\)|[а-яёa-z]\.)", re.IGNORECASE),
     lambda m: m.group('marker').replace(')', '').replace('(', '').replace('.', '').lower(),
     TokenType.SUBPOINT),

    (TokenType.POINT,
     re.compile(r"^(?P<num>\d+(?:\.\d+)*)\)|^\((?P<num2>\d+(?:\.\d+)*)\)"),
     lambda m: m.group('num') or m.group('num2'),
     TokenType.POINT),

    (TokenType.PART,
     re.compile(r"^(?P<num>\d+(?:\.\d+)*)\.(?=\s)"),
     lambda m: m.group('num'),
     TokenType.PART),

    (TokenType.PART,
     re.compile(r"^(?:часть|ч\.)\s*(?P<num>\d+)", re.IGNORECASE),
     lambda m: m.group('num'),
     TokenType.PART),

    (TokenType.ARTICLE,
     re.compile(r"^(?:Статья|ст\.)\s+(?P<num>\d+(?:\.\d+)*)", re.IGNORECASE),
     lambda m: m.group('num'),
     TokenType.ARTICLE),

    (TokenType.PARAGRAPH,
     re.compile(r"^(?:Параграф|§)\s+(?P<num>[\dIVXLC]+)", re.IGNORECASE),
     lambda m: m.group('num'),
     TokenType.PARAGRAPH),

    (TokenType.SUBCHAPTER,
     re.compile(r"^(?:Подраздел|Подглава)\s+(?P<num>[\d\w\.]+)", re.IGNORECASE),
     lambda m: m.group('num'),
     TokenType.SUBCHAPTER),

    (TokenType.CHAPTER,
     re.compile(r"^(?:Глава|гл\.)\s+(?P<num>[\dIVXLC]+|[а-яА-ЯёЁ]+)", re.IGNORECASE),
     lambda m: m.group('num'),
     TokenType.CHAPTER),

    (TokenType.SECTION,
     re.compile(r"^Раздел\s+(?P<num>[\dIVXLC]+|[а-яА-ЯёЁ]+)", re.IGNORECASE),
     lambda m: m.group('num'),
     TokenType.SECTION),

    (TokenType.PREAMBLE,
     re.compile(r"^(Российская Федерация|Настоящий Федеральный закон|Указ|Постановление)", re.IGNORECASE),
     lambda m: "",
     TokenType.PREAMBLE),
]
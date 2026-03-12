from enum import Enum


class NodeType(Enum):
    DOCUMENT = "документ"
    SECTION = "раздел"
    CHAPTER = "глава"
    ARTICLE = "статья"
    PARAGRAPH = "параграф"
    POINT = "пункт"
    SUBPOINT = "подпункт"
    TEXT = "текст"

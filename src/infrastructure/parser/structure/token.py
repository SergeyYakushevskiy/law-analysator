from dataclasses import dataclass

from src.infrastructure.parser.structure.token_type import TokenType


@dataclass
class Token:
    type: TokenType
    raw_value: str
    norm_id: str
    level_class: int
    line_number: int
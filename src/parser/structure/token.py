from dataclasses import dataclass
from typing import Optional

from src.parser.structure.token_type import TokenType


@dataclass
class Token:

    type: TokenType
    text: str
    number: Optional[str] = None

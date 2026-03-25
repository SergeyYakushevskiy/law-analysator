from dataclasses import dataclass, field
from typing import List, Optional

from src.infrastructure.parser.structure.builder import TreeNode
from src.infrastructure.parser.structure.token_type import TokenType


@dataclass
class FrequencyNode:
    node: TreeNode
    name: str
    total: int
    children: List['FrequencyNode'] = field(default_factory=list)

@dataclass
class FrequencySet:
    target_type : TokenType
    frequencies: List[FrequencyNode] = field(default_factory=list)

@dataclass
class FrequencyReport:
    root: FrequencyNode
    freq_list: List[FrequencyNode] = field(default_factory=list)
    most_changed_node: List[FrequencyNode] = field(default_factory=list)




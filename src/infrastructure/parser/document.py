from dataclasses import dataclass
from pathlib import Path

from src.infrastructure.parser.structure.builder import TreeNode


@dataclass
class ParsedDocument:
    path: Path
    root: TreeNode

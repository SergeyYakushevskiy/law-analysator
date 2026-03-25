from dataclasses import dataclass
from typing import Optional, List

from src.infrastructure.parser.structure.builder import TreeNode
from src.presentation.ui.features.context_builder import RenderContext
from src.presentation.ui.features.diff_view import DocumentHighlights


@dataclass
class RenderResult:
    text: str
    highlights: DocumentHighlights
    title: str


class SingleRenderer:
    def __init__(self, root: Optional[TreeNode], context: RenderContext, title: str):
        self._root = root
        self._context = context  # Общая карта для всех деревьев
        self._title = title

    def render(self) -> RenderResult:
        if not self._root:
            return RenderResult("", {}, self._title)

        lines: List[str] = []
        highlights: DocumentHighlights = {}

        stack = [(self._root, 0)]
        current_line_idx = 0

        while stack:
            node, depth = stack.pop()
            if not hasattr(node, 'level_class'):
                print(node)
            indent = "  " * max(0, node.level_class)
            content = node.content or ""
            line_text = f"{indent}{content}"
            lines.append(line_text)

            node_id = id(node)

            if node_id in self._context:
                instruction = self._context[node_id]
                line_spans = []

                if instruction.full_line_format:
                    start_pos = len(indent)
                    length = len(content)
                    if length > 0:
                        line_spans.append((start_pos, length, instruction.full_line_format))

                for span_instr in instruction.spans:
                    global_start = len(indent) + span_instr.start
                    line_spans.append((global_start, span_instr.length, span_instr.format))

                if line_spans:
                    highlights[current_line_idx] = line_spans

            current_line_idx += 1

            for child in reversed(node.children):
                stack.append((child, depth + 1))

        return RenderResult("\n".join(lines), highlights, self._title)
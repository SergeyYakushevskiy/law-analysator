from dataclasses import dataclass, field
from typing import Dict, List, Optional
from PyQt6.QtGui import QTextCharFormat

from src.domain.diff.change import ChangeType
from src.domain.diff.change_set import ChangeSet
from src.presentation.ui.styles.colors import COLORS


@dataclass
class SpanInstruction:
    start: int
    length: int
    format: QTextCharFormat

@dataclass
class NodeInstruction:
    spans: List[SpanInstruction] = field(default_factory=list)
    full_line_format: Optional[QTextCharFormat] = None

RenderContext = Dict[int, NodeInstruction]

class DiffContextBuilder:
    def __init__(self, change_set: ChangeSet):
        self._change_set = change_set

    def build(self) -> RenderContext:
        context: RenderContext = {}

        for change in self._change_set.changes:
            node_id = id(change.node)

            if node_id not in context:
                context[node_id] = NodeInstruction()

            instruction = context[node_id]
            change_type = change.change_type

            if change_type in (ChangeType.DELETE, ChangeType.INSERT):
                # Красим весь узел
                fmt = self._get_format(change_type)
                instruction.full_line_format = fmt

            elif change_type == ChangeType.MODIFY:
                # Красим диапазоны
                for tc in change.text_diff:
                    span_start = tc.start
                    span_length = tc.end - tc.start
                    fmt = self._get_format(tc.change_type)

                    instruction.spans.append(SpanInstruction(
                        start=span_start,
                        length=span_length,
                        format=fmt
                    ))

        return context

    def _get_format(self, change_type: ChangeType) -> QTextCharFormat:
        fmt = QTextCharFormat()
        if change_type == ChangeType.DELETE:
            fmt.setBackground(COLORS["delete_bg"])
            fmt.setForeground(COLORS["delete_text"])
            fmt.setFontStrikeOut(True)
        elif change_type == ChangeType.INSERT:
            fmt.setBackground(COLORS["insert_bg"])
            fmt.setForeground(COLORS["insert_text"])
        elif change_type == ChangeType.MODIFY:
            fmt.setBackground(COLORS["modify_bg"])
        return fmt
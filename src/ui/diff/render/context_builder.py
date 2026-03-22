from dataclasses import dataclass, field
from typing import Dict, List, Optional
from src.diff.change_set import ChangeSet
from src.diff.change import ChangeType
from src.ui.diff.styles import COLORS
from PyQt6.QtGui import QTextCharFormat


@dataclass
class SpanInstruction:
    """Инструкция для подсветки части строки"""
    start: int      # Позиция начала относительно начала строки (с учетом отступов)
    length: int     # Длина участка
    format: QTextCharFormat

@dataclass
class NodeInstruction:
    """Инструкции для конкретного узла"""
    # Если список пуст, но узел помечен как DELETE/INSERT, значит красим всю строку
    spans: List[SpanInstruction] = field(default_factory=list)
    full_line_format: Optional[QTextCharFormat] = None

# Контекст рендеринга: Map[ID_узла, Инструкция]
RenderContext = Dict[int, NodeInstruction]

class DiffContextBuilder:
    def __init__(self, change_set: ChangeSet):
        self._change_set = change_set

    def build(self) -> RenderContext:
        context: RenderContext = {}

        # Проходим по ВСЕМ изменениям, не фильтруя.
        # Создаем инструкции для всех узлов, которые упомянуты в ChangeSet.
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
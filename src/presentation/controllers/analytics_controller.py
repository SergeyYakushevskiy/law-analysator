import logging
from typing import List

from PyQt6.QtWidgets import QFileDialog, QMessageBox

from src.application.services.diff_service import DiffService
from src.application.services.project_service import ProjectService
from src.application.services.statistics_service import StatisticsService
from src.domain.statistics.frequency_aggregator import TYPE_LABELS
from src.domain.statistics.frequency_report import FrequencyReport, FrequencyNode
from src.infrastructure.parser.document import ParsedDocument
from src.infrastructure.parser.structure.token_type import TokenType
from src.presentation.ui.windows.main_window import MainWindow

logger = logging.getLogger(__name__)


class AnalyticsController:
    def __init__(
            self,
            window: MainWindow,
            project_service: ProjectService,
            diff_service : DiffService,
            statistics_service : StatisticsService
    ):
        self.window = window
        self.project_service = project_service
        self.diff_service = diff_service
        self.statistics_service = statistics_service

        self._last_report_text: str = ""
        self._connect_signals()

    def _connect_signals(self):
        ws = self.window.workspace
        ws.stats_panel.type_selector.activated.connect(self._handle_recalculate)
        self.window.report_requested.connect(self._handle_generate_report)

    def load_types(self):
        ws = self.window.workspace
        documents = self.load_all_documents()

        if not documents:
            return

        change_sets = self.diff_service.compare_documents(documents)
        types = self.statistics_service.get_changed_types(change_sets)
        ws.stats_panel.set_types(types)

    def _handle_recalculate(self):
        try:
            target_type = self.window.workspace.stats_panel.get_selected_type()

            documents = self.load_all_documents()

            if not documents:
                return

            change_sets = self.diff_service.compare_documents(documents)

            report = self.statistics_service.build_report(
                change_sets=change_sets,
                target_type=target_type
            )

            self._update_ui(report)

        except Exception as e:
            logger.exception(e)
            QMessageBox.critical(None, "Ошибка", str(e))

    def load_all_documents(self) -> List[ParsedDocument]:
        result = self.project_service.sync_project()
        file_names = result.get("files", [])

        if len(file_names) < 2:
            return []

        documents = [
            self.project_service.load_document(name)
            for name in file_names
        ]

        return documents

    def _handle_generate_report(self):
        try:
            path, _ = QFileDialog.getSaveFileName(
                None,
                "Сохранить отчёт",
                "",
                "Text Files (*.txt)"
            )

            if not path:
                return

            with open(path, "w", encoding="utf-8") as f:
                f.write(self._last_report_text)

        except Exception as e:
            QMessageBox.critical(None, "Ошибка", str(e))

    def _update_ui(self, report: FrequencyReport):
        lines = ["Статистика изменений по всем документам", ""]

        def walk(fn: FrequencyNode, indent: int = 0):
            prefix = "  " * indent
            if fn.children:
                # Промежуточный узел
                lines.append(f"{prefix}{fn.name}")
                for child in sorted(fn.children, key=lambda x: x.name or ""):
                    walk(child, indent + 1)
            else:
                # Лист
                lines.append(f"{prefix}{fn.name}: {fn.total}")

        for child in sorted(report.root.children, key=lambda x: x.name or ""):
            walk(child)

        if report.most_changed_node:
            lines.append('Наибольшее количество изменений')
            for node in report.most_changed_node:
                line = f"{self._get_full_name(node)}: {node.total}"
                lines.append(line)

        text = "\n".join(lines)

        self._last_report_text = text
        self.window.workspace.stats_panel.set_text_stats(text)

        histogram_data = {fn.name: fn.total for fn in sorted(report.freq_list, key=lambda fn: fn.total, reverse=True)}

        self.window.workspace.stats_panel.set_chart_data(histogram_data)

    def _get_full_name(self, fn: FrequencyNode) -> str:
        path = []
        current = fn
        while current:
            if current.name:
                path.append(current.name)
            if not current.node.parent:
                break
            parent = current.node.parent
            if parent.node_type == TokenType.DOCUMENT_ROOT:
                break
            name = f'{TYPE_LABELS.get(parent.node_type)} {parent.id}'
            current = FrequencyNode(node=parent, name=name, total=0)
        return ", ".join(reversed(path))



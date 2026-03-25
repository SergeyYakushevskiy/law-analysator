from typing import List

from src.domain.statistics.frequency_aggregator import FrequencyAggregator
from src.domain.statistics.node_type_selector import NodeTypeSelector
from src.domain.statistics.frequency_report import FrequencyReport
from src.infrastructure.parser.structure.token_type import TokenType

class StatisticsService:

    def __init__(self):
        self.aggregator = FrequencyAggregator()
        self.selector = NodeTypeSelector()

    def get_available_types(self, documents):
        return self.selector.get_available_types(documents)

    def get_common_types(self, documents):
        return self.selector.get_common_types(documents)

    def get_changed_types(self, change_sets):
        return self.selector.get_changed_types(change_sets)

    def build_report(
        self,
        change_sets,
        target_type: TokenType
    ) -> FrequencyReport:

        freq_set, most_changed = self.aggregator.aggregate(change_sets, target_type)
        report = self.aggregator.build_report(freq_set)
        report.most_changed_node = most_changed
        return report

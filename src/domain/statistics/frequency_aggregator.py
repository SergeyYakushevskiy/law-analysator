import logging
from typing import Dict, Optional, List, Tuple

from src.domain.diff.change import ChangeType
from src.domain.diff.change_set import ChangeSet
from src.domain.statistics.frequency_report import FrequencyReport, FrequencySet, FrequencyNode
from src.infrastructure.parser.structure.builder import TreeNode
from src.infrastructure.parser.structure.token_type import TokenType

logger = logging.getLogger(__name__)

TYPE_LABELS = {
    TokenType.SECTION: "Раздел",
    TokenType.CHAPTER: "Глава",
    TokenType.SUBCHAPTER: "Подглава",
    TokenType.PARAGRAPH: "Параграф",
    TokenType.ARTICLE: "Статья",
    TokenType.PART: "Часть",
    TokenType.POINT: "Пункт",
    TokenType.SUBPOINT: "Подпункт",
    TokenType.PREAMBLE: "Преамбула",
}

class FrequencyAggregator:

    def aggregate(self, change_sets: List[ChangeSet], target_type: TokenType) -> Tuple[
        FrequencySet, List[FrequencyNode]]:
        logger.debug(f'построение множества частот изменений для целевого типа: {target_type}')

        # Словарь: ключ = TreeNode целевого типа, значение = соответствующий FrequencyNode
        all_nodes: Dict[TreeNode, FrequencyNode] = {}

        # Собираем все NodeChange
        for cs in change_sets:
            for nc in cs.changes:
                # Поднимаемся к ближайшему родителю целевого типа
                current = nc.node
                while current and current.node_type != target_type:
                    current = current.parent
                if current is None:
                    continue  # Нет родителя целевого типа

                # Создаем FrequencyNode, если ещё не создан
                if current not in all_nodes:
                    all_nodes[current] = FrequencyNode(
                        node=current,
                        name=f"{TYPE_LABELS.get(current.node_type)} {current.id}",
                        total=0
                    )

        # Связываем детей с родителями
        for fn in all_nodes.values():
            for child in fn.node.children:
                if child in all_nodes:
                    fn.children.append(all_nodes[child])

        # Функция подсчета total с учетом всех дочерних изменений
        def compute_total(fn: FrequencyNode) -> int:
            node_total = 0

            # Все NodeChange для текущего узла и его детей
            relevant_changes = [nc for cs in change_sets for nc in cs.changes
                                if nc.node == fn.node or is_descendant(nc.node, fn.node)]

            for nc in relevant_changes:
                if nc.change_type in {ChangeType.INSERT, ChangeType.DELETE}:
                    node_total += 1
                elif nc.change_type == ChangeType.MODIFY:
                    text_ch = set(ch.change_type for ch in nc.text_diff)
                    node_total += len(text_ch)

            # Total детей
            child_total = sum(compute_total(child) for child in fn.children)
            fn.total = node_total + child_total
            return fn.total

        # Проверка, что один узел является потомком другого
        def is_descendant(node: TreeNode, ancestor: TreeNode) -> bool:
            current = node.parent
            while current:
                if current == ancestor:
                    return True
                current = current.parent
            return False

        roots = list(all_nodes.values())
        for root in roots:
            compute_total(root)

        freq_set = FrequencySet(target_type=target_type, frequencies=roots)

        max_total = max(fn.total for fn in roots)
        max_nodes = [fn for fn in roots if fn.total == max_total]

        logger.debug(f'множество построено: {freq_set}')
        return freq_set, max_nodes

    def build_report(self, freq_set: FrequencySet) -> Optional[FrequencyReport]:
        logger.debug(f'построение дерева для узла с целевым типом: {freq_set.target_type.name}')
        all_nodes: Dict[TreeNode, FrequencyNode] = {}

        # 1. Создаем все узлы и связи родитель-ребенок
        for freq_node in freq_set.frequencies:
            current = freq_node.node
            prev_fn = None
            while current:
                if current not in all_nodes:
                    total = freq_node.total if current == freq_node.node else 0
                    if  current == freq_node.node:
                        name = freq_node.name
                    else:
                        name = f'{TYPE_LABELS.get(current.node_type)} {current.id}'
                    all_nodes[current] = FrequencyNode(node=current, name=name, total=total)
                fn = all_nodes[current]
                if prev_fn and prev_fn not in fn.children:
                    fn.children.append(prev_fn)
                prev_fn = fn
                current = current.parent

        # 2. Находим корень (узел без родителя)
        root_candidates = [fn for fn in all_nodes.values() if fn.node.parent is None]
        if not root_candidates:
            return None

        # 3. Сортируем freq_list для удобного отображения
        freq_list = sorted(
            [fn for fn in all_nodes.values() if fn.total != 0],
            key=lambda fn: fn.name or ""
        )
        logger.debug(f'список кандидатов на роль дерева: {root_candidates}')
        logger.debug(f'дерево построено: {root_candidates[0]}')
        return FrequencyReport(root=root_candidates[0], freq_list=freq_list, most_changed_node=[])

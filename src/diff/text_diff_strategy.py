from deepdiff import DeepDiff
from src.diff.base_strategy import BaseDiffStrategy
from src.diff.change_set import ChangeSet
from src.diff.change import Change
from src.diff.change_type import ChangeType
from src.parser.document.document import ParsedDocument

class TextDiffStrategy(BaseDiffStrategy):
    def diff(self, old_doc: ParsedDocument, new_doc: ParsedDocument) -> ChangeSet:
        change_set = ChangeSet()

        old_leaves = list(old_doc.iter_leaf_nodes())
        new_leaves = list(new_doc.iter_leaf_nodes())

        # Пробежимся по парам листьев
        for old_node, new_node in zip(old_leaves, new_leaves):
            # используем DeepDiff для сравнения строковых текстов
            diff = DeepDiff(old_node.text, new_node.text, ignore_order=True)

            if diff:  # если есть изменения
                change_set.add_change(
                    Change(
                        node=new_node,
                        change_type=ChangeType.MODIFY,
                        old_text=old_node.text,
                        new_text=new_node.text
                    )
                )

        # Обработка лишних листьев (вставка / удаление)
        if len(new_leaves) > len(old_leaves):
            for node in new_leaves[len(old_leaves):]:
                change_set.add_change(Change(node=node, change_type=ChangeType.INSERT))
        elif len(old_leaves) > len(new_leaves):
            for node in old_leaves[len(new_leaves):]:
                change_set.add_change(Change(node=node, change_type=ChangeType.DELETE))

        return change_set

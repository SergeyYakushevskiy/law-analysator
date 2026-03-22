from difflib import SequenceMatcher
from typing import List, Optional, Tuple

from src.config import TEXT_SIMILARITY_THRESHOLD, FALLBACK_THRESHOLD
from src.parser.structure.builder import TreeNode


class NodeMatcher:

    def match(
            self,
            old_nodes: List[TreeNode],
            new_nodes: List[TreeNode],
    ) -> List[Tuple[Optional[TreeNode], Optional[TreeNode]]]:

        pairs: List[Tuple[Optional[TreeNode], Optional[TreeNode]]] = []
        used_new = set()
        used_old = set()

        for i, old_node in enumerate(old_nodes):
            for j, new_node in enumerate(new_nodes):
                if j in used_new:
                    continue

                if (old_node.node_type == new_node.node_type and
                        old_node.id == new_node.id and
                        old_node.level_class == new_node.level_class):
                    pairs.append((old_node, new_node))
                    used_new.add(j)
                    used_old.add(i)
                    break

        total_old = len(old_nodes)
        unmatched_old = total_old - len(used_old)

        if total_old > 0 and (unmatched_old / total_old) > FALLBACK_THRESHOLD:
            fallback_pairs = self._fallback_text_match(old_nodes, new_nodes, used_old, used_new)

            pairs.extend(fallback_pairs)

            for old_n, new_n in fallback_pairs:
                if old_n is not None:
                    try:
                        idx_old = old_nodes.index(old_n)
                        used_old.add(idx_old)
                    except ValueError:
                        pass

                if new_n is not None:
                    try:
                        idx_new = new_nodes.index(new_n)
                        used_new.add(idx_new)
                    except ValueError:
                        pass

        final_pairs = []

        pairs_dict = {id(o): n for o, n in pairs if o is not None and n is not None}

        for i, old_node in enumerate(old_nodes):
            if i in used_old:
                new_node = pairs_dict.get(id(old_node))
                final_pairs.append((old_node, new_node))
            else:
                final_pairs.append((old_node, None))  # DELETE

        for j, new_node in enumerate(new_nodes):
            if j not in used_new:
                final_pairs.append((None, new_node))

        return final_pairs

    def _fallback_text_match(
            self,
            old_nodes: List[TreeNode],
            new_nodes: List[TreeNode],
            used_old: set,
            used_new: set
    ) -> List[Tuple[Optional[TreeNode], Optional[TreeNode]]]:
        pairs = []
        local_used_new = set(used_new)

        for i, old_node in enumerate(old_nodes):
            if i in used_old:
                continue

            best_idx = None
            best_score = 0.0

            for j, new_node in enumerate(new_nodes):
                if j in local_used_new:
                    continue

                if old_node.level_class != new_node.level_class:
                    continue

                score = self._similarity(old_node.content, new_node.content)
                if score > best_score and score >= TEXT_SIMILARITY_THRESHOLD:
                    best_score = score
                    best_idx = j

            if best_idx is not None:
                pairs.append((old_node, new_nodes[best_idx]))
                local_used_new.add(best_idx)

        return pairs

    def _similarity(self, text1: str, text2: str) -> float:
        t1 = self._normalize(text1)
        t2 = self._normalize(text2)
        if not t1 or not t2:
            return 0.0
        return SequenceMatcher(None, t1, t2).ratio()

    @staticmethod
    def _normalize(text: str) -> str:
        return " ".join(text.lower().split())
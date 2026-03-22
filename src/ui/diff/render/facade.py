from typing import Optional
from src.parser.document import ParsedDocument
from src.diff.change_set import ChangeSet
from src.parser.structure.builder import TreeNode
from src.ui.diff.render.context_builder import DiffContextBuilder
from src.ui.diff.render.single_render import SingleRenderer, RenderResult


class DiffRenderer:
    def __init__(self, old_doc: Optional[ParsedDocument], new_doc: Optional[ParsedDocument], change_set: ChangeSet):
        self._old_doc = old_doc
        self._new_doc = new_doc
        self._change_set = change_set

        self._global_context = DiffContextBuilder(change_set).build()

    def render_for_tree(self, root: TreeNode, title: str) -> RenderResult:
        renderer = SingleRenderer(root, self._global_context, title)
        return renderer.render()

    def render_old(self) -> RenderResult:
        if not self._old_doc or not self._old_doc.root:
            return RenderResult("", {}, "Старый документ")
        return self.render_for_tree(self._old_doc.root, self._old_doc.path.name)

    def render_new(self) -> RenderResult:
        if not self._new_doc or not self._new_doc.root:
            return RenderResult("", {}, "Новый документ")
        return self.render_for_tree(self._new_doc.root, self._new_doc.path.name)
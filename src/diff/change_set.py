import logging
from dataclasses import dataclass, field

from src.diff.change import NodeChange, ChangeType

logger = logging.getLogger(__name__)

@dataclass
class ChangeSet:
    changes: list[NodeChange] = field(default_factory=list)

    def add_change(self, change: NodeChange):
        self.changes.append(change)

    def add_all(self, changes: list[NodeChange]):
        self.changes.extend(changes)

    def is_empty(self) -> bool:
        return not self.changes

    def inserted(self):
        return [c for c in self.changes if c.change_type is ChangeType.INSERT]

    def modified(self):
        return [c for c in self.changes if c.change_type is ChangeType.MODIFY]

    def deleted(self):
        return [c for c in self.changes if c.change_type is ChangeType.DELETE]

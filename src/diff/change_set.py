import logging
from dataclasses import dataclass, field
from typing import List
from src.diff.change import Change
from src.diff.change_type import ChangeType

logger = logging.getLogger(__name__)

@dataclass
class ChangeSet:
    changes: List[Change] = field(default_factory=list)

    def add_change(self, change: Change):
        self.changes.append(change)

    def is_empty(self) -> bool:
        return not self.changes

    def inserted(self):
        return [c for c in self.changes if c.change_type is ChangeType.INSERT]

    def modified(self):
        return [c for c in self.changes if c.change_type is ChangeType.MODIFY]

    def deleted(self):
        return [c for c in self.changes if c.change_type is ChangeType.DELETE]

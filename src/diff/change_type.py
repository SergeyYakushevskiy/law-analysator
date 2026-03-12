from enum import Enum, auto

class ChangeType(Enum):
    INSERT = "вставлено"
    DELETE = "удалено"
    MODIFY = "изменено"

    def __str__(self):
        return self.value
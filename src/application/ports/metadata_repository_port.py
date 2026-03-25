from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional, Dict, Any

from src.infrastructure.parser.document import ParsedDocument


class MetadataRepositoryPort(ABC):

    @abstractmethod
    def get_all(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def find_by_path(self, file_path: Path) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def find_by_hash(self, file_hash: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def add_file(self, file_path: Path, file_hash: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def update_file(self, file_hash: str, **kwargs) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def delete_file(self, file_hash: str) -> None:
        pass

    @abstractmethod
    def set_order(self, file_hash: str, order_index: int) -> None:
        pass

    @abstractmethod
    def calculate_hash(self, file_path: Path) -> str:
        pass

    @abstractmethod
    def load_document(self, file_path: Path) -> ParsedDocument:
        pass
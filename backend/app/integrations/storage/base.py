# base.py
from abc import ABC, abstractmethod

class StorageBackend(ABC):
    @abstractmethod
    def save_file(self, relative_path: str, content: bytes) -> str:
        pass

    @abstractmethod
    def delete_file(self, relative_path: str) -> None:
        pass

    @abstractmethod
    def get_file_path(self, relative_path: str) -> str:
        pass
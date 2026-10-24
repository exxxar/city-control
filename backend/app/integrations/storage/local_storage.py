import os
import shutil
from app.core.config import settings

class LocalStorage:
    def __init__(self):
        self.base_path = settings.LOCAL_STORAGE_PATH
        os.makedirs(self.base_path, exist_ok=True)

    def save_file(self, relative_path: str, content: bytes):
        full_path = os.path.join(self.base_path, relative_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "wb") as f:
            f.write(content)
        return relative_path

    def delete_file(self, relative_path: str):
        full_path = os.path.join(self.base_path, relative_path)
        if os.path.exists(full_path):
            os.remove(full_path)

    def get_file_path(self, relative_path: str) -> str:
        return os.path.join(self.base_path, relative_path)

storage = LocalStorage()
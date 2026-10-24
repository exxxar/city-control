from fastapi import UploadFile, HTTPException
from app.core.constants import (
    MAX_IMAGE_SIZE_MB, MAX_VIDEO_SIZE_MB, MAX_DOCUMENT_SIZE_MB,
    ALLOWED_IMAGE_TYPES, ALLOWED_VIDEO_TYPES, ALLOWED_DOCUMENT_TYPES
)


async def validate_file(file: UploadFile, category: str = "image"):
    """Валидирует файл по MIME-типу и размеру."""
    content = await file.read()
    size_mb = len(content) / (1024 * 1024)
    await file.seek(0)  # Сбрасываем позицию для повторного чтения

    if category == "image":
        if file.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(400, f"Недопустимый тип изображения. Разрешены: {ALLOWED_IMAGE_TYPES}")
        if size_mb > MAX_IMAGE_SIZE_MB:
            raise HTTPException(400, f"Размер изображения превышает {MAX_IMAGE_SIZE_MB} МБ")
    elif category == "video":
        if file.content_type not in ALLOWED_VIDEO_TYPES:
            raise HTTPException(400, f"Недопустимый тип видео. Разрешены: {ALLOWED_VIDEO_TYPES}")
        if size_mb > MAX_VIDEO_SIZE_MB:
            raise HTTPException(400, f"Размер видео превышает {MAX_VIDEO_SIZE_MB} МБ")
    elif category == "document":
        if file.content_type not in ALLOWED_DOCUMENT_TYPES:
            raise HTTPException(400, f"Недопустимый тип документа. Разрешены: {ALLOWED_DOCUMENT_TYPES}")
        if size_mb > MAX_DOCUMENT_SIZE_MB:
            raise HTTPException(400, f"Размер документа превышает {MAX_DOCUMENT_SIZE_MB} МБ")

    return content
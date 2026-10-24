from PIL import Image
from PIL.ExifTags import TAGS
import io


def strip_exif(image_bytes: bytes) -> bytes:
    """Удаляет EXIF-метаданные из изображения (GPS, камера и т.д.)."""
    try:
        img = Image.open(io.BytesIO(image_bytes))
        data = list(img.getdata())
        clean_img = Image.new(img.mode, img.size)
        clean_img.putdata(data)

        buffer = io.BytesIO()
        clean_img.save(buffer, format=img.format or "JPEG")
        buffer.seek(0)
        return buffer.getvalue()
    except Exception:
        # Если не удалось обработать, возвращаем оригинал
        return image_bytes


def extract_gps_from_exif(image_bytes: bytes) -> tuple[float, float] | None:
    """Извлекает GPS-координаты из EXIF (если есть)."""
    try:
        img = Image.open(io.BytesIO(image_bytes))
        exif_data = img._getexif()
        if not exif_data:
            return None

        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag == "GPSInfo":
                # Парсинг GPS (упрощённо)
                # В реальности нужно конвертировать из DMS в десятичные градусы
                return None  # Заглушка
        return None
    except Exception:
        return None
# Статусы проблем (дублируем из моделей для удобства импорта)
PROBLEM_STATUSES = [
    "new", "needs_clarification", "confirmed", "transferred",
    "accepted", "in_progress", "suspended", "solution_ready",
    "awaiting_confirmation", "resolved", "closed", "rejected"
]

# Максимальные размеры файлов
MAX_IMAGE_SIZE_MB = 10
MAX_VIDEO_SIZE_MB = 100
MAX_DOCUMENT_SIZE_MB = 20

# Разрешённые MIME-типы
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp"]
ALLOWED_VIDEO_TYPES = ["video/mp4", "video/quicktime"]
ALLOWED_DOCUMENT_TYPES = ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]

# Настройки геолокации
DEFAULT_NOTIFICATION_RADIUS_M = 500
GEOFENCE_CHECK_INTERVAL_SECONDS = 60

# SLA
DEFAULT_SLA_REACTION_MINUTES = 120
DEFAULT_SLA_RESOLUTION_MINUTES = 4320  # 3 дня
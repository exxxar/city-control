from loguru import logger

class EmailSender:
    def send(self, to_email: str, subject: str, html_body: str):
        """Отправляет письмо. В прототипе просто логирует."""
        logger.info(f"[EMAIL] To: {to_email} | Subject: {subject}")
        # TODO: Реальная отправка через SMTP
        return True

email_sender = EmailSender()
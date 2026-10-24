class EmailService:
    def send_problem_created_email(self, to_email: str, problem_public_id: str):
        """Отправляет письмо о создании проблемы."""
        # TODO: Вызвать email_tasks.send_email.delay(...)
        print(f"[EmailService] Sending email to {to_email} about problem {problem_public_id}")

email_service = EmailService()
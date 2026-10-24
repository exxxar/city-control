from celery import shared_task
from app.integrations.email.sender import email_sender
from loguru import logger

@shared_task
def send_problem_created_email(to_email: str, problem_public_id: str, problem_title: str):
    html = f"""
    <h2>Ваше обращение зарегистрировано</h2>
    <p>Номер: <b>{problem_public_id}</b></p>
    <p>Заголовок: {problem_title}</p>
    <p>Мы уже передали его на рассмотрение.</p>
    """
    email_sender.send(to_email, f"Обращение №{problem_public_id} создано", html)

@shared_task
def send_status_change_email(to_email: str, problem_public_id: str, new_status: str):
    html = f"""
    <h2>Статус обращения изменен</h2>
    <p>Номер: <b>{problem_public_id}</b></p>
    <p>Новый статус: <b>{new_status}</b></p>
    """
    email_sender.send(to_email, f"Статус обращения №{problem_public_id} обновлен", html)
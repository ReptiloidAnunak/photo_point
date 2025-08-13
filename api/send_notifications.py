from settings import PROVIDERS_LIST, TWILIO_AUTH_TOKEN, TWILIO_FROM_PHONE, TWILIO_SID
from database.create_db import User
from tasks import send_mail_task, send_sms_task, send_tg_message_task
from typing import List



async def send_notification(message: str, user: User, providers: List[str]):
    for provider in providers:
        if provider not in PROVIDERS_LIST:
            return {"error": f"Invalid provider: {provider}"}
        
        if provider == 'email':
            task_mail = send_mail_task.delay(message) #  user.email
            print(f"Task_mail ID: {task_mail.id}")

        if provider == 'sms':
            task_sms = send_sms_task.delay(
            to_phone= user.phone,
            text=message,
            sid=TWILIO_SID,
            auth_token=TWILIO_AUTH_TOKEN,
            from_phone=TWILIO_FROM_PHONE
            )
            print(f"Task_phone ID: {task_sms.id}")

        if provider == 'telegram':
            task_tg = send_tg_message_task.delay(message, user.tg_chat_id)
            print(f"Task ID: {task_tg.id}")
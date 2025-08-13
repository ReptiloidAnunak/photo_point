from celery_app import celery_app
from providers.email_provider import send_email
from celery_app import celery_app
from providers.email_provider import send_email
from providers.sms_provider import send_sms
from celery_app import celery_app

from twilio.base.exceptions import TwilioRestException
from providers.telegram_provider import send_telegram_ptb


@celery_app.task(bind=True, autoretry_for=(TwilioRestException,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def send_sms_task(
    self,
    to_phone: str,
    text: str,
    sid: str,
    auth_token: str,
    from_phone: str | None = None,
    messaging_service_sid: str | None = None
    ) -> dict:

    send_sms(
        to_phone=to_phone,
        text=text,
        sid=sid,
        auth_token=auth_token,
        from_phone=from_phone,
        messaging_service_sid=messaging_service_sid
    )


@celery_app.task
def send_mail_task(message: str = "Hello from Celery!"):
    send_email("test@example.com", "Hi", message, smtp_host="mailhog", smtp_port=1025)


@celery_app.task
def send_tg_message_task(text: str):
    return send_telegram_ptb(text)
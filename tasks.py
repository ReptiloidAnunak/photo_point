from celery_app import celery_app
from providers.email_provider import send_email
from providers.sms_provider import send_sms
from providers.telegram_provider import send_telegram_ptb


class SkipChannel(Exception):
    """Exception to skip sending to a specific channel."""
    pass


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
    soft_time_limit=20, time_limit=30,
    name="tasks.send_with_fallback",
)
def send_with_fallback(self, message: str, user: dict, providers: list[str]) -> dict:
    last_err = None

    for ch in providers:
        try:
            if ch == "telegram":
                tg_id = user.get("tg_chat_id")
                if not tg_id:
                    continue
                send_telegram_ptb(message, tg_id)
                return {"status": "SENT", "channel": "telegram"}

            elif ch == "sms":
                if not (user.get("phone") and user.get("twilio_sid") and user.get("twilio_auth_token")):
                    continue
                sms_sid = send_sms(
                    to_phone=user["phone"],
                    text=message,
                    sid=user["twilio_sid"],
                    auth_token=user["twilio_auth_token"],
                    from_phone=user.get("twilio_from_phone"),
                    messaging_service_sid=user.get("twilio_messaging_service_sid"),
                )
                return {"status": "SENT", "channel": "sms", "provider_id": sms_sid}

            elif ch == "email":
                to = user.get("email")
                if not to:
                    continue
                send_email(to, "Photo Point Notification", message, smtp_host="mailhog", smtp_port=1025)
                return {"status": "SENT", "channel": "email"}

            else:
                continue

        except Exception as e:
            last_err = e
            print(f"[fallback:{ch}] {e}")
            continue

    raise last_err or RuntimeError("All channels failed")

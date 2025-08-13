
import smtplib
from email.message import EmailMessage

def send_email(
    subject: str,
    text: str,
    to_email: str = "test@example.com",
    smtp_host: str = "127.0.0.1",
    smtp_port: int = 1025,                  
    smtp_from: str = "no-reply@example.com",
    smtp_user: str | None = None,
    smtp_pass: str | None = None,
    use_tls: bool = False,
) -> None:
    
    msg = EmailMessage()
    msg["From"] = smtp_from
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(text)

    with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as s:
        if use_tls:
            s.starttls()
        if smtp_user and smtp_pass:
            s.login(smtp_user, smtp_pass)
        s.send_message(msg)

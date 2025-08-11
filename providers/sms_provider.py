#+18597192825


from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


def send_sms(to_phone: str, 
             text: str, 
             sid: str, 
             auth_token: str, 
             messaging_service_sid: str,
             from_phone: str) -> str:
    
    client = Client(sid, auth_token)
    try:
        if messaging_service_sid:
            msg = client.messages.create(
                messaging_service_sid=messaging_service_sid,
                to=to_phone,
                body=text,
            )
        else:
            msg = client.messages.create(
                from_=from_phone,
                to=to_phone,
                body=text,
            )
        return {"sid": msg.sid, "status": msg.status}
    except TwilioRestException as e:
        raise

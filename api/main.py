from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Form
from typing import Annotated, Optional, List

from settings import TEMPLATES_DIR, TWILIO_AUTH_TOKEN, TWILIO_FROM_PHONE, TWILIO_SID
from database.models import Message
from tasks import send_mail_task, send_sms_task, send_tg_message_task
from celery_app import celery_app



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory=TEMPLATES_DIR)


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/send_message")
async def send_message(request: Request, 
                       message: Annotated[str, Form()],
                       providers: Annotated[Optional[List[str]], Form(None)],
                       ):
    print(f"Received message: {message}")
    print(f"Selected providers: {providers}")

    # task_mail = send_mail_task.delay(message)
    # print(f"Task ID: {task_mail.id}")

    # task_sms = send_sms_task.delay(
    # to_phone="+541133433412",
    # text=message,
    # sid=TWILIO_SID,
    # auth_token=TWILIO_AUTH_TOKEN,
    # from_phone=TWILIO_FROM_PHONE
    # )
    # print(f"Task ID: {task_sms.id}")


    task_tg = send_tg_message_task.delay(message)
    print(f"Task ID: {task_tg.id}")

    return RedirectResponse(url="/", status_code=303)


@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    result = celery_app.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None
        }
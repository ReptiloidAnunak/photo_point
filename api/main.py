from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Form
from typing import Annotated, Optional, List

from settings import TEMPLATES_DIR, TWILIO_AUTH_TOKEN, TWILIO_FROM_PHONE, TWILIO_SID
from database.create_db import register_user, get_all_users
from tasks import send_mail_task, send_sms_task, send_tg_message_task
from celery_app import celery_app


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory=TEMPLATES_DIR)

@app.get("/register", response_class=HTMLResponse)
async def get_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register_user")
async def post_register_user(request: Request, 
                              username: Annotated[str, Form()],
                              email: Annotated[str, Form()],
                              phone: Annotated[str, Form()],
                              ):
    print(f"Registering user: {username}, {email}, {phone}")
    user = register_user(username=username, email=email, phone=phone)
    print(f"Registered user ID: {user.id}")
    return RedirectResponse(url="/", status_code=303)


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/send_message")
async def send_message(request: Request, 
                       message: Annotated[str, Form()],
                       providers: Annotated[Optional[List[str]], Form()],
                       ):
    providers_lst = ['sms', 'email', 'telegram']
    print(f"Received message: {message}")
    print(f"Selected providers: {providers}")


    users = get_all_users()
    print(f"Registered users: {users}")

    for user in users:
        for provider in providers:
            if provider not in providers_lst:
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
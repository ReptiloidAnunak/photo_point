from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Form
from typing import Annotated, Optional, List
import asyncio
from starlette.middleware.sessions import SessionMiddleware
from settings import TEMPLATES_DIR
from database.create_db import register_user, get_all_users
from celery_app import celery_app
from tasks import send_with_fallback
from settings import TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_PHONE

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(SessionMiddleware, secret_key="superkey")

templates = Jinja2Templates(directory=TEMPLATES_DIR)

@app.get("/register", response_class=HTMLResponse)
async def get_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register_user")
async def post_register_user(
    request: Request, 
    username: Annotated[str, Form()],
    email: Annotated[str, Form()],
    phone: Annotated[str, Form()],
):
    print(f"Registering user: {username}, {email}, {phone}")
    user = register_user(username=username, email=email, phone=phone)
    print(f"Registered user ID: {user.id}")
    return RedirectResponse(url="/", status_code=303)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):    
    users = get_all_users()

    if not users:
        return RedirectResponse(url="/register", status_code=303)

    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/send_message")
async def send_message(
    request: Request, 
    message: Annotated[str, Form()],
    providers: Annotated[Optional[List[str]], Form()],
):
    print(f"Received message: {message}")
    print(f"Selected providers: {providers}")

    users = get_all_users()

    if not providers:
        return RedirectResponse(url="/", status_code=303)

    tasks_info = []

    for user in users:
        print(f"! EMAIL: {user.email}")

        payload = {
            "email": user.email,
            "phone": user.phone,
            "tg_chat_id": getattr(user, "tg_chat_id", None),
            "twilio_sid": TWILIO_SID,
            "twilio_auth_token": TWILIO_AUTH_TOKEN,
            "twilio_from_phone": TWILIO_FROM_PHONE,
        }

        print(f"PAYLOAD: {payload}")

        task = send_with_fallback.delay(message, payload, providers)
        await asyncio.sleep(1.5)

        tasks_info.append({
            "task_id": task.id,
            "email": user.email,
            "phone": user.phone,
            "message": message,
            "username": user.username
        })

    request.session["tasks"] = tasks_info
    return RedirectResponse(url="/tasks/", status_code=303)


@app.get("/tasks/", response_class=HTMLResponse)
async def tasks_lst(request: Request):
    saved = request.session.get('tasks', [])
    
    tasks_with_status = []
    
    for item in saved:
        result = celery_app.AsyncResult(item["task_id"])
        tasks_with_status.append(
            {
            "task_id": item["task_id"],
            "status": result.status,
            "result": result.result or None,
            "message": item["message"],
            "username": item["username"]
            }
        )

    return templates.TemplateResponse(
        "tasks.html",
        {"request": request,
         "tasks": tasks_with_status
         }
    )


@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    result = celery_app.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None
    }

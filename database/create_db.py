
from __future__ import annotations
import os
from typing import Optional, Iterable
import sqlite3
from sqlmodel import SQLModel, Field, Session, create_engine, select
from sqlalchemy import Column, Integer, String, Boolean, event
from settings import DATABASE_URL

class User(SQLModel, table=True):
    __tablename__ = "user"

    id: Optional[int] = Field(default=None, primary_key=True)

    tg_chat_id: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer, unique=True, index=True, nullable=True),
        description="chat_id лички; None если не известен",
    )

    username: Optional[str] = Field(
        default=None,
        sa_column=Column(String, unique=True, nullable=False),
    )

    phone: Optional[str] = Field(
        default=None,
        sa_column=Column(String, unique=True, nullable=False),
    )
    email: Optional[str] = Field(
        default=None,
        sa_column=Column(String, unique=True, nullable=False),
    )

    tg_chat_is_blocked: bool = Field(
        default=False,
        sa_column=Column(Boolean, nullable=False),
        description="1 = заблокировал бота / chat not found",
    )


def _sqlite_url(db: str) -> str:
    return db if db.startswith("sqlite:///") else f"sqlite:///{db}"

def _ensure_dir(db_path_or_url: str) -> None:
    if db_path_or_url.startswith("sqlite:///"):
        path = db_path_or_url.replace("sqlite:///", "", 1)
    else:
        path = db_path_or_url
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)

DB_URL = _sqlite_url(DATABASE_URL)
_ensure_dir(DB_URL)

engine = create_engine(DB_URL, echo=False, connect_args={"check_same_thread": False})


@event.listens_for(engine, "connect")
def set_sqlite_pragmas(dbapi_conn, _):
    cur = dbapi_conn.cursor()
    cur.execute("PRAGMA journal_mode=WAL;")
    cur.execute("PRAGMA busy_timeout=5000;")
    cur.close()

def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)


def register_user(username: str, email: str, phone: str) -> User:
    with get_session() as s:
        user = s.exec(select(User).where((User.username == username) | (User.email == email) | (User.phone == phone))).one_or_none()
        if user is None:
            user = User(username=username, email=email, phone=phone, tg_chat_is_blocked=False)
            s.add(user)
            s.commit()
            s.refresh(user)
        return user

def upsert_chat(tg_chat_id: int, username: Optional[str] = None) -> User:

    with get_session() as s:
        user = s.exec(select(User).where(User.tg_chat_id == tg_chat_id)).one_or_none()
        if user is None:
            user = User(tg_chat_id=tg_chat_id, username=username, tg_chat_is_blocked=False)
            s.add(user)
        else:
            if username and not user.username:
                user.username = username
            user.tg_chat_is_blocked = False
        s.commit()
        s.refresh(user)
        return user

def mark_blocked(tg_chat_id: int) -> None:
    with get_session() as s:
        user = s.exec(select(User).where(User.tg_chat_id == tg_chat_id)).one_or_none()
        if user:
            user.tg_chat_is_blocked = True
            s.add(user)
            s.commit()

def list_active_ids() -> list[int]:
    with get_session() as s:
        rows: Iterable[int] = s.exec(
            select(User.tg_chat_id).where(
                User.tg_chat_is_blocked == False,
                User.tg_chat_id.is_not(None)
            )
        )
        return [cid for cid in rows if cid is not None]
    

def get_all_users() -> list[User]:
    with get_session() as s:
        return s.exec(select(User)).all()
    

print("DB_URL:", DB_URL)
real_path = DB_URL.replace("sqlite:///", "", 1) if DB_URL.startswith("sqlite:///") else DB_URL
print("DB file path:", real_path)
init_db()
print("Exists:", os.path.exists(real_path))
con = sqlite3.connect(real_path)
print(con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())




from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Integer, String, Boolean


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: Optional[int] = Field(default=None, primary_key=True)

    tg_chat_id: Optional[int] = Field(
        default=None,
        sa_column=Column(Integer, unique=True, index=True, nullable=True),
        description="tg_chat_id лички; None если не известен",
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
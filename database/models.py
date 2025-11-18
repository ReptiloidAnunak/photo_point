

from typing import Optional, Annotated
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Integer, String, Boolean

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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

    disabled: bool | None = Field(default=False,
                                  sa_column=Column(Boolean, nullable=False)
    )   

    def fake_decode_token(token):
        return User(
            username=token + 'fakedecoded', email="john@example.com", full_name="John Doe"
        )
    
    async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
        user = fake_decode_token(token)
        return user

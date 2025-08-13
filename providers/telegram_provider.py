import asyncio
from telegram import Bot
from telegram.error import TimedOut
from settings import TG_BOT_TOKEN


async def _send(text: str, tg_chat_id: int) -> dict:
    bot = Bot(token=TG_BOT_TOKEN)
    try:
        msg = await bot.send_message(chat_id=tg_chat_id, text=text)
    except TimedOut:
        print("Telegram message sending timed out.")
    return {"message_id": msg.message_id}


def send_telegram_ptb(text: str, tg_chat_id: int) -> dict:
    return asyncio.run(_send(text, tg_chat_id))


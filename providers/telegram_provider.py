import asyncio
from telegram import Bot
from telegram.error import TimedOut
from settings import TG_BOT_TOKEN, TG_BOT_CHAT

# providers/telegram_ptb.py (асинхронная отправка)

async def _send(text: str):
    bot = Bot(token=TG_BOT_TOKEN)
    try:
        msg = await bot.send_message(chat_id=TG_BOT_CHAT, text=text)
    except TimedOut:
        print("Telegram message sending timed out.")
    return {"message_id": msg.message_id}


def send_telegram_ptb(text: str):
    return asyncio.run(_send(text))


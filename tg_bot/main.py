from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CommandHandler, ContextTypes, MessageHandler, filters
from database.create_db import get_user_by_username,set_user_tg_chat_id
from settings import TG_BOT_TOKEN

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Received command: {update.message.chat_id} {update.message.text}")
    await update.message.reply_text(f'Enter your username after your registration, please!')

async def check_site_username_in_db(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = get_user_by_username(update.message.text)

    if user:
        set_user_tg_chat_id(user.username, update.message.chat_id)
        await update.message.reply_text(f'Hello, {user.username}!\nYou`ll receive our notifications.')
    else:
        await update.message.reply_text(f'User with username {update.message.text} not found in the database. Please register first.')


def main() -> None:
    print("Starting Telegram bot...")
    # Create the application and pass it your bot
    app = ApplicationBuilder().token(TG_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", hello))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_site_username_in_db))

    app.run_polling()


if __name__ == '__main__':
    main()
    print("Telegram bot started.")
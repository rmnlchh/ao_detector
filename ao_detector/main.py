import logging
import traceback

from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters

from database import init_db
from handler import photo, share, handle_text_message, add_corrected_object
from handler import start, help

TOKEN = "TOKEN"


def main():
    init_db()

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.contact, share))
    dp.add_handler(MessageHandler(Filters.photo, photo))
    dp.add_handler(CallbackQueryHandler(add_corrected_object))
    dp.add_handler(MessageHandler(Filters.text, handle_text_message))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()

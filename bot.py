from dotenv import load_dotenv
import os
from typing import Final
from telegram import Update
update = Update
from telegram.ext import MessageHandler,Application, CommandHandler, filters
load_dotenv()
TOKEN : Final = os.getenv("TOKEN")
botUsername : Final = os.getenv("botUsername")
from commands import start_command ,help_command
from handleMessage import handle_message
from handleError import error
if __name__ == '__main__':
    print('Starting bot ...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help',help_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
   
    # Errors
    app.add_error_handler(error)
    print('Polling ...')
    app.run_polling(poll_interval=3, timeout=600)


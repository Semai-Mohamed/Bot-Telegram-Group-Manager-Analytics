from telegram import Update
from telegram.ext import CommandHandler
async def list_admins(update:Update,chat):
    admins = await chat.get_administrators()
    admin_list = '\n'.join([f'{admin.user.username}'for admin in admins])
    print("mohamed")
    await update.message.reply_text(f"List of admins:\n{admin_list}")
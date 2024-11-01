from telegram import Update
from telegram.ext import CommandHandler
async def block_user(update:Update,chat_id,user_id_to_ban,context:CommandHandler):
        context.bot.ban_chat_member(chat_id,user_id_to_ban)
        await update.message.reply_text("User has been banned!")
async def unblock_user(update:Update,chat_id,user_id_to_unban,context:CommandHandler):
        context.bot.unban_chat_member(chat_id,user_id_to_unban)
        await update.message.reply_text("User has been unbanned!")
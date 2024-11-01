from telegram.ext import CallbackContext
from telegram import ChatPermissions
def unmute_user(context: CallbackContext):
        job = context.job
        chat_id = job.context['chat_id']
        user_id = job.context['user_id']

        context.bot.restrict_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                permissions=ChatPermissions(can_send_messages=True)
        )
        context.bot.send_message(chat_id, text=f"User {user_id} has been unmuted.")
def unmute_user_manuell(context: CallbackContext,user_id,chat_id):
        context.bot.restrict_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                permissions=ChatPermissions(can_send_messages=True)
        )
        context.bot.send_message(chat_id, text=f"User {user_id} has been unmuted.")
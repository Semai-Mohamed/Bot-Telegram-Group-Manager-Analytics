import os
from telegram import ChatPermissions
from telegram.ext import CallbackContext
from typing import Final
from unmuteUser import unmute_user
Token : Final = os.getenv('TOKEN')
def mute_user(context: CallbackContext,chat_id,user_id,mute_duration):
        context.bot.restrict_chat_member(
           chat_id=chat_id,
           user_id=user_id,
           permissions=ChatPermissions(can_send_messages=False)       
           )
        context.bot.send_message(chat_id,text=f'User {user_id} had been muted')
        if mute_duration:
                context.job_queue.run_once(
                        unmute_user,
                        mute_duration,
                        context={'chat_id':chat_id, 'user_id':user_id}
                )
                context.bot.send_message(chat_id,text=f'User {user_id} will be unmuted in {mute_duration // 60} minutes')
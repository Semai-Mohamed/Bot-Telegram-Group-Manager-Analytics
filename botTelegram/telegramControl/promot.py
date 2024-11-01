from telegram import Update , ChatPermissions
from telegram.ext import  ContextTypes
update=Update
context = ContextTypes.DEFAULT_TYPE
async def promot_to_admin(user_to_promote_to_admin,chat_id):   
    try:
        permissions = ChatPermissions(
            can_change_info = False,
            can_send_media_messages=True,      
            can_delete_messages=True,
            can_invite_users=True,
            can_restrict_member=True,
            can_pin_messages=True,
            can_promote_members=False
        )
        await context.bot.promote_chat_member(
            chat_id=chat_id,
            user_id=user_to_promote_to_admin,
            permissions = permissions
            
        )
        await update.message.reply_text('User has been promoted to admin!')
    except Exception as e:
        await update.message.reply_text(f'An error occured: {str(e)}')

  
async def promot_to_special(user_to_promote_to_special,chat_id):
    try:
        permissions = ChatPermissions(
            can_send_messages=True,          
            can_send_media_messages=True,      
            can_send_polls=False,              
            can_send_other_messages=True,     
            can_add_web_page_previews=False,  
            can_invite_users=True,            
            can_pin_messages=False,           
            can_change_info=False      
        )
        await context.bot.promote_chat_member(
            chat_id=chat_id,
            user_id=user_to_promote_to_special,
            permissions=permissions
                   
        )
        await update.message.reply_text('User has been promoted to admin!')
    except Exception as e:
        await update.message.reply_text(f'An error occured: {str(e)}')

    

     
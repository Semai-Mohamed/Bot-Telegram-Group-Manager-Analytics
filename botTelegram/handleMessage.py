import os
import re
from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.error import TimedOut
from telegram.ext import ContextTypes
from dotenv import load_dotenv
from telegramControl.handleResponse import handle_response
from telegramOutsideControl.music import download_music
from telegramControl.muteUser import mute_user
from telegramControl.unmuteUser import unmute_user, unmute_user_manuell
from telegramControl.block import block_user,unblock_user
from telegramControl.listAdmin import list_admins
from telegramControl.promot import promot_to_admin,promot_to_special
from telegramOutsideControl.interactions import increment_group_interaction,increment_user_interaction,get_most_active_groups,get_ranked_users
import sys
sys.path.append(os.path.abspath('/database'))
sys.path.append(os.path.abspath('/telegramControl'))
sys.path.append(os.path.abspath('/telegramOutsideControl'))
load_dotenv()
Token = os.getenv('TOKEN')
botUsername = os.getenv('botUsername')
async def reply(update: Update, user, chat, mute_duration):
    user_to_mute = update.message.reply_to_message.from_user
    if user_to_mute.id == user.id:
        return await update.message.reply_text("You can't mute yourself.")
    
    admins = await chat.get_administrators()  
    if user_to_mute.id in [admin.user.id for admin in admins]:
        return await update.message.reply_text("Can't mute an admin.")
    
    return await mute_user(chat.id, user_to_mute.id, mute_duration)
async def mentioned(update: Update, username, chat, context, user, mute_duration):
    admins = await context.bot.get_chat_administrators(chat.id)
    
    if username == user.username:
        return await update.message.reply_text("You can't mute yourself.")
    
    if username in [admin.user.username for admin in admins]:
        return await update.message.reply_text("Can't mute an admin.")
    
    try:
        member = await context.bot.get_chat_member(chat.id, username) 
        if member:
            return await mute_user(chat.id, member.user.id, mute_duration)
    except:
        return await update.message.reply_text("Can't find this username.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    increment_user_interaction(update.message.from_user.id, update.message.from_user.username)
    increment_group_interaction(update.message.chat_id, update.message.chat.title)

    if not text or not text.strip():
        await update.message.reply_text("Empty message received.")
        return
    new_text: str = text.strip().lower()

    if 'group' in message_type:
        if botUsername in text:
            new_text = text.replace(botUsername, '').strip()
            
    else:
        new_text = text.strip().lower()

    # Music handling
    if 'music' in new_text:
     song_name = new_text.replace("music", "").strip()
     if song_name:
        music_file, thumbnail_file = download_music(song_name)
        keyboard = [
            [InlineKeyboardButton("🎧 Play Now", callback_data='play')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        
        if music_file and os.path.exists(music_file):
                with open(music_file, 'rb') as audio_file:
                    if thumbnail_file and os.path.exists(thumbnail_file):
                        with open(thumbnail_file, 'rb') as thumb_image:
                            await update.message.reply_audio(
                                audio_file,
                                caption=f"🎶 Now playing: *{song_name}*\nEnjoy the music! 🎧",
                                parse_mode='Markdown',
                                thumbnail=thumb_image,
                                reply_markup=reply_markup
                            )
                    else:
                        await update.message.reply_audio(
                            audio_file,
                            caption=f"🎶 Now playing: *{song_name}*\nEnjoy the music! 🎧",
                            parse_mode='Markdown',
                            reply_markup=reply_markup,
                            read_timeout=120, 
                            write_timeout=120,
                            connect_timeout=60,
                            pool_timeout=60   
                                           )

                # Cleanup files after sending
                os.remove(music_file)
                if thumbnail_file and os.path.exists(thumbnail_file):
                    os.remove(thumbnail_file)
        else:
                await update.message.reply_text("Sorry, I couldn't find the music you're looking for.")
        
     else:
        await update.message.reply_text("Please specify the name of the song you want.")
    # Mute handling
    if new_text.startswith("mute"):
        user = update.message.from_user
        chat = update.message.chat

        admins = await chat.get_administrators()
        if user.id in [admin.user.id for admin in admins]:
            match = re.match(r'mute (\d+)([mh])(?:\s*@([A-Za-z0-9_]+))?', new_text.lower())
            mute_duration = None
            mentioned_username =""
            print(match)
            if match:
                value = match.group(1)  
                unit = match.group(2) 
                mentioned_username = match.group(3) 
                print(value)
                print(unit)
                print(mentioned_username,'estin')
                value = int(value)
                if unit == "m":
                    mute_duration = value * 60
                elif unit == "h":
                    mute_duration = value * 3600
                elif unit == "d":
                    mute_duration = value * 3600 * 24
            
            # Case 1: replying
            if update.message.reply_to_message:
                await reply(update, user, chat, mute_duration)
            # Case 2: mentioned
            elif mentioned_username:
                await mentioned(update, mentioned_username, chat, context, user, mute_duration)
            else:
                return await update.message.reply_text("Wrong! the expression should be ' mute + valueUnit +username '")
        else:
            return await update.message.reply_text("You don't have permission to do that.")

    if new_text.startswith("unmute"):
        user = update.message.from_user
        chat = update.message.chat
        admins = await chat.get_administrators()

        if user.id in [admin.user.id for admin in admins]:
            match = re.match(r'unmute (?:\s*@([A-Za-z0-9_]+))?', new_text)
            if match:
                mentioned_username = match.group(1)
                try:
                    member = await context.bot.get_chat_member(chat.id, mentioned_username)
                    return await unmute_user(chat.id, member.user.id)
                except:
                    return await update.message.reply_text("User not found.")
    
    if new_text == "unmute all":
        members = await context.bot.get_chat_members(chat.id)
        for member in members:
            await unmute_user_manuell(context, member.user.id, chat.id)
    if new_text=="block":
        user_to_ban_id= update.message.reply_to_message.from_user.id
        AdminUser_id = update.message.from_user.id
        chat_id = update.message.chat_id
        chat = update.message.chat
        admins = await chat.get_administrators()
        if AdminUser_id in [admin.user.id for admin in admins]:
         if update.message.reply_to_message:
            if user_to_ban_id == AdminUser_id :
                return await update.message.reply_text("You can't block your self")
            elif user_to_ban_id in [admin.user.id for admin in admins]:
                return await update.message.reply_text("Can't block an admin")
            else :
                return await block_user(chat_id,user_to_ban_id)
         else:
                return await update.message.reply_text("Wrong! the expression should be and reply to a message and with expression ' block  '")
        else :
            return await update.message.reply_text("You can't do this operation")
    if new_text=="unblock":
        user_to_unban_id = update.message.reply_to_message.from_user.id
        AdminUser_id = update.message.from_user.id
        chat_id = update.message.chat_id
        chat = update.message.chat
        admins = await chat.get_administrators()
        if AdminUser_id in [admin.user.id for admin in admins]:
            if update.message.reply_to_message:
                if user_to_ban_id == AdminUser_id:
                    return await update.message.reply_text("You can't unban your self")
                else :
                    return await unblock_user(update,chat_id,user_to_unban_id)
            else:
                return await update.message.reply_text("Wrong! the expression should be and reply to a message and with expression ' unblock'")
    if new_text =="list admins":
        chat = update.message.chat
        await list_admins(update,chat)
    if new_text == "raiseAdmin":
        chat = update.message.chat
        user_id = update.message.from_user.id
        user_to_promote_to_admin_id = update.message.reply_to_message.from_user.id   
        owner_id = "" 
        if update.message.reply_to_message :
         admins = await chat.get_administrators()
         for admin in admins :
            if admin.status == 'creator':
                owner_id = admin.user.id
                break
         if user_id == owner_id:
           await promot_to_admin(user_to_promote_to_admin_id,chat.id)
         else:
           return await  update.message.reply_text('You are not the creator to promot users')
        else:
           return await update.message.reply_text('there no user to promot')
    if new_text =="raiseSpecial":
        chat = update.message.chat
        user_id = update.message.from_user.id
        user_to_promote_to_special_id = update.message.reply_to_message.from_user.id   
        owner_id = "" 
        if update.message.reply_to_message :
            admins = await chat.get_administrators()
            for admin in admins :
              if admin.status == 'creator':
                owner_id = admin.user.id
                break
            if user_id == owner_id:
               return await promot_to_special(user_to_promote_to_special_id,chat.id)
            else:
                return await  update.message.reply_text("You are not the creator you can't do this operation")
        else :
            return await update.message.reply_text('there no user to promot')
    if new_text == "gI":
     return await get_most_active_groups(update)
    
    else :
         print(new_text)
         if handle_response(new_text):
           await update.message.reply_text(handle_response(new_text))
         
     
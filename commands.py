from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardMarkup,InlineKeyboardButton
keyboard = [
    [InlineKeyboardButton("/Help",callback_data='play')],
    [InlineKeyboardButton("/Updates",callback_data="play")],
    
]
reply_commande = InlineKeyboardMarkup(keyboard)
async def start_command(update : Update,context:ContextTypes):
    await update.message.reply_text("""
Hello, this is manage_bot, a bot specialized in managing groups with many features provided by my developer @guts_al.
""",reply_markup=reply_commande)

async def help_command(update : Update,context:ContextTypes):
    await update.message.reply_text("""
1. Group Management:

Block a user:
Command: block

Unblock a user:
Command: unblock

Mute a user:

By username: mute + @username
By replying to their message: mute
Unmute a user:
Command: unmute

Play music:
Command: music + nameOfSong

List all admins:
Command: admin list

List special members:
Command: special list

Show rank:

Your own rank: myRank
Someone else's rank: Rank + @username
View statistics:

Your own statistics: myStatistics
Someone else's statistics: Statistics + @username
Promote a user:

Promote to special member: raiseSpecial
Promote to admin: raiseAdmin
Remove ranks:

Remove a single user's rank: wipe + @username
Remove ranks for everyone: wipeAll
2. Bot-Related Commands:

Most active groups:
Command: gI

Rank users by interaction:
Command: pI

3. Under Development:

Image design
Creating relationships between groups linked to the main group
Allowing users to change commands"""
                                    )


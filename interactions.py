import pyodbc
from telegram import Update
from telegram.ext import  ContextTypes

# Database connection
def connect_to_db():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server}'
        'SERVER=localhost'
        'DATABASE=bot_database'
        'UID=bot_databse'
        'PWD=123'  
    )
    return conn
async def increment_user_interaction(user_id, username):
    db = connect_to_db()
    cursor = db.cursor()
    query = '''
    MERGE INTO users_interaction AS target
    USING (SELECT ? AS user_id, ? AS username) AS source
    ON (target.user_id = source.user_id)
    WHEN MATCHED THEN 
        UPDATE SET interaction_count = interaction_count + 1
    WHEN NOT MATCHED THEN
        INSERT (user_id, username, interaction_count) 
        VALUES (source.user_id, source.username, 1);
    '''
    cursor.execute(query, (user_id, username))
    db.commit()

    cursor.close()
    db.close()

async def increment_group_interaction(group_id, group_name):
    db = connect_to_db()
    cursor = db.cursor()
    query = '''
    MERGE INTO groups_interaction AS target
    USING (SELECT ? AS group_id, ? AS group_name) AS source
    ON (target.group_id = source.group_id)
    WHEN MATCHED THEN 
        UPDATE SET interaction_count = interaction_count + 1
    WHEN NOT MATCHED THEN
        INSERT (group_id, group_name, interaction_count) 
        VALUES (source.group_id, source.group_name, 1);
    '''
    cursor.execute(query, (group_id, group_name))
    db.commit()
    cursor.close()
    db.close()
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    username = update.message.from_user.username or "unknown"
    chat_type = update.message.chat.type
    chat_id = update.message.chat.id
    if chat_type == 'group' or chat_type == 'supergroup':
        group_name = update.message.chat.title
        await increment_group_interaction(chat_id, group_name)
    await increment_user_interaction(user_id, username)
    await update.message.reply_text(f"Message received! {username} sent a message.")
async def get_most_active_groups(update: Update):
    context= ContextTypes.DEFAULT_TYPE
    db = connect_to_db()
    cursor = db.cursor()
    query = '''
    SELECT group_name, interaction_count
    FROM groups_interaction
    ORDER BY interaction_count DESC
    OFFSET 0 ROWS FETCH NEXT 10 ROWS ONLY;
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    group_list = "\n".join([f"{group[0]}: {group[1]} messages" for group in result])
    await update.message.reply_text(f"Most Active Groups:\n{group_list}")
    cursor.close()
    db.close()
async def get_ranked_users(update: Update):
    context= ContextTypes.DEFAULT_TYPE
    db = connect_to_db()
    cursor = db.cursor()
    query = '''
    SELECT username, interaction_count
    FROM users_interaction
    ORDER BY interaction_count DESC
    OFFSET 0 ROWS FETCH NEXT 10 ROWS ONLY;
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    user_list = "\n".join([f"{user[0]}: {user[1]} interactions" for user in result])
    await update.message.reply_text(f"Top Users by Interaction:\n{user_list}")
    cursor.close()
    db.close()

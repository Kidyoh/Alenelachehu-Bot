import sqlite3
from config import DB_NAME
from datetime import datetime

def get_db_connection():
    return sqlite3.connect(DB_NAME)

def setup_database():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY, nickname TEXT, age INTEGER, gender TEXT, nationality TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS vents
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, content TEXT, timestamp TEXT, 
                  allow_reactions BOOLEAN, allow_public_comments BOOLEAN, allow_professional_comments BOOLEAN)''')
    conn.commit()
    conn.close()

def get_user_profile(user_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    profile = c.fetchone()
    conn.close()
    return profile

def update_user_profile(user_id, nickname, age, gender, nationality):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO users (user_id, nickname, age, gender, nationality) VALUES (?, ?, ?, ?, ?)",
              (user_id, nickname, age, gender, nationality))
    conn.commit()
    conn.close()

def save_vent(user_id, content, allow_reactions, allow_public_comments, allow_professional_comments):
    conn = get_db_connection()
    c = conn.cursor()
    timestamp = datetime.now().isoformat()
    c.execute("INSERT INTO vents (user_id, content, timestamp, allow_reactions, allow_public_comments, allow_professional_comments) VALUES (?, ?, ?, ?, ?, ?)",
              (user_id, content, timestamp, allow_reactions, allow_public_comments, allow_professional_comments))
    conn.commit()
    conn.close()
import sqlite3

from sqlite3 import Error


def create_db():
    conn = sqlite3.connect('bot.db')
    conn.execute("PRAGMA foreign_keys = 1")

    cursor_obj = conn.cursor()

    cursor_obj.execute(
        '''CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT, last_name TEXT, chat_id INTEGER);''')
    cursor_obj.execute(
        '''CREATE TABLE tasks(id INTEGER PRIMARY KEY, link TEXT, state TEXT, note REAL, user_id INTEGER, FOREIGN KEY(user_id) REFERENCES users(id));''')

    conn.commit()
    conn.close()

def insert_user(user_params):
    conn = sqlite3.connect('bot.db')
    cursor_obj = conn.cursor()

    cursor_obj.execute('''INSERT INTO users(name, last_name, chat_id) VALUES(?, ?, ?)''', user_params)

    conn.commit()
    conn.close()


def insert_task(task_params):
    conn = sqlite3.connect('bot.db')
    conn.execute("PRAGMA foreign_keys = 1")
    cursor_obj = conn.cursor()

    cursor_obj.execute('''INSERT INTO tasks(id, link, state, note, user_id) VALUES(?, ?, ?, ?)''', task_params)

    conn.commit()
    conn.close()


def get_user_by_chat_id(chat_id):
    conn = sqlite3.connect('bot.db')
    cursor_obj = conn.cursor()

    cursor_obj.execute('''SELECT * FROM users WHERE chat_id = ?''', [chat_id])

    row = cursor_obj.fetchone()
    conn.close()

    return row


def get_task_by_id(task_id):
    conn = sqlite3.connect('bot.db')
    cursor_obj = conn.cursor()

    cursor_obj.execute('''SELECT * FROM tasks WHERE id = %s''', task_id)

    row = cursor_obj.fetchone()
    conn.close()

    return row

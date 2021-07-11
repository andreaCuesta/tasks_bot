import sqlite3

DATABASE_PATH = 'src/DB/bot.db'

def create_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute("PRAGMA foreign_keys = 1")

    cursor_obj = conn.cursor()

    cursor_obj.execute(
        '''CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT, last_name TEXT, chat_id INTEGER);''')
    cursor_obj.execute(
        '''CREATE TABLE tasks(id INTEGER PRIMARY KEY, link TEXT, status TEXT, grade REAL, user_id INTEGER, FOREIGN KEY(user_id) REFERENCES users(id));''')

    conn.commit()
    conn.close()

def insert_user(user_params):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor_obj = conn.cursor()

    cursor_obj.execute('''INSERT INTO users(name, last_name, chat_id) VALUES(?, ?, ?)''', user_params)

    conn.commit()
    conn.close()

def insert_task(task_params):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute("PRAGMA foreign_keys = 1")
    cursor_obj = conn.cursor()

    cursor_obj.execute('''INSERT INTO tasks(link, status, grade, user_id) VALUES(?, ?, ?, ?)''', task_params)

    conn.commit()
    task_id = cursor_obj.lastrowid

    conn.close()

    return task_id

def get_user_by_chat_id(chat_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor_obj = conn.cursor()

    cursor_obj.execute('''SELECT * FROM users WHERE chat_id = ?''', [chat_id])

    row = cursor_obj.fetchone()
    conn.close()

    return row

def get_task_by_id_and_user(task_id, user_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor_obj = conn.cursor()

    cursor_obj.execute('''SELECT * FROM tasks WHERE id = ? and user_id = ?''', [task_id, user_id])

    row = cursor_obj.fetchone()
    conn.close()

    return row

def get_task_by_user_and_link(user_id, link):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor_obj = conn.cursor()

    cursor_obj.execute('''SELECT * FROM tasks WHERE user_id = ? and link = ?''', [user_id, link])

    row = cursor_obj.fetchone()
    conn.close()

    return row

def list_tasks_by_user(user_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor_obj = conn.cursor()

    cursor_obj.execute('''SELECT * FROM tasks WHERE user_id = ?''', [user_id])

    rows = cursor_obj.fetchall()
    conn.close()

    return rows

def edit_task(task_id, link):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor_obj = conn.cursor()

    cursor_obj.execute('''UPDATE tasks SET link = ? WHERE id = ?''', [link, task_id])

    conn.commit()
    affected_rows = cursor_obj.rowcount
    conn.close()

    return affected_rows

def delete_task(task_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor_obj = conn.cursor()

    cursor_obj.execute('''DELETE FROM tasks WHERE id = ?''', [task_id])

    conn.commit()
    affected_rows = cursor_obj.rowcount
    conn.close()

    return affected_rows

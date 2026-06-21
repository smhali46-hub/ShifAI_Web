import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("users/shifai.db")
DB_PATH.parent.mkdir(exist_ok=True)


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        full_name TEXT,
        created_at TEXT NOT NULL,
        role TEXT DEFAULT 'user'
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS workouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        date TEXT NOT NULL,
        exercise TEXT NOT NULL,
        reps INTEGER NOT NULL,
        calories REAL NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        date TEXT NOT NULL,
        sender TEXT NOT NULL,
        message TEXT NOT NULL
    )
    """)


    cur.execute("""
    CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        reps_goal INTEGER DEFAULT 100,
        calories_goal REAL DEFAULT 50
    )
    """)

    try:
        cur.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")
    except sqlite3.OperationalError:
        pass

    try:
        cur.execute("ALTER TABLE users ADD COLUMN age INTEGER")
    except:
        pass

    try:
        cur.execute("ALTER TABLE users ADD COLUMN height REAL")
    except:
        pass

    try:
        cur.execute("ALTER TABLE users ADD COLUMN weight REAL")
    except:
        pass


    cur.execute("""
    INSERT OR IGNORE INTO users
    (username, password, full_name, created_at, role)
    VALUES (?, ?, ?, ?, ?)
    """, (
        "admin",
        "admin123",
        "Administrator",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "admin"
    ))

    conn.commit()
    conn.close()


def create_user(username, password, full_name=""):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
        INSERT INTO users
        (username, password, full_name, created_at, role)
        VALUES (?, ?, ?, ?, ?)
        """, (
            username,
            password,
            full_name,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user"
        ))

        conn.commit()
        return True, "Account created successfully."

    except sqlite3.IntegrityError:
        return False, "Username already exists."

    finally:
        conn.close()

def update_user_health(username, age, height, weight):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    UPDATE users
    SET age=?, height=?, weight=?
    WHERE username=?
    """, (age, height, weight, username))

    conn.commit()
    conn.close()


def get_user_health(username):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT age, height, weight
    FROM users
    WHERE username=?
    """, (username,))

    row = cur.fetchone()
    conn.close()

    return row

def validate_user(username, password):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT username FROM users
    WHERE username = ? AND password = ?
    """, (username, password))

    user = cur.fetchone()
    conn.close()

    return user is not None


def get_user_role(username):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT role FROM users WHERE username = ?", (username,))
    row = cur.fetchone()

    conn.close()
    return row[0] if row else "user"


def save_workout_db(username, exercise, reps, calories):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO workouts
    (username, date, exercise, reps, calories)
    VALUES (?, ?, ?, ?, ?)
    """, (
        username,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        exercise,
        reps,
        calories
    ))

    conn.commit()
    conn.close()


def get_user_profile(username):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT username, full_name, role, created_at
    FROM users
    WHERE username = ?
    """, (username,))

    row = cur.fetchone()
    conn.close()

    return row


def get_user_stats(username):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT 
        COUNT(*),
        COALESCE(SUM(reps), 0),
        COALESCE(SUM(calories), 0)
    FROM workouts
    WHERE username = ?
    """, (username,))

    row = cur.fetchone()
    conn.close()

    return row


def save_chat_message(username, sender, message):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO chat_history
    (username, date, sender, message)
    VALUES (?, ?, ?, ?)
    """, (
        username,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        sender,
        message
    ))

    conn.commit()
    conn.close()


def get_chat_history(username):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT sender, message
    FROM chat_history
    WHERE username = ?
    ORDER BY id ASC
    """, (username,))

    rows = cur.fetchall()
    conn.close()

    return rows

def create_goal_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        reps_goal INTEGER DEFAULT 100,
        calories_goal REAL DEFAULT 50
    )
    """)

    conn.commit()
    conn.close()


def save_user_goal(username, reps_goal, calories_goal):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO goals (username, reps_goal, calories_goal)
    VALUES (?, ?, ?)
    ON CONFLICT(username)
    DO UPDATE SET
        reps_goal = excluded.reps_goal,
        calories_goal = excluded.calories_goal
    """, (username, reps_goal, calories_goal))

    conn.commit()
    conn.close()


def get_user_goal(username):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT reps_goal, calories_goal
    FROM goals
    WHERE username = ?
    """, (username,))

    row = cur.fetchone()
    conn.close()

    if row:
        return row

    return 100, 50
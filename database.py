import sqlite3
import threading

DB_FILE = "secure_chat.db"
_lock = threading.Lock()

# ===== DATABASE INIT =====
def init_db():
    """Create tables if they don't exist."""
    conn = sqlite3.connect(DB_FILE)
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS public_keys (
        username TEXT PRIMARY KEY,
        public_key TEXT NOT NULL,
        FOREIGN KEY (username) REFERENCES users(username)
    )''')
    conn.commit()
    conn.close()

# ===== USER REGISTRATION =====
def register_user(username, password_hash):
    with _lock:
        try:
            conn = sqlite3.connect(DB_FILE)
            conn.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                         (username, password_hash))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            conn.close()
            return False

# ===== USER LOGIN =====
def login_user(username, password_hash):
    conn = sqlite3.connect(DB_FILE)
    row = conn.execute("SELECT password_hash FROM users WHERE username = ?",
                       (username,)).fetchone()
    conn.close()
    return row is not None and row[0] == password_hash

# ===== PUBLIC KEY STORAGE =====
def store_public_key(username, public_key):
    with _lock:
        conn = sqlite3.connect(DB_FILE)
        conn.execute("INSERT OR REPLACE INTO public_keys (username, public_key) VALUES (?, ?)",
                     (username, public_key))
        conn.commit()
        conn.close()

def get_public_key(username):
    conn = sqlite3.connect(DB_FILE)
    row = conn.execute("SELECT public_key FROM public_keys WHERE username = ?",
                       (username,)).fetchone()
    conn.close()
    return row[0] if row else None

# ===== SESSION-SCOPED CHAT HISTORY (in-memory only) =====
chat_history = {}

def save_message(sender, receiver, msg):
    key = tuple(sorted([sender, receiver]))
    chat_history.setdefault(key, []).append(msg)

def get_history(user1, user2):
    key = tuple(sorted([user1, user2]))
    return chat_history.get(key, [])

def clear_user_history(username):
    """Erase all in-memory chat history involving this user."""
    keys_to_delete = [k for k in chat_history if username in k]
    for k in keys_to_delete:
        del chat_history[k]

# Initialize on import
init_db()
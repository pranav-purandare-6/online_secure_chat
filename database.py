import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import IntegrityError

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Default to SQLite locally
default_db_url = f"sqlite:///{os.path.join(BASE_DIR, 'secure_chat.db')}"
# Use DATABASE_URL from environment (Render sets this for Postgres)
DATABASE_URL = os.getenv("DATABASE_URL", default_db_url)

# Fix for older SQLAlchemy versions requiring 'postgresql://' instead of 'postgres://'
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Connect args specific to SQLite to avoid thread issues
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

class PublicKey(Base):
    __tablename__ = 'public_keys'
    username = Column(String, primary_key=True, index=True)
    public_key = Column(String, nullable=False)

def init_db():
    Base.metadata.create_all(bind=engine)

# ===== USER REGISTRATION =====
def register_user(username, password_hash):
    db = SessionLocal()
    try:
        user = User(username=username, password_hash=password_hash)
        db.add(user)
        db.commit()
        return True
    except IntegrityError:
        db.rollback()
        return False
    finally:
        db.close()

# ===== USER LOGIN =====
def login_user(username, password_hash):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        return user is not None and user.password_hash == password_hash
    finally:
        db.close()

# ===== PUBLIC KEY STORAGE =====
def store_public_key(username, public_key):
    db = SessionLocal()
    try:
        key_entry = db.query(PublicKey).filter(PublicKey.username == username).first()
        if key_entry:
            key_entry.public_key = public_key
        else:
            key_entry = PublicKey(username=username, public_key=public_key)
            db.add(key_entry)
        db.commit()
    finally:
        db.close()

def get_public_key(username):
    db = SessionLocal()
    try:
        key_entry = db.query(PublicKey).filter(PublicKey.username == username).first()
        return key_entry.public_key if key_entry else None
    finally:
        db.close()

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
import gevent.monkey
gevent.monkey.patch_all()

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from crypto import hash_password
from database import (register_user, login_user, store_public_key,
                      get_public_key, save_message, get_history,
                      clear_user_history)
from datetime import datetime, timezone, timedelta

def get_ist_time():
    return datetime.now(timezone(timedelta(hours=5, minutes=30)))
import socket

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secure-chat-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent')

online_users = {}   # sid -> username
user_sids = {}      # username -> sid
active_users = {}   # username -> sid

@app.route('/')
def index():
    return render_template('index.html')

# ===== REGISTER =====
@socketio.on('register')
def handle_register(data):
    username = data.get('username', '').strip()
    password = data.get('password', '')
    if not username or not password:
        emit('auth', {'msg': '❌ Username and password required'})
        return
    if register_user(username, hash_password(password)):
        emit('auth', {'msg': '✅ Registered successfully'})
    else:
        emit('auth', {'msg': '❌ User already exists'})

# ===== LOGIN =====
@socketio.on('login')
def handle_login(data):
    username = data.get('username', '').strip()
    password = data.get('password', '')
    if not username or not password:
        emit('auth', {'msg': '❌ Username and password required'})
        return
    
    if login_user(username, hash_password(password)):
        # If user was already logged in (e.g. they refreshed the page),
        # safely overwrite their previous session ID instead of blocking them.
        if username in user_sids:
            old_sid = user_sids[username]
            if old_sid in online_users:
                del online_users[old_sid]
                
        online_users[request.sid] = username
        user_sids[username] = request.sid
        active_users[username] = request.sid
        emit('auth', {'msg': f'✅ Welcome {username}', 'username': username})
        broadcast_users()
        print(f"[{get_ist_time().strftime('%H:%M:%S')}] {username} logged in")
    else:
        emit('auth', {'msg': '❌ Invalid credentials'})

# ===== STORE PUBLIC KEY (ECDH) =====
@socketio.on('store_public_key')
def handle_store_public_key(data):
    username = online_users.get(request.sid)
    if not username:
        return
    public_key = data.get('publicKey', '')
    if public_key:
        store_public_key(username, public_key)
        print(f"[{get_ist_time().strftime('%H:%M:%S')}] Stored ECDH public key for {username}")

# ===== GET PUBLIC KEY =====
@socketio.on('get_public_key')
def handle_get_public_key(data):
    target = data.get('username', '')
    if target:
        pub_key = get_public_key(target)
        emit('public_key', {'username': target, 'publicKey': pub_key or ''})

# ===== GET ALL ONLINE USERS' PUBLIC KEYS =====
@socketio.on('get_online_keys')
def handle_get_online_keys():
    username = online_users.get(request.sid)
    if not username:
        return
    keys = {}
    for user in user_sids:
        if user != username:
            pk = get_public_key(user)
            if pk:
                keys[user] = pk
    emit('online_keys', keys)

# ===== BROADCAST USER LIST =====
def broadcast_users():
    users = list(user_sids.keys())
    socketio.emit('users', users)

# ===== LOAD HISTORY =====
@socketio.on('load_history')
def handle_load_history(data):
    username = online_users.get(request.sid)
    if not username:
        return
    other = data.get('with', '')
    if not other:
        return
    history = get_history(username, other)
    emit('chat_history', history)

# ===== SEND MESSAGE (E2EE relay — server never sees plaintext) =====
@socketio.on('send_message')
def handle_send_message(data):
    sender = online_users.get(request.sid)
    if not sender:
        emit('error', {'msg': 'Not authenticated'})
        return
    receiver = data.get('to', '')
    encrypted = data.get('encrypted', '')
    msg_hash = data.get('hash', '')
    if not receiver or not encrypted:
        emit('error', {'msg': 'Missing data'})
        return

    payload = {
        'from': sender,
        'to': receiver,
        'encrypted': encrypted,
        'hash': msg_hash,
        'time': get_ist_time().strftime("%H:%M")
    }

    save_message(sender, receiver, payload)

    receiver_sid = user_sids.get(receiver)
    if receiver_sid:
        emit('receive', payload, to=receiver_sid)
    emit('receive', payload, to=request.sid)

    print(f"[{get_ist_time().strftime('%H:%M:%S')}] {sender} -> {receiver}: [E2EE relay]")

# ===== SEND GROUP MESSAGE (Broadcast — E2EE with wrapped keys) =====
@socketio.on('send_group_message')
def handle_send_group_message(data):
    sender = online_users.get(request.sid)
    if not sender:
        emit('error', {'msg': 'Not authenticated'})
        return
    encrypted = data.get('encrypted', '')
    msg_hash = data.get('hash', '')
    wrapped_keys = data.get('wrappedKeys', {})
    if not encrypted:
        emit('error', {'msg': 'Empty message'})
        return

    payload = {
        'from': sender,
        'to': '__broadcast__',
        'encrypted': encrypted,
        'hash': msg_hash,
        'wrappedKeys': wrapped_keys,
        'time': get_ist_time().strftime("%H:%M"),
        'group': True
    }

    socketio.emit('group_receive', payload)
    print(f"[{get_ist_time().strftime('%H:%M:%S')}] {sender} -> [BROADCAST]: [E2EE relay]")

# ===== DISCONNECT =====
@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    if sid in online_users:
        username = online_users[sid]
        online_users.pop(sid, None)
        user_sids.pop(username, None)
        active_users.pop(username, None)
        clear_user_history(username)
        print(f"[{get_ist_time().strftime('%H:%M:%S')}] {username} disconnected (history cleared)")
        broadcast_users()

# ===== TYPING INDICATOR =====
@socketio.on('typing')
def handle_typing(data):
    sender = online_users.get(request.sid)
    if not sender:
        return
    receiver = data.get('to')
    if receiver and receiver in user_sids:
        emit('typing', {'from': sender}, to=user_sids[receiver])

# ===== GET LAN IP =====
def get_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

if __name__ == '__main__':
    lan_ip = get_lan_ip()
    print("=" * 50)
    print("  SECURE CHAT SERVER (E2EE)")
    print("=" * 50)
    print(f"  Local:   http://127.0.0.1:5000")
    print(f"  Network: http://{lan_ip}:5000")
    print("=" * 50)
    socketio.run(app, host='0.0.0.0', port=5000)
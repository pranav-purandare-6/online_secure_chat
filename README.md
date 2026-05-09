# 🔐 Secure Chat — End-to-End Encrypted Messaging over LAN

A real-time encrypted chat application built for the **Cryptography and Security Systems** course. It demonstrates AES-128 encryption, SHA-256 integrity verification, and secure key management — all running over a local Wi-Fi network between multiple PCs.

---

## 📋 Table of Contents

- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Project Architecture](#-project-architecture)
- [Cryptographic Concepts Demonstrated](#-cryptographic-concepts-demonstrated)
- [How to Run](#-how-to-run)
- [Issues Found & Fixes Applied](#-issues-found--fixes-applied)
- [File Structure](#-file-structure)
- [Screenshots](#-screenshots)

---

## ✨ Features

- **Real-time messaging** using WebSockets (Socket.IO)
- **AES-128 CBC encryption** — every message is encrypted before transmission
- **SHA-256 integrity verification** — each message is hashed to detect tampering
- **Server-managed per-pair AES keys** — unique encryption key for every user pair
- **Multi-PC support** — works across devices connected to the same Wi-Fi
- **User registration & login** with SHA-256 password hashing
- **Live online user list** with real-time updates
- **Unread message badges** for conversations you haven't opened
- **Typing indicators** — see when the other person is typing
- **Chat history** — messages persist in-memory during the server session
- **Encryption Log panel** — view the raw AES ciphertext for every message

---

## 🛠 Technology Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3, Flask, Flask-SocketIO |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Encryption (Server)** | PyCryptodome (AES-CBC, SHA-256) |
| **Encryption (Client)** | CryptoJS 4.2.0 (AES-CBC decryption, SHA-256) |
| **Real-time Communication** | Socket.IO (WebSocket with polling fallback) |
| **Data Storage** | JSON file (users), In-memory dict (messages) |

---

## 🏗 Project Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        SERVER (Flask + SocketIO)                    │
│                                                                     │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────────────┐    │
│  │  database.py  │   │   crypto.py  │   │     server.py        │    │
│  │              │   │              │   │                      │    │
│  │ • User       │   │ • AES-128    │   │ • Socket.IO events   │    │
│  │   Register   │   │   Encrypt    │   │ • Key management     │    │
│  │ • User       │   │ • AES-128    │   │ • Message routing     │    │
│  │   Login      │   │   Decrypt    │   │ • User sessions      │    │
│  │ • Chat       │   │ • SHA-256    │   │ • Chat history       │    │
│  │   History    │   │   Hashing    │   │ • Typing relay       │    │
│  └──────────────┘   │ • Key Gen    │   └──────────────────────┘    │
│                      └──────────────┘                               │
└──────────────────────────┬──────────────────────────────────────────┘
                           │ WebSocket (Socket.IO)
              ┌────────────┴────────────┐
              │                         │
    ┌─────────▼─────────┐    ┌─────────▼─────────┐
    │   PC 1 (Browser)   │    │   PC 2 (Browser)   │
    │                    │    │                    │
    │  • CryptoJS        │    │  • CryptoJS        │
    │    AES Decrypt      │    │    AES Decrypt      │
    │  • SHA-256 Verify   │    │  • SHA-256 Verify   │
    │  • Chat UI          │    │  • Chat UI          │
    └────────────────────┘    └────────────────────┘
```

### Message Flow

```
User A types "Hello"
       │
       ▼
[Client A] ──emit('send_message', {to: B, message: "Hello"})──▶ [SERVER]
                                                                    │
                                                          1. Get/Create AES key
                                                             for pair (A, B)
                                                          2. Encrypt "Hello" with
                                                             AES-128-CBC
                                                          3. Compute SHA-256 hash
                                                             of "Hello"
                                                          4. Build payload:
                                                             { encrypted, enc_key,
                                                               hash, from, to, time }
                                                                    │
       ┌────────────────────────────────────────────────────────────┘
       │                                    │
       ▼                                    ▼
[Client A receives payload]          [Client B receives payload]
       │                                    │
  1. Parse enc_key (hex)               1. Parse enc_key (hex)
  2. Decrypt ciphertext                2. Decrypt ciphertext
     with CryptoJS AES-CBC               with CryptoJS AES-CBC
  3. Compute SHA-256 of plaintext      3. Compute SHA-256 of plaintext
  4. Compare with hash field           4. Compare with hash field
     → ✔ Verified / ⚠ Tampered           → ✔ Verified / ⚠ Tampered
  5. Display decrypted message         5. Display decrypted message
```

---

## 🔒 Cryptographic Concepts Demonstrated

### 1. AES-128 CBC Encryption
- **Algorithm:** Advanced Encryption Standard (AES) with 128-bit keys
- **Mode:** Cipher Block Chaining (CBC) — each block depends on the previous one
- **Padding:** PKCS7 — pads plaintext to a multiple of 16 bytes
- **IV:** A random 16-byte Initialization Vector is generated for each message, prepended to the ciphertext
- **Implementation:** PyCryptodome on the server, CryptoJS on the client for decryption

### 2. SHA-256 Integrity Hashing
- Every plaintext message is hashed with SHA-256 before encryption
- The hash is sent alongside the ciphertext
- The receiver decrypts the message, re-computes the SHA-256 hash, and compares it
- If the hashes match → **✔ Verified** (message was not tampered with)
- If they don't match → **⚠ Tampered** (message integrity compromised)

### 3. Per-Pair Key Generation
- When two users communicate for the first time, the server generates a random 16-byte AES key using `Crypto.Random.get_random_bytes(16)`
- This key is unique to each user pair (e.g., Alice↔Bob has a different key from Alice↔Charlie)
- The key is stored in server memory and sent to clients for client-side decryption

### 4. Password Hashing
- User passwords are hashed with SHA-256 before storage
- Only the hash is stored in `users.json`, never the plaintext password
- Login compares SHA-256(input) with the stored hash

---

## 🚀 How to Run

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Two devices on the same Wi-Fi network (or two browser tabs for local testing)

### Step 1: Install Dependencies

```bash
pip install flask flask-socketio pycryptodome
```

### Step 2: Start the Server

```bash
cd secure-chat
python server.py
```

You will see:
```
==================================================
  SECURE CHAT SERVER
==================================================
  Local:   http://127.0.0.1:5000
  Network: http://192.168.x.x:5000
  (Share the Network URL with other PCs on same Wi-Fi)
==================================================
```

### Step 3: Connect from Devices

| Device | URL |
|--------|-----|
| **Host PC** (where server runs) | `http://127.0.0.1:5000` |
| **Other PC** (same Wi-Fi) | `http://192.168.x.x:5000` (use the Network URL from terminal) |

### Step 4: Register & Chat
1. Register a new account (or use existing accounts)
2. Log in on both devices with different accounts
3. Click on a user in the "Online Users" list to open a chat
4. Send messages — they appear encrypted in the Encryption Log and decrypted in the chat

### Firewall Note
If the other PC cannot connect, allow port 5000 through Windows Firewall:
```
Control Panel → Windows Defender Firewall → Allow an app → Add port 5000 (TCP)
```

---

## 🐛 Issues Found & Fixes Applied

### Issue 1: Diffie-Hellman Key Exchange Never Triggered (CRITICAL)

**What was happening:**
The original code had a Diffie-Hellman (DH) key exchange system with functions `generate_dh()` and `generate_shared()` in `crypto.py`, and a `send_public` Socket.IO event handler in `server.py`. However, the client-side JavaScript **never emitted the `send_public` event**. This meant:
- The `shared_keys` dictionary on the server was always **empty**
- Every call to `send_message` hit the check `if not aes_key:` and returned `"Key not established"`
- **No messages could ever be sent**

**Additionally**, even if the event were emitted, the DH implementation was **one-sided** — it only computed the shared secret using the *receiver's* private key and the *sender's* public key. The reverse direction was never computed, so only one user in a pair could decrypt messages.

**The DH parameters were also insecure:**
```python
P = 23   # Only 23 possible shared secrets (1-22)
G = 5    # Trivially small generator
```

**How it was fixed:**
Replaced the broken DH system with **server-managed per-pair AES keys**. When two users first communicate, the server generates a random 16-byte AES-128 key using `Crypto.Random.get_random_bytes(16)` and stores it for that user pair. This key is included in every message payload so both clients can decrypt.

**Files changed:** `crypto.py`, `server.py`

---

### Issue 2: Message Payload Missing Required Fields (CRITICAL)

**What was happening:**
The server's `send_message` handler encrypted the message but sent an incomplete payload:
```python
# OLD — missing enc_key and hash
payload = {
    'from': sender,
    'to': receiver,
    'encrypted': encrypted,
    'time': datetime.now().strftime("%H:%M")
}
```

The client-side `handleReceive()` function expected `enc_key` (the AES key in hex for decryption) and `hash` (the SHA-256 hash for integrity verification):
```javascript
// Client checked for these fields and bailed if missing
const keyHex = data.enc_key;  // ← was undefined
if (!data.encrypted || !keyHex) return;  // ← always returned
```

This meant even if encryption succeeded on the server, the **client could never decrypt** because it didn't have the key.

**How it was fixed:**
The server now includes all required fields in every message payload:
```python
# NEW — complete payload
payload = {
    'from': sender,
    'to': receiver,
    'encrypted': encrypted,
    'enc_key': aes_key.hex(),           # AES key for client-side decryption
    'hash': hash_message(msg),           # SHA-256 hash for integrity check
    'time': datetime.now().strftime("%H:%M")
}
```

**Files changed:** `server.py`

---

### Issue 3: Client `send_message` Missing `from` Field (CRITICAL)

**What was happening:**
The client JavaScript `send()` function emitted:
```javascript
// OLD — no 'from' field
socket.emit('send_message', { to: currentUser, message: msg });
```

But the server read `data['from']` to identify the sender:
```python
sender = data['from']  # ← KeyError! Field doesn't exist
```

This caused a Python `KeyError` exception on the server for every message attempt.

**How it was fixed:**
1. Added `from: myUsername` to the client's emit call
2. More importantly, the server now reads the sender from the authenticated session instead of trusting client data (more secure):
```python
# NEW — server identifies sender from session, not client data
sender = online_users.get(request.sid)
```

**Files changed:** `server.py`, `templates/index.html`

---

### Issue 4: `window.crypto.subtle` Undefined on HTTP (CRITICAL)

**What was happening:**
The client-side decryption used the **Web Crypto API** (`window.crypto.subtle`) for AES decryption and SHA-256 hashing:
```javascript
// OLD — only works on HTTPS or localhost
const cryptoKey = await window.crypto.subtle.importKey(...);
const dec = await window.crypto.subtle.decrypt(...);
const hash = await crypto.subtle.digest("SHA-256", buf);
```

The Web Crypto API is **only available in secure contexts** (HTTPS or `localhost`). When the second PC connected via plain HTTP (e.g., `http://192.168.29.37:5000`), `window.crypto.subtle` was `undefined`, causing:
```
[DECRYPT] Failed: Cannot read properties of undefined (reading 'importKey')
```

This meant:
- **Messages sent FROM the other PC** were encrypted and delivered successfully (server-side encryption works fine)
- **Messages could not be DISPLAYED on the other PC** because client-side decryption failed
- The host PC (localhost) worked normally because `crypto.subtle` is available on localhost

**How it was fixed:**
Replaced `window.crypto.subtle` with **CryptoJS** (a pure JavaScript crypto library loaded from CDN) which works on any HTTP context:
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.2.0/crypto-js.min.js"></script>
```
```javascript
// NEW — works on HTTP and HTTPS
function sha256(message) {
    return CryptoJS.SHA256(message).toString(CryptoJS.enc.Hex);
}

function safeDecrypt(encryptedBase64, keyHex) {
    var rawWords   = CryptoJS.enc.Base64.parse(encryptedBase64);
    var iv         = CryptoJS.lib.WordArray.create(rawWords.words.slice(0, 4), 16);
    var ciphertext = CryptoJS.lib.WordArray.create(rawWords.words.slice(4), rawWords.sigBytes - 16);
    var key        = CryptoJS.enc.Hex.parse(keyHex);

    var decrypted  = CryptoJS.AES.decrypt(
        { ciphertext: ciphertext }, key,
        { iv: iv, mode: CryptoJS.mode.CBC, padding: CryptoJS.pad.Pkcs7 }
    );
    return decrypted.toString(CryptoJS.enc.Utf8);
}
```

**Files changed:** `templates/index.html`

---

### Issue 5: `load_history` Could Crash with KeyError (MODERATE)

**What was happening:**
```python
# OLD — direct dict access, crashes if sid not found
user = online_users[request.sid]
```
If a user disconnected and a race condition occurred, this would crash the server.

**How it was fixed:**
```python
# NEW — safe access with early return
username = online_users.get(request.sid)
if not username:
    return
```

**Files changed:** `server.py`

---

### Issue 6: `users.json` Could Corrupt on Concurrent Access (MODERATE)

**What was happening:**
Two users registering at the exact same time could cause both threads to read the file, each add their user, and then both write — with the second write overwriting the first user.

**How it was fixed:**
Added a `threading.Lock` around all file read/write operations:
```python
_lock = threading.Lock()

def load_users():
    with _lock:
        # ... read file

def save_users(users):
    with _lock:
        # ... write file
```

**Files changed:** `database.py`

---

### Issue 7: No LAN IP Displayed (MINOR)

**What was happening:**
The server started with Flask's default output, and users had no way to know what IP address to share with the other PC.

**How it was fixed:**
Added `get_lan_ip()` function and a startup banner:
```
==================================================
  SECURE CHAT SERVER
==================================================
  Local:   http://127.0.0.1:5000
  Network: http://192.168.29.37:5000
  (Share the Network URL with other PCs on same Wi-Fi)
==================================================
```

**Files changed:** `server.py`

---

### Issue 8: Missing Input Validation & UX (MINOR)

**What was happening:**
- Empty username/password could be submitted
- No Enter key support on login/register forms
- No XSS protection on usernames displayed in HTML
- No connection status feedback

**How it was fixed:**
- Added empty-field validation on both client and server
- Added Enter-key handlers on password fields
- Added `escapeHtml()` on all user-generated strings rendered in HTML
- Added Socket.IO `connect`/`disconnect` event handlers with status messages

**Files changed:** `server.py`, `templates/index.html`

---

## 📁 File Structure

```
secure-chat/
├── server.py          # Flask + SocketIO server, message routing, key management
├── crypto.py          # AES-128 encrypt/decrypt, SHA-256 hashing, key generation
├── database.py        # User registration/login (JSON), chat history (in-memory)
├── users.json         # Stored user credentials (SHA-256 hashed passwords)
├── templates/
│   └── index.html     # Full chat UI + CryptoJS client-side decryption
├── static/
│   └── style.css      # Dark theme styling with animations
└── README.md          # This file
```

### File Details

| File | Lines | Purpose |
|------|-------|---------|
| `server.py` | ~140 | WebSocket event handlers for login, register, send/receive messages, typing indicators. Manages per-pair AES keys and broadcasts user lists. |
| `crypto.py` | ~42 | `encrypt_message()` and `decrypt_message()` using AES-128-CBC with random IV. `hash_password()` and `hash_message()` using SHA-256. `generate_pair_key()` for random key generation. |
| `database.py` | ~45 | Thread-safe JSON file I/O for user accounts. In-memory dictionary for chat history during server session. |
| `index.html` | ~330 | Three-panel layout (sidebar, chat, encryption log). CryptoJS-based AES decryption and SHA-256 verification. Socket.IO client for real-time events. |
| `style.css` | ~172 | Dark theme (`#0f172a` background), message bubbles (green sent, gray received), animations (fadeIn, slideIn, pulse for badges). |

---

## 👥 Existing Test Accounts

| Username | Password |
|----------|----------|
| Pranav   | 1234     |
| Rahul    | abcd     |
| Swarali  | *(set during registration)* |
| Abhinav  | *(set during registration)* |
| Swarangi | *(set during registration)* |

---

## 📝 Summary of All Changes

| # | Severity | Issue | Root Cause | Fix |
|---|----------|-------|-----------|-----|
| 1 | 🔴 Critical | Messages never sent | DH key exchange never triggered → `shared_keys` always empty | Replaced DH with server-managed per-pair AES keys |
| 2 | 🔴 Critical | Client can't decrypt | Payload missing `enc_key` and `hash` fields | Server now includes both in every payload |
| 3 | 🔴 Critical | Server crashes on send | Client didn't send `from` field → `KeyError` | Server reads sender from session; client also sends `from` |
| 4 | 🔴 Critical | Other PC can't decrypt | `crypto.subtle` unavailable on plain HTTP | Replaced with CryptoJS library (works on HTTP) |
| 5 | 🟡 Moderate | Server crash on disconnect | Direct dict access without `.get()` | Safe access with early return |
| 6 | 🟡 Moderate | User data corruption | No file locking on concurrent writes | Added `threading.Lock` |
| 7 | 🟢 Minor | Can't find server IP | No LAN IP displayed on startup | Added `get_lan_ip()` + startup banner |
| 8 | 🟢 Minor | Poor UX | No validation, no Enter key, no XSS protection | Added all missing UX features |

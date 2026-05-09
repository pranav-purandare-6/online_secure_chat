# 🔐 Secure Chat — True End-to-End Encrypted Messaging (E2EE)

A production-grade, real-time encrypted chat application built for the **Cryptography and Security Systems** course. It features **True End-to-End Encryption (E2EE)** using Elliptic Curve Diffie-Hellman (ECDH) key exchange and AES-128-CBC encryption. The server acts purely as a zero-knowledge relay and never has access to plaintext messages or encryption keys.

---

## 📋 Table of Contents

- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Project Architecture (E2EE)](#-project-architecture-e2ee)
- [Cryptographic Concepts Demonstrated](#-cryptographic-concepts-demonstrated)
- [How to Run (Local & Deployment)](#-how-to-run-local--deployment)
- [File Structure](#-file-structure)

---

## ✨ Features

- **True E2EE (End-to-End Encryption)** — encryption and decryption happen strictly in the browser.
- **Zero-Knowledge Server** — the backend server never sees your messages or encryption keys.
- **ECDH Key Exchange** — automatic secure generation of shared secrets between users.
- **Broadcast E2EE (Group Chat)** — secure group messaging using ephemeral wrapped AES keys.
- **SQLite Database** — persistent storage for users, passwords (hashed), and public keys.
- **Ephemeral Chat History** — messages exist only in server memory and are wiped when you disconnect.
- **SHA-256 Integrity Verification** — detects message tampering.
- **Production Ready** — uses `eventlet` async workers, ready for deployment on platforms like Render.
- **Encryption Log Panel** — view the raw encrypted payloads flying across the network.

---

## 🛠 Technology Stack

| Layer | Technology |
|-------|-----------|
| **Backend Framework** | Python 3, Flask, Flask-SocketIO |
| **Backend Async/Server** | `eventlet`, `gunicorn` |
| **Database** | SQLite3 (`sqlite3` module) |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Encryption (Client)** | `elliptic.js` (ECDH), CryptoJS 4.2.0 (AES-128-CBC, SHA-256) |
| **Authentication (Server)** | PyCryptodome (SHA-256 for passwords) |

---

## 🏗 Project Architecture (E2EE)

The application follows a strictly client-side cryptographic architecture. The server is completely blind to the contents of the conversations.

```
┌─────────────────────────────────────────────────────────────────────┐
│                   ZERO-KNOWLEDGE SERVER (Flask)                     │
│                                                                     │
│  • Stores User Passwords (Hashed)                                   │
│  • Stores ECDH Public Keys                                          │
│  • Relays Encrypted Payloads (Ciphertext only)                      │
│  • Maintains Session-Scoped Ephemeral Chat History                  │
│                                                                     │
└──────────────────────────┬──────────────────────────────────────────┘
                           │ WebSocket (Socket.IO)
              ┌────────────┴────────────┐
              │                         │
    ┌─────────▼─────────┐    ┌─────────▼─────────┐
    │   PC 1 (Alice)    │    │    PC 2 (Bob)     │
    │                   │    │                   │
    │ 1. Gen ECDH Keys  │    │ 1. Gen ECDH Keys  │
    │ 2. Derive Secret  │    │ 2. Derive Secret  │
    │ 3. AES Encrypt    │    │ 3. AES Decrypt    │
    │ 4. Send Ciphertext│    │ 4. Read Message   │
    └───────────────────┘    └───────────────────┘
```

### Direct Message Flow (ECDH + AES)
1. **Login:** Alice logs in. Her browser generates an ECDH keypair and sends the Public Key to the server.
2. **Key Exchange:** When Alice wants to talk to Bob, her browser requests Bob's Public Key from the server.
3. **Derive Secret:** Alice's browser combines her Private Key with Bob's Public Key to calculate a Shared Secret. The shared secret is hashed to generate an AES-128 key.
4. **Encrypt:** The message is encrypted locally using AES-128-CBC.
5. **Transmit:** Only the **ciphertext** and an **integrity hash** are sent to the server.
6. **Decrypt:** Bob receives the ciphertext, derives the exact same shared AES key using his Private Key and Alice's Public Key, and decrypts the message.

### Broadcast Message Flow (Wrapped Keys)
To send a message to the "Broadcast Channel" (all online users):
1. The sender generates a random **ephemeral AES key**.
2. The message is encrypted with this ephemeral key.
3. The sender gets the public keys of *every online user*.
4. The sender uses ECDH to encrypt (wrap) the ephemeral key individually for every recipient.
5. The payload contains the encrypted message and a dictionary of wrapped keys. Each user unwraps the key meant for them and decrypts the message.

---

## 🔒 Cryptographic Concepts Demonstrated

### 1. Elliptic Curve Diffie-Hellman (ECDH)
- **Curve:** P-256
- **Implementation:** `elliptic.js` in the browser
- **Purpose:** Allows two users to establish a shared secret over an insecure channel without ever transmitting the secret itself.

### 2. Client-Side AES-128-CBC Encryption
- **Mode:** Cipher Block Chaining (CBC) with PKCS7 Padding
- **Initialization Vector (IV):** A random 16-byte IV is generated for *every single message*, ensuring the same text encrypts to different ciphertexts every time.
- **Execution:** Happens entirely in the browser using `CryptoJS`. The server *never* sees the AES keys.

### 3. Key Wrapping (Group Chat Security)
- Instead of sharing a single group key (which compromises forward secrecy), broadcast messages use an ephemeral key that is wrapped (encrypted) individually for every recipient using their unique ECDH shared secret. This is standard in modern E2EE apps (like Signal/WhatsApp).

### 4. SHA-256 Integrity & Password Hashing
- Every encrypted payload includes a SHA-256 hash of the plaintext. The receiver decrypts the text, hashes it, and verifies it matches to prevent MITM tampering.
- Server-side, user passwords are mathematically one-way hashed with SHA-256 before being stored in SQLite.

---

## 🚀 How to Run (Local & Deployment)

### Running Locally

**Prerequisites:** Python 3.8+

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the server:
   ```bash
   python server.py
   ```
3. Open `http://127.0.0.1:5000` in your browser.
4. To chat between multiple PCs, look at the terminal output for the `Network` URL (e.g., `http://192.168.x.x:5000`) and open that on a second PC connected to the same Wi-Fi.

### Deploying to Render.com

This project is fully configured for production deployment on Render.

1. Push this folder to a GitHub repository.
2. Go to [Render.com](https://render.com) and create a **New Web Service**.
3. Connect your GitHub repository.
4. Set the configurations:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn --worker-class eventlet -w 1 server:app`
5. Go to Advanced Settings -> Environment Variables and add:
   - Key: `PYTHONUNBUFFERED` | Value: `1`
6. Click **Create Web Service**. 

---

## 📁 File Structure

```
secure-chat/
├── server.py          # Pure relay server (zero-knowledge)
├── crypto.py          # Server-side hashing (passwords only)
├── database.py        # SQLite database logic and in-memory history
├── secure_chat.db     # Auto-generated SQLite database (Users & Public Keys)
├── Procfile           # Render deployment configuration
├── requirements.txt   # Python dependencies (Flask, eventlet, gunicorn)
├── templates/
│   └── index.html     # Client UI and full ECDH/AES client-side cryptography
├── static/
│   └── style.css      # Dark theme UI styling
└── README.md          # This file
```

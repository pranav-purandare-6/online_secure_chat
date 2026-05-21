# 🔐 Secure Chat — True End-to-End Encrypted Messaging (E2EE)

[![Render Deployment](https://img.shields.io/badge/Deploy-Render.com-46cbf5?style=for-the-badge&logo=render&logoColor=white)](https://render.com)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Socket.IO](https://img.shields.io/badge/Socket.io-010101?style=for-the-badge&logo=socket.io&logoColor=white)](https://socket.io/)
[![Cryptography](https://img.shields.io/badge/Cryptography-ECDH%20%26%20AES-22c55e?style=for-the-badge)](https://developer.mozilla.org/en-US/docs/Web/API/Web_Crypto_API)

A production-grade, highly secure, real-time web chat application featuring **True End-to-End Encryption (E2EE)**. Designed with a gorgeous, responsive, glassmorphic dark interface, it demonstrates state-of-the-art cryptographic concepts like **Elliptic Curve Diffie-Hellman (ECDH)** key exchanges, **AES-128-CBC** message encryption, and **ephemeral key wrapping** for broadcast groups. The backend operates on a strict **zero-knowledge principle**—serving only as an encrypted relay and public key repository. It never has access to plaintext conversations, images, or shared keys.

---

## 📋 Table of Contents

- [✨ Premium Features](#-premium-features)
- [🛠️ Technology Stack](#%EF%B8%8F-technology-stack)
- [🏗️ Architectural Flow (E2EE & Zero-Knowledge)](#%EF%B8%8F-architectural-flow-e2ee--zero-knowledge)
- [🔒 Cryptographic Implementation Details](#-cryptographic-implementation-details)
- [🛠️ Recent Architecture & Stability Improvements](#%EF%B8%8F-recent-architecture--stability-improvements)
- [🚀 Local Setup & Deployment Guide](#-local-setup--deployment-guide)
- [☁️ Deploying on Render.com (Global Chat Guide)](#%EF%B8%8F-deploying-on-rendercom-global-chat-guide)
- [📁 File Structure](#-file-structure)

---

## ✨ Premium Features

### 🔐 Cryptographic Integrity
*   **True E2EE Direct Messaging:** Key exchange, shared secret generation, and AES encryption/decryption happen exclusively in the browser. 
*   **Zero-Knowledge Backend:** The server only relays binary/base64 ciphertexts and password hashes.
*   **Secure Broadcast Channel:** Message keys are dynamically wrapped for all active users using individual ECDH secrets.
*   **SHA-256 Tamper Detection:** Automatic integrity verification showing `✔ Verified` or `⚠ Tampered` based on cryptographic hash validation.

### 🎨 Stunning Modern UI & UX
*   **Dynamic Responsive Layout:** Smooth slide-out mobile mechanics using CSS transforms and stateful hardware back-button history navigation.
*   **Visual Micro-Animations:** Mouse-move radial card glows, active indicator transitions, status shakes, badge expansions, and button click ripple effects.
*   **Real-time Typing Indicators:** Smooth, bounce-animated typing feedback for direct chats.
*   **In-App Cryptographic Log Panel:** A real-time transparent log displaying outgoing and incoming encrypted payloads, offering full transparency.

### 🖼️ Enhanced Media & Input Systems
*   **Hardware Image Compression:** Files uploaded via chat are compressed and scaled client-side using an HTML5 Canvas downsampler before E2EE encryption, preventing payload congestion and maximizing speed.
*   **Full Emoji Integration:** Fully integrated native emoji picker with click-away dismissal.
*   **Dynamic Reply Quotes:** Message threading allows quoting and replying to messages, with active author indicator coloring.

---

## 🛠️ Technology Stack

| Component | Stack Selection | Purpose |
|---|---|---|
| **Backend Framework** | Python 3, Flask, Flask-SocketIO | Robust routing, request lifecycle, and WebSocket events |
| **Backend Workers** | `gevent`, `gevent-websocket` | High-concurrency asynchronous event loop handling |
| **Production Server** | `gunicorn` | Production-grade WSGI/WebSocket container |
| **Database ORM** | SQLAlchemy (SQLite / PostgreSQL) | Thread-safe active records for credentials and keys |
| **Client-Side Crypto** | `elliptic.js` (P-256), CryptoJS | Fast Elliptic-Curve math and cryptographic ciphers |
| **Server-Side Crypto** | PyCryptodome (SHA-256) | Zero-knowledge password verification |
| **Interface Styling** | CSS3 (Variable tokens, HSL palettes) | Immersive glassmorphic dark theme and responsive panels |

---

## 🏗️ Architectural Flow (E2EE & Zero-Knowledge)

The system enforces a client-side sandbox model where cryptographic boundaries are never crossed by the server.

```
                  ┌─────────────────────────────────────────────────────────────┐
                  │                 ZERO-KNOWLEDGE SERVER (Flask)               │
                  │                                                             │
                  │  • Handles User Authentications (SHA-256 password hash DB)  │
                  │  • Stores & Relays ECDH Public Keys                         │
                  │  • Relays Encrypted Payloads (Ciphertext only)              │
                  │  • Manages Ephemeral, Session-Scoped Chat History           │
                  └──────────────────────────────┬──────────────────────────────┘
                                                 │
                                                 │ Secure WebSockets (Socket.IO)
                                                 │
                             ┌───────────────────┴───────────────────┐
                             │                                       │
                  ┌──────────▼──────────┐                 ┌──────────▼──────────┐
                  │     Client Alice    │                 │     Client Bob      │
                  │                     │                 │                     │
                  │  1. Generates ECDH  │                 │  1. Generates ECDH  │
                  │     Keypair (P-256) │                 │     Keypair (P-256) │
                  │  2. Requests Bob's  │                 │  2. Requests Alice's│
                  │     Public Key      │                 │     Public Key      │
                  │  3. Derives AES Key │                 │  3. Derives AES Key │
                  │  4. Encrypts Msg    │                 │  4. Decrypts Msg    │
                  │  5. Transmits raw   │                 │  5. Performs        │
                  │     Ciphertext      │                 │     Integrity Check │
                  └─────────────────────┘                 └─────────────────────┘
```

---

## 🔒 Cryptographic Implementation Details

### 1. Key Derivation via ECDH (P-256)
Upon secure login, the client browser creates an ephemeral Elliptic Curve keypair based on the **NIST P-256 (secp256r1)** curve using `elliptic.js`:
*   The **Private Key** is kept strictly inside client-side JS memory.
*   The **Public Key** (in Hex format) is transmitted to the server's database via the `store_public_key` socket event.
*   When Alice selects Bob, their browsers query each other's public keys. They execute:
    $$\text{Shared Secret} = \text{Alice's Private Key} \times \text{Bob's Public Key}$$
*   The shared secret is padded, passed through a **SHA-256** hash, and truncated to the first 32 characters (16 bytes / 128 bits) to form a high-entropy **AES-128** encryption key.

### 2. Client-Side AES-128-CBC
Every message is encrypted locally using the Derived AES Key in **Cipher Block Chaining (CBC)** mode with standard **PKCS7** padding:
*   A cryptographically secure random **16-byte Initialization Vector (IV)** is generated for *every single message*.
*   The IV is prepended to the encrypted ciphertext block and encoded as a base64 string before transmission. This ensures that sending the same text multiple times results in completely different ciphertexts.

### 3. Broadcast Ephemeral Key Wrapping
To send E2EE messages to a broadcast channel containing variable numbers of online users, the sender uses **Key Wrapping**:
1. The sender generates a random **ephemeral AES-128 key** ($K_{eph}$) specifically for that one message.
2. The message is encrypted using $K_{eph}$.
3. For every online participant $U_i$ (including the sender themselves), the sender derives their shared ECDH key ($K_{shared\_i}$) and encrypts the ephemeral key:
    $$\text{Wrapped Key}_i = \text{Encrypt}_{AES}(K_{eph}, K_{shared\_i})$$
4. The final payload containing the ciphertext, the message hash, and the map of user-wrapped keys `{"Bob": wrappedKeyB, "Charlie": wrappedKeyC}` is emitted.
5. Receivers decrypt only the specific wrapped key mapped to their username, retrieve $K_{eph}$, and decrypt the message payload.

---

## 🛠️ Recent Architecture & Stability Improvements

To elevate the application to production grade, several critical bugs, race conditions, and vulnerabilities were resolved in the codebase:

1.  **Resolved Public Key Race Condition (Server & Client):** Previously, the server broadcasted a user's online status as soon as their socket authenticated, *before* writing their new ECDH public key to the database. This caused immediate key derivation errors for other clients. The server now defers `broadcast_users()` until the public key has been successfully written to the database.
2.  **3-Pass Broadcast Decryption Buffer (Client-Side):** Broadcast messages received from newly joined users occasionally failed to decrypt because their public keys were still transitively fetching. The client now uses a robust `handleGroupReceive` function with a **3-pass retry queue** spaced at `500ms` intervals, letting asynchronous key exchanges settle cleanly before giving up.
3.  **Strict XSS Protection & Schema Verification for Base64 Images:** Message attachments are now locked down by checking that incoming photo data is a valid base64 payload (`startsWith('data:image/')`) and enforcing `escapeHtml()` sanitation on it before inserting it into the DOM, fully immunizing the application against cross-site scripting (XSS) vectors.
4.  **Auto-Tearing Connection Recovery:** Socket connections lost due to transient network drops could lead to stale public keys in active client states. The client now detects socket disconnects immediately, prints a clear warning notification, and triggers an automated `location.reload()` after 2 seconds to cleanly cycle keypairs and refresh the active environment.
5.  **Refined Mobile UI Panel Shifting:** The responsive layout was optimized on mobile breakpoints by replacing sidebar block rendering with modern flex-flows, tuning layout structures, and styling card sizes to ensure a native app feel on modern mobile screens.
6.  **Emoji Picker Keyboard & Layout Stability (Mobile UI):** Selecting emojis on mobile devices previously triggered focus losses (blurs) and viewport shifts as the virtual keyboard repeatedly closed and reopened. The client now intercepts `pointerdown` events on the picker to call `event.preventDefault()` (bypassing the search bar), keeping the input field and keyboard active. It also restricts custom `focus()` calls on mobile to already-active fields, preventing layout flickering.

---

## 🚀 Local Setup & Deployment Guide

### Running Locally

Ensure you have **Python 3.8+** installed.

1.  **Clone or navigate** into the project workspace directory.
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Launch the application:**
    ```bash
    python server.py
    ```
4.  **Access the client:**
    *   **Local Access:** Open `http://127.0.0.1:5000` on your machine.
    *   **Local Network Access:** Check the startup banner in the console for your LAN IP (e.g., `http://192.168.1.15:5000`). Other devices (laptops, phones) connected to the same Wi-Fi network can visit this URL to test multi-device chat.

---

## ☁️ Deploying on Render.com (Global Chat Guide)

This application is fully compatible with [Render.com](https://render.com) and is optimized to run smoothly on their free hosting platform.

### Step-by-Step Render Deployment

1.  Push your code to a personal repository on **GitHub** or **GitLab**.
2.  Log in to the [Render Dashboard](https://dashboard.render.com/) and click **New > Web Service**.
3.  Connect your repository.
4.  Configure the environment settings:
    *   **Name:** `secure-chat` (or any preferred name)
    *   **Runtime:** `Python 3`
    *   **Region:** Select the closest region to you and your friends.
    *   **Branch:** `main`
    *   **Build Command:** `pip install -r requirements.txt`
    *   **Start Command:** `gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 server:app`
5.  Under **Advanced Settings**, add the following **Environment Variables**:
    *   `PYTHONUNBUFFERED` = `1`
6.  Click **Deploy Web Service**. Render will build the virtual environment and launch your secure server.

---

### 💡 Crucial Operational Details for Render Hosting

To ensure a seamless experience with your friends around the world, please read the following operational considerations:

> [!NOTE]
> **Render Free Tier Spin-Down (Cold Starts)**
> Since this is hosted on Render's free tier, the web container automatically spins down (enters a sleep state) after 15 minutes of inactivity. When you or a friend first visit your deployment URL, the page may take **50 to 90 seconds** to load as Render boots the container up. Once awake, the application operates instantly and seamlessly.

> [!IMPORTANT]
> **Database Persistence: Ephemeral SQLite vs. Permanent PostgreSQL**
> By default, the application runs on a local SQLite database (`secure_chat.db`). However, **Render's free tier containers have an ephemeral filesystem**. Every time the service spins down due to inactivity or restarts during a redeploy, your SQLite file is deleted—meaning **all registered user accounts and public keys will be completely wiped!**
> 
> **The Solution:** Link a free **Render PostgreSQL Database** to your web service:
> 1. In Render, click **New > PostgreSQL** and create a free database.
> 2. Once provisioned, copy the **Internal Database URL**.
> 3. Go to your Secure Chat Web Service **Environment Variables** and add:
>    *   **Key:** `DATABASE_URL` | **Value:** *[Paste your copied PostgreSQL URL]*
> 4. Save changes. The app's `database.py` will automatically detect the variable, convert the `postgres://` dialect to `postgresql://`, and connect using SQLAlchemy. **Your user accounts and public keys will now be permanently persisted across all restarts!**

> [!TIP]
> **Why Chat History is Ephemeral (Perfect Forward Secrecy by Design)**
> You may notice that refreshing the browser page or losing connection wipes out your chat history. **This is a security feature, not a bug!** 
> 1. plain text messages are *never* stored on the server's hard drive—they only exist as encrypted payloads inside the server's volatile RAM (`chat_history` dictionary).
> 2. When a user disconnects or refreshes the page, the server calls `clear_user_history(username)`, instantly erasing all session history involving that user from memory.
> 3. Because cryptographic keypairs are generated in-memory on login and are never saved to disk, refreshing the page generates a brand new keypair, rendering older encrypted session history unreadable. This guarantees **Perfect Forward Secrecy**!

### 🌍 Chatting Worldwide
Yes! Because the server is hosted publicly on HTTPS with full WebSocket support, **you can chat with friends anywhere in the world**! Simply share your public Render URL (e.g., `https://your-app-name.onrender.com`). As long as you are logged in at the same time, you can register accounts, establish ECDH key exchanges, and enjoy secure, end-to-end encrypted chats globally!

---

## 📁 File Structure

```
secure-chat/
├── server.py              # Zero-knowledge message router and WebSocket handler
├── crypto.py              # Server-side cryptographic functions (password hashing only)
├── database.py            # SQLAlchemy config (dynamic SQLite/Postgre support & volatile memory logs)
├── Procfile               # Production startup instructions for Gunicorn + Gevent
├── requirements.txt       # Python dependencies (Flask, Flask-SocketIO, gevent-websocket, SQLAlchemy, etc.)
├── templates/
│   └── index.html         # Rich UI templates, Canvas compression, and ECDH/AES client engine
├── static/
│   └── style.css          # Premium glassmorphic stylesheets and responsive layouts
└── README.md              # Documentation and Operational Guide (this file)
```

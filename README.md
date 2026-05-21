# 🔐 Secure Chat-E2EE — Ultra-Secure End-to-End Encrypted Chat Console

[![Live on Render](https://img.shields.io/badge/Live-Render.com-46cbf5?style=for-the-badge&logo=render&logoColor=white)](https://render.com)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Socket.IO](https://img.shields.io/badge/Socket.io-010101?style=for-the-badge&logo=socket.io&logoColor=white)](https://socket.io/)
[![Cryptography](https://img.shields.io/badge/Crypto-ECDH%20P--256%20%2B%20AES--128--CBC-22c55e?style=for-the-badge)](https://developer.mozilla.org/en-US/docs/Web/API/Web_Crypto_API)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

A production-grade, real-time web chat application featuring **True End-to-End Encryption (E2EE)**, wrapped inside a stunning **holographic cybersecurity console UI**. The interface is inspired by military-grade tactical displays — deep-space dark panels, neon cyan/indigo accent glows, CRT scanline overlays, glassmorphism layouts, and immersive interactive boot sequences.

The backend operates on a strict **zero-knowledge principle** — the server is a pure encrypted relay. It never sees plaintext messages, images, or derived encryption keys. All cryptographic operations (key generation, key exchange, encryption, decryption, integrity verification) happen **exclusively inside the user's browser**.

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🎨 HoloGrid Visual Design System](#-hologrid-visual-design-system)
- [🛠️ Technology Stack](#️-technology-stack)
- [🏗️ Architectural Flow (E2EE & Zero-Knowledge)](#️-architectural-flow-e2ee--zero-knowledge)
- [🔒 Cryptographic Implementation Details](#-cryptographic-implementation-details)
- [🛡️ Security & Stability Engineering](#️-security--stability-engineering)
- [🚀 Local Setup & Deployment](#-local-setup--deployment)
- [☁️ Deploying on Render.com (Chat Globally)](#️-deploying-on-rendercom-chat-globally)
- [📁 Project Structure](#-project-structure)

---

## ✨ Features

### 🔐 Cryptographic Core
| Feature | Description |
|---|---|
| **True E2EE Direct Messaging** | ECDH key exchange, AES encryption/decryption — all in-browser. The server never sees plaintext. |
| **Zero-Knowledge Backend** | Server relays only Base64 ciphertexts and SHA-256 password hashes. |
| **Secure Broadcast Channel** | Ephemeral AES key per message, individually wrapped for each online user via their ECDH shared secrets. |
| **SHA-256 Tamper Detection** | Every message carries a hash. Recipients verify payload integrity and display `✔ Verified` or `⚠ Tampered`. |
| **Interactive Crypto Inspector** | Tap any integrity badge to open a detailed forensic audit modal showing sender, receiver, ciphertext, plaintext, SHA-256 hash, and verification status. |
| **Real-Time Telemetry HUD** | Active chat sessions display live cryptographic parameters: target node, curve type, truncated peer key, derived shared secret, and last IV. |

### 🎨 Premium UI & Interactions
| Feature | Description |
|---|---|
| **System Boot Splash** | On first load, a full-screen holographic terminal runs a diagnostic sequence (curve isolation, CPU checks, relay connection) with a progress bar before revealing the main cockpit. |
| **Handshake Scanner Animation** | Clicking a contact triggers a 400ms tactical scanning overlay simulating P-256 curve verification and cryptographic tunnel establishment. |
| **CRT Scanline Overlay** | A subtle retro CRT sweep effect runs across the entire viewport for an authentic cyberpunk console feel. |
| **Laser Sweep Line** | A horizontal neon-cyan beam continuously sweeps vertically across the screen. |
| **Glassmorphic Panels** | All UI modules use frosted-glass blur effects with neon border glows. |
| **Cursor-Tracking Hover Glows** | User contact cards have radial gradient glows that follow the mouse cursor position. |
| **Micro-Animations** | Message pop-in slides, typing dot bounces, button ripple effects, badge pop-scales, send-button pulses, and form slide transitions. |
| **Staggered History Loading** | Chat history messages fade in sequentially with skeleton shimmer placeholders during decryption. |

### 🖼️ Media & Input Systems
| Feature | Description |
|---|---|
| **Canvas Image Compression** | Photos are scaled and compressed client-side via HTML5 Canvas before E2EE encryption, keeping payloads lightweight. |
| **Native Emoji Picker** | Fully integrated `emoji-picker-element` with mobile-stable viewport handling. |
| **Threaded Replies** | Quote and reply to specific messages with color-coded author indicators. |
| **Real-Time Typing Indicators** | Animated bounce-dot feedback when the other user is typing. |

### 📱 Mobile Optimization
| Feature | Description |
|---|---|
| **Sliding Panel Navigation** | CSS transform-based panel transitions for native app-like feel. |
| **Hardware Back Button** | History API integration for Android back-button chat closure. |
| **Emoji Picker Stability** | `pointerdown` event interception prevents keyboard/viewport jumps when selecting emojis on touch devices. |
| **Dynamic Viewport Units** | Uses `100dvh` for accurate mobile viewport sizing. |

---

## 🎨 Secure Chat Visual Design System

The interface is built on a unified cyberpunk design token system:

```
DESIGN TOKENS
─────────────────────────────────
Background:     #030712 (Deep Space Obsidian)
Panel Glass:    rgba(15, 23, 42, 0.45) + backdrop-filter: blur(12px)
Accent Cyan:    #06b6d4 (Primary neon)
Accent Purple:  #8b5cf6 (Secondary neon)
Status Green:   #10b981 (Verified / Online)
Status Red:     #ef4444 (Error / Tampered)
─────────────────────────────────
Heading Font:   Space Grotesk (Google Fonts)
Body Font:      Inter (Google Fonts)
─────────────────────────────────
Layout:         Three-panel cockpit grid
                ├── Left:   Identity Node Terminal (Auth + Contacts)
                ├── Center: Comms Conduit (Chat + Telemetry HUD)
                └── Right:  Telemetry Decoupler (Encryption Logs)
```

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Backend** | Python 3, Flask, Flask-SocketIO | HTTP routing, WebSocket event handling |
| **Async Workers** | `gevent`, `gevent-websocket` | High-concurrency asynchronous I/O |
| **Production Server** | `gunicorn` | Production WSGI + WebSocket container |
| **Database ORM** | SQLAlchemy (SQLite / PostgreSQL) | Thread-safe user credentials and public key storage |
| **Client Crypto** | `elliptic.js` (NIST P-256), `CryptoJS` | ECDH key exchange, AES-128-CBC encryption, SHA-256 hashing |
| **Server Crypto** | PyCryptodome (SHA-256) | Zero-knowledge password hashing only |
| **UI Framework** | Vanilla HTML5/CSS3/JS | Custom cyberpunk HUD with glassmorphism, neon glows, and CRT effects |
| **Typography** | Google Fonts (Space Grotesk + Inter) | Tactical HUD headers + readable chat text |
| **Emoji System** | `emoji-picker-element` (Web Component) | Native emoji selection with touch-safe handling |

---

## 🏗️ Architectural Flow (E2EE & Zero-Knowledge)

The system enforces a client-side sandbox model. Cryptographic boundaries are never crossed by the server.

```
                  ┌─────────────────────────────────────────────────────────────┐
                  │                 ZERO-KNOWLEDGE SERVER (Flask)               │
                  │                                                             │
                  │  • Authenticates users via SHA-256 password hashes          │
                  │  • Stores & relays ECDH public keys (never private keys)   │
                  │  • Relays encrypted payloads (ciphertext only)             │
                  │  • Manages ephemeral session-scoped chat history (RAM)     │
                  │  • Clears all user history on disconnect (PFS)             │
                  └──────────────────────────────┬──────────────────────────────┘
                                                 │
                                                 │ Secure WebSockets (Socket.IO)
                                                 │
                             ┌───────────────────┴───────────────────┐
                             │                                       │
                  ┌──────────▼──────────┐                 ┌──────────▼──────────┐
                  │     Client Alice    │                 │     Client Bob      │
                  │                     │                 │                     │
                  │  1. Generate ECDH   │                 │  1. Generate ECDH   │
                  │     Keypair (P-256) │                 │     Keypair (P-256) │
                  │  2. Request Bob's   │                 │  2. Request Alice's │
                  │     Public Key      │                 │     Public Key      │
                  │  3. Derive AES Key  │                 │  3. Derive AES Key  │
                  │     via ECDH        │                 │     via ECDH        │
                  │  4. Encrypt message │                 │  4. Decrypt message │
                  │     (AES-128-CBC)   │                 │     (AES-128-CBC)   │
                  │  5. Transmit cipher │                 │  5. Verify SHA-256  │
                  │     + SHA-256 hash  │                 │     integrity hash  │
                  └─────────────────────┘                 └─────────────────────┘
```

---

## 🔒 Cryptographic Implementation Details

### 1. Key Derivation via ECDH (P-256)

On login, the browser generates an ephemeral Elliptic Curve keypair on the **NIST P-256 (secp256r1)** curve using `elliptic.js`:

- The **Private Key** stays strictly inside client-side JavaScript memory — never transmitted.
- The **Public Key** (hex-encoded) is stored on the server via the `store_public_key` socket event.
- When Alice selects Bob, both browsers query each other's public keys and compute:

  **Shared Secret = Alice's Private Key × Bob's Public Key (on P-256)**

- The raw shared secret is SHA-256 hashed and truncated to the first 32 hex characters (16 bytes) to form a high-entropy **AES-128** encryption key.

### 2. Client-Side AES-128-CBC Encryption

Every message is encrypted locally using the derived AES key in **Cipher Block Chaining (CBC)** mode with **PKCS7** padding:

- A cryptographically random **16-byte IV** is generated per message.
- The IV is prepended to the ciphertext and Base64-encoded before transmission.
- Identical plaintext produces completely different ciphertext each time.

### 3. Broadcast Ephemeral Key Wrapping

For group broadcast messages to all online users:

1. Generate a random **ephemeral AES-128 key** for that single message.
2. Encrypt the message content using the ephemeral key.
3. For each online user, wrap the ephemeral key using their individual ECDH shared secret.
4. Transmit: `{ ciphertext, SHA-256 hash, wrappedKeys: { "Bob": ..., "Charlie": ... } }`.
5. Each receiver unwraps only their copy of the ephemeral key and decrypts the message.

### 4. SHA-256 Integrity Verification

Every message includes a SHA-256 hash of the original plaintext JSON payload. Recipients recompute the hash after decryption and compare:

- **Match** → `✔ Verified` (green badge)
- **Mismatch** → `⚠ Tampered` (red badge)

Tapping the badge opens the **Cryptographic Inspector** modal with full forensic details.

---

## 🛡️ Security & Stability Engineering

### Resolved Issues & Hardened Systems

1. **Public Key Race Condition Fix** — Server now defers `broadcast_users()` until after the ECDH public key is written to the database, preventing key derivation failures for other clients.

2. **3-Pass Broadcast Decryption Buffer** — `handleGroupReceive` retries up to 3 times at 500ms intervals, allowing asynchronous key exchanges to settle before decryption.

3. **XSS Protection for Base64 Images** — All image payloads are validated (`startsWith('data:image/')`) and HTML-escaped via `escapeHtml()` before DOM insertion.

4. **Auto-Recovering Connection Handler** — Socket disconnects trigger an immediate warning notification followed by an automatic `location.reload()` after 2 seconds to cleanly cycle keypairs.

5. **History-Pending Key Buffer** — If chat history loads before the peer's public key arrives, messages are buffered in `pendingHistoryData` and automatically processed when the key exchange completes.

6. **Mobile Emoji Picker Stability** — `pointerdown` event interception with `event.preventDefault()` on the emoji picker prevents the mobile virtual keyboard from causing viewport jumps and layout shifts. Custom `focus()` calls are restricted to already-active input fields on touch devices.

7. **Session-Based Boot Splash** — The initialization sequence uses `sessionStorage` to run only once per browser session, skipping on subsequent page loads.

---

## 🚀 Local Setup & Deployment

### Prerequisites

- **Python 3.8+** installed on your system.

### Running Locally

```bash
# 1. Clone the repository
git clone https://github.com/your-username/secure-chat.git
cd secure-chat

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the server
python server.py
```

The startup banner will display:
```
==================================================
  SECURE CHAT SERVER (E2EE)
==================================================
  Local:   http://127.0.0.1:5000
  Network: http://192.168.x.x:5000
==================================================
```

- **Local:** Open `http://127.0.0.1:5000` in your browser.
- **LAN Testing:** Use the Network URL on other devices connected to the same Wi-Fi to test multi-device E2EE chat.

---

## ☁️ Deploying on Render.com (Chat Globally)

This application is production-ready for [Render.com](https://render.com) free-tier hosting with full WebSocket support.

### Step-by-Step Deployment

1. Push your code to a **GitHub** or **GitLab** repository.
2. Log in to [Render Dashboard](https://dashboard.render.com/) → **New > Web Service**.
3. Connect your repository and configure:

| Setting | Value |
|---|---|
| **Name** | `secure-chat` (or your preferred name) |
| **Runtime** | `Python 3` |
| **Region** | Closest to you and your friends |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 server:app` |

4. Under **Environment Variables**, add:
   - `PYTHONUNBUFFERED` = `1`
5. Click **Deploy Web Service**.

### ⚠️ Important Operational Notes

> **🕐 Cold Starts (Free Tier)**
> Render's free containers spin down after ~15 minutes of inactivity. The first visit after sleep may take **50–90 seconds** to boot. Once awake, the app runs instantly.

> **💾 Database Persistence**
> By default, the app uses local SQLite — but Render's filesystem is **ephemeral**. Every restart wipes the database.
>
> **Recommended:** Create a free **Render PostgreSQL** database and add the `DATABASE_URL` environment variable to your web service. The app's `database.py` automatically detects and connects to PostgreSQL, persisting user accounts and keys across all restarts.
>
> Steps:
> 1. Render Dashboard → **New > PostgreSQL** → Create free database.
> 2. Copy the **Internal Database URL**.
> 3. Add to your Web Service: **Environment Variable** → Key: `DATABASE_URL`, Value: *(your PostgreSQL URL)*.

> **🔄 Ephemeral Chat History (Perfect Forward Secrecy)**
> Chat history is stored only in server RAM — never on disk. When a user disconnects or refreshes, `clear_user_history()` erases all their session messages. ECDH keypairs are regenerated on every login, making old encrypted history permanently unreadable. This is **Perfect Forward Secrecy by design**.

### 🌍 Chat with Friends Worldwide

Once deployed, share your public Render URL (e.g., `https://your-app.onrender.com`). Anyone can:
1. Register an account
2. Log in simultaneously with friends
3. Establish automatic ECDH key exchanges
4. Chat with full end-to-end encryption across the globe!

---

## 📁 Project Structure

```
secure-chat/
├── server.py              # Zero-knowledge Flask server — WebSocket routing & encrypted relay
├── crypto.py              # Server-side SHA-256 password hashing (only server crypto operation)
├── database.py            # SQLAlchemy ORM — auto-detects SQLite (local) or PostgreSQL (Render)
├── Procfile               # Gunicorn + GeventWebSocket production startup command
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html         # HoloGrid UI — ECDH/AES crypto engine, boot splash, telemetry HUD,
│                          #   handshake scanner, crypto inspector, emoji picker, canvas compressor
├── static/
│   └── style.css          # Cyberpunk design system — glassmorphism, neon glows, CRT overlays,
│                          #   responsive mobile handlers, animations, and HUD layouts
└── README.md              # This file
```

---

<p align="center">
  <strong>Secure Chat-E2EE</strong> — Built with 🔐 cryptography, 🎨 cyberpunk aesthetics, and ☕ caffeine.
  <br>
  <em>Zero-knowledge. Full encryption. Maximum style.</em>
</p>

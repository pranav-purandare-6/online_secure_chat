from Crypto.Hash import SHA256

# ===== PASSWORD HASH =====
def hash_password(password):
    """SHA-256 hash of a password string, returned as hex.
    This is the ONLY server-side crypto operation.
    All message encryption/decryption happens client-side (E2EE).
    """
    return SHA256.new(password.encode('utf-8')).hexdigest()
import hashlib
import os
import hmac

ITERATIONS = 100000


def hash_password(password):

    salt = os.urandom(32)  # 32-byte salt
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        ITERATIONS
    )
    return salt.hex(), key.hex()


def verify_password(stored_password_hash_hex, stored_salt_hex, provided_password):
    # Convert hex strings back to bytes
    salt = bytes.fromhex(stored_salt_hex)
    stored_hash = bytes.fromhex(stored_password_hash_hex)

    # Hash the provided password using the stored salt
    provided_key = hashlib.pbkdf2_hmac(
        'sha256',
        provided_password.encode('utf-8'),
        salt,
        ITERATIONS
    )

    # Compare the hashes securely
    return hmac.compare_digest(stored_hash, provided_key)
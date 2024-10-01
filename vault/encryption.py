"""Tools and helpers regarding encryption operations for Vault."""

import base64
import random
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def generate_key_from_password(password: str) -> bytes:
    """Generate an Encryption key using a password.

    :arg password: The password to generate the key for.
    :type password: str

    :returns: The encryption key as bytes.
    :rtype: bytes
    """
    pass_as_bytes: bytes = password.encode("utf-8")

    # Generate the Salt
    random.seed(pass_as_bytes)  # Set the seed
    salt = random.randbytes(100)  # Get the Salt
    random.seed(os.urandom(100))  # Undo the seed

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt, iterations=480_000
    )
    key: bytes = base64.urlsafe_b64encode(kdf.derive(pass_as_bytes))

    return key


def fernet_from_password(password: str) -> Fernet:
    """Returns a Fernet class instance primed with the password generated key."""
    return Fernet(generate_key_from_password(password))

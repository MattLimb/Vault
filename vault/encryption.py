from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
import pathlib

class Encryption:
    """Handle the encryption of files and strings in a standard method
    """
    def __init__(self, key):
        """Setup the encryption class.

        Params:
        key : The encryption key to use for encryption
        """
        self.key = key

    def encrypt(self, data):
        """Encrypt a file given a filepath

        Params:
        data : The data in Bytes to encrypt

        Return:
        The encrypted data in bytes
        """
        f = Fernet(self.key)
        return f.encrypt(data)

    def decrypt(self, data):
        """Decrypt a file given a filepath

        Params:
        data : The data in Bytes to encrypt

        Return:
        The decrypted data in bytes
        """
        f = Fernet(self.key)
        return f.decrypt(data)
    
    
    @staticmethod
    def read_file(filepath:pathlib.Path):
        """Read a file for encryption

        Params:
        filepath: The filepath of the file

        Return:
        The file contents as bytes
        """
        with filepath.open("rb") as f:
            return f.read()

    @staticmethod
    def write_file(filepath:pathlib.Path, data:bytes):
        """Write to a file

        Params:
        filepath : The filepath of the file
        data     : The data in Bytes to write
        """
        with filepath.open("wb") as f:
            f.write(data)

    @staticmethod
    def generate_key():
        """Generate an encryption key

        Returns:
        An encryption key in bytes
        """
        return Fernet.generate_key()

    @staticmethod
    def generate_nonce():
        """Generate a nonce for encryption

        Returns:
        32 random bytes
        """
        return os.urandom(32)
    
    @staticmethod
    def master_key(term, salt):     
        kdf = PBKDF2HMAC(    
            algorithm=hashes.SHA512(),
            length=32,
            salt=salt,
            iterations=100000,
        )

        return base64.urlsafe_b64encode(kdf.derive(term.encode()))
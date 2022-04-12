import pathlib
import uuid
import binascii
import os

from datetime import datetime

from cryptography.hazmat.primitives.hashes import Hash
from .encryption import Encryption
from .hash import HashTool

class Vault:
    """Class representing a Vault
    """
    def __init__(self, uuid, name, filepath, nonce, sanity, default, added, modified):
        """Setup the default information needed for Vault operations
        """
        self.uuid = uuid
        self.name = name
        self.filepath = pathlib.Path(filepath)
        self.nonce = binascii.unhexlify(nonce.encode())
        self.sanity = sanity
        self.default = default
        self.added = datetime.fromtimestamp(added)
        self.modified = datetime.fromtimestamp(modified)

    def update_modified(self):
        self.modified = datetime.now()

    def to_config(self):
        """Return a Tuple to represent the Vault in the confguration file
        """
        config = dict(
            name=self.name,
            filepath=str(self.filepath),
            nonce=binascii.hexlify(self.nonce).decode(),
            sanity=self.sanity,
            default=self.default,
            added=self.added.timestamp(),
            modified=self.modified.timestamp()
        )
        return (self.uuid, config) 

    def verify_password(self, password):
        """Verify that the password for this Vault is correct
        """
        key = Encryption.master_key(password, self.nonce)
        new_sanity = HashTool("sha256", vault=self.name).hash_string("SanityCheck", key.decode())

        if new_sanity == self.sanity:
            return True
        else:
            return False

    @staticmethod
    def new(filepath, password, name=None, default=False):
        """Create a new Vault

        Params:
        filepath: The filepath of the Vault
        password: The Password for the Vault
        name [optional]: The name of the vault
        default [optional]: Set Vault as default
        """
        
        filepath = pathlib.Path(filepath)
        nonce = os.urandom(32)
        key = Encryption.master_key(password, nonce)
        sanity = HashTool("sha256", vault=name).hash_string("SanityCheck", key.decode())
        added = modified = datetime.now().timestamp()


        if filepath.exists() == False:
            filepath.mkdir()
        
        return Vault(
            uuid=str(uuid.uuid4()),
            name=name,
            filepath=str(filepath.resolve()),
            nonce=binascii.hexlify(nonce).decode(),
            sanity=sanity,
            default=default,
            added=added,
            modified=modified
        )
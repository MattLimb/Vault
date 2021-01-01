import hashlib
import pathlib

from .excptions import VaultIOException

class HashTool:
    """Hash files/strings
    """
    BUFFER_SIZE = 65536

    def __init__(self, algrithm, **kwargs):
        """Setup initial settings for hashing files or strings

        Params:
        algorithm : The hashing algorithm to use. Can be anything supported by Python hashlib.
        kwargs    : Optional settings that can be used to tweak how the hash is created.
        """

        self.algorithm = algrithm
        self.vault = kwargs.get("vault")

    def hash_file(self, filepath):
        """Hash files of varying size

        Params:
        filepath : The filepath to the file to be hashed.

        Returns:
        The hexadecimal hash of the file.
        """
        hash = hashlib.new(self.algorithm)
        filepath = pathlib.Path(filepath)

        if filepath.exists() == False:
            raise VaultIOException(f"Given filepath \"{filepath}\" does not exist.")
        if filepath.is_file() != True:
            raise VaultIOException(f"Given filepath \"{filepath}\" is not a file.", self.vault)

        with filepath.open("rb") as f:
            read = True
            while read:
                data = f.read(HashTool.BUFFER_SIZE)

                if data:
                    hash.update(data)
                else:
                    read = False
        return hash.hexdigest()

    def hash_string(self, data):
        """Hash arbitary strings of varying size

        Params:
        data : The string to be hashed.

        Returns:
        The hexadecimal hash of the string.
        """
        hash = hashlib.new(self.algorithm)
        
        hash.update(data.encode())

        return hash.hexdigest()
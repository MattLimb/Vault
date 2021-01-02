import hashlib
import pathlib

from .excptions import VaultIOException, HashError

class HashTool:
    """Hash files/strings
    """
    BUFFER_SIZE = 65536

    def __init__(self, algorithm, **kwargs):
        """Setup initial settings for hashing files or strings

        Params:
        algorithm : The hashing algorithm to use. Can be anything supported by Python hashlib.
        kwargs    : Optional settings that can be used to tweak how the hash is created.
        """

        self.algorithm = algorithm
        self.vault = kwargs.get("vault")

    def hash_file(self, filepath):
        """Hash files of varying size

        Params:
        filepath : The filepath to the file to be hashed.

        Returns:
        The hexadecimal hash of the file.
        """
        try:
            hash = hashlib.new(self.algorithm)
        except ValueError as e:
            raise HashError(f"Error: Unknown hash algorithm \"{self.alorithm}\".", self.vault)

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

    def hash_string(self, data, salt=None):
        """Hash arbitary strings of varying size

        Params:
        data : The string to be hashed.

        Returns:
        The hexadecimal hash of the string.
        """
        try:
            hash = hashlib.new(self.algorithm)
        except ValueError as e:
            raise HashError(f"Error: Unknown hash algorithm \"{self.algorithm}\".", self.vault)
        
        if salt == None:
            hash.update(data.encode())
        else:
            hash.update(f"{data}{salt}".encode())

        return hash.hexdigest()
from .cli.cli_outputs import Outputs

class VaultIOException(IOError):
    """The base IO Exception for Vault
    """
    pass

class HashError(Exception):
    """Errors regarding the Hash
    """
    pass
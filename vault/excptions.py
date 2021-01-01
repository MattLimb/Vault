from .cli.cli_outputs import Outputs
from .cli.cli_exceptions import VaultException

class VaultIOException(IOError):
    """The base IO Exception for Vault
    """
    pass

class HashError(VaultException):
    """Errors regarding the Hash
    """
    pass
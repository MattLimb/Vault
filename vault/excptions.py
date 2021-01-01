from .cli.cli_outputs import Outputs

class VaultIOException(IOError):
    """The base IO Exception for Vault
    """
    def __init__(self, message, vault):
        """Override the base exception to do our own thing.
        """
        super().__init__(message)

        Outputs().write({
            "error": 1,
            "message": message,
            "vault": vault            
        })
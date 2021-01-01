import logging
import click

from .cli_outputs import Outputs

log = logging.getLogger()

ERROR_NUMBERS = {
    0: "Success",
    1: "Unknown Error",
    10: "Value Errors"
}

class VaultException(Exception):
    """The base Vault Exception
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
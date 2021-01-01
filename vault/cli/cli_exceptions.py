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
    pass
from .cli_outputs import Outputs
from vault import __version__ as vault_version

import click
import platform

__author__ = "Matt Limb <matt.limb17@gmail.com>"

@click.command("version", help="Get version info about Vault")
@click.option("-d", "--debug", "debug", is_flag=True, help="Enable debug mode")
@click.option("-o", "--output", "output", type=click.Choice(["TEXT", "JSON", "XML"], case_sensitive=False), default="TEXT", help="Format to output to the terminal in")
def version(debug, output):
    """Show version infoamtion for Vault

    Options:
    -d/--debug  : Enable debug mode for more information.
    -o/--output : The format to output to the terminal in.

    Returns:
    The version information
    """
    version_string = f"Vault {vault_version}"
    
    if debug:
        system_info = platform.uname()
        version_string = f"{version_string} - {platform.python_implementation()}/Python {platform.python_version()} running on {system_info.node} ({system_info.system} {system_info.release} version {system_info.version})"

    Outputs(format_=output.lower()).write(dict(
        type="normal",
        error=0,
        message=version_string
    ))
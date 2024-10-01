"""Command Line Interface for Vault."""

import click

from .vault import vault_group
from .file import file_group
from .tools import tools_group


@click.group()
def cli():
    """Vault CLI Root."""


cli.add_command(vault_group)
cli.add_command(file_group)
cli.add_command(tools_group)

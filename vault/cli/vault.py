"""Vault Group of Commands. Expressed under the 'vault' collective."""

from pathlib import Path
from typing import Optional

import click

from .. import CONFIG_DIR
from ..vaults import Vault
from .password_option import password_option


@click.group(name="vault")
def vault_group():
    """Vault Group of Commands."""


@vault_group.command()
@click.argument("name", type=click.STRING, required=True)
@click.argument("filepath", type=click.STRING, required=False, default=None)
@click.password_option("-p", "--password", type=click.STRING, required=True)
def new(name: str, filepath: Optional[str], password: str):
    """Create a New Vault."""
    filepath_obj: Path

    if filepath is None:
        filepath_obj = Path.cwd()
    else:
        filepath_obj = Path(filepath)

    vlt = Vault.new(name, root=filepath_obj, password=password)

    click.echo(f"Successfully Created Vault: {vlt.name}")


@vault_group.command()
@click.argument("name", type=click.STRING, required=True)
@password_option("-p", "--password", type=click.STRING, required=True)
def delete(name: str, password: str):
    """Remove a File Vault and its Contents."""
    vlt = Vault.open(name, password=password)

    click.confirm(
        "This is a destructive action. This cannot be undone. Do you still want to?",
        abort=True,
    )

    vlt.delete()
    click.echo(f"Vault {name} Deleted.")


@vault_group.command()
@click.argument("name", type=click.STRING, required=True)
@password_option("-p", "--password", type=click.STRING, required=True)
def info(name: str, password: str):
    """Display Information about our Vault."""
    vlt = Vault.open(name, password=password)

    click.echo(f"Files Availiable In Vault {name}:")

    for filename, data in vlt.data.items():
        click.echo(f"  - {filename} | {data['size']} Bytes")


@vault_group.command()
def list():
    """Display Configured Vault Names."""
    click.echo("Configured Vaults:")

    for vault in CONFIG_DIR.glob("*.vault"):
        print(f" - {vault.name.removesuffix('.vault')}")

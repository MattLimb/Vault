"""CLI to manage files in Vaults."""

from pathlib import Path

import click

from ..vaults import Vault
from ..vfile import VaultFile
from .password_option import password_option


@click.group(name="file")
def file_group():
    """Vault Group of Commands."""


@file_group.command()
@click.argument("filepath", type=click.STRING, required=True)
@click.option("-v", "--vault", type=click.STRING, required=True)
@password_option("-p", "--password", type=click.STRING, required=True)
def add(filepath: str, vault: str, password: str):
    """Add a file to a Vault."""
    filepath_obj: Path = Path(filepath)

    if not filepath_obj.exists() or filepath_obj.is_dir():
        click.echo("[ERROR] No file at specified path.")
        exit(1)

    vfile = VaultFile.new(filepath=filepath_obj)

    vlt = Vault.open(vault, password=password)
    vlt.add_file(vfile)

    click.echo(f"Successfully Added {vfile.filename} to Vault.")


@file_group.command()
@click.argument("filename", type=click.STRING, required=True)
@click.argument("output", type=click.STRING, required=True)
@click.option("-v", "--vault", type=click.STRING, required=True)
@password_option("-p", "--password", type=click.STRING, required=True)
def decrypt(filename: str, output: str, vault: str, password: str):
    """Decrypt and Retrieve a file from the Vault."""
    filepath = Path(output)

    if filepath.exists():
        click.echo("Cannot decrypt. Output file already present.")
        exit(1)

    vlt = Vault.open(vault, password=password)

    vfile = vlt.get_file(filename)
    vfile.open_into(vlt.root, filepath)

    click.echo(f"Successfully Added {vfile.filename} to Vault.")


@file_group.command()
@click.argument("filename", type=click.STRING, required=True)
@click.option("-v", "--vault", type=click.STRING, required=True)
@password_option("-p", "--password", type=click.STRING, required=True)
def info(filename: str, vault: str, password: str):
    """Decrypt and Retrieve a file from the Vault."""
    vlt = Vault.open(vault, password=password)
    vfile = vlt.get_file(filename)

    click.echo(f"{vfile.filename} | {vfile.size}")


@file_group.command()
@click.argument("filename", type=click.STRING, required=True)
@click.option("-v", "--vault", type=click.STRING, required=True)
@password_option("-p", "--password", type=click.STRING, required=True)
def delete(filename: str, vault: str, password: str):
    """Decrypt and Retrieve a file from the Vault."""
    vlt = Vault.open(vault, password=password)
    vfile = vlt.get_file(filename)

    vfile.delete_file(vlt.root)
    del vlt.data[filename]

    vlt.save()

    click.echo(f"{filename!r} Deleted.")

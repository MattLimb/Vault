"""Helpful CLI Tools."""

import hashlib
import uuid
from pathlib import Path
from typing import Optional

import click
from cryptography.fernet import Fernet

from .. import ENCODING

HASH_CHOICES: list[str] = [
    "md5",
    "sha1",
    "sha224",
    "sha256",
    "sha384",
    "sha512",
    "sha3_224",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "shake_128",
    "shake_256",
    "blake2b",
    "blake2s",
]


@click.group(name="tools")
def tools_group():
    """Vault Group of Commands."""


@tools_group.command("uuid")
@click.option("-n", "--number", type=click.INT, default=1)
def random_uuid(number: int):
    """Generate a random UUID."""
    for _ in range(number):
        click.echo(str(uuid.uuid4()))


@tools_group.command("encryption-key")
def random_encryption_key():
    """Generate a random Encryption Key."""
    click.echo(Fernet.generate_key().decode("utf-8"))


@tools_group.command("hash")
@click.argument("input_string", type=click.STRING, required=True)
@click.option("-f", "--is-filepath", is_flag=True)
@click.option(
    "-t",
    "--hash-type",
    type=click.Choice(HASH_CHOICES, case_sensitive=False),
    default="SHA256",
)
def generate_hash(input_string: str, is_filepath: bool, hash_type: str):
    """Generate a hash from a file or command-line input."""
    data: bytes
    output_prefix: str = hash_type.upper()

    if is_filepath:
        with Path(input_string).open("rb") as reader:
            data = reader.read()

        output_prefix = f"{output_prefix} | {input_string}"
    else:
        data = input_string.encode(ENCODING)

    hsh = hashlib.new(hash_type)
    hsh.update(data)

    click.echo(f"{output_prefix} | {hsh.hexdigest()}")


@tools_group.command("encrypt-text")
@click.argument("input_string", type=click.STRING, required=True)
@click.option("-e", "--encryption-key", type=click.STRING, required=True)
def encrypt(input_string: str, encryption_key: str):
    """Generate a hash from a file or command-line input."""
    fernet = Fernet(encryption_key.encode(ENCODING))
    enc_bytes = fernet.encrypt(input_string.encode(ENCODING))

    print(enc_bytes.decode(ENCODING))


@tools_group.command("decrypt-text")
@click.argument("input_string", type=click.STRING, required=True)
@click.option("-e", "--encryption-key", type=click.STRING, required=True)
def decrypt(input_string: str, encryption_key: str):
    """Generate a hash from a file or command-line input."""
    fernet = Fernet(encryption_key.encode(ENCODING))
    enc_bytes = fernet.decrypt(input_string.encode(ENCODING))

    print(enc_bytes.decode(ENCODING))


@tools_group.command("encrypt-file")
@click.argument("filepath", type=Path, required=True)
@click.option("-e", "--encryption-key", type=click.STRING, required=True)
@click.option("-o", "--output", type=Path, default=None)
def encrypt_file(filepath: Path, encryption_key: str, output: Optional[Path]):
    """Generate a hash from a file or command-line input."""
    if output is None:
        output = filepath.parent / f"{filepath.name}.enc"

    with filepath.open("rb") as reader:
        raw_bytes = reader.read()

    fernet = Fernet(encryption_key.encode(ENCODING))
    enc_bytes = fernet.encrypt(raw_bytes)

    with output.open("wb+") as writer:
        writer.write(enc_bytes)


@tools_group.command("decrypt-file")
@click.argument("filepath", type=Path, required=True)
@click.option("-e", "--encryption-key", type=click.STRING, required=True)
@click.option("-o", "--output", type=Path, required=True)
def decrypt_file(filepath: Path, encryption_key: str, output: Path):
    """Generate a hash from a file or command-line input."""
    with filepath.open("rb") as reader:
        raw_bytes = reader.read()

    fernet = Fernet(encryption_key.encode(ENCODING))
    enc_bytes = fernet.decrypt(raw_bytes)

    with output.open("wb+") as writer:
        writer.write(enc_bytes)

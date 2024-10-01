"""Class to manage vaults on this machine.

This file contains helper methods and useful tools for interacting with Vaults.
"""

import os
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict, TypeAlias, Optional

from cryptography.fernet import Fernet

from .encryption import fernet_from_password

Filename: TypeAlias = str


class VaultFileData(TypedDict):
    """Dict containing all relevant information about a file within a Vault."""

    uid: str
    encryption_nonce: int
    size: int


@dataclass
class VaultFile:
    """Class containing all the logic to represent a File in a Vault."""

    uid: str
    filename: str
    encryption_nonce: int
    size: int

    orginal_filepath: Optional[Path] = None

    @property
    def enc_filename(self) -> str:
        """The Encrypted Filename of the File in the Vault."""
        return f"{self.uid}.vf"

    def as_vault_data(self) -> tuple[Filename, VaultFileData]:
        """Represent this file as a Dict for the Vault Data."""
        return self.filename, {
            "uid": self.uid,
            "encryption_nonce": self.encryption_nonce,
            "size": self.size,
        }

    def save(self, vault_dir: Path) -> None:
        """Save the file to the vault."""
        if self.orginal_filepath is None:
            raise ValueError(
                f"{self.filename!r} cannot be added to the Vault. "
                "Original File reference has been lost."
            )

        output_filename = vault_dir / self.enc_filename

        # Step 1: Read the File
        with self.orginal_filepath.open("rb") as reader:
            file_bytes = reader.read()

        # Step 2: Encrypt the File
        fernet: Fernet = fernet_from_password(str(self.encryption_nonce))
        encrypted_file_bytes = fernet.encrypt(file_bytes)

        # Step 3: Save the File
        with output_filename.open("wb") as writer:
            writer.write(encrypted_file_bytes)

    def open_into(self, vault_dir: Path, output_path: Path) -> None:
        """Decrypt the file into another."""
        # Step 1: Open Encrypted File
        with (vault_dir / self.enc_filename).open("rb") as reader:
            enc_data = reader.read()

        # Step 2: Decrypt
        fernet: Fernet = fernet_from_password(str(self.encryption_nonce))
        unenc_data = fernet.decrypt(enc_data)

        # Step 3: Save to New Location
        with output_path.open("wb") as writer:
            writer.write(unenc_data)

    def delete_file(self, vault_dir: Path) -> None:
        """Delete the file in the vault."""
        (vault_dir / self.enc_filename).unlink()

    @classmethod
    def new(cls, filepath: Path) -> "VaultFile":
        """New file to add to a vault, from a filepath."""
        return cls(
            uid=uuid.uuid4().hex,
            filename=filepath.name,
            encryption_nonce=int.from_bytes(os.urandom(100), byteorder="big"),
            size=filepath.stat().st_size,
            orginal_filepath=filepath,
        )

    @classmethod
    def from_vault_info(cls, filename: str, data: VaultFileData) -> "VaultFile":
        """Create a VaultFile class from the given information in a Vault."""
        return cls(
            uid=data["uid"],
            filename=filename,
            encryption_nonce=data["encryption_nonce"],
            size=data["size"],
        )

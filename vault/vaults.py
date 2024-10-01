"""Class to manage vaults on this machine.

This file contains helper methods and useful tools for interacting with Vaults.
"""

import json
from dataclasses import dataclass
from pathlib import Path

from cryptography.fernet import Fernet

from . import CONFIG_DIR, ENCODING
from .encryption import fernet_from_password
from .vfile import Filename, VaultFileData, VaultFile


@dataclass
class Vault:
    """A class which represents a Vault and allows management of it."""

    name: str
    root: Path

    data: dict[Filename, VaultFileData]

    _pass: str

    @property
    def config_filepath(self) -> Path:
        """The full filepath to the vault metadata file."""
        return CONFIG_DIR / f"{self.name}.vault"

    def save(self) -> None:
        """Save the vault to the config directory."""
        # Step 1 - Create the JSON
        json_bytes: bytes = json.dumps(
            {
                "name": self.name,
                "root": self.root.resolve().as_posix(),
                "data": self.data,
            }
        ).encode(ENCODING)

        # Step 2 - Encrypt the JSON
        fernet: Fernet = fernet_from_password(self._pass)
        encryt_bytes = fernet.encrypt(json_bytes)

        # Step 3 - Write the Encrypted JSON
        with self.config_filepath.open("wb+") as writer:
            writer.write(encryt_bytes)

    def add_file(self, file: VaultFile) -> None:
        """Add a file to a vault."""
        # Add the file to the vault.
        file.save(self.root)

        # Add the file metadata to the vault.
        filename, data = file.as_vault_data()
        self.data[filename] = data
        self.save()

    def get_file(self, filename: str) -> VaultFile:
        """Get a File from the Filename."""
        if filename not in self.data:
            raise ValueError("File not in vault.")

        file_data = self.data[filename]

        return VaultFile.from_vault_info(filename, file_data)

    def delete(self) -> None:
        """Delete the vault. Remove all files on the disk - keeping the containing folder."""
        for fname, data in self.data.items():
            fle = VaultFile.from_vault_info(fname, data)
            fle.delete_file(self.root)

        self.data.clear()
        self.config_filepath.unlink()

    @classmethod
    def new(cls, name: str, root: Path, password: str) -> "Vault":
        """Create a new Vault with given parameters."""
        root = root.resolve()

        if not root.exists():
            root.mkdir()
        elif root.is_file():
            raise ValueError(
                f"Vault Filepath: {str(root)!r} is a file not a directory."
            )
        new_vault = cls(name=name, root=root, data={}, _pass=password)
        new_vault.save()

        return new_vault

    @classmethod
    def open(cls, name: str, password: str) -> "Vault":
        """Open an existing Vault."""
        # Step 1 - Read Encrypted JSON
        vault_filename = CONFIG_DIR / f"{name}.vault"

        if not vault_filename.exists():
            raise ValueError(f"Vault with name {name!r} does not exist.")

        with vault_filename.open("rb") as reader:
            encrypted_json_bytes = reader.read()

        # Step 2: Decrypt and Parse JSON
        fernet: Fernet = fernet_from_password(password)
        json_bytes = fernet.decrypt(encrypted_json_bytes)

        # Step 3: Format Class
        json_document = json.loads(json_bytes.decode(ENCODING))

        return cls(
            name=name,
            root=Path(json_document["root"]),
            data=json_document["data"],
            _pass=password,
        )

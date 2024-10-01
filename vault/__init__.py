"""Key configurations needed for Vault Setup."""

import os
from pathlib import Path

__author__ = "Matt Limb <matt.limb17@gmail.com>"


def determine_root_location() -> Path:
    """Get the base directory for configuration files."""
    user_root = os.environ.get("VAULT_CONFIG_DIR", None)
    root_path: Path

    if user_root is None:
        root_path = Path.home()
    else:
        root_path = Path(user_root)

        if not root_path.exists():
            raise ValueError(
                f"Configured Config Directory does not exist: {str(root_path)!r}"
            )

    root_path /= ".vault"

    if not root_path.exists():
        root_path.mkdir()

    return root_path


CONFIG_DIR: Path = determine_root_location()
ENCODING: str = "UTF-8"

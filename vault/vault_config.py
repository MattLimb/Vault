import pathlib
import yaml

from .vault import Vault

class VaultConfig:
    """Configuration options regarding the main vault.yaml file.
    """
    def __init__(self):
        """Setup options for configuration

        Params:
        location: The location of the yaml config file.
        """
        self._verify_config_locations()
        self.root_location = pathlib.Path(pathlib.Path.home(), ".vault")
        self.files_location = pathlib.Path(self.root_location, "files")
        self.location = pathlib.Path(self.root_location, "vault.yaml")

        self.data = self._parse_yaml()

        if self.data == None:
            self.data = {
                "vaults": {}
            }
    
    def _parse_yaml(self):
        """Read the config YAML file.
        """
        with self.location.open("r") as f:
            return yaml.safe_load(f.read())
                
    def save(self):
        """Write changes to the config YAML file.
        """
        with self.location.open("w") as f:
            f.write(yaml.safe_dump(self.data))

    def get_vault(self, name_or_uuid=None):
        """Check if a vault exists, or return None

        Params:
        name_or_uuid : The name or uuid of a Vault.

        Return:
        List of Vault Objects or an empty List
        """
        vaults = []

        for key, config in self.data.get("vaults").items():
            if name_or_uuid == None:
                vaults.append(Vault(uuid=key, **config))
            elif ( key == name_or_uuid ) or ( config.get("name") == name_or_uuid ):
                vaults.append(Vault(uuid=key, **config))

        return vaults

    def update_vault(self, vault):
        """Add and update Vault config in the configuration file

        Params:
        vault : The Vault object to add to the configuration.
        """
        key, config = vault.to_config()
        self.data["vaults"][key] = config
        self.save()

    @staticmethod
    def _verify_config_locations():
        """Ensure that the Vault config is present. Create it if not.
        """
        root_folder = pathlib.Path(pathlib.Path.home(), ".vault")
        root_yaml = pathlib.Path(root_folder, "vault.yaml")
        root_db_folder = pathlib.Path(root_folder, "files")

        if root_folder.exists() == False:
            root_folder.mkdir()
        
        if root_db_folder.exists() == False:
            root_db_folder.mkdir()
        
        if root_yaml.exists() == False:
            root_yaml.touch()

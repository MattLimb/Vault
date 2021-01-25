import uuid
import pathlib
from sqlalchemy.sql.expression import false

from sqlalchemy.sql.functions import modifier

from .hash import HashTool
from .encryption import Encryption
from datetime import datetime
from magic import Magic

class VaultFile:
    """Class for managing Vault Files
    """
    def __init__(self, uuid, key, filename, folder, extension, size, mime, hash_alg, unenc_hash, added, modified, enc_hash=None):
        """Setup all information needed for administering files for a Vault

        Params:
        uuid: The Unique ID for this file
        key: The encrypted encryption key for this file
        filename: The filename of the file
        folder: The folder structure where this file was found (excluding the root path)
        extension: The extension of the file
        size: The file size in Bytes
        mime: The mime type of the file being encrypted
        hash_alg: The algorithm to be used to verify file integrity
        unenc_hash: The unencrypted hash of the file - in the hash_alg format
        enc_hash: The encrypted has of the file, to ensure no tampering has happened to the file on disk before decryption
        added: The timestamp that the file was added to Vault
        modified: The timestamp of the last time the file was modified in the Vault
        """

        self.uuid = uuid
        self.key = key
        self.filename = filename 
        self.folder = folder
        self.extension = extension
        self.size = size
        self.mime = mime
        self.hash_alg = hash_alg
        self.unenc_hash = unenc_hash
        self.enc_hash = enc_hash
        self.added = datetime.fromtimestamp(added)
        self.modified = datetime.fromtimestamp(modified)

    def insert(self, db):
        """Insert the file into the database

        Params:
        db: The VaultDatabase class to use
        """
        with db.engine.begin() as conn:
            query = db.files_table.insert().values(
                uuid=self.uuid,
                key=self.key,
                filename=self.filename,
                folder=self.folder,
                extension=self.extension,
                size=self.size,
                mime=self.mime,
                hash_alg=self.hash_alg,
                unenc_hash=self.unenc_hash,
                enc_hash=self.enc_hash,
                created=self.added.timestamp(),
                modified=self.modified.timestamp()
            )

            conn.execute(query)
    
    def update(self, db):
        """Update the file into the database

        Params:
        db: The VaultDatabase class to use
        """
        with db.engine.begin() as conn:
            query = db.files_table.update().values(
                key=self.key,
                filename=self.filename,
                folder=self.folder,
                extension=self.extension,
                size=self.size,
                mime=self.mime,
                hash_alg=self.hash_alg,
                unenc_hash=self.unenc_hash,
                enc_hash=self.enc_hash,
                added=self.added.timestamp(),
                modified=datetime.now().timestamp()
            ).where(db.files_table.c.uuid == self.uuid)

            conn.execute(query)

    def remove(self, db):
        """Delete the file into the database

        Params:
        db: The VaultDatabase class to use
        """
        with db.engine.begin() as conn:
            query = db.files_table.delete().where(
                db.files_table.c.uuid == self.uuid
            )

            conn.execute(query)

    def add_groups(self, groups, db):
        """Add groups to the file
    
        Params:
        groups : A list of groups
        db : A VaultDatabase class to use
        """
        with db.engine.begin() as conn:
            query = db.group_files.insert()
            data = []
            for group_uuid in groups:
                data.append(
                    {
                        "file": str(self.uuid),
                        "group": str(group_uuid),
                        "added": datetime.now().timestamp() 
                    }
                )
            conn.execute(query, data)

    def encrypt(self, master_key, vault, orig_path, delete=False):
        """Encrypt the file and store it in the Vault
        
        Params:
        master_key: The master key to decrypt the actual encryption key
        vault : The Vault class to use
        """
        key = Encryption(master_key).decrypt(self.key)

        enc = Encryption(key)
        storage_location = pathlib.Path(vault.filepath, self.extension.replace(".", "")).absolute()
        
        if storage_location.exists() == False:
            storage_location.mkdir()
        
        file_contents = Encryption.read_file(orig_path)
        Encryption.write_file(pathlib.Path(storage_location, f"{self.uuid}.vault"), enc.encrypt(file_contents))

        if delete:
            orig_path.unlink()

        
    @staticmethod
    def new(root_filepath, filepath, master_key, hash_alg="sha256"):
        """Discover all the required metadata about a new file

        Params:
        root_filepath: The given root filepath
        filepath: The full filepath to the file
        hash_alg: The hash algorithm to use to verify integrity
        """
        new_key = Encryption(master_key).encrypt(Encryption.generate_key())
        added = datetime.now().timestamp()
        filepath = pathlib.Path(filepath).resolve()
        extension = filepath.suffix
        stats = filepath.stat()
        size = stats.st_size
        folder = str(filepath).replace(str(root_filepath), "").replace(str(filepath.name), "")
        hash_alg=hash_alg
        hasht = HashTool(hash_alg)
        unenc_hash = hasht.hash_file(str(filepath))
        mime = Magic(mime=True).from_file(str(filepath))

        return VaultFile(
            uuid=str(uuid.uuid4()),
            key=new_key,
            filename=filepath.name,
            folder=folder,
            extension=extension,
            size=size,
            mime=mime,
            hash_alg=hash_alg,
            unenc_hash=unenc_hash,
            added=added,
            modified=added
        )

import pathlib
import uuid
from datetime import datetime

from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, BLOB, Boolean, ForeignKey

class VaultDatabase:
    """Configuration options regarding a Vault database.
    """
    def __init__(self, vault_uuid):
        """Setup options for database

        Params:
        vault_uuid: The uuid of the vault.
        """
        self.root_location = pathlib.Path(pathlib.Path.home(), ".vault")
        self.files_location = pathlib.Path(self.root_location, "files")
        self.db_location = pathlib.Path(self.files_location, f"{vault_uuid}.db")

        self.meta = MetaData()

        self.engine = create_engine(f"sqlite:///{str(self.db_location)}")
        self.meta.bind = self.engine

        self.group_table = Table(
            "groups",
            self.meta,
            Column("uuid", String(32), primary_key=True),
            Column("group_name", String),
            Column("default", Boolean),
            Column("created", Integer),
            Column("modified", Integer)
        )

        self.files_table = Table(
            "files",
            self.meta,
            Column("uuid", String(32), primary_key=True),
            Column("file_name", String),
            Column("file_mime", String),
            Column("extension", String),
            Column("file_size", Integer),
            Column("key", BLOB),
            Column("unencrypted_hash", String),
            Column("encrypted_hash", String),
            Column("created", Integer),
            Column("modified", Integer)
        ) 

        self.group_files = Table(
            "group_files",
            self.meta,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("file", String, ForeignKey("files.uuid")),
            Column("group", String, ForeignKey("groups.uuid")),
            Column("added", Integer)
        )

        self._create_db()

    def _create_db(self):
        """Create the database if it doesn't exist.
        """

        if self.db_location.exists() == False:
            self.files_table.create()
            self.group_table.create()
            self.group_files.create()

            with self.engine.begin() as conn:
                create_date = datetime.now().timestamp()
                self.new_group("default", True)
    
    def new_group(self, name, default):
        """Create a new group in the database
        
        Params:
        name (str): The name of the new group
        default (bool): If this is the default group
        """
        create_date = datetime.now().timestamp()

        with self.engine.begin() as conn:
            conn.execute(self.group_table.insert().values(
                uuid=str(uuid.uuid4()),
                group_name=name,
                default=default,
                created=create_date,
                modified=create_date
            ))
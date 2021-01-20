from os import O_CREAT
import uuid
from datetime import datetime

from sqlalchemy.sql.expression import false, true

class VaultGroup:
    """Class for managing Vault Groups
    """
    def __init__(self, uuid, name, default, created, modified):
        """Setup a group

        Params:
        uuid: The UUID of the Group
        name: The Name of the Group
        default: If the Group is UUID
        created: The datetime that the group was created
        modified: The datetime that the last time the group was modified
        """
        self.uuid = uuid
        self.name = name
        self.default = default
        self.created = datetime.fromtimestamp(created)
        self.modified = datetime.fromtimestamp(modified)

    def insert(self, db):
        """Insert the group into the db

        Params:
        db: The VaultDatabase class to use to interact with the database
        """
        with db.engine.begin() as conn:
            if self.default:
                def_query = db.group_table.update().values(default=False)
                conn.execute(def_query)
                
            ins_query = db.group_table.insert().values(
                uuid=self.uuid,
                group_name=self.name,
                default=self.default,
                created=self.created.timestamp(),
                modified=self.modified.timestamp()
            )
            
            conn.execute(ins_query)

    def update(self, db):
        """Update the group into the db

        Params:
        db: The VaultDatabase class to use to interact with the database
        """
        with db.engine.begin() as conn:
            if self.default:
                def_query = db.group_table.update().values(default=False)
                conn.execute(def_query)
            
            query = db.group_table.update().values(
                group_name=self.name,
                default=self.default,
                created=self.created.timestamp(),
                modified=datetime.now().timestamp()
            ).where(
                db.group_table.c.uuid == self.uuid
            )

            conn.execute(query)

    def delete(self, db):
        """Remove the group into the db

        Params:
        db: The VaultDatabase class to use to interact with the database
        """
        with db.engine.begin() as conn:
            query = db.group_table.delete().where(
                db.group_table.c.uuid == self.uuid
            )
            conn.execute(query)

    @staticmethod
    def from_db(name, db):
        """Get a group object from the database the group into the db

        Params:
        name: The name of the group to get from the database
        db: The VaultDatabase class to use to interact with the database
        """
        with db.engine.begin() as conn:
            query = db.group_table.select().where(
                db.group_table.c.group_name == name
            )

            data = conn.execute(query).fetchall()

            for c, d in enumerate(data):
                data[c] = VaultGroup(
                    uuid=d[0],
                    name=d[1],
                    default=d[2],
                    created=d[3],
                    modified=d[4]
                )
        return data

    @staticmethod
    def all_groups(db):
        """Get all groups from the database.
        
        Params:
        db: The VaultDatabase object to use to interact with the database

        Returns:
        A list of VaultGroup objects of all groups in database
        """
        with db.engine.begin() as conn:
            query = db.group_table.select()
            all_data = conn.execute(query).fetchall()

        vault_groups = []

        for data in all_data:
            vault_groups.append(
                VaultGroup(
                    uuid=data[0],
                    name=data[1],
                    default=data[2],
                    created=data[3],
                    modified=data[4]
                )
            )
            
        return vault_groups


    @staticmethod
    def new(name, default=False):
        """Create a new group

        Params:
        name: The name of the group to create
        default: If this group is a default group

        Returns:
        The VaultGroup object for the new group
        """        
        create_date = datetime.now().timestamp()

        return VaultGroup(
            uuid=str(uuid.uuid4()),
            name=name,
            default=default,
            created=create_date,
            modified=create_date
        )

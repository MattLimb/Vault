import click
import pathlib
import os

from .cli_outputs import Outputs
from ..encryption import Encryption
from ..vault_config import VaultConfig
from ..vault_database import VaultDatabase
from ..vault_group import VaultGroup
from ..vault_file import VaultFile

__author__ = "Matt Limb <matt.limb17@gmail.com>"

def confirm_user(prompt, confirm):
    if confirm != None:
        return True if confirm == "yes" else False

    click.echo(prompt)
    user_prompt = click.prompt("Would you like to continue? [y/N]: ", default="n").lower()

    if ( user_prompt == "yes" ) or ( user_prompt == "y" ):
        return True
    else:
        return False

@click.group("file", help="Tools for administering Vault Files")
def file_main():
    """Command group for the management of Vaults files
    """
    pass

@file_main.command("new", help="Add a new file to a Vault")
@click.option("-d", "--debug", "debug", is_flag=True, help="Enable debug mode")
@click.option("-o", "--output", "output", type=click.Choice(["TEXT", "JSON", "XML"], case_sensitive=False), default="text", help="Enable debug mode")
@click.option("-v", "--vault", "vault", default=None, type=str, help="The Vault to add the file to.")
@click.option("-g", "--group", "group", default=None, type=str, help="The Group(s) to add the file to. Comma Seperate for more than 1")
@click.option("-r", "--remove", "remove", is_flag=True, default=False, type=bool, help="Remove the original file after encryption.")
@click.password_option("-p", "--password", "password", type=str, prompt=True, confirmation_prompt=False, help="The password for the Vault")
@click.argument("filepath", nargs=-1, type=str)
def file_new(debug, output,vault, group, remove, password, filepath):
    """Generate a new vault group in a given Vault.

    Options:
    -d/--debug    : Enable debug mode for more information.
    -o/--output   : The format to output to the terminal in.
    -v/--vault    : The vault to add the group too
    -p/--password : The Vault password

    Arguments:
    filepath : The filepath of the file to add

    Returns:
    Comfirmation of new group creation
    """
    config = VaultConfig()
    working_vault = None

    if vault == None:
        vault_config = config.get_vault()
        for vault in vault_config:
            if vault.default:
                working_vault = vault

        if working_vault == None:
            Outputs(format_=output.lower()).write(dict(
                type="error",
                error=0,
                message=f"Error: No Vaults Exist. Please Make a Vault first."
            ))
            quit(1)
    else:
        vault_config = config.get_vault(vault)
        if len(vault_config) == 1:
            working_vault = vault_config[0]
        elif len(vault_config) == 0:
            Outputs(format_=output.lower()).write(dict(
                type="error",
                error=0,
                message=f"Error: No Vaults Exist Using That Name."
            ))
            quit(1)
        else:
            Outputs(format_=output.lower()).write(dict(
                type="error",
                error=0,
                message=f"Error: Multiple Vaults Exist Using This Name."
            ))
            quit(1)

    if working_vault.verify_password(password):
        db = VaultDatabase(working_vault.uuid)
        master_key = Encryption.master_key(password, working_vault.nonce)
        
        files_to_add = []

        for pot_file in filepath:
            given_root = pathlib.Path(pot_file).absolute()

            if given_root.is_dir():
                for root, dirs, files in os.walk(given_root):
                    for f in files:
                        files_to_add.append(
                            (
                                VaultFile.new(given_root, pathlib.Path(root, f).absolute(), master_key),
                                pathlib.Path(root, f).absolute()
                            )
                        )

            elif given_root.is_file():
                files_to_add.append(
                    (
                        VaultFile.new(str(given_root).replace(str(given_root.name), ""), given_root, master_key),
                        pathlib.Path(given_root)
                    )
                )
            else:
                Outputs(format_=output.lower()).write(dict(
                    type="error",
                    error=0,
                    message=f"Error: Filepath given {str(given_root)} does not point to a directory or file."
                ))
                quit(1)

        group_ids = []

        if group != None:
            for g in group.split(","):
                if g != "":
                    gr = VaultGroup.from_db(g, db)
                    if len(gr) == 1:
                        group_ids.append(gr[0].uuid)
                    else:
                        Outputs(format_=output.lower()).write(dict(
                            type="error",
                            error=0,
                            message=f"Error: Group {str(g)} Specified Does Not Exist"
                        ))
                        quit(1)
        else:
            all_groups = VaultGroup.all_groups(db)
            
            for g in all_groups:
                if g.default == True:
                    group_ids.append(g.uuid) 
        
        for f, root in files_to_add:
            f.encrypt(master_key, working_vault, root, remove)
            f.insert(db)
            f.add_groups(group_ids, db)
            Outputs(format_=output.lower()).write(dict(
                type="success",
                error=0,
                message=f"Added {f.filename} to Vault {working_vault.name}"
            ))
        
        ## Need to add 
            # 1) Add all files to vault
            # 2) Add groups to files
            # 3) Add the recursive ability
            # 4) Create extension folders in the actual Vault
        
    else:
        Outputs(format_=output.lower()).write(dict(
            type="error",
            error=0,
            message=f"Error: Password is not correct for this Vault"
        ))
        quit(1)
    
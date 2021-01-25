import click
import pathlib
import os

from .cli_outputs import Outputs
from ..encryption import Encryption
from ..vault_config import VaultConfig
from ..vault_database import VaultDatabase
from ..vault_group import VaultGroup

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

@click.group("group", help="Tools for administering Vault groups")
def group_main():
    """Command group for the management of Vaults groups
    """
    pass

@group_main.command("new", help="Add a new group to a Vault")
@click.option("-d", "--debug", "debug", is_flag=True, help="Enable debug mode")
@click.option("-o", "--output", "output", type=click.Choice(["TEXT", "JSON", "XML"], case_sensitive=False), default="text", help="Enable debug mode")
@click.option("-v", "--vault", "vault", default=None, type=str, help="The Vault to add the groups too.")
@click.password_option("-p", "--password", "password", type=str, prompt=True, confirmation_prompt=False, help="A new password for the Vault")
@click.argument("group_name", nargs=1, type=str, default="new_group")
def group_new(debug, output,vault, password, group_name):
    """Generate a new vault group in a given Vault.

    Options:
    -d/--debug    : Enable debug mode for more information.
    -o/--output   : The format to output to the terminal in.
    -v/--vault    : The vault to add the group too
    -p/--password : The Vault password

    Arguments:
    group_name : A friendly name for the group.

    Returns:
    Comfirmation of new group creation
    """
    config = VaultConfig()
    default = False
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
        current_groups = VaultGroup.from_db(group_name, db)
        
        if len(current_groups) == 0:
            group = VaultGroup.new(group_name, default).insert(db)
            Outputs(format_=output.lower()).write(dict(
                type="success",
                error=0,
                message=f"Group {group_name} Created!"
            ))
            quit(0)
        else:
            Outputs(format_=output.lower()).write(dict(
                type="error",
                error=0,
                message=f"Error: A Group Already Exists with this Name"
            ))
            quit(1)
    else:
        Outputs(format_=output.lower()).write(dict(
            type="error",
            error=0,
            message=f"Error: Password is not correct for this Vault"
        ))
        quit(1)

@group_main.command("delete", help="Delete a group from a Vault")
@click.option("-d", "--debug", "debug", is_flag=True, help="Enable debug mode")
@click.option("-o", "--output", "output", type=click.Choice(["TEXT", "JSON", "XML"], case_sensitive=False), default="text", help="Enable debug mode")
@click.option("-v", "--vault", "vault", default=None, type=str, help="The Vault to add the groups too.")
@click.option("-y", "--yes", "confirm", flag_value="yes", help="Confirm deletion of a Vault Group.")
@click.option("-n", "--no", "confirm", flag_value="no", help="Deny the deletion of a Vault Group.")
@click.option("-f", "--files", "files", flag_value=True, help="Delete all files attached to the group.")
@click.password_option("-p", "--password", "password", type=str, prompt=True, confirmation_prompt=False, help="A new password for the Vault")
@click.argument("group_name", nargs=-1, type=str)
def group_delete(debug, output,vault, confirm, files, password, group_name):
    """Delete a vault group.

    Options:
    -d/--debug    : Enable debug mode for more information.
    -o/--output   : The format to output to the terminal in.
    -v/--vault    : The vault to add the group too
    -y/--yes      : Confirm the delete prompt
    -n/--no       : Deny the delete prompt
    -f/--files    : Delete the files attached to the group
    -p/--password : The Vault password

    Arguments:
    group_name : A friendly name for the group.

    Returns:
    Comfirmation of new group deletion
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

        for g in group_name:
            group = VaultGroup.from_db(g, db)
            if len(group) == 1:
                if group[0].default == False:
                    group[0].delete(db)
                    Outputs(format_=output.lower()).write(dict(
                        type="success",
                        error=0,
                        message=f"Group {group[0].name} Deleted!"
                    ))
                else:
                    Outputs(format_=output.lower()).write(dict(
                        type="error",
                        error=0,
                        message=f"Error: Default Group {g} Cannot be Deleted. Please Create Anoter Default Group."
                    ))
            elif len(group) > 1:
                Outputs(format_=output.lower()).write(dict(
                    type="error",
                    error=0,
                    message=f"Error: Multiple Groups With Name {g} - Cannot Continue"
                ))
            else:
                Outputs(format_=output.lower()).write(dict(
                    type="error",
                    error=0,
                    message=f"Error: No Goups With Name {g} - Cannot Continue"
                ))

    else:
        Outputs(format_=output.lower()).write(dict(
            type="error",
            error=0,
            message=f"Error: Password is not correct for this Vault"
        ))
        quit(1)

@group_main.command("default", help="Show group from a Vault")
@click.option("-d", "--debug", "debug", is_flag=True, help="Enable debug mode")
@click.option("-o", "--output", "output", type=click.Choice(["TEXT", "JSON", "XML"], case_sensitive=False), default="text", help="Enable debug mode")
@click.option("-v", "--vault", "vault", default=None, type=str, help="The Vault to add the groups too.")
@click.password_option("-p", "--password", "password", type=str, prompt=True, confirmation_prompt=False, help="A new password for the Vault")
@click.argument("group_name", nargs=1, type=str)
def group_default(debug, output,vault, password, group_name):
    """Redefine the default group

    Options:
    -d/--debug    : Enable debug mode for more information.
    -o/--output   : The format to output to the terminal in.
    -v/--vault    : The vault to add the group too
    -p/--password : The Vault password

    Arguments:
    group_name : The friendly name of the group

    Returns:
    Confirmation that the default group has been changed
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
        all_groups = VaultGroup.all_groups(db)

        for group in all_groups:
            if ( group.name == group_name ) or ( group.uuid == group_name ):
                group.default = True
                group.update(db)

        Outputs(format_=output.lower()).write(dict(
            type="success",
            error=0,
            message=f"{group_name} has been set as the default Vault."
        ))

    else:
        Outputs(format_=output.lower()).write(dict(
            type="error",
            error=0,
            message=f"Error: Password is not correct for this Vault"
        ))
        quit(1) 

@group_main.command("rename", help="Rename a group from a Vault")
@click.option("-d", "--debug", "debug", is_flag=True, help="Enable debug mode")
@click.option("-o", "--output", "output", type=click.Choice(["TEXT", "JSON", "XML"], case_sensitive=False), default="text", help="Enable debug mode")
@click.option("-v", "--vault", "vault", default=None, type=str, help="The Vault to add the groups too.")
@click.option("-y", "--yes", "confirm", flag_value="yes", help="Confirm renameing of a Vault Group.")
@click.option("-n", "--no", "confirm", flag_value="no", help="Deny the renameing of a Vault Group.")
@click.password_option("-p", "--password", "password", type=str, prompt=True, confirmation_prompt=False, help="A new password for the Vault")
@click.argument("group_name", nargs=1, type=str, default="new_group")
@click.argument("new_group_name", nargs=1, type=str, default="new_group")
def group_rename(debug, output,vault, confirm, password, group_name, new_group_name):
    """Rename a Vault Group

    Options:
    -d/--debug    : Enable debug mode for more information.
    -o/--output   : The format to output to the terminal in.
    -v/--vault    : The vault to add the group too
    -y/--yes      : Confirm the rename prompt
    -n/--no       : Deny the rename prompt
    -p/--password : The Vault password

    Arguments:
    group_name : A friendly name for the group.
    new_group_name : A new friendly name for the group.

    Returns:
    Comfirmation of new group rename
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

        prompt_text = f"You are about to rename Group \"{group_name}\" to \"{new_group_name}\". Renaming Groups is irreversable."
        if confirm_user(prompt_text, confirm):
            working_group = VaultGroup.from_db(group_name, db)

            if len(working_group) == 1:
                potential_group = VaultGroup.from_db(new_group_name, db)

                if len(potential_group) == 0:
                    working_group[0].name = new_group_name
                    working_group[0].update(db)

                    Outputs(format_=output.lower()).write(dict(
                        type="success",
                        error=0,
                        message=f"Vault {group_name} renamed to {new_group_name}"
                    ))
                else:
                    Outputs(format_=output.lower()).write(dict(
                        type="error",
                        error=0,
                        message=f"Error: A Group Already Exists Using The Name {new_group_name}."
                    ))
                    quit(1)
            elif len(working_group) == 0:
                Outputs(format_=output.lower()).write(dict(
                    type="error",
                    error=0,
                    message=f"Error: No Groups Exist Using That Name."
                ))
                quit(1)
            else:
                Outputs(format_=output.lower()).write(dict(
                    type="error",
                    error=0,
                    message=f"Error: There are Multiple Groups Using That Name."
                ))
                quit(1)
        else:
            Outputs(format_=output.lower()).write(dict(
                type="error",
                error=0,
                message=f"Error: User Confirm Failed"
            ))
            quit(1)

    else:
        Outputs(format_=output.lower()).write(dict(
            type="error",
            error=0,
            message=f"Error: Password is not correct for this Vault"
        ))
        quit(1) 


@group_main.command("show", help="Show group from a Vault")
@click.option("-d", "--debug", "debug", is_flag=True, help="Enable debug mode")
@click.option("-o", "--output", "output", type=click.Choice(["TEXT", "JSON", "XML"], case_sensitive=False), default="text", help="Enable debug mode")
@click.option("-v", "--vault", "vault", default=None, type=str, help="The Vault to add the groups too.")
@click.option("-i", "--info", "info", is_flag=True, help="Show addiional information about the Groups.")
@click.password_option("-p", "--password", "password", type=str, prompt=True, confirmation_prompt=False, help="A new password for the Vault")
@click.argument("group_name", nargs=-1, type=str)
def group_show(debug, output,vault, password, info, group_name):
    """Show Vault Groups

    Options:
    -d/--debug    : Enable debug mode for more information.
    -o/--output   : The format to output to the terminal in.
    -v/--vault    : The vault to add the group too
    -p/--password : The Vault password

    Arguments:
    group_name : A friendly name for the group.

    Returns:
    The groups for a given Vault
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

        if len(group_name) == 0:
            groups = VaultGroup.all_groups(db)
        else:
            groups = []
            for group in group_name:
                for pot_group in VaultGroup.from_db(group, db):
                    groups.append(pot_group)


        if len(groups) == 0:
            Outputs(format_=output.lower()).write(dict(
                type="normal",
                error=0,
                message=f"There are no configured Groups"
            ))
        else:
            output_dict = dict(
                type="normal",
                error=0,
                message=f"Showing Confiured Vaults",
                data_about="vault",
                seperate_data=True,
                data=[]
            )

            for item in groups:
                if info:
                    output_dict["data"].append(
                        {   
                            "Group": item.name,
                            "UUID":item.uuid,
                            "Is Default": item.default,
                            "Added": str(item.created),
                            "Last Modified": str(item.modified)
                        }
                    )
                else:
                    output_dict["seperate_data"] = False
                    output_dict["initial_line"] = False
                    output_dict["data"].append(
                        {   
                            "Group": item.name,
                        }
                    )

            Outputs(format_=output.lower()).write(output_dict)
    else:
        Outputs(format_=output.lower()).write(dict(
            type="error",
            error=0,
            message=f"Error: Password is not correct for this Vault"
        ))
        quit(1)
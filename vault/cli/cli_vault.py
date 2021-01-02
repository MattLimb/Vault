from vault.cli.cli_outputs import Outputs
import click
import pathlib
import os

from .cli_exceptions import VaultExists, VaultNotExists, VaultPasswordFailure
from ..vault import Vault
from ..vault_config import VaultConfig

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

@click.group("vault", help="Tools for administering Vaults")
def vault():
    """Command group for the management of Vaults
    """
    pass

@vault.command("new", help="Generate a new Vault.")
@click.option("-d", "--debug", "debug", is_flag=True, help="Enable debug mode")
@click.option("-o", "--output", "output", type=click.Choice(["TEXT", "JSON", "XML"], case_sensitive=False), default="text", help="Enable debug mode")
@click.option("-n", "--name", "name", prompt=True, type=str, help="A friendly name for the Vault")
@click.password_option("-p", "--password", "password", type=str, prompt=True, confirmation_prompt=True, help="A new password for the Vault")
@click.argument("location", nargs=1, type=str, default="./")
def vault_new(debug, output, name, password, location):
    """Generate a new vault at the specified location.

    Options:
    -d/--debug    : Enable debug mode for more information.
    -o/--output   : The format to output to the terminal in.
    -n/--name     : A friendly name for the vault
    -p/--password : A new password for the Vault

    Arguments:
    location : The new location for the Vault. Defauts to current directory.

    Returns:
    Comfirmation of new Vault creation
    """
    config = VaultConfig()
    default = False

    if config.get_vault() == []:
        default = True
    
    if config.get_vault(name) == []:
        vault = Vault.new(location, password, name, default)
        config.update_vault(vault)
    else:
        Outputs(format_=output.lower()).write(dict(
            type="error",
            error=0,
            message=f"Error: A Vault by this name already exists."
        ))
        quit(1)
        
    Outputs(format_=output.lower()).write(dict(
        type="success",
        error=0,
        message=f"Vault {name} Created"
    ))

@vault.command("delete", help="Delete a Vault.")
@click.option("-d", "--debug", "debug", is_flag=True, help="Enable debug mode")
@click.option("-o", "--output", "output", type=click.Choice(["TEXT", "JSON", "XML"], case_sensitive=False), default="text", help="Enable debug mode")
@click.option("-y", "--yes", "confirm", flag_value="yes", help="Confirm deletion of a Vault.")
@click.option("-n", "--no", "confirm", flag_value="no", help="Deny the deletion of a Vault.")
@click.option("-f", "--force", "force", is_flag=True, help="Force delete all files in a Vault.")
@click.password_option("-p", "--password", "password", type=str, prompt=True, confirmation_prompt=False, help="A new password for the Vault")
@click.argument("vault", nargs=1, type=str)
def vault_delete(debug, output, confirm, password, vault, force):
    """Remove a Vault.

    ### New Feature - Add Removal of DB and Files

    Options:
    -d/--debug    : Enable debug mode for more information.
    -o/--output   : The format to output to the terminal in.
    -y/--yes      : Confirm deletion of a Vault.
    -n/--no       : Deny the deletion of a Vault.
    -f/--force    : Force delete all files in a Vault.
    -p/--password : A new password for the Vault

    Arguments:
    vault : The new name of the Vault to delete.

    Returns:
    Confirmation of Vault deletion.
    """
    config = VaultConfig()
    vault_old = vault
    vault = config.get_vault(vault_old)

    if len(vault) != 1:
        Outputs(format_=output.lower()).write(dict(
            type="error",
            error=0,
            message=f"Error: The Vault specified does not exist"
        ))
        quit(1)
    
    vault = vault[0]
    if vault.verify_password(password):
        prompt_text = f"You are about to delete \"{vault_old}\". Deleting Vaults is irreversable."
        if confirm_user(prompt_text, confirm):
            del config.data["vaults"][vault.uuid]
            
            if force:
                if vault.filepath.exists():
                    os.remove(vault.filepath)
                if pathlib.Path(config.files_location, f"{vault.uuid}.db").exists():
                    os.remove(pathlib.Path(config.files_location, f"{vault.uuid}.db"))
            
            config.save()
            
            Outputs(format_=output.lower()).write(dict(
                type="success",
                error=0,
                message=f"Vault {vault_old} Deleted"
            ))
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
    

@vault.command("rename", help="Change the friendly name of a Vault.")
@click.option("-d", "--debug", "debug", is_flag=True, help="Enable debug mode")
@click.option("-o", "--output", "output", type=click.Choice(["TEXT", "JSON", "XML"], case_sensitive=False), default="text", help="Enable debug mode")
@click.option("-y", "--yes", "confirm", flag_value="yes", help="Confirm deletion of a Vault.")
@click.option("-n", "--no", "confirm", flag_value="no", help="Deny the deletion of a Vault.")
@click.password_option("-p", "--password", "password", type=str, prompt=True, confirmation_prompt=False, help="A new password for the Vault")
@click.argument("vault", nargs=1, type=str)
@click.argument("new_name", nargs=1, type=str)
def vault_rename(debug, output, confirm, password, vault, new_name):
    """Rename a Vault.

    Options:
    -d/--debug    : Enable debug mode for more information.
    -o/--output   : The format to output to the terminal in.
    -y/--yes      : Confirm deletion of a Vault.
    -n/--no       : Deny the deletion of a Vault.
    -p/--password : A new password for the Vault.

    Arguments:
    vault    : The name of the Vault to change the name of.
    new_name : The new name of the Vault.

    Returns:
    Confirmation of Vault rename.
    """
    config = VaultConfig()
    vault_old = vault
    vault = config.get_vault(vault_old)

    if len(vault) != 1:
        Outputs(format_=output.lower()).write(dict(
            type="error",
            error=0,
            message=f"Error: The Vault specified does not exist"
        ))
        quit(1)
    
    vault = vault[0]
    if vault.verify_password(password):
        prompt_text = f"You are about to rename \"{vault_old}\" to \"{new_name}\". Renaming Vaults is irreversable."
        if confirm_user(prompt_text, confirm):
            vault.name = new_name
            vault.update_modified()
            config.update_vault(vault)

            Outputs(format_=output.lower()).write(dict(
                type="success",
                error=0,
                message=f"Vault {vault_old} renamed to {new_name}"
            ))
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
    

@vault.command("list", help="Change the friendly name of a Vault.")
@click.option("-d", "--debug", "debug", is_flag=True, help="Enable debug mode")
@click.option("-o", "--output", "output", type=click.Choice(["TEXT", "JSON", "XML"], case_sensitive=False), default="text", help="Enable debug mode")
@click.option("-i", "--info", "info", is_flag=True, help="Show addiional information about the Vaults.")
def vault_list(debug, output, info):
    """List all Vaults shown in the Vault.yaml.

    Options:
    -d/--debug  : Enable debug mode for more information.
    -o/--output : The format to output to the terminal in.
    -i/--info   : Show additional information about the Vaults.

    Returns:
    The Vault names and/or additional information.
    """
    config = VaultConfig()
    vaults = config.get_vault()

    if len(vaults) == 0:
        Outputs(format_=output.lower()).write(dict(
            type="normal",
            error=0,
            message=f"There are no configured Vaults"
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

        for item in vaults:
            if info:
                output_dict["data"].append(
                    {   
                        "Vault": item.name,
                        "UUID":item.uuid,
                        "Location":item.filepath,
                        "Is Default": item.default,
                        "Added": str(item.added),
                        "Last Modified": str(item.modified)
                    }
                )
            else:
                output_dict["seperate_data"] = False
                output_dict["initial_line"] = False
                output_dict["data"].append(
                    {   
                        "Vault": item.name,
                    }
                )

        Outputs(format_=output.lower()).write(output_dict)
    

@vault.command("show", help="Change the friendly name of a Vault.")
@click.option("-d", "--debug", "debug", is_flag=True, help="Enable debug mode")
@click.option("-o", "--output", "output", type=click.Choice(["TEXT", "JSON", "XML"], case_sensitive=False), default="text", help="Enable debug mode")
@click.argument("vault_name", type=str, nargs=-1)
def vault_show(debug, output, vault_name):
    """Show all specific information about a particular vault.

    Options:
    -d/--debug  : Enable debug mode for more information.
    -o/--output : The format to output to the terminal in.
    
    Arguments:
    vault_name : The Vault name(s) to show more information about.

    Returns:
    The Vault information.
    """
    config = VaultConfig()

    if len(vault_name) == 0:
        Outputs(format_=output.lower()).write(dict(
            type="error",
            error=0,
            message=f"No Vaults Specified."
        ))
    
    for name in vault_name:
        vaults = config.get_vault(name)

        if len(vaults) == 0:
            click.echo()
            Outputs(format_=output.lower()).write(dict(
                type="normal",
                error=0,
                message=f"There are no configured Vaults with name {name}"
            ))
        else:
            item = vaults[0]
            output_dict = dict(
                type="normal",
                error=0,
                message=f"Showing Confiured Vaults",
                data_about="vault",
                seperate_data=True,
                data=[
                    {   
                        "Vault": item.name,
                        "UUID":item.uuid,
                        "Location":item.filepath,
                        "Is Default": item.default,
                        "Added": str(item.added),
                        "Last Modified": str(item.modified)
                    }
                ]
            )
            Outputs(format_=output.lower()).write(output_dict)


@vault.command("default", help="Change the friendly name of a Vault.")
@click.option("-d", "--debug", "debug", is_flag=True, help="Enable debug mode")
@click.option("-o", "--output", "output", type=click.Choice(["TEXT", "JSON", "XML"], case_sensitive=False), default="text", help="Enable debug mode")
@click.argument("vault_name", type=str, nargs=-1, default=None)
def vault_default(debug, output, vault_name):
    """Generate a new vault at the specified location.

    Options:
    -d/--debug  : Enable debug mode for more information.
    -o/--output : The format to output to the terminal in.
    
    Arguments:
    vault_name : The Vault name(s) to show more information about.

    Returns:
    Confirmation that the default Vault, or show the default Vault.
    """

    config = VaultConfig()
    all_vaults = config.get_vault()

    if len(vault_name) == 0:
        for vault in all_vaults:
            if vault.default:
                Outputs(format_=output.lower()).write(dict(
                    type="normal",
                    error=0,
                    message=f"{vault.name} is the default Vault."
                )) 
                break

    elif len(vault_name) == 1:
        the_vault = config.get_vault(vault_name[0])
        if len(the_vault) != 1:
            Outputs(format_=output.lower()).write(dict(
                type="normal",
                error=0,
                message=f"There are no configured Vaults with name {vault_name[0]}"
            ))
        else:
            for vault in all_vaults:
                if vault.name == vault_name[0]:
                    vault.default = True
                    config.update_vault(vault)
                else:
                    vault.default = False
                    config.update_vault(vault)

            Outputs(format_=output.lower()).write(dict(
                type="success",
                error=0,
                message=f"{vault_name[0]} has been set as the default Vault."
            ))
    else:
        Outputs(format_=output.lower()).write(dict(
            type="error",
            error=0,
            message=f"Too many arguments. Please specify 0 or 1 arguments"
        ))
        
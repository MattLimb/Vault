import click

__author__ = "Matt Limb <matt.limb17@gmail.com>"

@click.group("vault", help="Tools for administering Vaults")
def vault():
    """Command group for the management of Vaults
    """
    pass

@vault.command("new", help="Generate a new Vault.")
@click.option("-d", "--debug", "debug", is_flag=True, help="Enable debug mode")
@click.option("-o", "--output", "output", type=click.Choice(["TEXT", "JSON", "XML"], case_sensitive=False), help="Enable debug mode")
@click.option("-n", "--name", "name", prompt=True, type=str, help="A friendly name for the Vault")
@click.password_option("-p", "--password", "password", type=str, prompt=True, confirmation_prompt=True, help="A new password for the Vault")
@click.argument("location", nargs=1, type=str, default="./")
def vault_new(debug, ouput, name, password, location):
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
    pass

@vault.command("delete", help="Delete a Vault.")
@click.option("-d", "--debug", "debug", is_flag=True, help="Enable debug mode")
@click.option("-o", "--output", "output", type=click.Choice(["TEXT", "JSON", "XML"], case_sensitive=False), help="Enable debug mode")
@click.option("-y", "--yes", "confirm", flag_value="yes", help="Confirm deletion of a Vault.")
@click.option("-n", "--no", "confirm", flag_value="no", help="Deny the deletion of a Vault.")
@click.option("-f", "--force", "force", is_flag=True, help="Force delete all files in a Vault.")
@click.password_option("-p", "--password", "password", type=str, prompt=True, confirmation_prompt=True, help="A new password for the Vault")
@click.argument("vault", nargs=1, type=str)
def vault_delete(debug, ouput, confirm, password, vault):
    """Generate a new vault at the specified location.

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
    pass

@vault.command("rename", help="Change the friendly name of a Vault.")
@click.option("-d", "--debug", "debug", is_flag=True, help="Enable debug mode")
@click.option("-o", "--output", "output", type=click.Choice(["TEXT", "JSON", "XML"], case_sensitive=False), help="Enable debug mode")
@click.option("-y", "--yes", flag_value="yes", help="Confirm deletion of a Vault.")
@click.option("-n", "--no", flag_value="no", help="Deny the deletion of a Vault.")
@click.password_option("-p", "--password", "password", type=str, prompt=True, confirmation_prompt=True, help="A new password for the Vault")
@click.argument("vault", nargs=1, type=str)
@click.argument("new_name", nargs=1, type=str)
def vault_rename(debug, ouput, confirm, password, vault, new_name):
    """Generate a new vault at the specified location.

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
    Confirmation of Vault deletion.
    """
    pass

@vault.command("list", help="Change the friendly name of a Vault.")
@click.option("-d", "--debug", "debug", is_flag=True, help="Enable debug mode")
@click.option("-o", "--output", "output", type=click.Choice(["TEXT", "JSON", "XML"], case_sensitive=False), help="Enable debug mode")
@click.option("-i", "--info", "info", is_flag=True, help="Show addiional information about the Vaults.")
def vault_list(debug, ouput, info):
    """Generate a new vault at the specified location.

    Options:
    -d/--debug  : Enable debug mode for more information.
    -o/--output : The format to output to the terminal in.
    -i/--info   : Show additional information about the Vaults.

    Returns:
    The Vault names and/or additional information.
    """
    pass

@vault.command("show", help="Change the friendly name of a Vault.")
@click.option("-d", "--debug", "debug", is_flag=True, help="Enable debug mode")
@click.option("-o", "--output", "output", type=click.Choice(["TEXT", "JSON", "XML"], case_sensitive=False), help="Enable debug mode")
@click.argument("vault_name", type=str, nargs=-1)
def vault_showq(debug, ouput, vault_name):
    """Generate a new vault at the specified location.

    Options:
    -d/--debug  : Enable debug mode for more information.
    -o/--output : The format to output to the terminal in.
    
    Arguments:
    vault_name : The Vault name(s) to show more information about.

    Returns:
    The Vault information.
    """
    pass

@vault.command("default", help="Change the friendly name of a Vault.")
@click.option("-d", "--debug", "debug", is_flag=True, help="Enable debug mode")
@click.option("-o", "--output", "output", type=click.Choice(["TEXT", "JSON", "XML"], case_sensitive=False), help="Enable debug mode")
@click.argument("vault_name", type=str, nargs=-1, default=None)
def vault_default(debug, ouput, vault_name):
    """Generate a new vault at the specified location.

    Options:
    -d/--debug  : Enable debug mode for more information.
    -o/--output : The format to output to the terminal in.
    
    Arguments:
    vault_name : The Vault name(s) to show more information about.

    Returns:
    Confirmation that the default Vault, or show the default Vault.
    """
    pass

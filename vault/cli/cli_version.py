import click

__author__ = "Matt Limb <matt.limb17@gmail.com>"

@click.command("version", help="Get version info about Vault")
@click.option("-d", "--debug", "debug", is_flag=True, help="Enable debug mode")
@click.option("-o", "--output", "output", type=click.Choice(["TEXT", "JSON", "XML"], case_sensitive=False), default="TEXT", help="Format to output to the terminal in")
def version(debug):
    """Show version infoamtion for Vault

    Options:
    -d/--debug  : Enable debug mode for more information.
    -o/--output : The format to output to the terminal in.

    Returns:
    The version information
    """
    pass

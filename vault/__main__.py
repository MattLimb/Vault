import click
import colorama

colorama.init()

__author__ = "Matt Limb <matt.limb17@gmail.com>"

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass

from .cli.cli_generate import generate
from .cli.cli_vault import vault
from .cli.cli_version import version

cli.add_command(generate)
cli.add_command(vault)
cli.add_command(version)

if __name__ == "__main__":
    cli(prog_name="vault")